import pandas as pd
import os
import numpy as np
from pathlib import Path

def read_excel_data(excel_file_path):
    all_sheets = {}
    
    excel = pd.ExcelFile(excel_file_path)
    sheet_names = excel.sheet_names
    
    for sheet_name in sheet_names:
        df = pd.read_excel(excel, sheet_name=sheet_name)
        required_columns = ['filename', 'model_type', 'new_chain_id', 'x', 'y', 'z']
        
        if not all(col in df.columns for col in required_columns):
            print(f"Warning: Sheet {sheet_name} doesn't have all required columns. Skipping.")
            continue
            
        all_sheets[sheet_name] = df
    
    return all_sheets

def parse_atom_records(pdb_file_path):
    atom_records = []
    
    with open(pdb_file_path, 'r') as f:
        for line in f:
            if line.startswith('ATOM'):
                try:
                    x = float(line[30:38].strip())
                    y = float(line[38:46].strip())
                    z = float(line[46:54].strip())
                    
                    atom_id = line[6:11].strip()
                    atom_name = line[12:16].strip()
                    residue_name = line[17:20].strip()
                    chain_id = line[21:22].strip()
                    residue_seq = line[22:26].strip()
                    
                    atom_records.append({
                        'line': line.strip(),
                        'x': x,
                        'y': y,
                        'z': z,
                        'atom_id': atom_id,
                        'atom_name': atom_name,
                        'residue_name': residue_name,
                        'chain_id': chain_id,
                        'residue_seq': residue_seq
                    })
                except ValueError:
                    print(f"Warning: Could not parse coordinates from line: {line.strip()}")
    
    return atom_records

def match_coordinates_to_group(atom_records, excel_data):
    # Create a dictionary to store results by group
    results_by_group = {
        'af3_E1E2': [],
        'af3_E2_only': [],
        'colabfold_E1E2': [],
        'colabfold_E2_only': [],
        'boltz_E1E2': [],
        'boltz_E2_only': [],
        'chai_E1E2': [],
        'chai_E2_only': []
    }
    
    sheet_to_group = {
        'af3_e2': 'af3_E2_only',
        'colabfold_e2': 'colabfold_E2_only',
        'boltz_e2': 'boltz_E2_only',
        'chai_e2': 'chai_E2_only',
        'af3_e1e2': 'af3_E1E2',
        'colabfold_e1e2': 'colabfold_E1E2',
        'boltz_e1e2': 'boltz_E1E2',
        'chai_e1e2': 'chai_E1E2'
    }
    
    tolerance = 0.001
    
    for atom in atom_records:
        matched = False
        
        for sheet_name, df in excel_data.items():
            if sheet_name not in sheet_to_group:
                continue
                
            mask = (
                (abs(df['x'] - atom['x']) < tolerance) &
                (abs(df['y'] - atom['y']) < tolerance) &
                (abs(df['z'] - atom['z']) < tolerance)
            )
            
            matches = df[mask]
            
            if not matches.empty:
                group_name = sheet_to_group[sheet_name]
                results_by_group[group_name].append(atom['line'])
                matched = True
                break
        
        if not matched:
            print(f"Warning: No match found for coordinates: {atom['x']}, {atom['y']}, {atom['z']}")
    
    return results_by_group

def write_output_files(results_by_group, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    for group_name, lines in results_by_group.items():
        if lines:  
            output_path = os.path.join(output_dir, f"{group_name}.txt")
            
            with open(output_path, 'w') as f:
                for line in lines:
                    f.write(line + '\n')
            
            print(f"Created {output_path} with {len(lines)} entries")

def main():
    excel_file_path = r"path\to\model_data.xlsx"
    pdb_file_path = r"path\to\first_residue_alpha_carbon_list.txt"
    output_dir = r"path\to\first_residue_pdb_by_folding_method_output"
    
    print("Reading Excel data...")
    excel_data = read_excel_data(excel_file_path)
    
    print("Parsing ATOM records...")
    atom_records = parse_atom_records(pdb_file_path)
    
    print("Matching coordinates to groups...")
    results_by_group = match_coordinates_to_group(atom_records, excel_data)
    
    print("Writing output files...")
    write_output_files(results_by_group, output_dir)
    
    print("Done!")

if __name__ == "__main__":
    main()