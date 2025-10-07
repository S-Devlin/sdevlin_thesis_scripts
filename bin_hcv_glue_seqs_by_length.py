from Bio.SeqIO.FastaIO import SimpleFastaParser

def split_dictionary(record_dict):
    dict_0_to_500 = {}
    dict_501_to_1000 = {}
    dict_1001_to_1500 = {}
    dict_1501_to_2000 = {}
    dict_2001_to_2500 = {}
    dict_2501_to_3000 = {}
    dict_3001_to_3500 = {}
    dict_3501_to_4000 = {}
    dict_4001_to_4500 = {}
    dict_4501_to_5000 = {}
    dict_5001_to_5500 = {}
    dict_5501_to_6000 = {}
    dict_6001_to_6500 = {}
    dict_6501_to_7000 = {}
    dict_7001_to_7500 = {}
    dict_7501_to_8000 = {}
    dict_8001_to_8500 = {}
    dict_8501_to_9000 = {}
    dict_9001_to_9500 = {}
    dict_9501_to_10000 = {}
    not_sorted_dict = {}
    
    for key, value in record_dict.items():
        seq_length = len(value)  # Get the length of the current sequence
        if seq_length <= 500:
            dict_0_to_500[key] = value
        elif 500 < seq_length <= 1000:
            dict_501_to_1000[key] = value
        elif 1000 < seq_length <= 1500:
            dict_1001_to_1500[key] = value
        elif 1500 < seq_length <= 2000:
            dict_1501_to_2000[key] = value
        elif 2000 < seq_length <= 2500:
            dict_2001_to_2500[key] = value
        elif 2500 < seq_length <= 3000:
            dict_2501_to_3000[key] = value
        elif 3000 < seq_length <= 3500:
            dict_3001_to_3500[key] = value
        elif 3500 < seq_length <= 4000:
            dict_3501_to_4000[key] = value
        elif 4000 < seq_length <= 4500:
            dict_4001_to_4500[key] = value
        elif 4500 < seq_length <= 5000:
            dict_4501_to_5000[key] = value
        elif 5000 < seq_length <= 5500:
            dict_5001_to_5500[key] = value
        elif 5500 < seq_length <= 6000:
            dict_5501_to_6000[key] = value
        elif 6000 < seq_length <= 6500:
            dict_6001_to_6500[key] = value
        elif 6500 < seq_length <= 7000:
            dict_6501_to_7000[key] = value
        elif 7000 < seq_length <= 7500:
            dict_7001_to_7500[key] = value
        elif 7500 < seq_length <= 8000:
            dict_7501_to_8000[key] = value
        elif 8000 < seq_length <= 8500:
            dict_8001_to_8500[key] = value
        elif 8500 < seq_length <= 9000:
            dict_8501_to_9000[key] = value
        elif 9000 < seq_length <= 9500:
            dict_9001_to_9500[key] = value
        elif 9500 < seq_length <= 10000:
            dict_9501_to_10000[key] = value
        else:
            not_sorted_dict[key] = value

    # Return dictionaries for further use or inspection
    return dict_0_to_500, dict_501_to_1000, dict_1001_to_1500, dict_1501_to_2000, dict_2001_to_2500, dict_2501_to_3000, dict_3001_to_3500, dict_3501_to_4000, dict_4001_to_4500, dict_4501_to_5000, dict_5001_to_5500, dict_5501_to_6000, dict_6001_to_6500, dict_6501_to_7000, dict_7001_to_7500, dict_7501_to_8000, dict_8001_to_8500, dict_8501_to_9000, dict_9001_to_9500, dict_9501_to_10000, not_sorted_dict
def write_fasta_files_from_dictionaries(dictionaries, base_file_path):
    """
    Write each dictionary of sequences to a separate FASTA file.
    
    Parameters:
    - dictionaries (dict of dict): A dictionary where keys are descriptive names of each sequence dictionary,
      and values are the dictionaries containing sequences.
    - base_file_path (str): The base path for output files, which will be appended with descriptive names.
    """
    for dict_name, sequences in dictionaries.items():
        # Construct file path for each dictionary
        file_path = f"{base_file_path}_{dict_name}_gt7.fasta"
        with open(file_path, 'w') as file:
            for accession, sequence in sequences.items():
                file.write(f'>{accession}\n{sequence}\n')
        print(f"Written {len(sequences)} sequences to {file_path}")

# Load FASTA file into a dictionary
record_dict = {}
with open(r"C:\Users\sdevl\Desktop\hvr1_extraction_new_20022024\gt7\gt7_sequences_25_percent_e2_coverage.fasta") as fasta_file:
    for title, seq in SimpleFastaParser(fasta_file):
        record_dict[title] = seq

# Split the dictionary by sequence length
dict_0_to_500, dict_501_to_1000, dict_1001_to_1500, dict_1501_to_2000, dict_2001_to_2500, dict_2501_to_3000, dict_3001_to_3500, dict_3501_to_4000, dict_4001_to_4500, dict_4501_to_5000, dict_5001_to_5500, dict_5501_to_6000, dict_6001_to_6500, dict_6501_to_7000, dict_7001_to_7500, dict_7501_to_8000, dict_8001_to_8500, dict_8501_to_9000, dict_9001_to_9500, dict_9501_to_10000, not_sorted_dict = split_dictionary(record_dict)

# Group dictionaries together for iteration
dictionaries = {
    "0_to_500": dict_0_to_500,
    "501_to_1000": dict_501_to_1000,
    "1001_to_1500": dict_1001_to_1500,
    "1501_to_2000": dict_1501_to_2000,
    "2001_to_2500": dict_2001_to_2500,
    "2501_to_3000": dict_2501_to_3000,
    "3001_to_3500": dict_3001_to_3500,
    "3501_to_4000": dict_3501_to_4000,
    "4001_to_4500": dict_4001_to_4500,
    "4501_to_5000": dict_4501_to_5000,
    "5001_to_5500": dict_5001_to_5500,
    "5501_to_6000": dict_5501_to_6000,
    "6001_to_6500": dict_6001_to_6500,
    "6501_to_7000": dict_6501_to_7000,
    "7001_to_7500": dict_7001_to_7500,
    "7501_to_8000": dict_7501_to_8000,
    "8001_to_8500": dict_8001_to_8500,
    "8501_to_9000": dict_8501_to_9000,
    "9001_to_9500": dict_9001_to_9500,
    "9501_to_10000": dict_9501_to_10000,
    "not_sorted": not_sorted_dict
}

# Specify the base path for output files
base_file_path = r"C:\Users\sdevl\Desktop\hvr1_extraction_new_20022024\gt7\splitting_sequences_by_length_output"

# Write the FASTA files
write_fasta_files_from_dictionaries(dictionaries, base_file_path)
