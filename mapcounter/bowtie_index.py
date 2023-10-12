'''
Created on Aug 30, 2017

@author: dgrewal
'''
from subprocess import PIPE, Popen
import argparse
import os

class bowtieIndex(object):
    """
    aligns simulated reads from the reference fasta file.
    """
    
    def __init__(self, infile, outfile, reference, bwt_path):
        """
        :param infile: sam file with reads simulated from the reference fasta
        :param outfile: output file with aligned reads in bowtie's output format
        :param reference: reference fasta file (must be bowtie indexed)
        :param bwt_path: path to bowtie executable
        """
        self.input = infile
        self.output = outfile
        self.bowtie = bwt_path
        self.reference = reference

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        #clean up output if there are any exceptions
        if exc_type and os.path.exists(self.output):
            os.remove(self.output)

     
    def cmd(self):
        """build the command string
        """
        cmd = [self.bowtie, self.reference,
               '-f', self.input, '-v', '0',
               '--quiet', '|' 'gzip', '-',
               '>', self.output]
     
        return cmd

    def main(self):
        """
        run bowtie on input file
        """
        cmd = self.cmd()

        cmd = " ".join(cmd)

        print(cmd)

        cmd = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
          
        stdout, stderr =  cmd.communicate()
        
        retc = cmd.returncode
        if retc != 0:
            raise Exception(stderr)
        
        return stdout

def parse_args():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('input')
    parser.add_argument('output')
    parser.add_argument('reference')
    parser.add_argument('--bowtie',
                        default="bowtie")

    args = parser.parse_args()
    
    return args

if __name__ == "__main__":
    args = parse_args()

    with bowtieIndex(args.input, args.output, args.reference, args.bowtie) as bwt:
        bwt.main()
