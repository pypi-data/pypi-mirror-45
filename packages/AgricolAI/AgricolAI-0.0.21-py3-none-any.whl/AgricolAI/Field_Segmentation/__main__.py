from .Agents import *

class Model():
    def __init__(self):
        '''
        '''
        self.ch_NIR = -1
        self.field = -1
        print("Field_Segmentation()")
    def fit(self, img, map, ch_NIR=1,\
            k=3, strict=True,\
            tol=5, coef_grid=.2,\
            path_out=None):
        '''
        '''
        self.load_data(img=img, map=map, ch_NIR=ch_NIR)
        self.to_binary(k=k, strict=strict, path_out=path_out)
        self.put_anchors(path_out=path_out)
        self.search_by_agent(tol=tol, coef_grid=coef_grid, path_out=path_out)
    def load_data(self, img, map, ch_NIR=1):
        '''
        '''
        # load image and map
        img = np.array(Image.open(img)) if isinstance(img, str) else img
        map = pd.read_csv(map, header=None) if isinstance(map, str) else map
        # standardization
        means, stds = img.mean(axis=(0, 1)), img.std(axis=(0, 1))
        img_std = (img-means)/stds
        img_max, img_min = img_std.max(axis=(0, 1)), img_std.min(axis=(0, 1))
        img_std2 = (img_std-img_min)/(img_max-img_min)
        # instantiate filed class
        self.ch_NIR = ch_NIR
        self.field = Field(img=img, img_std=img_std2, map=map)
    def to_binary(self, k=3, strict=True, path_out=None):
        '''
        '''
        # data type conversion for opencv
        img_std = self.field.img_std
        img_z = img_std.reshape((-1, img_std.shape[2])).astype(np.float32)
        # define criteria, number of clusters(K) and apply kmeans()
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 50, 1.0)
        param_k = dict(data=img_z,\
                       K=k,\
                       bestLabels=None,\
                       criteria=criteria,\
                       attempts=30,\
                       flags=cv2.KMEANS_PP_CENTERS)
        _, img_k, center = cv2.kmeans(**param_k)
        # Convert back
        img_k = img_k.astype(np.uint8).reshape((img_std.shape[0], -1))
        # Find proper label for NIR
        if strict:
            idx_plot = np.argmax([center[i, self.ch_NIR]/center[i, :].sum() for i in range(k)])
            img_k = (img_k == idx_plot)*1
        else:
            idx_plot = np.argmin([center[i, self.ch_NIR]/center[i, :].sum() for i in range(k)])
            img_k = (img_k != idx_plot)*1
        self.field.set_binary(img_k)
        # output
        if path_out!=None:
            plt.figure()
            plt.imshow(img_k)
            plt.savefig(path_out+"_kmean.png", dpi=300)
            plt.close()
    def put_anchors(self, path_out=None):
        '''
        '''
        img = self.filed.img_bin
        map = self.filed.map
        ls_row, mean_h = self.get_peak(img=img, map=map, axis=0)
        ls_col, mean_v = self.get_peak(img=img, map=map, axis=1)
        self.field.set_anchors(ls_row, ls_col)
        if path_out!=None:
            plt.figure()
            plt.plot(mean_h)
            plt.plot(ls_row, mean_h[ls_row], "x")
            plt.savefig(path_out+"_row_scan.png", dpi=300)
            plt.close()
            plt.figure()
            plt.plot(mean_v)
            plt.plot(ls_col, mean_v[ls_col], "x")
            plt.savefig(path_out+"_col_scan.png", dpi=300)
            plt.close()
            self.pt_seed = np.array(np.meshgrid(ls_row, ls_col)).T.reshape(-1, 2).swapaxes(0, 1)
            plt.figure()
            plt.plot(self.pt_seed[1], self.pt_seed[0], "x", ms=2)
            plt.imshow(self.field.img_bin)
            plt.savefig(path_out+"_anchor.png", dpi=300)
            plt.close()
    def search_by_agent(self, tol=tol, coef_grid=coef_grid, path_out=None):
        '''
        '''
        self.field.cpu_pre_dim(tol=tol)
        self.field.cpu_bound(coef_grid=coef_grid)
        if path_out!=None:
            plt.figure()
            currentAxis = plt.gca()
            for row in range(self.field.nrow):
                for col in range(self.field.ncol):
                    agent = self.field.get_agent(row, col)
                    east = agent.get_border(Dir.EAST)
                    west = agent.get_border(Dir.WEST)
                    north = agent.get_border(Dir.NORTH)
                    south = agent.get_border(Dir.SOUTH)
                    rec = Rectangle((west, north), east-west, south-north, fill=None, linewidth=.3, color="red")
                    currentAxis.add_patch(rec)
            plt.plot(self.pt_seed[1], self.pt_seed[0], "x", ms=2)
            plt.imshow(self.field.img_bin)
            plt.savefig(path_out+"_seg.png", dpi=300)
            plt.close()
    def get_peak(self, img, map, axis=0, n_smooth=2):
        '''
        '''
        # compute signal
        ls_mean = img.mean(axis=(not axis)*1) # ncol
        # smooth signal
        for i in range(n_smooth):
            ls_mean = np.convolve([0.1, 0.3, 0.5, 0.7, 1, 0.7, 0.5, 0.3, 0.1], ls_mean, mode='valid')
        # find the peaks
        interval = round(img.shape[axis]/(map.shape[axis]*2+img.shape[axis]*.01))
        peaks, _ = find_peaks(ls_mean, distance=interval)
        # eliminate reduncdent peaks
        while len(peaks) > map.shape[axis]:
            ls_diff = [peaks[i+1]-peaks[i] for i in range(len(peaks)-1)]
            idx_diff = np.argmin(ls_diff)
            idx_kick = idx_diff if (ls_mean[peaks[idx_diff]] < ls_mean[peaks[idx_diff+1]]) else (idx_diff+1)
            peaks = np.delete(peaks, idx_kick)
        return peaks, ls_mean
    def get_DF(self, NIR=1, Red=0):
        '''
        '''
        df_map = self.map.stack().reset_index()
        df_map.columns = ["row", "col", "var"]
        df_merge = pd.merge(self.df, df_map, on=["row", "col"])
        img_ndvi = (self.img[:,:,NIR]-self.img[:,:,Red])/(self.img[:,:,NIR]+self.img[:,:,Red])
        ls_area = []
        ls_area_veg = []
        ls_avg_ndvi = []
        for i in range(len(df_merge)):
            sub_df = df_merge.iloc[i]
            n_area = 0
            n_veg = 0
            val_ndvi = 0
            for x in range(sub_df.bd_left, sub_df.bd_right):
                for y in range(sub_df.bd_up, sub_df.bd_bottom):
                    n_area += 1
                    if self.img_k[y, x] == 1:
                        n_veg += 1
                        val_ndvi += img_ndvi[y, x]
            ls_area.append(n_area)
            ls_area_veg.append(n_veg)
            ls_avg_ndvi.append(val_ndvi/n_veg)
        df_merge['area_all'] = ls_area
        df_merge['area_veg'] = ls_area_veg
        df_merge['ndvi_avg'] = ls_avg_ndvi
        return(df_merge)
