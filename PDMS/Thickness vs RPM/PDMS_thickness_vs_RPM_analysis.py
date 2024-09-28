import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy as sp
import os
import sys


def main():
	# Modules
	sys.path.insert(0, '../../Analyzers')
	import thickness_vs_RPM_analyzer as tR

	# Directory, parameters for plot and function for curve fit
	directory = './Data/'

#	colors = ['Purple', 'Red', '#0bb']
#	labels = ["05-09-24 test", "11-09-24", "19-09-24"]
	colors = ['Purple', 'Red', '#0bb', 'Blue', 'Green']
	labels = ["05-09-24 test", "11-09-24", "19-09-24", 'Inclined 24/11-09-24', 'Inclined 24/19-09-24']
	title = "PDMS - Thickness vs RPM\nFit function: thickness = p / RPM"
	graph_filename = "./Figures/PDMS - Thickness vs RPM with inclined plane.pdf"

	function = lambda R, p: p / R

	# I/O
	listdir = os.listdir(directory)
	listdir = [directory + filename for filename in listdir]
	listdir = sorted(listdir)
	dfs = []
	for filename in listdir:
		dfs.append(pd.read_csv(filename))

	# Curve fits
	parameters, covariances = tR.individual_curve_fit(dfs, function)
	global_p, global_c = tR.global_curve_fit(dfs, function)

	# rcParams 
	rc_update = {'font.size': 18, 'font.family': 'serif', 'font.serif': ['Times New Roman', 'FreeSerif']}
	plt.rcParams.update(rc_update)

	# Plot
	RPM_bounds = [800, 6000]
	fig, ax = plt.subplots(figsize = (16, 9))

	# Plotting individual fits (skip test run [1:])
	for df, p, c, label, color in zip(dfs[1:], parameters[1:], covariances[1:], labels[1:], colors[1:]):
		RPM = df['RPM']
		rpm = np.linspace(RPM_bounds[0], RPM_bounds[-1], 1000)
		# Relative error
		rel_STD = float(np.sqrt(c) / p)
		ax.plot(rpm, function(rpm, p),
				label = f'Fit - {label}\np: {float(p):.2f}\nrel. STD: {rel_STD:.2f}',
				linestyle = '--', color = color, alpha = 0.5)

	# Plotting global fit
	# RPM = df['RPM']
	# rpm = np.linspace(RPM_bounds[0], RPM_bounds[-1], 1000)
	# Relative error
	# rel_STD = float(np.sqrt(global_c) / global_p)
	# ax.plot(rpm, function(rpm, global_p),
	#					  label = f'Global fit\np: {float(global_p):.2f}\nSTD: {rel_STD:.2f}', color = 'k')

	# Plotting data (skip test run [1:])
	tR.graph(dfs[1:], fig, ax, labels[1:], title, colors[1:], plot = True)
	plt.savefig(graph_filename, bbox_inches='tight', dpi=200)


if __name__ == '__main__':
	main()