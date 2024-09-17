import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def normalize(X):
	return (X - np.min(X)) / (np.max(X) - np.min(X))


# Import data
string_RPM = "1.5kRPM"
file_path_ref = f"23-08-24 Mediciones espectrómetro/silicio_ref_{string_RPM}.SSM"
file_path_samp = f"23-08-24 Mediciones espectrómetro/pdms_{string_RPM}.SSM"

string_RPM = "Referencia"
file_path_ref = f"23-08-24 Mediciones espectrómetro/silicio.SSM"
file_path_samp = f"23-08-24 Mediciones espectrómetro/pdms_ref.SSM"



df_ref = pd.read_csv(file_path_ref, skiprows = 2, sep = "  ", names=["Wavelength", "Counts"])
df_samp = pd.read_csv(file_path_samp, skiprows = 2, sep = "  ", names=["Wavelength", "Counts"])

# Wavelengths, reference counts and sample counts
wavelengths = df_ref["Wavelength"]
ref_counts, samp_counts = [df_ref["Counts"], df_samp["Counts"]]

# Normalizing
norm_ref_counts, norm_samp_counts = [normalize(ref_counts), normalize(samp_counts)]
norm_diff_counts = norm_ref_counts - norm_samp_counts


# Plots
fig, axs = plt.subplot_mosaic([["ref", "norm_ref"], ["samp", "norm_samp"], ["diff", "diff"]])
fig.suptitle(f"PDMS - Velocidad: {string_RPM}")
lower_limit = 650
upper_limit = 1500
axs["ref"].plot(wavelengths[lower_limit:upper_limit], ref_counts[lower_limit:upper_limit])
axs["samp"].plot(wavelengths[lower_limit:upper_limit], samp_counts[lower_limit:upper_limit])
axs["norm_ref"].plot(wavelengths[lower_limit:upper_limit], norm_ref_counts[lower_limit:upper_limit])
axs["norm_samp"].plot(wavelengths[lower_limit:upper_limit], norm_samp_counts[lower_limit:upper_limit])
axs["diff"].plot(wavelengths[lower_limit:upper_limit], norm_diff_counts[lower_limit:upper_limit])

# Titles for plots
titles = ["Referencia", "Referencia normalizada", "Muestra", "Muestra normalizada", "Diferencia normalizada"]
y_labels = ["Counts", "Normalized counts", "Counts", "Normalized counts", "Normalized counts"]
for ax_name, title, y_label in zip(axs, titles, y_labels):
	axs[ax_name].set(title = title, xlabel = "Wavelength (nm)", ylabel = y_label)
plt.subplots_adjust(hspace = 0.75)
plt.show()