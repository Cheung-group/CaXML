# Description: Add hydrogens to a PDB file

from pymol import cmd
import argparse
import os

script = os.path.basename(__file__)


def bb_mod(infile, outfile, loopSize=12, firstResinLoop=1):
   pre = firstResinLoop - 1
   post = pre + loopSize + 1
   cmd.load(infile)
   cmd.sort()
   cmd.h_add("`"+str(pre)+"/CA")
   cmd.h_add("`"+str(post)+"/CA")

   cmd.save(outfile)

def main():
   # loopSize = 12
   # firstResinLoop = (20,56,93,129)
   parser = argparse.ArgumentParser(description='Add hydrogens to a PDB file')
   parser.add_argument('-i', '--ifile', type=str, default='in.pdb', help='input file')
   parser.add_argument('-o', '--ofile', type=str, default='out.pdb', help='output file')
   parser.add_argument('--loopSize', type=int, default=12, help='loop size')
   parser.add_argument('--firstResinLoop', type=int, default=1, help='ID number of first residue in the loop')
   args = parser.parse_args()

   bb_mod(args.ifile, args.ofile, args.loopSize, args.firstResinLoop)

if __name__ == "__main__":
   main()