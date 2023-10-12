from pymol import cmd
import sys, getopt
import os
script = os.path.basename(__file__)
loopSize = 12
firstResinLoop = (20,56,93,129)

def bb_mod(infile, outfile, loop):
    pre = firstResinLoop[loop-1] - 1
    post = pre + 12 + 1
    cmd.load(infile)

    # Convert resid for SOL to some unique numbers.
    # There is a slight chance that several solvent molecules
    # coincidentally have the same resid
    # cmd.alter('resn SOL', 'resi=str(int(resi,16)%200+200)')
    # cmd.alter('resn SOL', 'resi=str(int(resi,16))')
    cmd.sort()
    cmd.h_add("`"+str(pre)+"/CA")
    cmd.h_add("`"+str(post)+"/CA")

    cmd.save(outfile)

def main(argv):
   inputfile = 'in.pdb'
   outputfile = 'out.pdb'
   loop = 1
   try:
       opts, args = getopt.getopt(argv,"hi:o:l:",["ifile=","ofile=","loop="])
   except getopt.GetoptError:
      print (script + ' -i <inputfile> -o <outputfile> -l 1')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print (script + ' -i <inputfile> -o <outputfile> -l <1>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
      elif opt in ("-l", "-loop"):
         loop = int(arg)
   bb_mod(inputfile, outputfile, loop)


if __name__ == "__main__":
   main(sys.argv[1:])

