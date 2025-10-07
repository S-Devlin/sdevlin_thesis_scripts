from Bio import SeqIO

def filter_fasta_sequences(input_fasta, output_fasta):
   
    valid_nucleotides = {'A', 'T', 'C', 'G'}

    with open(input_fasta, "r") as input_handle, open(output_fasta, "w") as output_handle:
        # Iterate over each sequence in the input FASTA file
        for record in SeqIO.parse(input_handle, "fasta"):
            # Check if the sequence contains only valid nucleotides
            sequence = record.seq.upper()
            if set(sequence).issubset(valid_nucleotides):
                SeqIO.write(record, output_handle, "fasta")
            else:
                print(f"Removed sequence: {record.id} (contains invalid characters)")

    print(f"Filtered sequences saved to {output_fasta}")

# Paths to the input and output FASTA files
input_fasta = r"path\to\input.fasta"
output_fasta = r"path\to\output.fasta"

# Run the function
filter_fasta_sequences(input_fasta, output_fasta)
