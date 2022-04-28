import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import preprocessing
import re
import numpy as np

# pre data config
sns.set_theme(style="whitegrid")
file_loc = r"C:\Users\brody.westberg\OneDrive - Thermo Fisher Scientific\Documents\HistDataDeleteThisLater.xlsx"
save_loc = r"C:\Users\brody.westberg\OneDrive - Thermo Fisher Scientific\Documents\WCX-10\\"
#for the color dimension (seperate box plots in same X,Y position

Hue_vars = ["Main Set",
              "Good Set",
              "Resized and Washed"]
#just defines the corresponding legend for that info
Ledg_vars = ["Main Set",
              "Good Set",
              "Resized and Washed"]

u55 = pd.read_excel(file_loc, sheet_name=0, header = 0,
                    names = ["Isocratic: Retention", "Isocratic: Symmetry", "Isocratic: Efficiency", "Isocratic: Pressure", "Lot: Efficiency", "Lot: Symmetry", "Lot: Resolution", "Lot: Lysozyme Ret", "Lot: L-R Ret", "Tmab: Resolution 4", "Tmab: Peaks", "Tmab: Selectivity"],
                    usecols="R:AC", skiprows=1, nrows=72)
Main=u55.loc[:47]
Good=u55.loc[48:61]
#Rework=u55.loc[62:]
Rework=u55.loc[62:69]
Main["name"]="Main Set"
Good["name"]="Good Set"
Rework["name"]="Rework Set"

total=pd.concat([Main,Good,Rework], ignore_index=True)
total.drop(columns=["Tmab: Resolution 4", "Tmab: Peaks", "Tmab: Selectivity"], inplace=True)

Main_melt = pd.melt(total, ["name"],value_name="Normalized Value", var_name="Measurement")

f, ax = plt.subplots(figsize=(8, 8))
ax.set(xlim = (-2,2))
plt.subplots_adjust(top=1, left=0.25, bottom=0.1, right=0.9)
sns.boxplot(x='Normalized Value', y='Measurement', hue="name", whis=[0.10, 0.90], data=Main_melt, linewidth=2, palette="Set3", fliersize=1)
ax.legend().set_visible(True)  # Set visible will add or remove the legend.
ax.xaxis.grid(True), ax.set(ylabel=""), plt.show()  # I know this is terrible code. Just less lines.

