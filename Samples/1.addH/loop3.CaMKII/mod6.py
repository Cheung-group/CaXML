#import pymol
from pymol import cmd
#pymol.finish_launching(['pymol', '-qi'])
import sys, getopt

def bb_mod(infile, outfile):
    cmd.load(infile)
    cmd.alter('resn SOL', 'resi=200')

    cmd.sort()

    cmd.h_add("PHE`92/CA")
    cmd.h_add("LEU`105/CA")

    #cmd.select("res","resi 93 or resi 95 or resi 97 or resi 99 or \
    #        resi 101 or resi 104 or resi 151 or resi 200")

    cmd.save(outfile)
    cmd.quit()

def main(argv):
   inputfile = 'in.pdb'
   outputfile = 'out.pdb'
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print ('mod.py -i <inputfile> -o <outputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('mod.py -i <inputfile> -o <outputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   bb_mod(inputfile, outputfile)


if __name__ == "__main__":
   main(sys.argv[1:])

