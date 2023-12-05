# Description: Modifications to a PDB file

from pymol import cmd
import argparse
import os

script = os.path.basename(__file__)


def add_hydrogen(infile, outfile, loopSize=12, firstResinLoop=1):
   pre = firstResinLoop - 1
   post = pre + loopSize + 1
   cmd.delete('all')
   cmd.load(infile)
   cmd.sort()
   cmd.h_add("`"+str(pre)+"/CA")
   cmd.h_add("`"+str(post)+"/CA")

   cmd.save(outfile)

def strip_water_and_caps(infile, outfile, loopSize=12, firstResinLoop=1):
   pre = firstResinLoop - 1
   post = pre + loopSize + 1
   cmd.delete('all')

   cmd.load(infile)
   cmd.sort()
   
   cmd.remove('resname HOH')
   cmd.remove('elem H')
   cmd.remove(f"resid {pre}")
   cmd.remove(f"resid {post}")
   cmd.save(outfile)


def main():
   # loopSize = 12
   # firstResinLoop = (20,56,93,129)
   parser = argparse.ArgumentParser(description='Add hydrogens to a PDB file')
   parser.add_argument('-i', '--ifile', type=str, default='in.pdb', help='input file')
   parser.add_argument('-o', '--ofile', type=str, default='out.pdb', help='output file')
   parser.add_argument('-s', '--loopSize', type=int, default=12, help='loop size')
   parser.add_argument('-fr', '--firstResinLoop', type=int, default=1, help='ID number of first residue in the loop')
   args = parser.parse_args()

   if False:
      add_hydrogen(args.ifile, args.ofile, loopSize=args.loopSize, firstResinLoop=args.firstResinLoop)
   else:
      strip_water_and_caps(args.ifile, args.ofile, loopSize=args.loopSize, firstResinLoop=args.firstResinLoop)

if __name__ == "__main__":
   main()
