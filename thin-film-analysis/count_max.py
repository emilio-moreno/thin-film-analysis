import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def import_data(filename):
	df = pd.read_csv(filename, skiprows = 2, sep = "  ", names=["Wavelength", "Transmitance"], engine='python')
	return df


def graph(x, y, dev_y, maximum_positions):
	fig, ax= plt.subplots()
	ax.scatter(x, y, label = "Transmitance vs Wavelength")
	ax.scatter(x, dev_y, label = "Derivative")
	ax.set(title = "Transmitance vs Wavelength", xlabel = "Wavelength (nm)", ylabel = "Trans (%)")
	ax.legend()

	for m in maximum_positions:
		ax.axvline(m)
	plt.show()


filename = "./04-09-24 PDMS/PDMS_4kRPM.TRM"
# filename = "./04-09-24 PDMS/silicio_ref.TRM"
# Wavelength bounds
min_wl = 425
max_wl = 740
df = import_data(filename)
df = df[min_wl < df['Wavelength']][df['Wavelength'] < max_wl].dropna()

# graph(df["Wavelength"], df["Transmitance"])
# gradient(y, x)
derivative = np.gradient(df["Transmitance"], df["Wavelength"])
wavelength = df["Wavelength"]
transmitance = df["Transmitance"]

maximum_positions = []
for d, n_d, wl in zip(derivative[:-1], derivative[1:], wavelength[:-1]):
	if d >= 0 and n_d <= 0:
		maximum_positions.append(wl)


graph(wavelength, transmitance, derivative, maximum_positions)