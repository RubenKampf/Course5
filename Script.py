import os
import mysql
from mysql import connector

""" 
   Important: Run in linux/a windows-ubuntu terminal 
 Will probably want to change the filepath (see main()) too.
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

        # Waste of time, just put the files in the same place as the script
        # self.dir_path = path
        # self.msa_path = self.make_msa(self.dir_path + "/initial.fasta", "mafft_msa.fasta")
        # self.profile_path = self.make_hmm_profile(self.dir_path + "/HMM", self.msa_path)

    def go_once(self):
        """ Shortcut for one whole "(MSA >) HMM > HMM seqs > new MSA" iteration """
        self.make_hmm_profile("HMM", "mafft_msa.fasta")
        self.hmm_search()
        self.make_msa("HMMsearch", "mafft_msa.fasta")

    def make_msa(self, infile, outfile):
        """Creates a sorted MSA using mafft, output in fasta format.
        :param infile: Input file, A FASTA file with at least two sequences.
        :param outfile: Output file, any filename.
        :return: Path to MSA file. Might not be needed?
        """
        os.system("mafft --auto --reorder "+infile+" > "+outfile)
        os.system("")

    def make_hmm_profile(self, outfile, msafile):
        os.system("hmmbuild "+outfile+" "+msafile)  # "Usage: hmmbuild [-options] <hmmfile_out> <msafile>"

    def hmm_search(self):
        os.system("hmmsearch -A HMMsearch HMM mafft_msa.fasta")  # "Usage: hmmsearch [options] <hmmfile> <seqdb>"
        # What's valid for "seqdb"? Not in HMMer manual. # Fixme: Current main problem
        #   An MSA file (apparently) works? (Good output in a few tests, now gives fatal errors (Reasons unknown).)
        # -o - Save whole output to file (Human readable, not very computer-readable)
        # -A - Save results to file in MSA format?

    def insert(self, table, data):  # Todo
        """To make: Generic, reuseable database insertion?
        Also get the data out of the files.
        Also, what data is needed?"""
        query = ""
        self.cursor.execute(query)
        self.database.commit()


def main():
    # File location (read and write)
    filepath = "/mnt/d/'Bioinformatica (Opleiding)'/Files/'Weektaken Jaar 2'/'Jaar2Blok1 project'"
    os.system("cd "+filepath)
    collector = DataCollector(filepath)
    collector.make_msa("initial.fasta", "mafft_msa.fasta")
    for _ in range(1):
        # collector.go_once()
        # print("\n ##### Finished one loop \n")
        collector.make_hmm_profile("HMM", "mafft_msa.fasta")
        print("\n ##### HMM profile finished \n")
        collector.hmm_search()
        print("\n ##### HMM search finished \n")
        collector.make_msa("HMMsearch", "mafft_msa.fasta")
        print("\n ##### New MSA finished \n")
    #database insertions here?


main()
