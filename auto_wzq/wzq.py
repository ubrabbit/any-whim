import numpy as np
from collections import OrderedDict
from itertools import groupby

# 五子棋类
# 包装了下棋函数，判断是否胜利函数以及估值函数
# 下棋函数如果返回值为真则在该点下棋，否则下棋失败（被其他棋子占用）
# 每下一步棋就会更新 self.win 。如果该值不为 False 则为胜利者
# player in[1, 2]
class WZQ:
    def __init__(self, h, w):
        self.s_map = np.zeros((h,w)).astype(np.int32)
        self._lu = np.zeros((h,w)).astype(np.bool8)
        self._ru = np.zeros((h,w)).astype(np.bool8)
        self._area_eval = np.zeros((h,w)).astype(np.int32)
        self._scal_eval = self._create_scal(5)
        self._scal_ecal_large = self._create_scal(9)
        self.win = False
        self._values = OrderedDict([
            [(1,1,1,1,1),1000],#活五
            [(1,0,1,1,1,0,1),400],#活四
            [(0,1,1,1,1,0),400],#活四
            [(1,1,1,1,0),100],#冲四
            [(1,1,1,0,1),100],#冲四
            [(1,1,0,1,1),100],#冲四
            [(1,0,1,1,1),100],#冲四
            [(0,1,1,1,1),100],#冲四
            [(0,1,1,1,0),100],#活三
            #优冲三：因为这里如果被对手中间截断也能很快再生成冲三，所以分值较高
            [(0,1,1,0,1),60],#优冲三
            [(1,0,1,0,1),60],#优冲三
            [(1,0,1,1,0),60],#优冲三
            #劣冲三：因为这里如果被对手截断那么在这一维就直接失去价值所以分值低
            [(1,1,1,0,0),20],#劣冲三
            [(0,0,1,1,1),20],#劣冲三
            [(1,1,0,1,0),20],#劣冲三
            [(0,1,0,1,1),20],#劣冲三
            [(0,1,1,0,0),6],#活二
            [(0,0,1,1,0),6],#活二
            [(0,1,0,1,0),6],#活二
            [(1,0,1,0,0),2],#冲二
            [(0,0,1,0,1),2],#冲二
            [(1,1,0,0,0),2],#冲二
            [(0,0,0,1,1),2],#冲二
            [(0,0,0,0,1),1],#一
            [(0,0,0,1,0),1],#一
            [(0,0,1,0,0),1],#一
            [(0,1,0,0,0),1],#一
            [(1,0,0,0,0),1],#一
            ])









    #这里中间的函数主要是处理对计算范围的优化，并进行对其进行多层估值前的前置处理
    #为了类空间的优化，这里暂时就让之后的计算都共用三个变量函数内建变量：
    #self._temp_area_eval, self._temp_s_map, self._temp_win

    #另外的想法，是不是需要用一种递归的方式进行这样的处理
    #如果是递归的话，那么需要怎么存放数据，还有主要是怎么将计算范围表传递出去。
    #有点困难的就是这些。
    def _temp_area_eval_add(self, point):
        self._temp_area_eval = self._area_eval.copy()
        ph,pw = point
        (u,l) = np.maximum(np.array(point)-2, 0)
        (d,r) = np.minimum(np.array(point)+3, self.s_map.shape)
        gu,gl,gd,gr = 2-(ph-u), 2-(pw-l), 2+(d-ph), 2+(r-pw)
        self._temp_area_eval[u:d,l:r] |= self._scal_eval[gu:gd,gl:gr]
        return self._temp_area_eval

    def _temp_area_eval_adds(self, points):
        for point in points:
            self._temp_area_eval_add(point)

    def _get_points_from_temp(self):
        return np.vstack(np.where((self._temp_area_eval==1)&(self._temp_s_map==0))).transpose()

    def _temp_play_1_round(self, point):
        self._temp_s_map = self.s_map.copy()
        
        self._temp_area_eval_add(self._area_eval, point)
        self._temp_win = self._jug_win(point)
        if not self._temp_win:
            print(_get_points_from_temp(self))
    #以上函数暂时没有建好，因未调用，对程序无影响。










    #米字形的矩阵生成，用于优化计算范围
    def _create_scal(self, n):
        c = int(n/2)
        v = np.zeros((n,n),dtype=np.int32)
        v[c,:],v[:,c] = 1,1
        v = np.eye(n,dtype=np.int32)|np.eye(n,dtype=np.int32)[:,::-1]|v
        return v
    
    #找到一个点所在位置的横竖斜上的所有点以及该点在其array里的坐标
    def _find_crossNslash(self, point):
        oh,ow = self.s_map.shape
        h,w = point
        self._lu = np.eye(oh,ow,w-h).astype(np.bool8)
        self._ru = np.eye(oh,ow,ow-w-1-h).astype(np.bool8)[:,::-1]
        ph,harray = w,self.s_map[h,:]
        pw,warray = h,self.s_map[:,w]    
        plu,luarray = min((h,w))        ,self.s_map[self._lu]
        pru,ruarray = min((h,ow-w-1))   ,self.s_map[self._ru]
        return [(ph,harray),(pw,warray),(plu,luarray),(pru,ruarray)]
    
    #判断胜利
    def _jug_win(self, point):
        for idx,arr in self._find_crossNslash(point):
            for i,j in groupby(arr):
                if i!=0 and len(list(j)) >= 5:
                    return i
        return False
    
    #确保当前point没有其他落子
    #确保每下一步都会更新 self.win 。
    def play_1_round(self, point, player):
        assert player in [1,2]
        if self.s_map[point] != 0:
            return False
        self.s_map[point] = player
        self._area_eval_add(point)
        self.win = self._jug_win(point)
        return True

    #根据自身修正 array 排除对手棋子的干扰
    def _revise_array(self, idx, arr, player):
        k = 3 - player
        v = np.where(arr[:idx]==k)[0]
        minx = v.max() + 1 if len(v) else 0
        ridx = idx - minx if len(v) else idx
        v = np.where(arr[idx:]==k)[0]
        maxx = v.min() + idx if len(v) else len(arr)
        return ridx,arr[minx:maxx]

    #估值算法
    def evaluate(self, point, player):
        assert self.s_map[point] == 0 #函数只估值未下过棋的点
        self.s_map[point] = player
        core = 0
        for idx,arr in self._find_crossNslash(point):
            idx,arr = self._revise_array(idx, arr, player)
            _core_list = []
            for val in self._values:
                iidx = idx - len(val)+1 if idx - len(val)+1 > 0 else 0
                jidx = idx + 1
                _val = np.array(val) * player
                for i in range(iidx,jidx):
                    _arr = arr[i:i+len(_val)]
                    if len(_arr) == len(_val) and np.any(_arr^_val)==False:
                        _core_list.append(self._values[val])
                        break
                if len(_core_list)!= 0:
                    break
            core += max(_core_list) if len(_core_list) else 0
        #估值结束再把 s_map 原本样子还回去
        self.s_map[point] = 0
        return core

    #需要计算估值的范围
    def _area_eval_add(self, point):
        ph,pw = point
        (u,l) = np.maximum(np.array(point)-2, 0)
        (d,r) = np.minimum(np.array(point)+3, self.s_map.shape)
        gu,gl,gd,gr = 2-(ph-u), 2-(pw-l), 2+(d-ph), 2+(r-pw)
        self._area_eval[u:d,l:r] |= self._scal_eval[gu:gd,gl:gr]

    #将估值函数包装一下，使得使用起来会更加方便
    def _calc_eval_map(self, player):
        self._temp1_eval_map = np.zeros(self.s_map.shape).astype(np.int32)
        self._temp2_eval_map = np.zeros(self.s_map.shape).astype(np.int32)
        for i,j in np.vstack(np.where((self._area_eval==1)&(self.s_map==0))).transpose():
            self._temp1_eval_map[i,j] = self.evaluate((i,j),player)
        for i,j in np.vstack(np.where((self._area_eval==1)&(self.s_map==0))).transpose():
            self._temp2_eval_map[i,j] = self.evaluate((i,j),3-player)
        #这里的0.8是为了防止在预测中对手权重过高过度防御导致连自己的连五都被无视
        return (self._temp1_eval_map+self._temp2_eval_map*.8)

    #test 一层的逻辑
    #经过测试，该简单算法不能应对较为复杂的多层考虑，仅仅应用于简单难度
    def robot_level1(self, player):
        v = self._calc_eval_map(player)
        v = np.vstack(np.where(v==v.max())).transpose()
        v = v[np.random.choice(range(len(v)))]
        return v

    def robot_level2(self, player):
        pass
    
        

#以下只用于简单语法错误的检查测试test
if __name__== '__main__':
    wzq = WZQ(15,15)
    player = 2
    print(wzq.play_1_round((0,6),1))
    print(wzq.play_1_round((1,4),1))
    print(wzq.play_1_round((3,2),1))
    print(wzq.play_1_round((3,7),1))
    print(wzq.play_1_round((6,4),1))
    print(wzq.play_1_round((1,5),player))
    print(wzq.play_1_round((2,4),player))
    print(wzq.play_1_round((3,3),player))
    print(wzq.play_1_round((3,5),player))
    print(wzq.play_1_round((4,2),player))
    print(wzq.play_1_round((4,4),player))
    print(wzq.play_1_round((3,4),player))
    print(wzq.play_1_round((12,12),player))
    print(wzq.play_1_round((14,14),player))
    print(wzq.s_map)
    import time
    _t = time.time()
    print(wzq.evaluate((2,2),2))
    h,w = wzq.s_map.shape
    v = np.zeros(wzq.s_map.shape).astype(np.int32)
    for i,j in np.vstack(np.where(wzq._area_eval==1)).transpose():
        if wzq.s_map[i,j] == 0:
            v[i,j] = wzq.evaluate((i,j),2)
    print(v)
    print(time.time()-_t)
