import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy as sp

def graph(dfs, fig, ax, labels, title, linestyles, xlabel, ylabel, colors):
	rc_update = {'font.size': 18, 'font.family': 'serif',
				 'font.serif': ['Times New Roman', 'FreeSerif'], 'mathtext.fontset': 'cm'}
	plt.rcParams.update(rc_update)

	for df, label, color, ls in zip(dfs, labels, colors, linestyles):
		# Plots
		RPM, thickness = df['RPM'], df['thickness (um)']
		ax.scatter(RPM, thickness, label = label, marker = 's', color = color, zorder=2)
		# Errors
		eb = ax.errorbar(RPM, thickness, xerr = df['RPM_std'], yerr = df['thickness_std'],
					color = color, capsize = 7, ls = 'none', elinewidth=5, zorder=2)
		eb[-1][0].set_linestyle(ls)
		
	# Format
	fig.suptitle(title)
	ax.set(xlabel = xlabel, ylabel = ylabel)
	ax.grid(color = '#999', linestyle = '--')
	ax.legend(loc = 1, fontsize = 10, ncols = 2)

	figManager = plt.get_current_fig_manager()
	figManager.full_screen_toggle()


def individual_curve_fit(dfs, function):
	parameters, covariances = [], []
	for df in dfs:
		RPM = df['RPM']
		thickness = df['thickness (um)']
		parameter, covariance = sp.optimize.curve_fit(function, RPM, thickness)
		parameters.append(parameter[0])
		covariances.append(covariance[0])
	return parameters, covariances


def global_curve_fit(dfs, function):
	RPM, thickness = [], []
	for df in dfs:
		RPM += list(df['RPM'].values)
		thickness += list(df['thickness (um)'].values)
	return sp.optimize.curve_fit(function, RPM, thickness)
