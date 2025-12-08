#!/bin/bash
#####################################################################
# Initialize
module purge
module load openmpi/4.0.6-intel-2021.4.0
LMP=/home/dmiliate/data/lammps-29Sep2021/build/lmp_kk
NSLOTS=$(($SLURM_NNODES*$SLURM_NTASKS_PER_NODE))

# Create an array of all files in the directory
inFile_arr=("S0_Min.in" "S1_NVT.in" "S2_NPT.in" "S3_NPT.in")

# Run simulation
for X in {0..3}; do
  echo "Running Step${X}"
  mkdir Step${X}
  mpirun -np ${NSLOTS} ${LMP} -log ./Step${X}/Step${X}.log -k on -sf kk -in ${inFile_arr[${X}]} > ./Step${X}/Realtime.txt
done

# Load ML4VP module
source /data/dmiliate/anaconda3/etc/profile.d/conda.sh # path to anaconda where ML4VP was installed
conda activate ML4VP

# Run python script
echo "Calculating features"
python calculate_features.py

echo "Done"
