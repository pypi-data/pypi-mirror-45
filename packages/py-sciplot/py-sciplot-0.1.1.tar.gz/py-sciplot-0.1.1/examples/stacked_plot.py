# -*- coding: utf-8 -*-
""" Stacked plot

In data science, often one wants to compare two different sets of data, like signal/background or prediction and
actual data.

In this very brief script we create two sets of data and compare them in one plot.

"""
import matplotlib.pyplot as plt
import sciplot as sp
import pandas as pd
import numpy as np

try:
    plt.style.use('sciplot_ticks')
except OSError:
    print("Please install sciplot matplotlib style")

# Create some pseudo data
nb = 5000
ns = 3000
df = dict({'mass': np.append(np.random.random_sample(nb)*7 - 3.5, np.random.normal(0, 0.5, ns))})
df['exp'] = np.random.randint(0, 6, ns+nb)
df = pd.DataFrame(df)

# Automatic creation of a stacked plot of 'mass' split by values of 'exp'
sp.stacked(df, "mass", 'exp', bins=50,)

sp.xlim()
sp.labels('$\Delta M$', "Events", "GeV", 0)
sp.save("stacked_plot.png")
