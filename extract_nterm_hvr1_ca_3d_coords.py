import pandas as pd
import os

def parse_txt_file(file_path):
    chain_data = {}
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith('ATOM'):
                chain_id = line[20:22].strip()
                x = float(line[30:38].strip())
                y = float(line[38:46].strip())
                z = float(line[46:54].strip())
                
                chain_data[chain_id] = {
                    'x': x,
                    'y': y,
                    'z': z
                }
    return chain_data

def parse_csv_file(file_path):
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        return pd.read_csv(file_path)
    else:
        return pd.DataFrame()

def create_excel_with_sheets(txt_data, e2_data, e1e2_data, output_path):
    # Create a dictionary to hold dataframes for each sheet
    sheets = {
        'af3_e2': [],
        'af3_e1e2': [],
        'colabfold_e2': [],
        'colabfold_e1e2': [],
        'boltz_e2': [],
        'boltz_e1e2': [],
        'chai_e2': [],
        'chai_e1e2': []
    }
    
    # Process E2 data
    if not e2_data.empty:
        for _, row in e2_data.iterrows():
            filename = row['filename']
            model_type = row['model_type']
            new_chain_id = row['new_chain_id']
            
            # Only process entries that match in the txt file
            if new_chain_id in txt_data:
                # Determine which sheet to add to
                if 'af3' in filename.lower():
                    software = 'af3'
                elif 'colabfold' in filename.lower():
                    software = 'colabfold'
                elif 'boltz' in filename.lower():
                    software = 'boltz'
                elif 'chai' in filename.lower():
                    software = 'chai'
                else:
                    software = 'unknown'
                
                sheet_key = f"{software}_e2"
                
                coords = txt_data[new_chain_id]
                data_entry = {
                    'filename': filename,
                    'model_type': model_type,
                    'new_chain_id': new_chain_id,
                    'x': coords['x'],
                    'y': coords['y'],
                    'z': coords['z']
                }
                
                if sheet_key in sheets:
                    sheets[sheet_key].append(data_entry)
    
    # Process E1E2 data (if it exists and is not empty)
    if not e1e2_data.empty:
        for _, row in e1e2_data.iterrows():
            filename = row['filename']
            model_type = row['model_type']
            new_chain_id = row['new_chain_id']
            
            # Only process entries that match in the txt file
            if new_chain_id in txt_data:
                # Determine which sheet to add to
                if 'af3' in filename.lower():
                    software = 'af3'
                elif 'colabfold' in filename.lower():
                    software = 'colabfold'
                elif 'boltz' in filename.lower():
                    software = 'boltz'
                elif 'chai' in filename.lower():
                    software = 'chai'
                else:
                    software = 'unknown'
                
                sheet_key = f"{software}_e1e2"
                
                coords = txt_data[new_chain_id]
                data_entry = {
                    'filename': filename,
                    'model_type': model_type,
                    'new_chain_id': new_chain_id,
                    'x': coords['x'],
                    'y': coords['y'],
                    'z': coords['z']
                }
                
                if sheet_key in sheets:
                    sheets[sheet_key].append(data_entry)
    
    # Convert lists to dataframes and create Excel file
    with pd.ExcelWriter(output_path) as writer:
        for sheet_name, data in sheets.items():
            df = pd.DataFrame(data)
            if not df.empty:
                df.to_excel(writer, sheet_name=sheet_name, index=False)

def main():
    txt_file_path = r'path\to\first_residue_alpha_carbon_list.txt'
    e2_csv_path = r'path\to\e2_alone_chains.csv'
    e1e2_csv_path = r'path\to\e1e2_chains.csv'
    output_excel_path = r'path\to\model_data.xlsx'
    
    print("Extracting chain data from text file...")
    txt_data = parse_txt_file(txt_file_path)
    print(f"Found {len(txt_data)} unique chains in text file")
    
    print("Reading E2 model data...")
    e2_data = parse_csv_file(e2_csv_path)
    print(f"Found {len(e2_data)} rows in E2 data")
    
    print("Reading E1E2 model data...")
    e1e2_data = parse_csv_file(e1e2_csv_path)
    print(f"Found {len(e1e2_data)} rows in E1E2 data")
    
    print("Creating Excel file with 8 sheets...")
    create_excel_with_sheets(txt_data, e2_data, e1e2_data, output_excel_path)
    print(f"Excel file created at: {output_excel_path}")

if __name__ == "__main__":
    main()
