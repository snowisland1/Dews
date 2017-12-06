import numpy as np


def AnomalyDetectionWithMedian(timeseries,period,direction,rate):
    result={
        "before":AnomalyDetectionWithMedianBefore(timeseries,period,rate),
        "after":AnomalyDetectionWithMedianAfter(timeseries,period,rate),
        "both":AnomalyDetectionWithMedianBoth(timeseries,period,rate)
    }
    return result.get(direction)(timeseries,period)

def AnomalyDetectionWithMedianBefore(timeseries,period,rate):
    result=np.array()
    for i in range(len(timeseries)):
        if i == 0 :
            result.append(False)
        elif i<period :
            tmp_timeseries=timeseries[0:i-1]
            median=np.median(tmp_timeseries)
            result.append(True) if abs(timeseries[i]-median)>abs(median)*rate else result.append(False)
        else :
            tmp_timeseries=timeseries[i-period:i-1]
            median=np.median(tmp_timeseries)
            result.append(True) if abs(timeseries[i]-median)>abs(median)*rate else result.append(False)
    return result

def AnomalyDetectionWithMedianAfter(timeseries,period,rate):
    result=np.array()
    length=len(timeseries)
    for i in range(len(timeseries)):
        if i<len(timeseries)-period:
            tmp_timeseries = timeseries[i + 1, length - 1]
            median = np.median(tmp_timeseries)
            result.append(True) if abs(timeseries[i] - median) > abs(median) * rate else result.append(False)
        elif i==(length-1):
            result.append(False)
        else:
            tmp_timeseries=timeseries[i+1,length-1]
            median=np.median(tmp_timeseries)
            result.append(True) if abs(timeseries[i] - median) > abs(median) * rate else result.append(False)
    return result

def AnomalyDetectionWithMedianBoth(timeseries,period,rate):
    return None
