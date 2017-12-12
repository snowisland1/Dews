import pandas as pd
import numpy as np
import pylab as pl
from sklearn.metrics import roc_auc_score,precision_score,recall_score

#one hot code
def add_dummy(samples,col):
    oht = pd.get_dummies(samples[col])
    oht.columns = map(lambda x:col+str(x),np.unique(samples[col].dropna().values))
    samples = samples.join(oht)
    return [samples,oht.columns]

#cross feature
def cross_feas(samples,cols1,cols2):
    feas=[]
    for col1 in cols1:
        for col2 in cols2:
            feas.append(col1+"*"+col2)
            samples[col1+"*"+col2] = [a*b for a,b in zip(samples[col1].values,samples[col2].values)]
    return feas

#get the period of time series
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
    pl.title("wave and frequency of timeseries")
    pl.subplot(212)
    pl.plot(freqs, xfp)
    pl.xlabel(u"frequency(Hz)")
    pl.subplots_adjust(hspace=0.4)
    pl.show()
    return xfp

def auc_score(true_y,pred_y):
    return roc_auc_score(true_y,pred_y)

def precision_score(true_y,pred_y):
    return precision_score(true_y=true_y,pred_y=pred_y)

def recall_score(true_y,pred_y):
    return recall_score(true_y=true_y,pred_y=pred_y)


def append_data(dic,key,value):
    """
    Insert a value to a dict
    :param dic: the target dict
    :param key:
    :param value:
    :return:
    """
    if(dic.has_key(key)):
        dic[key].append(value)
    else:
        dic[key] = [value]
    return dic

def getStrs(pre,num):
    """
    get a standard strings
    :param pre:
    :param num: how much strings to return
    :return:
    """
    result = []
    for i in range(num):
        result.append(pre+str(i))
    return result

def  SeriesStandard(series):
    """
    return a new series which the mean is 0 and variance is 1
    :param series:
    :return:
    """
    mean = np.mean(series)
    variance = np.var(series)
    series = (series-mean)/variance
    return series