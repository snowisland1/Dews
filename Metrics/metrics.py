import numpy as np
import pandas as pd
import json
from sys import argv
from sklearn.metrics import precision_score,recall_score,f1_score

# consider delay threshold and missing segments
def get_range_proba(predict, label, delay=7):

    splits = np.where(label[1:] != label[:-1])[0] + 1
    is_anomaly = label[0] == 1
    new_predict = np.array(predict)
    pos = 0

    for sp in splits:
        if is_anomaly:
            if 1 in predict[pos:min(pos + delay + 1,sp)]:
                new_predict[pos: sp] = 1
            else:
                new_predict[pos: sp] = 0
        is_anomaly = not is_anomaly
        pos = sp
    sp = len(label)

    if is_anomaly:  #anomaly in the end
        if 1 in predict[pos: min(pos + delay+1,sp)]:
            new_predict[pos: sp] = 1
        else:
            new_predict[pos: sp] = 0
    return new_predict

# set missing = 0
def reconstruct_label(timestamp, label):
    timestamp = np.asarray(timestamp, np.int64)
    timestamp_sorted = np.asarray(timestamp[np.argsort(timestamp)])
    interval = np.min(np.diff(timestamp_sorted))
    if interval == 0:
        print(timestamp_sorted)
    idx = (timestamp_sorted - timestamp_sorted[0]) // interval
    new_label = np.zeros(shape=((timestamp_sorted[-1] - timestamp_sorted[0]) // interval + 1,), dtype=np.int)
    new_label[idx] = label
    return new_label

def label_evaluation(truth_df, result_df, delay=7):
    data = {'result': False, 'data': "", 'message': ""}
    kpi_names = truth_df['KPI ID'].values
    kpi_names = np.unique(kpi_names)
    y_true_list = []
    y_pred_list = []
    for kpi_name in kpi_names:
        truth = truth_df[truth_df["KPI ID"] == kpi_name]
        y_true = reconstruct_label(truth["timestamp"], truth["label"])
        try:
            result = result_df[result_df["KPI ID"] == kpi_name]
            y_pred = reconstruct_label(result["timestamp"], result["predict"])
        except:
            data['message'] = "The file you submitted need contain 'predict','timestamp' and  \
                             'KPI ID' columns"
            return json.dumps(data)
        try:
            assert np.array_equal(len(y_true),len(y_pred)) == True
        except:
            data['message'] = "The length of your submitted file is wrong"
            return json.dumps(data)

        y_pred = get_range_proba(y_pred, y_true, delay)
        y_true_list.append(y_true)
        y_pred_list.append(y_pred)

    fscore = f1_score(np.concatenate(y_true_list), np.concatenate(y_pred_list))
    data['result'] = True
    data['data'] = fscore
    data['message'] = 'success'
    print(json.dumps(data))
    return json.dumps(data)
