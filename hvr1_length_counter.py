import csv

def clean_accession(line):
    while line.startswith('>'):
        line = line[1:]
    line = line.split('/')[0]
    return '>' + line

file_path = (r"path\to\input.fasta")
output_csv_path = (r"path\to\output.csv")

entries = []
sequences = []
with open(file_path) as file:
    for line in file:
        line = line.strip()
        if line.startswith('>'):
            cleaned_line = clean_accession(line)
            entries.append(cleaned_line)
            sequences.append('')  # Start a new sequence
        else:
            sequences[-1] += line.replace(" ", '').replace("-", '')  

seqlengthdict = {entry: len(seq) for entry, seq in zip(entries, sequences)}

csvheaders = ['Accession', 'Sequence', 'Length']
with open(output_csv_path, 'w+', newline="") as csvfile:
    csv_out = csv.writer(csvfile, delimiter=",")
    csv_out.writerow(csvheaders)
    for entry, sequence in zip(entries, sequences):
        csv_out.writerow([entry, sequence, seqlengthdict[entry]])

print("CSV file has been generated.")
