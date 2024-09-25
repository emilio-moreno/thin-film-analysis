import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
from uncertainties import ufloat


def main():
	sys.path.insert(0, '../Analyzers')
	import thickness_analyzer as ta

	# Directory for transmitance vs wavelength.
	trans_directory = "./trans/PDMS/"
	listdir = os.listdir(trans_directory)
	listdir = [trans_directory + filename for filename in listdir]
	listdir = sorted(listdir, key = ta.extract_integer)

	# Refractive index
	refrac_n = ufloat(1.76, 0.13) # Measured with microscope
	# refrac_n = ufloat(1.4235, 0) # Internet

	# Wavelength bounds
	default_min_wl = 440
	default_max_wl = 740

	# Default bounds
	wavelength_bounds = np.array([[default_min_wl, default_max_wl] for i in range(len(listdir))])
	# Max corrections adds value in list to calculation made by calculate_n_max
	max_corrections = np.zeros(len(listdir))

	# Modifying bounds and corrections for specific film
	max_corrections[2], wavelength_bounds[2, 0], wavelength_bounds[2, 1] = 4, 523, 711
	max_corrections[4], wavelength_bounds[4, 0], wavelength_bounds[4, 1] = -2, 512, 706
	max_corrections[5], wavelength_bounds[5, 0], wavelength_bounds[5, 1] = -1, 561, 654
	#max_corrections[6], wavelength_bounds[6, 0], wavelength_bounds[6, 1] = 0, 504, 534

	# RPM
	RPM_df = pd.read_csv('./11-09-24_RPM.CSV')
	RPM = RPM_df['RPM']
	RPM_std = [float(RPM_std) for RPM_std in RPM_df['RPM_std']]

	# Calculate number of maxima
	n_max = ta.calculate_n_max(listdir, wavelength_bounds, RPM, max_corrections, graph = False)

	# Calculate thickness
	uthickness = ta.calculate_thickness(refrac_n, n_max, wavelength_bounds[:, 0], wavelength_bounds[:, 1])
	uthickness = uthickness / 1000
	thickness = [t.n for t in uthickness]
	thickness_std = [t.s for t in uthickness]

	# I'll exclude PDMS # 7
	df_filename = 'PDMS_thickness_RPM_11-09-24.CSV'
	ta.export_df(RPM_df[:-1], thickness[:-1], thickness_std[:-1], wavelength_bounds[:-1], n_max[:-1], listdir[:-1], df_filename, show = True)
	ta.graph_thickness(RPM, RPM_std, thickness, thickness_std, "PDMS - Thickness vs RPM\n11-09-24")


if __name__ == '__main__':
	main()