import pandas as pd
import numpy as np
import pylab as pl
from sklearn.metrics import roc_auc_score

#独热编码函数
def add_dummy(samples,col):
    oht = pd.get_dummies(samples[col])
    oht.columns = map(lambda x:col+str(x),np.unique(samples[col].dropna().values))
    samples = samples.join(oht)
    return [samples,oht.columns]

#交叉特征函数
def cross_feas(samples,cols1,cols2):
    feas=[]
    for col1 in cols1:
        for col2 in cols2:
            feas.append(col1+"*"+col2)
            samples[col1+"*"+col2] = [a*b for a,b in zip(samples[col1].values,samples[col2].values)]
    return feas

#获得时间序列的周期
def getPeriod(timeseries,index,value,fft_size):
    length = len(timeseries)
    x = timeseries.loc[:,value]
    xs = x[:fft_size]
    xf = np.fft.rfft(xs)
    freqs = np.linspace(0, length / 2, fft_size / 2 + 1)
    xfp = 20 * np.log10(np.clip(np.abs(xf), 1e-20, 1e100))
    pl.figure(figsize=(8, 4))
    pl.subplot(211)
    pl.plot(timeseries[index][:fft_size], xs)
    pl.title("时间序列的波形和频谱")
    pl.subplot(212)
    pl.plot(freqs, xfp)
    pl.xlabel(u"频率(Hz)")
    pl.subplots_adjust(hspace=0.4)
    pl.show()
    return xfp

def auc_score(true_y,pred_y):
    return roc_auc_score(true_y,pred_y)



