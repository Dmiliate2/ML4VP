#!/bin/bash
#SBATCH --job-name=TRAIN_VP
#SBATCH --partition=test
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=10
#SBATCH --gres=gpu:1
#SBATCH --mem=80G
#SBATCH --time=01:00:00
#SBATCH --export=ALL

module purge
source /data/dmiliate/anaconda3/etc/profile.d/conda.sh
conda activate ML4VP
module load gcc/12.2.0 
module load cuda/11.8.0-zrz66eu

# #########################################
# #               USE MODEL
# #########################################

# define task to train model
task='VP_LOGPA'
data='GPR_Predictions'

# Prepare data 
echo "Prepare GPR data"
python prepare_data.py --data_name ${data}


# Convert string to graph
echo "Building graph data"
#python build_graph_dataset.py --task_name ${data}

# # Predicting mol
echo "Predicting"
python SMEG_for_mol.py --data_name ${data} --model_name ${task}

# Summarize predictions
echo "Summarize predictions (ONLY mol)"
python prediction_summary.py --data_name ${data} --task_name ${task} # summary the prediction of molecules with different substructures mask

# calculate attribution (if desired)
python attribution_calculate.py --task_name ${task} # calculate the attribution of different substructures

# Copy to target
cp "../prediction/summary/GNN_${data}_${task}_mol_prediction_summary.csv" ../../New_Molecules/.
