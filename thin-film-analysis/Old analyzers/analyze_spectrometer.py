import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def normalize(X):
	return (X - np.min(X)) / (np.max(X) - np.min(X))


# Import data
string_RPM = "4kRPM"
file_path = f"04-09-24 PDMS/PDMS_{string_RPM}.TRM"
df = pd.read_csv(file_path, skiprows = 2, sep = "  ", names=["Wavelength", "Transmitance"])

# Plots
fig, axs = plt.subplots()
fig.suptitle(f"PDMS - Velocidad: {string_RPM}")
lower_limit = 650
upper_limit = 1500
axs.plot(df["Wavelength"], df["Transmitance"])

# Titles for plots
axs.set(xlabel = "Wavelength (nm)", ylabel = "Transmitance")
plt.subplots_adjust(hspace = 0.75)
plt.show()