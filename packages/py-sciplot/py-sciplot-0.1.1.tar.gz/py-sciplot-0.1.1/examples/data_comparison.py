# -*- coding: utf-8 -*-
""" Data Comparison

In data science, often one wants to compare two different sets of data, like signal/background or prediction and
actual data.

In this very brief script we create two sets of data and compare them in one plot.

"""
import matplotlib.pyplot as plt
import sciplot as sp
import matplotlib
import numpy as np


matplotlib.use('Agg')

try:
    plt.style.use('sciplot')
except OSError:
    print("Please install sciplot matplotlib style")

# Create some pseudo data
simulation_data = np.append(np.random.random_sample(100)*7 - 3.5, np.random.normal(0, 0.5, 100))
data = np.append(np.random.random_sample(100)*7 - 3.5, np.random.normal(0, 0.4, 100))

# Plot both datasets with sciplot
sp.figure()
sp.errorhist(simulation_data, bins=30, color='black', label='Pseudo Simulation')
sp.hist(data, fill=True, style=0, label='Pseudo Data')

plt.legend()
sp.xlim()
sp.labels('$\Delta M$', "Events", "GeV", 0)
sp.save("data_comparison.png")
