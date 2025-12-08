import argparse
import pandas as pd
parser = argparse.ArgumentParser(description='Build graph data')
parser.add_argument('--data_name', type=str, help='the data name')
args = parser.parse_args()

data = args.data_name

input_csv = '../data/origin_data/' + data + '.csv'

df = pd.read_csv(input_csv)

if 'smiles' not in df.columns:
	print("'smiles' not detected")
	if 'SMILES' in df.columns:
		print("   -->'SMILES' found! ")
		df['smiles'] = df['SMILES']

if 'group' not in df.columns:
	print("'group' not detected, adding as 'test'")
	df['group'] = 'test'

if data not in df.columns:
	print(f"'{data}' not found as label")
	if 'Prediction_Mean' in df.columns:
		print("   -->'Prediction_Mean' found! Using values for continuity, not as true label ")
		df[data] = df['Prediction_Mean']

df.to_csv(input_csv, index=False)
