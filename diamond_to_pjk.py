import sys, math
from Bio import SeqIO


seqs = []
with open (sys.argv[1], "r") as fasta:
    for seq in SeqIO.parse(fasta,"fasta"):
        seqs.append(seq)

seq_dict = {}
for count,value in enumerate(seqs):
    seq_dict[value.id] = str(count + 1)


edges = {}
edges_e = {}
with open (sys.argv[2], "r") as dmd:
    for line in dmd:
        items = line.strip().split()
        if items[0] != items[1]:
            if tuple(sorted((seq_dict[items[0]], seq_dict[items[1]]))) not in edges:
                edges[tuple(sorted((seq_dict[items[0]], seq_dict[items[1]])))] = str(items [-1])
                edges_e[tuple(sorted((seq_dict[items[0]], seq_dict[items[1]])))] = str(-math.log(float(items[2]) + sys.float_info.epsilon))

    
   
## Output

with open (sys.argv[2].rsplit('.',1)[0] + '.net' , "w") as outfile1:

# NET, part 1
    outfile1.write(f"*Vertices {len(seqs)}\n")
    for seq in seqs:
        outfile1.write(f'{seq_dict[seq.id]} "{seq.id}"\n')

# NET, part 2
    outfile1.write(f"*arcs \n")
    for i,j in edges.items():
        outfile1.write(f'{" ".join(i)} {j}\n')


# CSV
with open (sys.argv[2].rsplit('.',1)[0] + '.csv', "w") as outfile2:
    outfile2.write("Id,Label,timeset,group\n")
    for seq in seqs:
        if "_group_" in seq.id:
            group = seq.id.split("_group_")[1].split()[0]
#                print (k, group)
        else:
            group = "none"
        outfile2.write(f'{seq_dict[seq.id]},{seq.id.replace(",","_")},,{group}\n')

            
#PJK with -log evalues     
with open (sys.argv[2].rsplit('.',1)[0] + '_evalues.net' , "w") as outfile3:

# NET, part 1
    outfile3.write(f"*Vertices {len(seqs)}\n")
    for seq in seqs:
        outfile3.write(f'{seq_dict[seq.id]} "{seq.id}"\n')

# NET, part 2
    outfile3.write(f"*arcs \n")
    for i,j in edges_e.items():
        outfile3.write(f'{" ".join(i)} {j}\n')


