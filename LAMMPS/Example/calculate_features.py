#%% IMPORTS
import os
from rdkit import Chem
from rdkit.Chem import Descriptors
from pyl3dmd import pyl3dmd
import pandas as pd
import numpy as np
import re 

#%% FUNCTIONS
def getMolDescriptors_static(smiles, missingVal=None):
    ''' calculate the full list of descriptors for a molecule
        missingVal is used if the descriptor cannot be calculated
    '''
    mol = Chem.MolFromSmiles(smiles)
    res = {}
    for nm,fn in Descriptors._descList:
        # some of the descriptor fucntions can throw errors if they fail, catch those here:
        try:
            val = fn(mol)
        except:
            # print the error message:
            import traceback
            traceback.print_exc()
            # and set the descriptor value to whatever missingVal is
            val = missingVal
        res[nm] = val
    # Calculate custom features that are not in here
    molecule_with_H = Chem.AddHs(mol)
    for element in ['C','H','O','F']:
        Num_X_Atoms = sum(1 for atom in molecule_with_H.GetAtoms() if atom.GetSymbol() == element)
        res[f'Num_{element}_Atoms'] = Num_X_Atoms
    return res

def find_eqmT_in_file(file_path):
    # Example: get 300 from "variable            eqmT        equal 300      "
    pattern = r"eqmT\s+equal\s+([-+]?\d*\.\d+|\d+)"
    with open(file_path, 'r') as file:
        for line in file:
            stripped_line = line.strip()  		# Remove leading/trailing whitespaces
            if stripped_line.startswith('#'):
                continue  						# Skip this iteration if the line is commented
            match = re.search(pattern, stripped_line)
            if match:
                float_number = float(match.group(1))  # Convert to float
                return float_number  # Return if you need to store or use it
    print("No matching line found.")
    return np.nan

#%% MAIN
# List directory files
structureFiles = os.listdir('./InitialStructure')

# Get step files
StepFiles = os.listdir('./Step3')

# Data file
dataFiles = [ filename for filename in structureFiles if filename.endswith( '.data' ) ]
dataFile = './InitialStructure/' + dataFiles[0]

# Get SMILES String
SMILESFiles = [ filename for filename in structureFiles if filename.endswith( '.smiles' ) ]
SMILESFile = './InitialStructure/' + SMILESFiles[0]
with open(SMILESFile, 'r') as file:
    SMILES_String = file.read().replace('\n', '')

# Get simulation temperature
logFiles = [ filename for filename in StepFiles if filename.endswith( '.log' ) ]
LogFile = './Step3/' + logFiles[0]
T = find_eqmT_in_file(LogFile)

# Final dump file
dumpFiles = [ filename for filename in StepFiles if filename.endswith( '.lammpstrj' ) ]
dumpFile = './Step3/' + dumpFiles[0]

# Initialize PyL3dMD program
program = pyl3dmd.pyl3dmd(dataFile, dumpFile,averageAll=True)

# Run PyL3dMD
program.start()

# Read the results
df_pyl3dmd = pd.read_csv('./AveragedAll.csv')

# index definition from describe function 
# describe_key = {
# 	0: 'count',
# 	1:'mean',
# 	2:'std',
# 	3:'min',
# 	4:'25%',
# 	5:'50%',
# 	6:'75%',
# 	7:'max',
# 	}

# Drop the "count" row and ["Molecule", 'Timeframe'] column
df_pyl3dmd.drop(columns=["molecule", 'Timeframe'], inplace=True)
df_pyl3dmd.drop(0, inplace=True)
# Flatten results
flat_desc = df_pyl3dmd.transpose().reset_index()

# Reset the column names
flat_desc.columns.name = None

# Prepare the new column names
new_columns = [f"{col}_{stat}" for col in flat_desc['index'] for stat in df_pyl3dmd.index]

# Create a new DataFrame with the flattened structure
flat_desc = pd.DataFrame(flat_desc.drop('index', axis=1).values.flatten()[None, :], columns=new_columns)

# Add Temperature column 
flat_desc.insert(0, 'Temperature[K]', T)

# Add SMILES column 
flat_desc.insert(0, 'SMILES', SMILES_String)

# Add target simulation temperature

# Calculate static features from rdkit
static_df = flat_desc['SMILES'].apply(getMolDescriptors_static).apply(pd.Series)

# Combine static and dynamic features
df_FULL_FEATURES = pd.concat([flat_desc, static_df], axis=1)

# Write the features to csv file
df_FULL_FEATURES.to_csv('./Example_Features.csv', index=False)

