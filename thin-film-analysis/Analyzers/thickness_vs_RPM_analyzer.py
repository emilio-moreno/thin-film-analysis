import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy as sp

def graph(dfs, fig, ax, labels, title, colors, plot = True): 
	for df, label, color in zip(dfs, labels, colors):
		# Plots
		RPM, thickness = df['RPM'], df['thickness (um)']
		ax.scatter(RPM, thickness, label = label, marker = '*', color = color, s = 70)
		# Errors
		ax.errorbar(RPM, thickness, xerr = df['RPM_std'], yerr = None,
					color = color, capsize = 5, ls = 'none')

	# Format
	ax.set(title = title, xlabel = "RPM", ylabel = "Thickness (um)")
	ax.grid(color = '#999', linestyle = '--')
	ax.legend(loc = 1, fontsize = 12, ncols = 2)

	figManager = plt.get_current_fig_manager()
	figManager.full_screen_toggle()
	if plot:
		plt.show()


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
