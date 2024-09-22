import pandas as pd
import numpy as np
df = pd.read_csv("índice de refracción.txt")
indices = (df["plumón_silicio"] - df["película"]) / (df["plumón_película"] - df["película"])
mean_std = indices.std() / np.sqrt(len(df["película"]) - 1)

print(f"Índice de refracción PDMS: {indices.mean():.2f}+/-{mean_std:.2f}")