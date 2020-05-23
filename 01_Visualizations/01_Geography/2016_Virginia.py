# GOAL: Plot General Election results by county in Virginia
# Data available from MIT Election Lab ("https://electionlab.mit.edu/data#data")

# ---------------------- IMPORTS ---------------------- #
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

here = os.getcwd()

# Specific to my local directory hierarchies
os.chdir("..")
os.chdir("04_Data")
os.chdir("dataverse_files")
data = pd.read_csv("countypres_2000-2016.csv")
os.chdir(here)


# ---------------------- CLEANING ---------------------- #

# Filter out only data from Virginia in 2016
VA16 = data[data["year"] == 2016]
VA16 = VA16[VA16["state"] == "Virginia"]

VA16.reset_index(inplace=True)
VA16.drop("index", axis=1, inplace=True)

for index, val in enumerate(VA16["candidatevotes"]):

    tot = VA16["totalvotes"][index]

    VA16.loc[index, "vote_share"] = (val / tot)

VA16 = VA16[VA16["candidate"] == "Hillary Clinton"]

# ---------------------- PLOTTING ---------------------- #

# NOTE: Best to run this in Jupyter to properly visualize the plot ... tough to export static images with Plotly

import plotly.figure_factory as ff

values = VA16["vote_share"]
fips = VA16["FIPS"]

fig = ff.create_choropleth(fips=fips, values=values,
                           scope=["Virginia"], county_outline={'color': 'rgb(255,255,255)', 'width': 0.5},
                          exponent_format=True, round_legend_values=True,
                          title="2016 Presidential Election: Hillary Clinton Vote %")

fig.layout.template = None
fig.update_layout(showlegend=False)
fig.show()
