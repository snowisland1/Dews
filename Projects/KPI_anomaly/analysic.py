import pandas as pd
import numpy as np
from utils.data_construct import make_samples,make_samples_without_label
from Metrics.metrics import label_evaluation

filepath1="../../dataset/anomaly_detection_1/train.csv"
data=pd.read_csv(filepath1)
filepath2 = "../../dataset/anomaly_detection_1/test_dataset.csv"
submit = pd.read_csv(filepath2)
KPI_ID = pd.unique(data['KPI ID'])
KPI_ID00 = data[data['KPI ID']==KPI_ID[0]]
KPI_ID01 = submit[submit['KPI ID']==KPI_ID[1]]
samples = make_samples(KPI_ID[0],np.array(KPI_ID00['timestamp']),np.array(KPI_ID00['value']),np.array(KPI_ID00['label']),40)
for kpi_id in KPI_ID[1:27]:
    kpi_data = data[data['KPI ID']==kpi_id]
    tmp = make_samples(kpi_id,np.array(kpi_data['timestamp']),np.array(kpi_data['value']),np.array(kpi_data['label']),40)
    samples = pd.concat([samples,tmp])
    print(kpi_id)
KPI_ID01 = submit[submit['KPI ID']==KPI_ID[0]]
submit_samples = make_samples_without_label(KPI_ID[0],np.array(KPI_ID00['timestamp']),np.array(KPI_ID00['value']),40)
for kpi_id in KPI_ID[1:27]:
    kpi_data = submit[submit['KPI ID']==kpi_id]
    tmp = make_samples_without_label(kpi_id,np.array(kpi_data['timestamp']),np.array(kpi_data['value']),40)
    submit_samples = pd.concat([submit_samples,tmp])
    print(kpi_id)
samples_train = samples[samples.label==0]
#Isolation Forest
from sklearn.ensemble import IsolationForest
clf = IsolationForest(n_estimators=50,max_samples = 0.0005,verbose=1)
clf.fit(samples_train.iloc[:,0:40])
y_pred_sampes=clf.predict(samples.iloc[:,0:40])
y_pred_submit=clf.predict(submit_samples.iloc[:,0:40])
samples['predict']=y_pred_sampes
submit_samples['predict']=y_pred_submit
data   = pd.merge(data,samples[["id","time","predict"]],left_on=["KPI ID","timestamp"],right_on=["id","time"],how='left')
submit=pd.merge(submit,submit_samples[["id","time","predict"]],left_on=["KPI ID","timestamp"],right_on=["id","time"],how='left')
data = data[["KPI ID","timestamp","label","predict"]]
data["predict"][np.isnan(data.predict)]=0
data["predict"][data.predict==1]=0
data["predict"][data.predict==-1]=1
submit[["KPI ID","timestamp","predict"]].to_csv("submit1.csv")
print (label_evaluation(data.iloc[:,[0,1,2]],data.iloc[:,[0,1,3]]))