""" Change structure with implicit Hydrogen to one with explicitely defined H-atoms.
Copyright 2019 Simulation Lab
University of Freiburg
Author: Johannes Hoermann <johannes.hoermann@imtek.uni-freiburg.de>
Modified: Lukas Elflein <elfleinl@cs.uni-freiburg.de>
"""

import os
import ase.io
import sys
import warnings
import numpy as np
import parmed as pmd

from ase.data import atomic_numbers
from ase.neighborlist import NeighborList
from matscipy.neighbours import neighbour_list
from parmed import gromacs
from smamp.insertHbyList import insertHbyList
from smamp.tools import find
from smamp.tools import read_atom_numbers



def read_input_files():
    """Search for and read input files (with implicit H-atoms)."""
    ase_struct, pmd_top = None, None

    pdb_file = find(path='..', 	folder_keyword='initial_structure', file_keyword='.pdb')[0]
    top_file = find(path='..', 	folder_keyword='initial_structure', file_keyword='.top')[0]

    ase_struct = ase.io.read(pdb_file)
    pmd_struct = pmd.load_file(pdb_file)
    pmd_top = gromacs.GromacsTopologyFile(top_file, parametrize=False)

    # Make sure we actually found everything we need
    if ase_struct is None:
        raise RuntimeError('structure file (.pdb) not found in {}'.format(input_dir))
    if pmd_top is None:
        raise RuntimeError('topology file (.top) not found in {}'.format(input_dir))
    return ase_struct, pmd_struct, pmd_top


def main(implicitHbondingPartners=None):
    """Execute everything."""

    # Read the hydrogen-number table by default
    if implicitHbondingPartners is None:
        implicitHbondingPartners = read_atom_numbers()

    # Read the united-atoms files extracted from the MD-simulation trajectory
    # throws some warnings on angle types, does not matter for bonding info
    with warnings.catch_warnings():
         warnings.simplefilter('ignore')
         ase_struct, pmd_struct, pmd_top = read_input_files()

    pmd_top.strip(':SOL,CL') # strip water and electrolyte from system

    pmd_top.box = pmd_struct.box # Needed because .prmtop contains box info
    pmd_top.positions = pmd_struct.positions

    # Insert the explicit hydrogens
    print('Inserting explicit hydrogens, please wait ...')
    with open('insert_H.log', 'w') as logfile:
       new_ase_struct, new_pmd_top, names, residues = insertHbyList(ase_struct,
                                                                    pmd_top,
                                                                    implicitHbondingPartners,
                                                                    bond_length=1.0, 
                                                                    debug=logfile)

    # Write output
    new_ase_struct.write('ase_pdbH.pdb')
    new_ase_struct.write('ase_pdbH.traj')

    # Write other output
    new_pmd_top.write_pdb('pmd_pdbH.pdb')
    test_pmd = pmd.load_file('pmd_pdbH.pdb')
    # some topology format, un functionality similar to GROMACS' .top, but readable by VMD
    # new_pmd_top.write_psf('pmd_pdbH.psf')
    print('Done.')


if __name__ == '__main__':
    main()
