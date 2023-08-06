from enum import Enum

class Dir(Enum):
    NORTH=0
    WEST=1
    SOUTH=2
    EAST=3


class Field():
    def __init__(self, img, img_std, map):
        '''
        '''
        self.img_raw = img
        self.img_std = img_std
        self.map = map
        self.img_bin = None
        self.px_H, self.px_W = img.shape[0], img.shape[1]
        self.nrow, self.ncol = map.shape[0], map.shape[1]
        self.agents = [[Agent(map.iloc[i, j], i, j) for j in range(self.ncol)] for i in range(self.nrow)]
    def set_binary(self, img_b):
        '''
        '''
        self.img_bin = img_b
    def get_agent(self, row, col):
        '''
        '''
        if (row<0) | (row>=self.nrow) | (col<0) | (col>=self.ncol):
            return 0
        else:
            return self.agents[row][col]
    def get_agent_neighbor(self, row, col, dir=Dir.NORTH):
        '''
        '''
        if dir==Dir.NORTH:
            return self.get_agent(row-1, col)
        elif dir==Dir.EAST:
            return self.get_agent(row, col+1)
        elif dir==Dir.SOUTH:
            return self.get_agent(row+1, col)
        elif dir==Dir.WEST:
            return self.get_agent(row, col-1)
    def set_anchors(self, ls_row, ls_col):
        '''
        '''
        for row in range(self.nrow):
            for col in range(self.ncol):
                self.get_agent(row, col).set_coordinate(ls_row[row], ls_col[col])
    def cpu_pre_dim(self, tol=5):
        '''
        '''
        for row in range(self.nrow):
            for col in range(self.ncol):
                agent_self = self.get_agent(row, col)
                rg_temp = dict()
                for dir in list([Dir.NORTH, Dir.EAST, Dir.SOUTH, Dir.WEST]):
                    # extract direction info
                    idx_axis = dir.value%2 # 0: N or S, 1: W or E
                    is_pos = 2*(dir.value//2)-1 # -1: N or W, 1: S or E
                    # extract agents info
                    agent_neig = self.get_agent_neighbor(row, col, dir)
                    # if neighbor exists
                    if agent_neig:
                        px_self = get_coordinate()[idx_axis]
                        px_neig = get_coordinate()[idx_axis]
                        pt_mid = (px_self+px_neig)/2
                        # iteratively search
                        img_1d = self.img_bin[px_self,:] if idx_axis else self.img_bin[:,px_self]
                        px_cur = px_self
                        tol = tol
                        tol_cur = 0
                        while (tol_cur < tol) & (px_self*is_pos < px_mid*is_pos):
                            try:
                                img_val = img_1d[px_cur]
                            else:
                                break
                            tol_cur += 1 if img_val==0 else -tol_cur #else reset to 0
                            px_cur += is_pos
                        rg_temp[dir.name] = px_cur
                    # exception: self is on the border (N and W)
                    elif is_pos==-1:
                        rg_temp[dir.name] = 0
                        agent_self.set_border(dir, 0)
                    # exception: self is on the border (S and E)
                    else:
                        rg_temp[dir.name] = self.img_bin.shape[idx_axis]
                        agent_self.set_border(dir, self.img_bin.shape[idx_axis])
                agent_self.set_pre_dim(rg_temp)
    def cpu_bound(self, coef_grid=.2):
        '''
        '''
        for row in range(self.nrow):
            for col in range(self.ncol):
                agent_self = self.get_agent(row, col)
                for dir in list([Dir.EAST, Dir.SOUTH]):
                    agent_neig = self.get_agent_neighbor(row, col, dir)
                    dir_neig = list(Dir)[(dir.value+2)%4] # reverse the direction
                    if agent_neig:
                        dist_agents = abs(agent_self.x-agent_neig.x) if dir==Dir.EAST else abs(agent_self.y-agent_neig.y)
                        while abs(agent_self.get_border(dir)-agent_neig.get_border(dir_neig))>1:
                            scA_self = agent_self.get_score_area(dir, self.img_bin)
                            scG_self = agent_self.get_score_grid(dir)/dist_agents
                            scA_neig = agent_neig.get_score_area(dir_neig, self.img_bin)
                            scG_neig = agent_neig.get_score_grid(dir_neig)/dist_agents
                            score_self = scA_self - (scG_self*coef_grid)
                            score_neig = scA_neig - (scG_neig*coef_grid)
                            if score_self > score_neig:
                                agent_self.update_border(dir, 1)
                            elif score_self < score_neig:
                                agent_neig.update_border(dir_neig, -1)
                            else:
                                agent_self.update_border(dir, 1)
                                agent_neig.update_border(dir_neig, -1)


class Agent():
    def __init__(self, name, row, col):
        '''
        '''
        self.name = name
        self.row, self.col = row, col
        self.y, self.x = 0, 0
        self.pre_rg_W, self.pre_rg_H = range(0), range(0)
        self.boundary = dict()
        for dir in list([Dir.NORTH, Dir.EAST, Dir.SOUTH, Dir.WEST]):
            self.boundary[dir.name] = 0
    def get_col(self):
        '''
        '''
        return self.col
    def get_row(self):
        '''
        '''
        return self.row
    def get_coordinate(self):
        '''
        '''
        return self.y, self.x
    def get_pre_dim(self, isHeight=True):
        '''
        '''
        return self.pre_rg_H if isHeight else self.pre_rg_W
    def get_border(self, dir):
        return self.border[dir.name]
    def get_score_area(self, dir, img):
        '''
        Will ragne from 0 to 1
        '''
        isH = dir.value%2 # E->1, S->0
        rg = self.get_pre_dim(isHeight=isH)
        bd = self.get_border(dir)
        return img[bd, rg].mean() if isH else img[rg, bd].mean()
    def get_score_grid(self, dir):
        '''
        Will ragne from 0 to 1
        '''
        isWE = dir.value%2 # is W, E or N, S
        pt_center = self.x if isWE else self.y
        pt_cur = self.get_border(dir)
        return abs(pt_cur-pt_center)
    def set_coordinate(self, y, x):
        '''
        '''
        self.y = y
        self.x = x
        self.set_border(Dir.NORTH) = y
        self.set_border(Dir.SOUTH) = y
        self.set_border(Dir.WEST) = x
        self.set_border(Dir.EAST) = x
    def set_pre_dim(self, rg):
        '''
        '''
        self.pre_rg_W = range(rg['WEST'], rg['EAST'])
        self.pre_rg_H = range(rg['NORTH'], rg['SOUTH'])
    def set_border(self, dir, value):
        '''
        '''
        self.border[dir.name] = value
    def update_border(self, dir, value):
        '''
        '''
        self.border[dir.name] += value
