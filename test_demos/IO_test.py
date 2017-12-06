from IOs.IOs import read_time_series

timeseries=read_time_series("../dataset/ydata-labeled-time-series-anomalies-v1_0/A1Benchmark/real_1.csv")
print(timeseries.head())