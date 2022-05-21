from shutil import which
import subprocess
import os, sys
import glob
import pathlib
import argparse


class HmmFile:
    def __init__(self, hmm_path):
        self.path = hmm_path
        self.name = ''
        self.file_name = pathlib.Path(hmm_path).name
        with open(hmm_path, 'r', encoding='UTF-8') as f:
            for line in f:
                if 'Name' in line:
                    self.name = line.split(' ')[1]
            if not self.name:
                self.name = os.path.splitext(hmm_path)[0]


def tool_installed(name):
    if which(name):
        return True
    else:
        return None


def get_hmm(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            path = os.path.join(path, "")
            return [HmmFile(file_path) for file_path in glob.glob(f"{path}**.hmm")]
        else:
            return HmmFile(path)
    else:
        print('Hmm source path invalid or empty')
        sys.exit(1)

parser = argparse.ArgumentParser(prog='GetTree',
                                    usage='\n%(prog)s <hmm file or folder with hmm models> <proteome fasta file>'
                                          ' <temp folder> <output folder>',
                                     epilog='Pavel Vychyk, 2022',
                                     description='Extract CRtag from protein sequence provided by hmmsearch ')
parser.add_argument('hmm_source', type=str, help='path to folder with hmm files or single hmm file')
parser.add_argument('proteome_fasta', type=str, help='path to proteome fasta file of interest')
parser.add_argument('tmp_dir', type=str, help='path to folder for temp data')
parser.add_argument('output_path', type=str, help='path to folder for FastTreeMP results')
args = parser.parse_args()
# check preinstalled tools
required_tools = ('makeblastdb',
                  'blastdbcmd',
                  'hmmsearch',
                  'mafft',
                  'FastTreeMP')
checks = [tool_installed(name) for name in required_tools]
if None in checks:
    sys.exit(1)
hmm_source = args.hmm_source
output_path = args.output_path
proteome_fasta = args.proteome_fasta
tmp_dir = args.tmp_dir
hmm_files = get_hmm(hmm_source)
if not os.path.exists(tmp_dir):
    try:
        os.mkdir(tmp_dir)
    except IOError:
        print(f"Can't create temporary folder {tmp_dir}")
        sys.exit(1)
if not os.path.exists(proteome_fasta):
    print("Proteome file doesn't exits, check path {proteome_fasta}")
    sys.exit(1)
if hmm_files:
    if os.path.exists(proteome_fasta) and os.path.isfile(proteome_fasta):
        protein_groups = {}
        matches_fasta = []
        proteome_blastdb_path = f"{tmp_dir}/_blastdb_{pathlib.Path(proteome_fasta).name}"
        proteins_combined = []
        if not os.path.exists(f"{proteome_blastdb_path}.phd"):
            print(f"Run makeblastdb")
            p = subprocess.run(f"makeblastdb -dbtype prot -in {proteome_fasta} "
                               f"-parse_seqids -hash_index -out {proteome_blastdb_path}",
                               shell=True)
        for hmm in hmm_files:
            hmm_table_path = f"{tmp_dir}/_hmmout_{hmm.file_name}"
            p = subprocess.run(f"hmmsearch -A {hmm_table_path} "
                                f"--notextw --cut_ga --max {hmm.path} {proteome_fasta}",
                               shell=True, capture_output=True)
            if not p.returncode:
                with open(hmm_table_path, 'r', encoding='UTF-8') as f:
                    for line in f:
                        if not line.startswith("#") or not line.startswith("\n"):
                            protein_id = line.split("/")[0]
                            if protein_id:
                                p = subprocess.run(f"blastdbcmd -db {proteome_blastdb_path}"
                                                   f" -entry '{protein_id}'",
                                                   shell=True,
                                                   capture_output=True,
                                                   text=True)
                                if p.stdout:
                                    proteins_combined.append(p.stdout)
                                    protein_groups[protein_id] = hmm.name
        # run aligner tool
        if proteins_combined:
            with open(f"{tmp_dir}/prot_to_align", 'w') as f:
                f.writelines(''.join(proteins_combined))
                p = subprocess.run(f"mafft --auto {tmp_dir}/prot_to_align > {tmp_dir}/aligned_proteins",
                                   shell=True,
                                   capture_output=True,
                                   text=True)
                if not p.returncode:
                    p = subprocess.run(f"FastTreeMP {tmp_dir}/aligned_proteins > {output_path}/FastTree_output.txt",
                                       shell=True,
                                       capture_output=True,
                                       text=True)
                    print(f"Succeed!")
                else:
                    print(f"Tree build failed due to aligner error: {p.stderr}")
else:
    print(f"No hmm models found in {hmm_source}, check if path exists,"
          f"or files have .hmm extensions")
    sys.exit(1)
