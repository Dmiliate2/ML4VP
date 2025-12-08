from SMEG_model_hyperopt import SMEG_hyperopt
from maskgnn import set_random_seed
import argparse
import warnings

warnings.filterwarnings('ignore')

parser = argparse.ArgumentParser(description='Develop RGCN models')
parser.add_argument('--task_name', type=str, help='the task name')
args = parser.parse_args()

if __name__ == '__main__':
    task = args.task_name
    set_random_seed(10)
    classification_task_list = [] # EDIT: No classifications in ML4VP
    
    # EDIT: Assume regression unless in classification list
    if task in classification_task_list:
        SMEG_hyperopt(10, task, 30, classification=True)
    else:
        SMEG_hyperopt(10, task, 30, classification=False)