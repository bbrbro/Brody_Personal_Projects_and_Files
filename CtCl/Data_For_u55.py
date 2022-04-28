import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import preprocessing
import re
import numpy as np

# pre data config
sns.set_theme(style="whitegrid")
file_loc = r"C:\Users\brody.westberg\OneDrive - Thermo Fisher Scientific\Documents\Chrom_Data_u55_edit.xlsx"
save_loc = r"C:\Users\brody.westberg\OneDrive - Thermo Fisher Scientific\Documents\WCX-10\\"
#for the color dimension (seperate box plots in same X,Y position
Hue_vars = ["Heat Rate",
              "CEA ratio",
              "Packing Type",
              "Experiment"]
#just defines the corresponding legend for that info
Ledg_vars = [": 1kw, 3kw, step",
              ": 0.062, 0.050, 0.039",
              ":4M KOAc, MHOAc, 2M KOAc",
              ":Broad, Matris 1, Matris 2"]

mapvals = {"1kw": "A", "3kw": "B", "step": "C",
           "1.0": "A", "1.22": "B", "1.54": "C",
           "A": "A", "B": "B", "C": "C", "D":"D",
           "Broad": "A",
           "Ref": "D"}

tags_to_drop = []

cols_to_drop = ["CEA ratio",
               "Heat Rate",
               "Packing Type",
               "Experiment",
               "Sample Name",
               "Sample Num",
               "Matris",
               "Overshoot"]

### Reading the NistMab data
redo_NistMab = False
redo_Lot = False

if redo_NistMab:
    # set up some values and read in the data
    u55 = pd.read_excel(r"C:\Users\brody.westberg\OneDrive - Thermo Fisher Scientific\Documents\Chrom_Data_u55.xlsx",
                        sheet_name="Chrom_Data_u55_NistMab", na_values=["n.a."])
    u55.drop(u55.loc[[x in tags_to_drop for x in u55["Sample Name"]]].index, inplace=True)
    u55.drop(["Sample Num"], axis=1, inplace=True)
    scaler = preprocessing.StandardScaler()

    # sets up the overall df
    tmp_u55 = u55.drop(["CEA ratio", "Heat Rate", "Pump_Pressure"], axis=1)
    tmp_u55 = pd.melt(tmp_u55, ["Sample Name"], var_name="measurement")
    # plots it overall
    f, ax = plt.subplots(figsize=(10, 10))
    sns.stripplot(x='value', y='measurement', marker='o', data=tmp_u55, linewidth=1, edgecolor="gray", size=8)
    ax.xaxis.grid(True), ax.set(ylabel=""), plt.show()
    # sets up a normal scaled version of the df
    tmp_u55 = u55.drop(["CEA ratio", "Heat Rate", "Sample Name"], axis=1)
    tmp_u55 = pd.DataFrame(scaler.fit_transform(tmp_u55), columns=tmp_u55.columns)
    tmp_u55[["CEA ratio", "Heat Rate", "Sample Name"]] = u55[["CEA ratio", "Heat Rate", "Sample Name"]]
    tmp_u55 = pd.melt(tmp_u55, ["Sample Name", "CEA ratio", "Heat Rate"], var_name="measurement")
    # plot based on heat rate
    f, ax = plt.subplots(figsize=(10, 10))
    sns.boxplot(x='value', y='measurement', whis=[0.25, 0.75], data=tmp_u55, width=0.6, color="0.8")
    sns.stripplot(x='value', y='measurement', hue="Heat Rate", marker='o', data=tmp_u55, linewidth=1, edgecolor="gray",
                  size=6, palette=color_dict)
    ax.xaxis.grid(True), ax.set(ylabel=""), plt.show()  # I know this is terrible code. Just less lines.
    # plot based on CEA/AA
    f, ax = plt.subplots(figsize=(10, 10))
    sns.boxplot(x='value', y='measurement', whis=[0.25, 0.75], data=tmp_u55, width=0.6, color="0.8")
    sns.stripplot(x='value', y='measurement', hue="CEA ratio", marker='o', data=tmp_u55, linewidth=1, edgecolor="gray",
                  size=6, palette=color_dict)
    ax.xaxis.grid(True), ax.set(ylabel=""), plt.show()  # I know this is terrible code. Just less lines.

    # sets up the individaul chart breakdowns.
    BreakDowns = [5, 2, 2, 5, 2, 1, 2, 2, 1, 2, 1]
    cValue = 3
    column_list = list(u55.columns)
    for value in BreakDowns:
        tmp_u55 = u55[column_list[cValue:cValue + value] + ["Sample Name", "CEA ratio", "Heat Rate"]]
        cValue += value
        tmp_u55 = pd.melt(tmp_u55, ["Sample Name", "CEA ratio", "Heat Rate"], var_name="measurement")

        f, ax = plt.subplots(figsize=(10, max(value / 2, 1)))
        plt.subplots_adjust(top=1, left=0.25, bottom=0.33, right=0.9)
        sns.stripplot(x='value', y='measurement', hue='Heat Rate', marker='o', data=tmp_u55, palette=color_dict,
                      linewidth=1, edgecolor="gray", size=8)
        ax.legend(loc='upper right').set_visible(False)  # Set visible will add or remove the legend.
        ax.xaxis.grid(True), ax.set(ylabel=""), plt.show()  # I know this is terrible code. Just less lines.

        f, ax = plt.subplots(figsize=(10, max(value / 2, 1)))
        plt.subplots_adjust(top=1, left=0.25, bottom=0.33, right=0.9)
        sns.stripplot(x='value', y='measurement', hue='CEA ratio', marker='o', data=tmp_u55, palette=color_dict,
                      linewidth=1, edgecolor="gray", size=8)
        ax.legend(loc='upper right').set_visible(False)  # Set visible will add or remove the legend.
        ax.xaxis.grid(True), ax.set(ylabel=""), plt.show()  # I know this is terrible code. Just less lines.

if redo_Lot:
    u55 = pd.read_excel(r"C:\Users\brody.westberg\OneDrive - Thermo Fisher Scientific\Documents\Chrom_Data_u55.xlsx",
                        sheet_name="Chrom_Data_u55_Lot", na_values=["n.a."])
    u55.drop(u55.loc[[x in tags_to_drop for x in u55["Sample Name"]]].index, inplace=True)
    u55.drop(["Sample Num"], axis=1, inplace=True)
    scaler = preprocessing.StandardScaler()

    # sets up the overall df
    tmp_u55 = u55.drop(["Packing Type", "CEA ratio", "Heat Rate", "Signal (0.5) ", "Signal (22) ", "Signal (15) "],
                       axis=1)
    tmp_u55 = pd.melt(tmp_u55, ["Sample Name"], var_name="measurement")
    # plots it overall
    f, ax = plt.subplots(figsize=(10, 10))
    sns.stripplot(x='value', y='measurement', marker='o', data=tmp_u55, linewidth=1, edgecolor="gray", size=8)
    ax.xaxis.grid(True), ax.set(ylabel=""), plt.show()
    # sets up a normal scaled version of the df
    tmp_u55 = u55.drop(["Packing Type", "CEA ratio", "Heat Rate", "Sample Name"], axis=1)
    tmp_u55 = pd.DataFrame(scaler.fit_transform(tmp_u55), columns=tmp_u55.columns)
    tmp_u55[["Packing Type", "CEA ratio", "Heat Rate", "Sample Name"]] = u55[
        ["Packing Type", "CEA ratio", "Heat Rate", "Sample Name"]]
    tmp_u55 = pd.melt(tmp_u55, ["Sample Name", "Packing Type", "CEA ratio", "Heat Rate"], var_name="measurement")
    # plot based on heat rate
    f, ax = plt.subplots(figsize=(10, 10))
    sns.boxplot(x='value', y='measurement', whis=[0.25, 0.75], data=tmp_u55, width=0.6, color="0.8")
    sns.stripplot(x='value', y='measurement', hue="Heat Rate", marker='o', data=tmp_u55, linewidth=1, edgecolor="gray",
                  size=6, palette=color_dict)
    ax.xaxis.grid(True), ax.set(ylabel=""), plt.show()  # I know this is terrible code. Just less lines.
    # plot based on CEA/AA
    f, ax = plt.subplots(figsize=(10, 10))
    sns.boxplot(x='value', y='measurement', whis=[0.25, 0.75], data=tmp_u55, width=0.6, color="0.8")
    sns.stripplot(x='value', y='measurement', hue="CEA ratio", marker='o', data=tmp_u55, linewidth=1, edgecolor="gray",
                  size=6, palette=color_dict)
    ax.xaxis.grid(True), ax.set(ylabel=""), plt.show()  # I know this is terrible code. Just less lines.
    # plot based on CEA/AA
    f, ax = plt.subplots(figsize=(10, 10))
    sns.boxplot(x='value', y='measurement', whis=[0.25, 0.75], data=tmp_u55, width=0.6, color="0.8")
    sns.stripplot(x='value', y='measurement', hue="Packing Type", marker='o', data=tmp_u55, linewidth=1,
                  edgecolor="gray", size=6, palette=color_dict)
    ax.xaxis.grid(True), ax.set(ylabel=""), plt.show()  # I know this is terrible code. Just less lines.

    # sets up the individaul chart breakdowns.
    BreakDowns = [3, 1, 1, 1, 1, 2, 1, 3]
    cValue = 3
    column_list = list(u55.columns)
    for value in BreakDowns:
        tmp_u55 = u55[column_list[cValue:cValue + value] + ["Sample Name", "CEA ratio", "Heat Rate"]]
        cValue += value
        tmp_u55 = pd.melt(tmp_u55, ["Sample Name", "CEA ratio", "Heat Rate"], var_name="measurement")

        f, ax = plt.subplots(figsize=(10, max(value / 2, 1)))
        plt.subplots_adjust(top=1, left=0.25, bottom=0.33, right=0.9)
        sns.stripplot(x='value', y='measurement', hue='Heat Rate', marker='o', data=tmp_u55, palette=color_dict,
                      linewidth=1, edgecolor="gray", size=8)
        ax.legend(loc='upper right').set_visible(False)  # Set visible will add or remove the legend.
        ax.xaxis.grid(True), ax.set(ylabel=""), plt.show()  # I know this is terrible code. Just less lines.

        f, ax = plt.subplots(figsize=(10, max(value / 2, 1)))
        plt.subplots_adjust(top=1, left=0.25, bottom=0.33, right=0.9)
        sns.stripplot(x='value', y='measurement', hue='CEA ratio', marker='o', data=tmp_u55, palette=color_dict,
                      linewidth=1, edgecolor="gray", size=8)
        ax.legend(loc='upper right').set_visible(False)  # Set visible will add or remove the legend.
        ax.xaxis.grid(True), ax.set(ylabel=""), plt.show()  # I know this is terrible code. Just less lines.


def Gen_Charts(Test_name, X_var, Hue_vars, Ledg_vars, Experiment=False, add_legend = False ,order = ["A", "B", "C", "D"]):

        #Reads the file from file_loc uses the test name for the sheet name
        u55 = pd.read_excel(file_loc, sheet_name="Chrom_Data_u55_" + Test_name, na_values=["n.a."], converters = {"CEA ratio":str})
        #define which experiment to use
        if Experiment!=False:
            u55 = u55[(u55["Experiment"] == Experiment) | (u55["Experiment"] == "Ref")]

        #removes all bad data tags from the list
        u55.drop(u55.loc[[x in tags_to_drop for x in u55["Sample Name"]]].index, inplace=True)
        #removes empty columns
        u55.dropna(how="all", axis = 1, inplace = True)

        #define which y_vars we are looking at. It is all the columns not in cols to drop
        y_vars = list(set(u55.columns)-set(cols_to_drop))

        #create some empty data
        u55[Test_name] = ""
        u55["hue"] = ""

        #creates a blank dataframe that we will stack on bottom each hue breakdown
        stacked_u55 = pd.DataFrame(columns=u55.columns)

        #breakdown is hue, for each hue we will stack a new dataframe. We can include or not include a legend
        for hue, legd in zip(Hue_vars, Ledg_vars):
            if hue in u55.columns:
                if add_legend:
                    u55["hue"] = hue + legd
                else:
                    u55["hue"] = hue

                #this replaces the whole X variable with the corresponding mapvals mapping
                u55[Test_name] = [X_var[x] for x in u55[hue]]
                stacked_u55 = pd.concat([stacked_u55, u55])

        for var in y_vars:
            #define the plot where X is the resulting variable you chose to define A,B,C with all Y and the hue is every legend_zip
            # g = sns.catplot(x=Test_name, y=var, hue="hue", palette="tab10", height=6, aspect=.75, kind="box",
            #                 data=stacked_u55, order=order, showfliers = False)
            fig, ax = plt.subplots()
            g = sns.catplot(x=Test_name, y=var, hue="hue", palette="tab10", height=6, aspect=.75, kind="box",
                            data=stacked_u55, order=order, showfliers=False, legend=add_legend)
            g = sns.stripplot(x=Test_name, y=var, hue="hue", palette="tab10", edgecolor = "gray", linewidth = 1,
                            data=stacked_u55, order=order, dodge = True, alpha = 0.5)
            plt.legend("", frameon = False)
            #plot and save
            plt.savefig(save_loc + Test_name + "_" + re.sub('[^A-Za-z0-9]+', '', var) + ".png")
            plt.close()

#see below
Hue_vars = ["Heat Rate",
            "CEA ratio",
            "Packing Type",
            "Matris"]
#Delete this for later if you want to remove the info
Ledg_vars = [": 1kw, 3kw, step, Reference",
              ": 0.062, 0.050, 0.039, Reference",
              ":4M KOAc, MHOAc, 2M KOAc, Reference"
              ":Matris A, Matris B, Nothing, Reference"]

# Gen_Charts("Lot", mapvals, Hue_vars, Ledg_vars, add_legend = False)
# Gen_Charts("Iso", mapvals, Hue_vars, Ledg_vars,  add_legend = False)
# Gen_Charts("NistMab", mapvals, Hue_vars, Ledg_vars, add_legend = False)
# Gen_Charts("TMab", mapvals, Hue_vars, Ledg_vars, add_legend = False)

# Gen_Charts("Lot", mapvals, Hue_vars, Ledg_vars, Experiment="Broad", add_legend = False)
# Gen_Charts("Iso", mapvals, Hue_vars, Ledg_vars, Experiment="Broad",  add_legend = False)
# Gen_Charts("NistMab", mapvals, Hue_vars, Ledg_vars, Experiment="Broad", add_legend = False)
# Gen_Charts("TMab", mapvals, Hue_vars, Ledg_vars, Experiment="Broad", add_legend = False)

# Hue_vars = ["Matris"]
# #Delete this for later if you want to remove the info
# Ledg_vars = [":Matris A, Matris B, Nothing, Reference"]
#
# Gen_Charts("Lot", mapvals, Hue_vars, Ledg_vars, Experiment="Matris", add_legend = False)
# Gen_Charts("Iso", mapvals, Hue_vars, Ledg_vars, Experiment="Matris",  add_legend = False)
# Gen_Charts("NistMab", mapvals, Hue_vars, Ledg_vars, Experiment="Matris", add_legend = False)
# Gen_Charts("TMab", mapvals, Hue_vars, Ledg_vars, Experiment="Matris", add_legend = False)
#
# Hue_vars = ["CEA ratio"]
# #Delete this for later if you want to remove the info
# Ledg_vars = [": 0.062, 0.050, 0.039, Reference"]
#
# Gen_Charts("Lot", mapvals, Hue_vars, Ledg_vars, Experiment="Const MI", add_legend = False)
# Gen_Charts("Iso", mapvals, Hue_vars, Ledg_vars, Experiment="Const MI",  add_legend = False)
# Gen_Charts("NistMab", mapvals, Hue_vars, Ledg_vars, Experiment="Const MI", add_legend = False)
# Gen_Charts("TMab", mapvals, Hue_vars, Ledg_vars, Experiment="Const MI", add_legend = False)

# Hue_vars = ["Heat Rate",
#             "Overshoot"]
# #Delete this for later if you want to remove the info
# Ledg_vars = [": 1kw, 3kw, step, Reference",
#              ": Lowest to Highest A -> D"]
#
# Gen_Charts("Lot", mapvals, Hue_vars, Ledg_vars, Experiment="Broad", add_legend = False)
# Gen_Charts("Iso", mapvals, Hue_vars, Ledg_vars, Experiment="Broad",  add_legend = False)
# Gen_Charts("NistMab", mapvals, Hue_vars, Ledg_vars, Experiment="Broad", add_legend = False)
# Gen_Charts("TMab", mapvals, Hue_vars, Ledg_vars, Experiment="Broad", add_legend = False)


Hue_vars = ["Packing Type"]
#Delete this for later if you want to remove the info
Ledg_vars = [":4M KOAc, MHOAc, 2M KOAc, Reference"]

Gen_Charts("Lot", mapvals, Hue_vars, Ledg_vars, Experiment="Broad", add_legend = False)
Gen_Charts("Iso", mapvals, Hue_vars, Ledg_vars, Experiment="Broad",  add_legend = False)
Gen_Charts("NistMab", mapvals, Hue_vars, Ledg_vars, Experiment="Broad", add_legend = True)
Gen_Charts("TMab", mapvals, Hue_vars, Ledg_vars, Experiment="Broad", add_legend = False)