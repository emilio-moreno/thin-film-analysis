import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def import_data(filename):
	df = pd.read_csv(filename, skiprows = 2, sep = "  ", names=["Wavelength", "Transmitance"], engine='python', dtype='float64')
	return df


def extract_integer(filename):
    return float(filename.split('_')[-1][:-4])


def graph_maxima(x, y, title, maximum_positions, max_correction, dev_y = None, extraticks = None):
	# rcParams
	rc_update = {'font.size': 18, 'font.family': 'Times New Roman'}
	plt.rcParams.update(rc_update)

	# Plots
	fig, ax= plt.subplots()
	ax.plot(x, y, label = "Transmitance vs Wavelength")

	if dev_y:
		ax.plot(x, dev_y, label = "Derivative")

	for m in maximum_positions[:-1]:
		ax.axvline(m, color = 'k', linestyle = '--')
	# Graph all maxima except last one, so we can add label
	ax.axvline(maximum_positions[-1], color = 'k', label = f"Maxima{max_correction:+.0f}", linestyle = '--')

	# Format
	ax.set(title = title, xlabel = "Wavelength (nm)", ylabel = "Trans (%)")
	ax.grid(color = '#999', linestyle = '--')
	if extraticks:
		ax.set_xticks(list(plt.xticks()[0]) + extraticks)
	ax.legend(loc = 1, fontsize = 10)

	figManager = plt.get_current_fig_manager()
	figManager.full_screen_toggle()
	plt.show()


def get_max_positions(derivative, wavelength):
	maximum_positions = []
	for d, n_d, wl in zip(derivative[:-1], derivative[1:], wavelength[:-1]):
		if d >= 0 and n_d <= 0:
			maximum_positions.append(wl)

	return maximum_positions


def calculate_n_max(listdir, wavelength_bounds, RPMs, max_corrections, graph = True):
	number_of_max = []
	for i, x in enumerate(zip(listdir, wavelength_bounds, max_corrections, RPMs)):
		filename = x[0]
		RPM = x[-1]
		min_wl, max_wl = x[1][0], x[1][1]
		correction = x[2]
		title = f"{filename}\n{RPM:.0f} RPM - Index: {i}"	

		trans_df = import_data(filename)
		trans_df = trans_df[min_wl < trans_df['Wavelength']][trans_df['Wavelength'] < max_wl].dropna()

		derivative = np.gradient(trans_df["Transmitance"], trans_df["Wavelength"])
		wavelength = trans_df["Wavelength"]
		transmitance = trans_df["Transmitance"]
		maximum_positions = get_max_positions(derivative, wavelength)
		number_of_max.append(len(maximum_positions) + correction)

		if graph:
			graph_maxima(wavelength, transmitance, title, maximum_positions, correction)

	return np.array(number_of_max)


def calculate_thickness(n, m, min_wl, max_wl):
	'''
	Parameters
	----------
	n : float
		Refractive index.

	m : int
		Number of maxima.

	min_wl : float
		Minimum wavelength.

	max_wl : float
		Maximum wavelength.
	'''
	wl_diff = 1 / min_wl - 1 / max_wl
	return m / (2 * n * wl_diff)


def export_df(RPM_df, thickness, thickness_std, listdir, df_filename, show = True):
		# Dictionary values for new dataframe including thickness
		short_filenames = [filename.split('/')[-1] for filename in listdir]
		df_values = []
		for key in RPM_df:
			df_values.append((key, RPM_df[key]))
		df_values.insert(1, ('transmitance_filename', short_filenames))
		df_values.append(('thickness (um)', thickness))
		df_values.append(('thickness_std', thickness_std))

		# Data to df and CSV
		thickness_RPM_df = pd.DataFrame(dict(df_values[1:]))

		# We'll save a copy of df in current directory
		thickness_RPM_df.to_csv(f'./{df_filename}')
		thickness_RPM_df.to_csv(f'../thickness_vs_RPM/PDMS/{df_filename}')

		if show:
			pd.set_option('display.max_rows', None, 'display.max_columns', None,
						  'display.width', 1000)
			print(thickness_RPM_df)


def graph_thickness(RPM, RPM_std, thickness, thickness_std, title, extraticks = None):
	# rcParams
	rc_update = {'font.size': 18, 'font.family': 'Times New Roman'}
	plt.rcParams.update(rc_update)

	# Plots
	fig, ax= plt.subplots()
	ax.scatter(RPM, thickness, label = "Thickness vs RPM", marker = '*',
			   color = 'Purple', s = 50)

	# Errors
	err = [(r_std, t_std) for r_std, t_std in zip(thickness_std, RPM_std)]
	ax.errorbar(RPM, thickness, xerr = RPM_std, yerr = None, 
				color = 'Purple', capsize = 5, ls = 'none')

	# Format
	ax.set(title = title, xlabel = "RPM", ylabel = "Thickness (um)")
	ax.grid(color = '#999', linestyle = '--')
	if extraticks:
		ax.set_xticks(list(plt.xticks()[0]) + extraticks)
	ax.legend()

	figManager = plt.get_current_fig_manager()
	figManager.full_screen_toggle()
	plt.show()


def main():
	pass



if __name__ == '__main__':
	main()