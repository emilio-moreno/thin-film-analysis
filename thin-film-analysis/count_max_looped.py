import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def import_data(filename):
	df = pd.read_csv(filename, skiprows = 2, sep = "  ", names=["Wavelength", "Transmitance"], engine='python', dtype='float64')
	return df



def graph_thickness(x, y, title, extraticks = None):
	# rcParams
	rc_update = {'font.size': 18, 'font.family': 'FreeSerif'}
	plt.rcParams.update(rc_update)

	# Plots
	fig, ax= plt.subplots()
	ax.scatter(x, y, label = "Thickness vs RPM", marker = '*', color = 'Purple')

	# Format
	ax.set(title = title, xlabel = "RPM", ylabel = "Thickness (um)")
	ax.grid(color = '#999', linestyle = '--')
	if extraticks:
		ax.set_xticks(list(plt.xticks()[0]) + extraticks)
	ax.legend()

	figManager = plt.get_current_fig_manager()
	figManager.full_screen_toggle()
	plt.show()


def graph_maxima(x, y, title, maximum_positions = [], dev_y = None, extraticks = None):
	# rcParams
	rc_update = {'font.size': 18, 'font.family': 'FreeSerif'}
	plt.rcParams.update(rc_update)

	# Plots
	fig, ax= plt.subplots()
	ax.plot(x, y, label = "Transmitance vs Wavelength")

	if dev_y:
		ax.plot(x, dev_y, label = "Derivative")

	for m in maximum_positions:
		ax.axvline(m, color = '#888', linestyle = '--')

	# Format
	ax.set(title = title, xlabel = "Wavelength (nm)", ylabel = "Trans (%)")
	ax.grid(color = '#999', linestyle = '--')
	if extraticks:
		ax.set_xticks(list(plt.xticks()[0]) + extraticks)
	ax.legend()

	figManager = plt.get_current_fig_manager()
	figManager.full_screen_toggle()
	plt.show()


def get_max_positions(derivative, wavelength):
	maximum_positions = []
	for d, n_d, wl in zip(derivative[:-1], derivative[1:], wavelength[:-1]):
		if d >= 0 and n_d <= 0:
			maximum_positions.append(wl)

	return maximum_positions


def calculate_n_max(listdir, wavelength_bounds, max_corrections, show_graph = True):
	number_of_max = []
	for i, x in enumerate(zip(listdir, wavelength_bounds, max_corrections)):
		filename = x[0]
		min_wl, max_wl = x[1][0], x[1][1]
		correction = x[2]
		title = f"{filename}\nIndex: {i}"	

		df = import_data(filename)
		df = df[min_wl < df['Wavelength']][df['Wavelength'] < max_wl].dropna()

		derivative = np.gradient(df["Transmitance"], df["Wavelength"])
		wavelength = df["Wavelength"]
		transmitance = df["Transmitance"]
		maximum_positions = get_max_positions(derivative, wavelength)
		number_of_max.append(len(maximum_positions) + correction)

		if show_graph:
			graph_maxima(wavelength, transmitance, title, maximum_positions)

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



def main():
	# Refractive index
	refrac_n = 1.4235

	# Wavelength bounds
	default_min_wl = 425
	default_max_wl = 740

	# Paths
	directory = "./11-09-24 PDMS/trans/claros"
	os.chdir(directory)
	listdir = os.listdir(os.getcwd())
	listdir = sorted(listdir)

	# Default bounds
	wavelength_bounds = [[default_min_wl, default_max_wl] for i in range(len(listdir))]
	max_corrections = np.zeros(len(listdir))
	
	# Modifying for specific bounds
	# Claros
	RPM = np.array([5604.93456703177, 4579.164402391075, 4055.7777164920026, 3680.08382714265, 4000, 5000])
	max_corrections[2] = -1

	wavelength_bounds[3][0] = 439
	wavelength_bounds[2] = [577, 709]

	# No claros
	# wavelength_bounds[0] = [474, 715]
	# wavelength_bounds[1] = [513, 703]

	n_max = calculate_n_max(listdir, wavelength_bounds, max_corrections, False)


	wavelength_bounds = np.array(wavelength_bounds)

	thickness = calculate_thickness(refrac_n, n_max, wavelength_bounds[:, 0], wavelength_bounds[:, 1])
	thickness = thickness / 1000
	
	graph_thickness(RPM, thickness, "RPM vs Thickness")



if __name__ == '__main__':
	main()