from pymol import cmd
import sys, getopt

def bb_mod(infile, outfile):

    cmd.load(infile)

    cmd.alter('resn SOL', 'resi=200')

    cmd.sort()

    # for ASP 93
    cmd.remove("ASP`93/N or ASP`93/C or ASP`93/O or ASP`93/H")
    cmd.h_add("ASP`93/CA")

    # for ASP 95
    cmd.remove("ASP`95/N or ASP`95/C or ASP`95/O or ASP`95/H")
    cmd.h_add("ASP`95/CA")

    # for GLU 104
    cmd.remove("GLU`104/N or GLU`104/C or GLU`104/O or GLU`104/H")
    cmd.h_add("GLU`104/CA")

    cmd.select("3res","resi 93 or resi 95 or resi 104 or resi 151 or resi 200")

    cmd.save(outfile,"3res")

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

