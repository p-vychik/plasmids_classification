# Systematics and classification of plasmids
Supervisor:
Mikhail Rayko

Authors:
Ekaterina Vostokova (BI)
Pavel Vychik (BI)

## Aim
Our project aims to create an approach to classify newly sequenced plasmids, unrevealing their relation to currently known and characterized.

## Motivation 
Plasmids are extrachromosomal DNA molecules, predominantly circular, capable of autonomous replication. Although plasmids are an optional part of bacterial genomes, their acquisition by a cell can provide significant adaptive advantages due to the carrier of genes providing antibiotic resistance, the ability to utilize new substrates, and the expression of virulence factors, etc. Despite a large amount of data from various metagenomic projects and microbiome research, little is known today about plasmid's origin and no general approach for systematics of plasmids exists. We suggest the usage of two types of topologies derived from the phylogenetic tree build and a graph reconstruction to determine the relation of the plasmid of interest. Suggested topologies were built on the alignment of the Rep proteins involved in the replication process of the majority of the plasmid. 

## Materials and methods
The main source of data for plasmids proteins sequences was NCBI RefSeq plasmid proteins ([source](https://ftp.ncbi.nlm.nih.gov/refseq/release/plasmid/)), and additionally unpublished data from the supervisor were used.<br />
To identify Rep proteins PFAM hidden Markov models for [Rep_1](https://pfam.xfam.org/family/Rep_1), [Rep_2](https://pfam.xfam.org/family/Rep_2), [Rep_3](https://pfam.xfam.org/family/Rep_3), [Duff1424](https://pfam.xfam.org/family/PF07232) families were used.
Search for Rep-proteins was performed via hmmsearch from [HMMER](http://hmmer.org/publications.html). [Mafft v.7.453](https://mafft.cbrc.jp/alignment/software/) aligner tool and [FastTree](http://www.microbesonline.org/fasttree) were used for acquired Rep sequences alignment and further draft tree reconstruction.<br />
The step for tree reconstruction was automized with the script ```gettree.py``` (available in the repository). Usage options are provided below:
```
gettree.py <hmm file or folder with hmm models> <proteome fasta file> <temp folder> <output folder>
