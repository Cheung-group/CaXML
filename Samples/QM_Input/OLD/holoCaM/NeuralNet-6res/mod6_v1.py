# Only keep the chelating atom and its bonded atoms

from pymol import cmd
import sys, getopt

def bb_mod(infile, outfile):
    cmd.load(infile)
    cmd.alter('resn SOL', 'resi=200')

    cmd.sort()

    # for ASP 93
    cmd.remove("ASP`93/CA or ASP`93/HB1 or ASP`93/HB2")
    cmd.h_add("ASP`93/CB")

    # for ASP 95
    cmd.remove("ASP`95/CB")
    cmd.h_add("ASP`95/CG")

    # for ASN 97
    cmd.remove("ASN`97/CB")
    cmd.h_add("ASN`97/CG")

    # for TYR 99
    # backbone chelating
    cmd.remove("TYR`99/N or TYR`99/H")
    cmd.remove("TYR`99/CB")
    cmd.h_add("TYR`99/CA")
    cmd.remove("ILE`100/CA")
    cmd.h_add("ILE`100/N")

    # for SER 101
    cmd.remove("SER`101/CA")
    cmd.h_add("SER`101/CB")

    # for GLU 104
    cmd.remove("GLU`104/CG")
    cmd.h_add("GLU`104/CD")

    cmd.select("asp93", "name CG+OD1+OD2+HD2+H01 in resi 93")
    cmd.select("asp95", "name CG+OD1+OD2+HD2+H01 in resi 95")
    cmd.select("asn97", "name CG+OD1+ND2+HD21+HD22+H01 in resi 97")
    cmd.select("tyr99", "name CA+C+O+H01+H02 in resi 99")
    cmd.select("ile100", "name N+H+H01 in resi 100")
    cmd.select("ser101", "name CB+HB1+HB2+H01+OG+HG in resi 101")
    cmd.select("glu104", "name CD+OE1+OE2+H01 in resi 104")
    cmd.select("6res", "asp93|asp95|asn97|tyr99|ile100|ser101|glu104|resi 151+200")

    cmd.save(outfile,"6res")

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

