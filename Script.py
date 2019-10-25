import os
import mysql
from mysql import connector

""" 
   Important: Run in linux/a windows-ubuntu terminal 
 Will probably want to change the filepath (see main) too.
"""

"""
Moet automatisch:
Maak MSA
Maak HMM  (Consensus patroon?)
Zoek nieuwe seq. met HMM?
Update MSA, check algoritme
Nieuwe iteratie

Beschikbare tools:
ClustalO - MSA's
T-Coffee - MSA's  (Exact, I think? Servers offline at time of writing so eh.)
MAFFT    - MSA's  (https://mafft.cbrc.jp/alignment/software/about.html)
MUSCLE   - MSA's
HMMer    - HMM's
Biopython- Voorgemaakte MSA, HMM etc objecten?
"""
# os.system("ubuntu")  # Doesn't work, just run from linux terminal.


class DataCollector:
    def __init__(self, path):
        host = "hannl-hlo-bioinformatica-mysqlsrv.mysql.database.azure.com"
        user = "kxxxf@hannl-hlo-bioinformatica-mysqlsrv"
        passw = "ConnectionPWD"
        dbname = "kxxxf"
        self.database = mysql.connector.connect(host=host, user=user, password=passw, db=dbname)
        self.cursor = self.database.cursor(buffered=True)

        self.dir_path = path
        self.msa_path = self.make_msa(self.dir_path + "/X4R0Q4-treS.fasta", "mafft_msa.fasta")
        self.profile_path = self.make_hmm_profile(self.dir_path + "/HMM", self.msa_path)

    def go_once(self):  # Todo
        """ Shortcut for one whole "MSA > HMM > HMM seqs > new MSA" iteration """
        self.make_msa()
        self.make_hmm_profile()
        self.hmm_search()
        self.make_msa()

    def make_msa(self, infile, outfile):  # Todo: (Auto-)Create initial MSA before using this?
        """Creates a sorted MSA using mafft, output in fasta format.
        :param infile: Input file, A FASTA file with at least two sequences.
        :param outfile: Output file, any filename.
        :return: Path to MSA file. Might not be needed?
        """
        os.system("mafft --auto --reorder \""+infile+"\" > \""+outfile+"\"")
        return self.dir_path+outfile

    def make_hmm_profile(self, outfile, msafile):
        os.system("hmmbuild "+outfile+" "+msafile)  # "Usage: hmmbuild [-options] <hmmfile_out> <msafile>"
        return self.dir_path+outfile

    def hmm_search(self):
        os.system("hmmsearch "+self.profile_path+" ")  # "Usage: hmmsearch [options] <hmmfile> <seqdb>"

    def insert(self, table, data):  # Todo
        """To make: Generic, reuseable database insertion?"""
        pass


def main():
    # File location (read and write)
    filepath = "/mnt/d/'Bioinformatica (Opleiding)'/Files/'Weektaken Jaar 2'/'Jaar2Blok1 project'"
    os.system("cd "+filepath)
    collector = DataCollector(filepath)
    for _ in range(10):
        collector.go_once()
    #database insertions here?


# Example automating terminal input
# os.system("cd /mnt/d/'Bioinformatica (Opleiding)'/Files/'Weektaken Jaar 2'")
# print(os.popen("ls").read())
# https://linuxhandbook.com/execute-shell-command-python/
