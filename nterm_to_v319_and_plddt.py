import os
import pandas as pd
import math
from Bio.PDB import PDBParser, MMCIFParser
import numpy as np

pdb_folder_path = r"path_to\pdb_and_cif_files"

subdirectory_name = os.path.basename(pdb_folder_path).replace(" ", "_").lower()
output_excel_path = os.path.join(pdb_folder_path, f"{subdirectory_name}_residue_distances.xlsx")

def calculate_distance(coord1, coord2):
    x1, y1, z1 = coord1
    x2, y2, z2 = coord2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

def parse_structure(file_path, file_type):
    if file_type == "pdb":
        parser = PDBParser(QUIET=True)
    elif file_type == "cif":
        parser = MMCIFParser(QUIET=True)
    else:
        raise ValueError("Unsupported file type")

    structure = parser.get_structure('structure', file_path)
    chains_data = {}

    for model in structure:
        for chain in model:
            chain_id = chain.id
            ca_data_list = []
            residue_numbers = []

            for residue in chain:
                if "CA" in residue:
                    ca_atom = residue["CA"]
                    residue_name = residue.resname
                    residue_number = residue.id[1]
                    x_pos, y_pos, z_pos = ca_atom.coord

                    ca_data_list.append([residue_name, residue_number, x_pos, y_pos, z_pos])
                    residue_numbers.append(residue_number)

            if len(residue_numbers) >= 250:
                chains_data[chain_id] = {
                    'ca_data_list': ca_data_list,
                    'residue_numbers': residue_numbers
                }

    return chains_data, structure

def calculate_residue_plddt(structure):
    residue_plddt = {}
    for model in structure:
        for chain in model:
            for residue in chain:
                res_id = (chain.id, residue.id[1])
                plddt_scores = [atom.bfactor for atom in residue]
                avg_plddt = np.mean(plddt_scores)
                residue_plddt[res_id] = avg_plddt
    return residue_plddt

def calculate_model_plddt(residue_plddt):
    avg_plddt = np.mean(list(residue_plddt.values()))
    return avg_plddt

def process_chains(chains_data, filename, structure):
    results = []

    for chain_id, data in chains_data.items():
        ca_data_list = data['ca_data_list']
        residue_numbers = data['residue_numbers']

        residue2_num = residue_numbers[-50]

        residue1 = ca_data_list[0]
        residue2 = next((res for res in ca_data_list if res[1] == residue2_num), None)

        if not residue2:
            print(f"Warning: Residue 49 amino acids from the end not found in {filename} for chain {chain_id}")
            continue

        if residue2[0] != 'VAL':
            print(f"Warning: Specified residue is not a valine in {filename} for chain {chain_id}")
            continue

        distance = calculate_distance(residue1[2:], residue2[2:])

        residue_plddt = calculate_residue_plddt(structure)
        model_plddt = calculate_model_plddt(residue_plddt)

        results.append([
            filename, chain_id,
            residue1[0], residue1[1], *residue1[2:],
            residue2[0], residue2[1], *residue2[2:],
            distance, model_plddt
        ])

    return results

all_data = []
for filename in os.listdir(pdb_folder_path):
    if filename.endswith(".pdb") or filename.endswith(".cif"):
        print(f"Processing file: {filename}")
        file_path = os.path.join(pdb_folder_path, filename)
        file_type = "pdb" if filename.endswith(".pdb") else "cif"
        chains_data, structure = parse_structure(file_path, file_type)
        parsed_data = process_chains(chains_data, filename, structure)
        all_data.extend(parsed_data)

if not all_data:
    print("No data collected. Please check the input files and parsing logic.")

# Convert to DataFrame
df = pd.DataFrame(all_data, columns=[
    "PDB File", "Chain ID",
    "Residue 1 Type", "Residue 1 Number", "Residue 1 X", "Residue 1 Y", "Residue 1 Z",
    "Residue 2 Type", "Residue 2 Number", "Residue 2 X", "Residue 2 Y", "Residue 2 Z",
    "Distance (Å)", "Average pLDDT"
])

# Write to Excel
with pd.ExcelWriter(output_excel_path) as writer:
    df.to_excel(writer, sheet_name="Residue Distances", index=False)

print(f"Excel file saved: {output_excel_path}")