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
# #              TRAIN MODEL
# #########################################

# define task to train model
task='VP_LOGPA'

# Convert string to graph
echo "Building graph data"
python build_graph_dataset.py --task_name ${task}

# Train models
echo "Training models"
python Main.py --task_name ${task}
exit 0
# Substructure-Mask-Explanation
echo "Substructure-Mask-Explanation"
python SMEG_explain_for_substructure.py --task_name ${task} # calculate the prediction of molecules with different substructures masked

# Summarize predictions
echo "Summarize predictions"
python prediction_summary.py --task_name ${task} # summary the prediction of molecules with different substructures mask

# Calculate attributions
echo "Calculate attributions"
python attribution_calculate.py --task_name ${task} # calculate the attribution of different substructures

# Final predictions and model evaluation
cd ../prediction
echo "Model evaluation"
python a_subtype_analyze.py --task_name ${task}
python model_evaluation.py --task_name ${task}

