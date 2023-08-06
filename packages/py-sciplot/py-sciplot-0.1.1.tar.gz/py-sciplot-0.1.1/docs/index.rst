==========
py-sciplot
==========

This is the documentation of **py-sciplot**, scientific plotting tools for python matplotlib.

.. note::

    This project is in development.


Sciplot offers additional features to matplotlib for making scientific plots, such as histograms and graphs.
One of the major features is the builtin :code:`hist` function for plotting multiple histograms and graphs on the same
x-axis with the same binning.
This package is intended to be used alongside with matplotlib.

Example
-------

Simple fit and plot of a Gaussian Distribution:

.. code-block:: python

   import matplotlib.pyplot as plt
   import sciplot as sp

   plt.style.use('sciplot')

   import numpy as np

   simulation_data = np.append(np.random.random_sample(100)*7 - 3.5, np.random.normal(0, 0.5, 100))
   data = np.append(np.random.random_sample(100)*7 - 3.5, np.random.normal(0, 0.4, 100))

   sp.errorhist(simulation_data, bins=30, color='black', label='Pseudo Simulation')
   sp.hist(data, fill=True, style=1, label='Pseudo Data')

   plt.legend()
   sp.labels('E', "Events", "GeV", 1)
   sp.save("example.png")

The produced output will look like this:

.. figure:: http://www.desy.de/~swehle/sciplot.png
   :width: 300 px
   :alt: Output of the example plot.

Another feature is the automaitc creation of stacked histograms:

.. code-block:: python

   import matplotlib.pyplot as plt
   import sciplot as sp
   import pandas as pd
   import numpy as np


   plt.style.use('sciplot_ticks')

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

The produced output will look like this:

.. figure:: http://www.desy.de/~swehle/sciplot2.png
   :width: 300 px
   :alt: Output of the example stacked plot.


Installation
============

This package will be made available for pip.


Contents
========

.. toctree::
   :maxdepth: 2

   License <license>
   Authors <authors>
   Changelog <changelog>
   Module Reference <api/modules>


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _toctree: http://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html
.. _reStructuredText: http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
.. _references: http://www.sphinx-doc.org/en/stable/markup/inline.html
.. _Python domain syntax: http://sphinx-doc.org/domains.html#the-python-domain
.. _Sphinx: http://www.sphinx-doc.org/
.. _Python: http://docs.python.org/
.. _Numpy: http://docs.scipy.org/doc/numpy
.. _SciPy: http://docs.scipy.org/doc/scipy/reference/
.. _matplotlib: https://matplotlib.org/contents.html#
.. _Pandas: http://pandas.pydata.org/pandas-docs/stable
.. _Scikit-Learn: http://scikit-learn.org/stable
.. _autodoc: http://www.sphinx-doc.org/en/stable/ext/autodoc.html
.. _Google style: https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings
.. _NumPy style: https://numpydoc.readthedocs.io/en/latest/format.html
.. _classical style: http://www.sphinx-doc.org/en/stable/domains.html#info-field-lists
