""" Misc tools
Copyright 2019 Simulation Lab
University of Freiburg
Author: Lukas Elflein <elfleinl@cs.uni-freiburg.de>
"""

import os 
import pandas as pd

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

def check_existence(path, neccessary_files, verbose=True):
	"""Check if all neccessary files exist in path, print warning for missing files.

	Arguments:
	path: string, the path to search
	neccessary_files: list of strings, check if they exist in path
	verbose: Bool, controls amount of printing

	Returns:
	String warning xor None 
	"""
	with cd(path):
		# Files should be here
		# if verbose:
		#	print([f for s, d, f in os.walk('.')])

		for f in neccessary_files:
			if not (os.path.islink(f) or os.path.isfile(f)):
				warning = 'File not found: {}'.format(f)
				if verbose:
					print(Warning(warning))
				return warning
	return None


def find(path, folder_keyword, file_keyword, nr_occ=1, exclude_kw=['template', 'exclude']):
	"""Search folderstructure for files, return paths containing them.

	Arguments:
	path: string, the path to search
	folder_keyword: strings of the subfolders where the files are supposed to be located
	file_keyword: parts of the filename to be located
	nr_occ: how often the file keyword is supposed to occur in the lowererst folder
	exclude_kw: list of keywords where search should be skipped

	Returns:
	List of strings, a collection of all matching paths

	Example:
	crawl(path='./', folder_keyword='dft', file_keyword='rho', nr_occ=1)
	['./600_ps_snapshot/2_dft_calculations/rho.cube', 
	 './600_ps_snapshot/2_dft_calculations/rho.cube', 
	 ...]
	"""
	paths = []
	# Crawl the directory structure
	for subdir, dirs, files in sorted(os.walk(path)):

		# Exclude template folders from search
		if any([keyword in subdir for keyword in exclude_kw]):
			continue

		# Select the folders with the required keyword in them
		if folder_keyword in subdir:

			if nr_occ is not None:
				# Check if at least one desired file exists
				if sum([file_keyword in f for f in files]) < 1:
					print(os.getcwd())
					raise RuntimeError('No {} file found.'.format(file_keyword))

				# No more than one file must exists for uniqueness
				if sum([file_keyword in f for f in files]) > nr_occ:
					print(os.getcwd())
					err = 'Multiple files containing {} found.'.format(file_keyword)
					raise RuntimeError(err)
						
			# If no error was raised, we can use the file we found:
			for f in files:
				if file_keyword in f:
					paths += [os.path.join(subdir, f)]
	return paths


def read_atom_numbers(path='../fitting_constraint_files/hydrogen_per_atom.csv'):
	"""Determines number of explicit Hydrogen atoms per Carbon from a table.
	Arguments
	path: Path to the table.

	Returns:
	hydrogen_per_atom: dictionary mapping atom names to number of hydrogens to insert.
	"""
	df = pd.read_csv(path)
	df = df.set_index('atom', drop=True)
	# target = {'CD4':1,'CD3':1,'CA2':2,'CA3':2,'CB2':2,'CB3':2}
	hydrogen_per_atom = df.to_dict()[df.columns[0]]

	return hydrogen_per_atom


def read_total_charge(path='../fitting_constraint_files/total_charge.csv'):
	"""Determine total charge of molecule by reading file.
	Arguments
	path: Path to the table.

	Returns:
	charge: a float
	"""
	# The default charge is zero, use this if no file is found
	if not os.path.isfile(path):
		print('WARNING: No charge file found at {}. Using default charge of 0.0'.format(path))
		return 0.0

	with open(path) as charge_file:
		for line in charge_file:
			charge = float(line)
	return charge
