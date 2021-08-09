To use:
# Preprocessing for gephi
Scripts:
    contactmapscriptForGephiInput.tcl \\VMD tkconsole
    loadpdbupdate.tcl \\VMD tkconsole

Usage:
    1. Open the tkconsole in VMD through VMD main> extentions.
    2. Navigate to the directory which houses loadpdbupdate.tcl and
        contactmapscriptForGephiInput.tcl, enter source loadpdbupdate.tcl then source
        contactmapscriptForGephiInput.tcl.
    3. Navigate to the directory with the pdb files and enter recursiveLoad 0 to load the files.
	    This may only load up to 509 files because of an unkown bug. Simply continue with
        recursiveLoad 509 then recursiveLoad 1018 etc.
    4. Use fResPair "element C N O" "element C N O" 3 to get contacts within 3 angstroms between
        the elements C,N, and O. Use VMD selection syntax (visible in representations) for other
        selections.
This produces an edges csv and a nodes csv in the pdb file directory.

# Gephi
Open a new project in gephi and import the edges file as edges and nodes file as nodes.
Do any gephi analysis.
Export the nodes table.

# Postprocessing
gephiOutToMLFeatures.py \\python3.8 pandas, numpy
kerasSpektral.py \\python3.8 tensorflow > 2.4 pandas, numpy, spektral and dependencies
plotKerasResults.py \\ matplotlib

1. Use gephiOutToMLFeatures.py to generate feature vectors for each frame.
    This file may require alteration for different pdbs than calmodulin loops.
2. Use the kerasSpektral.py by creating a custom dataset class
    as described in spektrals documentation.
