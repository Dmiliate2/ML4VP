import pandas as pd
import os
import argparse

parser = argparse.ArgumentParser(description='Build graph data')
parser.add_argument('--task_name', type=str, help='the task name')
parser.add_argument('--data_name', type=str, default='', help='the task name')
args = parser.parse_args()
task_name= args.task_name
if args.data_name != '':
    data_name = args.data_name + '_'
else:
    data_name=''


sub_type_list = ['mol', 'fg', 'murcko', 'brics', 'brics_emerge', 'murcko_emerge']
for sub_type in sub_type_list:
    try:
        print('{} {} sum succeed.'.format(task_name, sub_type))
        # 将训练集，验证集，测试集数据合并
        result_summary = pd.DataFrame()

        for i in range(10):
            seed = i + 1
            results_list = []
            group_list = []
            file_path = '../prediction/{}/{}{}_{}_{}_train_prediction.csv'.format(sub_type, data_name, task_name, sub_type, seed)
            if os.path.exists(file_path):
                result_train = pd.read_csv(file_path)
                results_list.append(result_train)
                group_list = group_list +  ['training' for x in range(len(result_train))]
            
            file_path = '../prediction/{}/{}{}_{}_{}_val_prediction.csv'.format(sub_type, data_name, task_name, sub_type, seed)
            if os.path.exists(file_path):
                result_val = pd.read_csv(file_path)
                results_list.append(result_val)
                group_list = group_list +  ['val' for x in range(len(result_val))]
            
            file_path = '../prediction/{}/{}{}_{}_{}_test_prediction.csv'.format(sub_type, data_name, task_name, sub_type, seed)
            if os.path.exists(file_path):

                result_test = pd.read_csv(file_path)
                # print('Got Here')    
                results_list.append(result_test)
                group_list = group_list +  ['test' for x in range(len(result_test))]
            # group_list = ['training' for x in range(len(result_train))] + ['val' for x in range(len(result_val))] + ['test' for
                                                                                                                 # x in range(
                    # len(result_test))]
            result = pd.concat(results_list, axis=0)
            # mol是模型最初预测的时候给的结果，batch是会随机乱序的，所以需要重新排序
            result['group'] = group_list

            if sub_type == 'mol':
                result.sort_values(by='smiles', inplace=True)
            # 合并五个随机种子结果，并统计方差和均值
            if seed == 1:
                result_summary['smiles'] = result['smiles']
                result_summary['label'] = result['label']
                result_summary['sub_name'] = result['sub_name']
                result_summary['group'] = result['group']
                result_summary['pred_{}'.format(seed)] = result['pred'].tolist()
            if seed > 1:
                result_summary['pred_{}'.format(seed)] = result['pred'].tolist()
        pred_columnms = ['pred_{}'.format(i+1) for i in range(10)]
        data_pred = result_summary[pred_columnms]
        result_summary['pred_mean'] = data_pred.mean(axis=1)
        result_summary['pred_std'] = data_pred.std(axis=1)
        dirs = '../prediction/summary/'
        if not os.path.exists(dirs):
            os.makedirs(dirs)
        result_summary.to_csv('../prediction/summary/{}{}_{}_prediction_summary.csv'.format(data_name, task_name, sub_type), index=False)
    except:
        print('{} {} sum failed.'.format(task_name, sub_type))