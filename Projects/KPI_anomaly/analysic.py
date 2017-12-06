import numpy as np
from IOs.IOs import read_time_series_with_ananomly
from Algorithms.AnomalyDetection.tsbitmaps.tsbitmapper import  TSBitMapper
from utils.utils import auc_score

filepath="../../dataset/demo.csv"
data=read_time_series_with_ananomly(file_path=filepath,timeparse="datetime",index_col="timestamp",
                                    header_num=0,ananomly_col="label")

if __name__ == '__main__':
    filepath = "../../dataset/anomaly_detection_1/train.csv"
    data = read_time_series_with_ananomly(file_path=filepath, timeparse="datetime", index_col="timestamp",types_col="KPI ID",
                                          header_num=0, ananomly_col="label",value_col="value")
    types = data.get_types()
    bmp = TSBitMapper(feature_window_size=20, bins=5, level_size=3, lag_window_size=200, lead_window_size=40)

    for type in types:
        ts1 = data.get_dataframe(type=type)
        ts = np.array(ts1.value)
        ypred_unsupervised = bmp.fit_predict(ts)
        real = np.array(ts1.label)
        auc = auc_score(real,ypred_unsupervised)
        print(ts1.value)
    #ts1 =
    print("end")
