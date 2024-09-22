import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys


def main():

	sys.path.insert(0, '../Analyzers')
	import thickness_analyzer as ta

	# Directory for transmitance vs wavelength.
	trans_directory = "./scope trans/PDMS/"
	listdir = os.listdir(trans_directory)
	listdir = [trans_directory + filename for filename in listdir]
	listdir = sorted(listdir, key = ta.extract_integer)

	# Refractive index
	refrac_n = 1.4235

	# Wavelength bounds
	default_min_wl = 440
	default_max_wl = 740

	# Default bounds
	wavelength_bounds = np.array([[default_min_wl, default_max_wl] for i in range(len(listdir))])
	# Max corrections adds value in list to calculation made by calculate_n_max
	max_corrections = np.zeros(len(listdir))

	# Modifying for specific film
	max_corrections[0] = -1
	wavelength_bounds[6, 0], wavelength_bounds[6, 1] = [623, 702]
	wavelength_bounds[7, 0], wavelength_bounds[7, 1] = [571, 686]
	wavelength_bounds[8, 0], wavelength_bounds[8, 1] = [593, 738]
	wavelength_bounds[12, 1] = 733

	# RPM
	RPM_df = pd.read_csv('./19-09-24_RPM.CSV', skiprows = [1, 11])
	RPM = RPM_df['RPM']
	RPM_std = [float(RPM_std) for RPM_std in RPM_df['RPM_std']]

	# Calculate number of maxima
	n_max = ta.calculate_n_max(listdir, wavelength_bounds, RPM, max_corrections, graph = False)

	# Calculate thickness
	thickness = ta.calculate_thickness(refrac_n, n_max, wavelength_bounds[:, 0], wavelength_bounds[:, 1])
	thickness = thickness / 1000
	thickness_std = np.zeros(len(thickness))

	df_filename = 'PDMS_thickness_RPM_19-09-24.CSV'
	ta.export_df(RPM_df, thickness, thickness_std, listdir, df_filename, show = True)
	ta.graph_thickness(RPM, RPM_std, thickness, thickness_std, "PDMS - Thickness vs RPM\n19-09-24")


if __name__ == '__main__':
	main()