import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy as sp
import os
import glob
import sys
from uncertainties import ufloat


def main():
	# Modules
	sys.path.insert(0, '../../Analyzers')
	import thickness_vs_RPM_analyzer as tR

	# Directory, parameters for plot and function for curve fit
	directory = './Data/*.CSV'
	xlabel = 'RPM'
	ylabel = 'Grosor (μm)'

	rc_update = {'font.size': 18, 'font.family': 'serif',
				 'font.serif': ['Times New Roman', 'FreeSerif'], 'mathtext.fontset': 'cm',
				 'lines.linewidth': 3, 'lines.markersize': 4}
	plt.rcParams.update(rc_update)
	# colors = ['#d0990099', '#fff20fff', '#00808699', '#41f8ffff', '#84848499', '#1a1a1aff']
	# colors = ['#fff20fff', '#41f8ffff', '#d09900ff', '#008086ff', '#848484ff', '#1a1a1aff']
	colors = ['#0040eb', '#ffbf14', '#ff7f79', '#008086', '#c10000', '#56cccc']
	linestyle = ['-', '--', '-', '--', '-', '--']
	labels = ["Incidencia normal - 1.5 min", "Incidencia $(29.8\\pm0.4)$° - 1.5 min",
			  "Incidencia normal - 2 min", 'Incidencia $(29.8\\pm0.4)$° - 2 min ',
			  "Incidencia normal - 2 min (extra PDMS)", "Incidencia $(29.8\\pm0.4)$° - 2 min (extra PDMS)"]
	title = "PDMS - Grosor vs RPM\nAjuste: $grosor = p / RPM$"
	graph_filename = "../../Experiment Diagrams/PDMS - Thickness vs RPM.pdf"

	function = lambda R, p: p / R

	# I/O
	listdir = glob.glob(directory)
	listdir = sorted(listdir)
	dfs = []

	for filename in listdir:
		# Skip test runs
		if '05' in filename:
			continue
		# Skip non separated data from the 24/19th
		if '19' in filename and not ('less' in filename or 'more' in filename):
			continue
		dfs.append(pd.read_csv(filename))

	# Curve fits
	parameters, covariances = tR.individual_curve_fit(dfs, function)

	# rcParams 
	rc_update = {'font.size': 18, 'font.family': 'serif', 'font.serif': ['Times New Roman', 'FreeSerif']}
	plt.rcParams.update(rc_update)

	# Plot
	RPM_bounds = [[1400, 6000], [1400, 6000],
				  [1000, 6000], [1000, 6000],
				  [1100, 6000], [1100, 6000]]
	fig, ax = plt.subplots(figsize = (13, 9))

	# Plotting data
	tR.graph(dfs, fig, ax, labels, title, linestyle, xlabel, ylabel, colors)

	# Plotting individual fits
	for df, p, c, label, color, ls, bounds in zip(dfs, parameters, covariances, labels, colors, linestyle, RPM_bounds):
		RPM = df['RPM']
		rpm = np.linspace(bounds[0], bounds[-1], 1000)
		u_parameter = ufloat(p, np.sqrt(c))
		# Relative error
		rel_STD = float(np.sqrt(c) / p) * 100
		ax.plot(rpm, function(rpm, p),
				label = f'{label}\n$p$ = $({float(p):.3E})\\pm{rel_STD:.2f}\\%$',
				linestyle = ls, color = color, alpha = 1, zorder=1)

	ax.legend(
		framealpha = 1,
		loc=1,
	    fontsize=12.5,
	    ncols=2, 
	    borderaxespad=0.3,
	    handletextpad=0.1,
	    markerscale=2,
    )
	plt.tight_layout()
	# plt.show()
	plt.savefig(graph_filename, bbox_inches='tight', dpi=300)


if __name__ == '__main__':
	main()