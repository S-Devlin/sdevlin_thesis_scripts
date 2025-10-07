from Bio.SeqIO.FastaIO import SimpleFastaParser


def filter_dna_sequences(dna_seqs_dict): 
    filtered_dna_seqs = {} 
    for accession, value in dna_seqs_dict.items(): 
        if value.count('n') < 3: 
            filtered_dna_seqs[accession] = value
    print("filtered_dna_sequences:", filtered_dna_seqs)
    return filtered_dna_seqs

def write_fasta_file(dictionary, file_path):  
    with open(file_path, 'w') as file:  
        for accession, sequence in dictionary.items():  
            file.write(f'>{accession}\n{sequence}\n') 

record_dict = {}
with open(r"c://path/to/.fasta") as fasta_file:
    for title, seq in SimpleFastaParser(fasta_file):
        record_dict[title] = seq


file_path = r"c://path/to/output"


write_fasta_file(filtered_dna_dict, file_path)
