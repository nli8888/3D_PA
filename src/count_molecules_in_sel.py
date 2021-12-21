import pymol
from pymol import cmd

def count_mols_in_sel(sel="sele"):
    """
    Returns the number of distinct molecules in a given selection.
    """

    sel_copy = "__selcopy"

    cmd.select(sel_copy, sel)

    num_objs = 0

    atoms_in_sel = cmd.count_atoms(sel_copy)

    while atoms_in_sel > 0:

        num_objs += 1

        cmd.select(sel_copy, "%s and not (bm. first %s)" % (sel_copy, sel_copy))

        atoms_in_sel = cmd.count_atoms(sel_copy)

    print "There are %d distinct molecules in the selection '%s'." % (num_objs, sel)

    return num_objs


cmd.extend("count_molecules_in_selection", count_mols_in_sel)