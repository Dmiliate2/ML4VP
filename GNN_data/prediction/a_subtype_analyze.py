import pandas as pd
from sklearn import metrics
from math import sqrt
import seaborn as sns
import matplotlib.pyplot as plt
import argparse



def prob2label(prob):
    if prob<0.5:
        return 0
    else:
        return 1


parser = argparse.ArgumentParser(description='More Explain')
parser.add_argument('--task_name', type=str, help='the task name')
args = parser.parse_args()
task_name = args.task_name


for sub_type in ['fg', 'murcko', 'brics', 'brics_emerge', 'murcko_emerge']:
    result = pd.read_csv('./attribution/{}_{}_attribution_summary.csv'.format(task_name,sub_type))
    # result = result[result['group']=='training']
    fg_list = list(set(result['sub_name'].tolist()))
    fg_list.sort()
    print(len(fg_list), fg_list)
    average_attribution_fg = pd.DataFrame()
    mol_num_list = []
    mean_att_list = []
    for i, fg in enumerate(fg_list):
        result_fg = result[result['sub_name']==fg]
        attribution_mean = result_fg['attribution'].mean()
        # 正负改过来，对应毒性问题时，正值是利于毒性，为了可视化，将其改为负值
        pred_labels = [prob2label(prob) for prob in result_fg['mol_pred_mean'].tolist()]
        if len(result_fg)>10:
            print('**************************************************************************************')
            print("{} {}. number of mol: {}; attribution: {}".format(fg, sub_type,len(result_fg), round(attribution_mean, 4)))
            print('**************************************************************************************')
            print()
        mol_num_list.append(len(result_fg))
        mean_att_list.append(round(attribution_mean, 4))

    print()
    average_attribution_fg['sub_name'] = [fg for fg in fg_list]
    average_attribution_fg['mol_num'] = mol_num_list
    average_attribution_fg['attribution_mean'] = mean_att_list
    average_attribution_fg.sort_values(by=['attribution_mean'], inplace=True)
    average_attribution_fg.to_csv('A_{}_{}_average_attribution_summary.csv'.format(task_name,sub_type), index=False)


