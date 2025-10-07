from Bio import SeqIO
from Bio.Seq import Seq

def cod_check(fasta_file, errors='critical'):
    records = SeqIO.parse(fasta_file, 'fasta')  

    problems = []

    for rec in records:
        seq = str(rec.seq).replace('-', '').replace('~', '').upper()

        if len(seq) % 3 != 0:
            print(f"\nSequence {rec.id} has length not a multiple of 3...\n")
            problems.append(rec.id)
            continue  
        
        aa = Seq(seq).translate()

        if '*' in aa[:-1]:  
            print(f"\nSequence {rec.id} has internal stop codons...\n")
            problems.append(rec.id)


        if (set(seq) - {'C', 'T', 'A', 'G'}) and errors == 'all':
            print(f"\nSequence {rec.id} has ambiguous nucleotides...\n")
            problems.append(rec.id)

    return problems


problems = cod_check(r"path\to\.fasta", errors='all')
print(problems)