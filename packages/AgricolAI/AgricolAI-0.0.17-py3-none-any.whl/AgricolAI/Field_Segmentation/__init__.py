import pandas as pd
import numpy as np
import sys
import urllib.request
import io
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from scipy.signal import find_peaks
from spectral import *
# for saving image in memory
from PIL import Image

def get_demo():
    path_map = "http://www.zzlab.net/James_Demo/seg_map.csv"
    path_img = "http://www.zzlab.net/James_Demo/seg_img.jpg"
    map = pd.read_csv(path_map, header=None)
    with urllib.request.urlopen(path_img) as url:
        file = io.BytesIO(url.read())
        img = np.array(Image.open(file))/255
    return img, map

class Model():
    def __init__(self, is_standardize=True, k=3, inval_row=None, inval_col=None, ch_NIR=1, ch_Red=0):
        '''
        '''
        self.is_standardize = is_standardize
        self.k = k
        self.inval_row = inval_row
        self.inval_col = inval_col
        self.ch_NIR = ch_NIR
        self.ch_Red = ch_Red
        print("Field_Segmentation(standardize=%s, kmean=%d, ch_NIR=%d, ch_Red=%d)"%\
        (self.is_standardize, self.k, self.ch_NIR, self.ch_Red))
    def fit(self, img, map, path_out=None):
        '''
        '''
        if isinstance(img, str):
            self.load_data(img=img, map=map, from_dir=True)
        else:
            self.load_data(img=img, map=map, from_dir=False)
        self.to_binary(k=self.k)
        self.put_anchors(inval_row=self.inval_row, inval_col=self.inval_col, path_out=path_out)
        self.search_by_agent(path_out=path_out)
        self.fill_the_gaps(path_out=path_out)
        df = self.get_DF(NIR=self.ch_NIR, Red=self.ch_Red)
        return df
    def load_data(self, img, map, from_dir=False):
        '''
        '''
        if from_dir:
            self.map = pd.read_csv(map, header=None)
            self.img = np.array(Image.open(img))
        else:
            self.map = map
            self.img = img
        if self.is_standardize:
            self.img = self.img/255
        px_h = self.img.shape[0]
        px_w = self.img.shape[1]
        n_row = self.map.shape[0]
        n_col = self.map.shape[1]
        self.__param__ = dict(px_w=px_w, px_h=px_h, n_row=n_row, n_col=n_col)
    def to_binary(self, k=3):
        '''
        '''
        img_k, center = kmeans(self.img, k, 50)
        # Convert plot class as 1, others as 0
        # isBinMajor = True
        # if (img_ar_k==0).sum() > (img_ar_k==1).sum():
        #     cat_plot = 0 if isBinMajor else 1
        # else:
        #     cat_plot = 1 if isBinMajor else 0
        #
        # if cat_plot != 1:
            # img_ar_k = np.logical_xor(img_ar_k, 1)*1
        img_k[img_k!=0] = 1
        self.img_k = np.logical_xor(img_k, 1)*1
    def put_anchors(self, inval_row=None, inval_col=None, path_out=None):
        '''
        '''
        if inval_row==None:
            inval_row = round(self.__param__['px_h']/(self.__param__['n_row']*2))
        if inval_col==None:
            inval_col = round(self.__param__['px_w']/(self.__param__['n_col']*2-1))
        mean_h = np.array([self.img_k[i, :].mean() for i in range(self.__param__['px_h'])])
        mean_v = np.array([self.img_k[:, i].mean() for i in range(self.__param__['px_w'])])
        ls_row = self.get_peak(mean_h, inval_row, self.__param__['n_row'])
        ls_col = self.get_peak(mean_v, inval_col, self.__param__['n_col'])
        self.__param__['ls_row'] = ls_row
        self.__param__['ls_col'] = ls_col
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
            plt.imshow(self.img_k)
            plt.savefig(path_out+"_anchor.png", dpi=300)
            plt.close()
    def search_by_agent(self, path_out=None):
        '''
        '''
        ls_bound = []
        ls_th_row = []
        ls_th_col = []
        for i_r in range(self.__param__['n_row']):
            for i_c in range(self.__param__['n_col']):
                ls_bound.append(self.get_boundary(self.img_k, i_r, i_c, **self.__param__))
                ls_th_row.append(i_r)
                ls_th_col.append(i_c)
        df = pd.DataFrame()
        df['bd_right'] = [bound[0] for bound in ls_bound]
        df['bd_left'] = [bound[1] for bound in ls_bound]
        df['bd_bottom'] = [bound[2] for bound in ls_bound]
        df['bd_up'] = [bound[3] for bound in ls_bound]
        df['row'] = ls_th_row
        df['col'] = ls_th_col
        # fill boundary first
        df.loc[(df.col==0), "bd_left"] = 0
        df.loc[(df.col==(self.__param__['n_col']-1)), "bd_right"] = self.__param__['px_w']
        df.loc[(df.row==0), "bd_up"] = 0
        df.loc[(df.row==(self.__param__['n_row']-1)), "bd_bottom"] = self.__param__['px_h']
        self.df = df
        if path_out!=None:
            plt.figure()
            currentAxis = plt.gca()
            # currentAxis.set_axis_off()
            for right, left, bottom, up in zip(df.bd_right, df.bd_left, df.bd_bottom, df.bd_up):
                rec = Rectangle((left, up), right-left, bottom-up, fill=None, linewidth=.3, color="red")
                currentAxis.add_patch(rec)
            plt.plot(self.pt_seed[1], self.pt_seed[0], "x", ms=2)
            plt.imshow(self.img_k)
            plt.savefig(path_out+"_agent.png", dpi=300)
            plt.close()
    def fill_the_gaps(self, path_out=None):
        '''
        '''
        self.df = self.get_filled_gap(self.img_k, self.df, **self.__param__)
        if path_out!=None:
            plt.figure()
            currentAxis = plt.gca()
            for right, left, bottom, up in zip(self.df.bd_right, self.df.bd_left, self.df.bd_bottom, self.df.bd_up):
                rec = Rectangle((left, up), right-left, bottom-up, fill=None, linewidth=.3, color="red")
                currentAxis.add_patch(rec)
            plt.plot(self.pt_seed[1], self.pt_seed[0], "x", ms=2)
            plt.imshow(self.img_k)
            plt.savefig(path_out+"_seg.png", dpi=300)
            plt.close()
    def get_DF(self, NIR=1, Red=0):
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
    def get_peak(self, vector, distance, n_exp, is_verify=False):
        '''
        '''
        pks, _ = find_peaks(vector, distance=distance)
        pks = pks[vector[pks] > 0.5]
        while len(vector[pks]) != n_exp:
            ls_diff = [pks[i+1]-pks[i] for i in range(len(pks)-1)]
            idx_kick = np.argmin(ls_diff) + 1
            # idx_kick = np.argmax(vector[pks])
            pks = np.delete(pks, idx_kick)
        if is_verify:
            plt.plot(vector)
            plt.plot(pks, vector[pks], "x")
            plt.show()
        return pks
    def get_1d_edge(self, map, agent_pt, is_toward_pos, tol, tol_temp, bound):
        '''
        Find the preliminary edge toward 1d direction
        (2*bol - 1) can convert True to 1 and False to -1
        '''
        step = 2*is_toward_pos-1
        if (tol_temp > tol) | (agent_pt*step > bound*step):
            return agent_pt
        try:
            map_value = map[agent_pt]
        except:
            return agent_pt
        if map_value == 0:
            tol_temp += 1
        else:
            tol_temp = 0
        return self.get_1d_edge(map, agent_pt+step, is_toward_pos, tol, tol_temp, bound)
    def get_2d_edge(self, map, agent_pt, search_range, is_search_by_row, is_toward_pos, ratio_tol):
        '''
        Find the finalized edge
        (2*bol - 1) can convert True to 1 and False to -1
        '''
        keep_searching = True
        step = 2*is_toward_pos-1
        while keep_searching & (agent_pt>0):
            try:
                score = map[agent_pt, search_range].mean() if is_search_by_row else map[search_range, agent_pt].mean()
            except:
                break
            # within_midpoint = (agent_pt*step < cutpoint*step) if cutpoint!=None else False
            keep_searching = (score > ratio_tol)
            agent_pt += step
        return agent_pt-step
    def get_boundary(self, map, i_r, i_c, px_w, px_h, n_row, n_col, ls_row, ls_col):
        '''
        '''
        # get agent's coordinate
        agent_row = ls_row[i_r]
        agent_col = ls_col[i_c]
        # get neighbor's coordinate
        agent_left = ls_col[i_c-1] if (i_c-1)//n_col == 0 else 0
        agent_right = ls_col[i_c+1] if (i_c+1)//n_col == 0 else px_w
        agent_up = ls_row[i_r-1] if (i_r-1)//n_row == 0 else 0
        agent_down = ls_row[i_r+1] if (i_r+1)//n_row == 0 else px_h
        # get 1D map based on agnet's coordinate
        map_1d_row = map[agent_row, :]
        map_1d_col = map[:, agent_col]
        # find 1D edges
        tol = 5
        param_row = dict(map=map_1d_row, agent_pt=agent_col, tol=tol, tol_temp=0)
        param_col = dict(map=map_1d_col, agent_pt=agent_row, tol=tol, tol_temp=0)
        pre_right = self.get_1d_edge(**param_row, is_toward_pos=True, bound=(agent_col+agent_right)/2)
        pre_left = self.get_1d_edge(**param_row, is_toward_pos=False, bound=(agent_col+agent_left)/2)
        pre_bottom = self.get_1d_edge(**param_col, is_toward_pos=True, bound=(agent_row+agent_down)/2)
        pre_up = self.get_1d_edge(**param_col, is_toward_pos=False, bound=(agent_row+agent_up)/2)
        # calculate rulers by the given edges
        rg_row = range(pre_up, pre_bottom)
        rg_col = range(pre_left, pre_right)
        # expected area size
        area_max = len(rg_row)*len(rg_col)
        # setup parameters for final search
        param_row_2d = dict(map=map, agent_pt=agent_col, search_range=rg_row, is_search_by_row=False)
        param_col_2d = dict(map=map, agent_pt=agent_row, search_range=rg_col, is_search_by_row=True)
        area_temp = 10e+9
        ratio = 0.1
        # find 2D edges and optimize the results
        while (area_temp > area_max) & (ratio < 1):
            right = self.get_2d_edge(**param_row_2d, is_toward_pos=True, ratio_tol=ratio)
            left = self.get_2d_edge(**param_row_2d, is_toward_pos=False, ratio_tol=ratio)
            bottom = self.get_2d_edge(**param_col_2d, is_toward_pos=True, ratio_tol=ratio)
            up = self.get_2d_edge(**param_col_2d, is_toward_pos=False, ratio_tol=ratio)
            area_temp = map[up:bottom, left:right].sum()
            ratio += 0.05
        return right, left, bottom, up
    def get_filled_gap(self, map, df, px_w, px_h, n_row, n_col, ls_row, ls_col):
        '''
        '''
        for i_r in range(n_row):
            for i_c in range(n_col):
                print("computing plot (%d, %d)"%(i_r, i_c))
                sys.stdout.flush()
                # top/bottom, compare with below one
                if i_r != (n_row-1):
                    while True:
                        df_self = df.loc[(df.col==i_c)&(df.row==i_r)]
                        df_neig = df.loc[(df.col==(i_c))&(df.row==i_r+1)]
                        if abs(df_self['bd_bottom'].values[0] - df_neig['bd_up'].values[0])>1:
                            rg_self = range(df_self['bd_left'].values[0], df_self['bd_right'].values[0])
                            rg_neig = range(df_neig['bd_left'].values[0], df_neig['bd_right'].values[0])
                            score_self = map[df_self['bd_bottom'], rg_self].mean()
                            score_neig = map[df_neig['bd_up'], rg_neig].mean()
                            if score_self > score_neig:
                                df.loc[(df.col==i_c)&(df.row==i_r), 'bd_bottom'] += 1
                            elif score_self < score_neig:
                                df.loc[(df.col==(i_c))&(df.row==i_r+1), 'bd_up'] -= 1
                            else:
                                df.loc[(df.col==i_c)&(df.row==i_r), 'bd_bottom'] += 1
                                df.loc[(df.col==(i_c))&(df.row==i_r+1), 'bd_up'] -= 1
                        else:
                            break;
                # left/right, compare with right-hand side
                if i_c != (n_col-1):
                    while True:
                        df_self = df.loc[(df.col==i_c)&(df.row==i_r)]
                        df_neig = df.loc[(df.col==(i_c+1))&(df.row==i_r)]
                        if abs(df_self['bd_right'].values[0] - df_neig['bd_left'].values[0])>1:
                            rg_self = range(df_self['bd_up'].values[0], df_self['bd_bottom'].values[0])
                            rg_neig = range(df_neig['bd_up'].values[0], df_neig['bd_bottom'].values[0])
                            score_self = map[rg_self, df_self['bd_right']].mean()
                            score_neig = map[rg_neig, df_neig['bd_left']].mean()
                            if score_self > score_neig:
                                df.loc[(df.col==i_c)&(df.row==i_r), 'bd_right'] += 1
                            elif score_self < score_neig:
                                df.loc[(df.col==(i_c+1))&(df.row==i_r), 'bd_left'] -= 1
                            else:
                                df.loc[(df.col==i_c)&(df.row==i_r), 'bd_right'] += 1
                                df.loc[(df.col==(i_c+1))&(df.row==i_r), 'bd_left'] -= 1
                        else:
                            break;
        return df
    def hint(self):
        print("self.load_data(path_img=path_img, path_map=path_map)")
        print("self.to_binary(k=self.k)")
        print("self.put_anchors(inval_row=self.inval_row, inval_col=self.inval_col, path_out=path_out)")
        print("self.search_by_agent(path_out=path_out)")
        print("self.fill_the_gaps(path_out=path_out)")
        print("df = self.get_DF(NIR=self.ch_NIR, Red=self.ch_Red)")


# TEST CODE
#
# "n_row
# n_col
# i_r = 20
# i_c = 10
#
#
# (agent_right-agent_left)*(agent_down-agent_up)
#
# #
# agent_row = ls_row[i_r]
# agent_col = ls_col[i_c]
# agent_left = ls_col[i_c-1] if (i_c-1)//n_col == 0 else 0
# agent_right = ls_col[i_c+1] if (i_c+1)//n_col == 0 else px_w
# agent_up = ls_row[i_r-1] if (i_r-1)//n_row == 0 else 0
# agent_down = ls_row[i_r+1] if (i_r+1)//n_row == 0 else px_h
# #
#
# map_1d_row = map[agent_row, :]
# map_1d_col = map[:, agent_col]
#
# tol = 5
# pre_right = get_1d_edge(map=map_1d_row, agent_pt=agent_col, is_toward_pos=True, tol=tol, tol_temp=0, bound=agent_right);pre_right
# pre_left = get_1d_edge(map=map_1d_row, agent_pt=agent_col, is_toward_pos=False, tol=tol, tol_temp=0, bound=agent_left);pre_left
# pre_bottom = get_1d_edge(map=map_1d_col, agent_pt=agent_row, is_toward_pos=True, tol=tol, tol_temp=0, bound=agent_down);pre_bottom
# pre_up = get_1d_edge(map=map_1d_col, agent_pt=agent_row, is_toward_pos=False, tol=tol, tol_temp=0, bound=agent_up);pre_up
# rg_row = range(pre_up, pre_bottom)
# rg_col = range(pre_left, pre_right)
# area_max = len(rg_row)*len(rg_col)
# area_temp = 10e+9
# ratio = 0.01
# while (area_temp > area_max) & (ratio < 1):
#     right = get_2d_edge(map, agent_col, rg_row, is_search_by_row=False, is_toward_pos=True, ratio_tol=ratio)
#     left = get_2d_edge(map, agent_col, rg_row, is_search_by_row=False, is_toward_pos=False, ratio_tol=ratio)
#     bottom = get_2d_edge(map, agent_row, rg_col, is_search_by_row=True, is_toward_pos=True, ratio_tol=ratio)
#     up = get_2d_edge(map, agent_row, rg_col, is_search_by_row=True, is_toward_pos=False, ratio_tol=ratio)
#     area_temp = map[up:bottom, left:right].sum()
#     ratio += 0.05
#
#
# plt.imshow(img_k[pre_up:pre_bottom, pre_left:pre_right])
# plt.imshow(img_k[up:bottom, left:right])
#
# ratio=0.05
# right = get_2d_edge(map, agent_col, rg_row, is_search_by_row=False, is_toward_pos=True, ratio_tol=ratio)
# left = get_2d_edge(map, agent_col, rg_row, is_search_by_row=False, is_toward_pos=False, ratio_tol=ratio)
# bottom = get_2d_edge(map, agent_row, rg_col, is_search_by_row=True, is_toward_pos=True, ratio_tol=ratio)
# up = get_2d_edge(map, agent_row, rg_col, is_search_by_row=True, is_toward_pos=False, ratio_tol=ratio)
# plt.imshow(img_k[up:bottom, left:right])


# # NOTE:
# (10, 1)
# __main__:20: RuntimeWarning: Mean of empty slice.
# (11, 1)
# __main__:19: RuntimeWarning: Mean of empty slice.
