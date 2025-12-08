import pandas as pd
from sklearn.metrics import r2_score, roc_auc_score
import argparse


def pred2label(prob):
    if prob < 0.5:
        return 0
    else:
        return 1

parser = argparse.ArgumentParser(description='More Explain')
parser.add_argument('--task_name', type=str, help='the task name')
args = parser.parse_args()

task = args.task_name

for group in ['val','training','test']:
    data = pd.read_csv('./summary/{}_mol_prediction_summary.csv'.format(task))

    if task in ['Mutagenicity', 'hERG']:
        data = data[data['group']==group]
        pred_label_list = [pred2label(prob) for prob in data['pred_mean'].tolist()]
        roc = roc_auc_score(data['label'], data['pred_mean'])
        print('{} {} roc_auc: {}'.format(task, group, roc))
        print(len(data))
    else:
        data = data[data['group']==group]
        r2 = r2_score(data['label'], data['pred_mean'])
        print('{} {} r2: {}'.format(task, group, r2))
        print(len(data))