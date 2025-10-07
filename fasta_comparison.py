def clean_accession(line):
    while line.startswith('>'):
        line = line[1:]

    line = line.split('/')[0]

    return '>' + line  

def e2_filtered_by_hvr1(pair):
    accession, sequence = pair
    return accession in hvr1_accessions

def write_fasta_file(dictionary, file_path):  
    with open(file_path, 'w') as file:  
        for accession, sequence in dictionary.items():  
            file.write(f'>{accession}\n{sequence}\n') 
   
hvr1_fasta_file_path = (r"path\to\hvr1.fasta")
with open(hvr1_fasta_file_path) as file:
    hvr1_fasta_text = [clean_accession(line.strip()) for line in file]   
   
hvr1_accessions = []   
for a in hvr1_fasta_text:   
    hvr1_fasta_line = a    
    if hvr1_fasta_line[0] == ">":   
        hvr1_accessions.append(hvr1_fasta_line.replace("\n",''))

print("hvr1_accessions:", hvr1_accessions)
       
e2_fasta_file_path = (r"path\to\input\e2.fasta")
with open (e2_fasta_file_path) as file:    
    text = file.readlines()    
 
entry = []   
for i in text:   
    line = i    
    if line[0] == ">":   
        entry.append(line.replace("\n",'')) 
             
seqs = ''   
for j in text:    
    line = j.replace("\n",'').replace(" ",'')   
    seqs = seqs + line    
  
acstartpositionlist = []    
acnamelength = []     
for k in entry:   
    ac = k    
    aclen = len(k)   
    acstartposition = seqs.find(ac)   
    acstartpositionlist.append(acstartposition)   
    acnamelength.append(aclen) 
      
sequencestartposition = []      
xlista = len(acstartpositionlist)      
xlistb = len(acnamelength)     
start_pos_list = []    
for l in range(xlista):   
   
    startp = acstartpositionlist[l]   
   
    acnomlength = acnamelength[l]   
   
    q = int(startp)   
   
    p = int(acnomlength)   
   
    startpositionoutput = q + p    
   
    start_pos_list.append(startpositionoutput) 
       
end_pos_range = range(1, xlista)   
final_pos_list = []   
for m in end_pos_range:   
    final_pos = int(acstartpositionlist[m])    
    final_pos_list.append(final_pos)   
final_pos_list.append(len(seqs)) 
  
sequencelist= [] 
for n in range(xlista): 
    startpos = start_pos_list[n] 
    endpos = final_pos_list[n] 
    sequence = seqs[int(startpos):int(endpos)] 
    sequencelist.append(sequence)     

dictseqs = {}   
for accession, sequence in zip(entry, sequencelist): 
    dictseqs[accession] = sequence 

filtered_e2_sequences = dict(filter(e2_filtered_by_hvr1, dictseqs.items()))
 
output_fasta_file_path = (r"path\to\output\.fasta")

write_fasta_file(filtered_e2_sequences, output_fasta_file_path)

print()
print("Updated FASTA file has been generated.")  
print("Filtered E2 fasta file path:", output_fasta_file_path) 