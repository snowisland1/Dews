import numpy as np
import scipy

#保存矩阵为图片
def save_as_img(x,names):
    scipy.misc.imsave(names+".jpg",x)