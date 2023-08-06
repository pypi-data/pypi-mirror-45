# -*- coding: utf-8 -*-
from pkg_resources import get_distribution, DistributionNotFound

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = 'unknown'
finally:
    del get_distribution, DistributionNotFound


from .functions import hist, errorbar, stacked, to_stack, xlim, sig_bkg_plot, errorhist, save
from .helpers import xaxis, nf, figure
from .decorations import draw_y_label, decorate, expand, watermark, labels
from .colors import cm, b2helix

import matplotlib as mpl
# mpl.rcParams['mathtext.fontset'] = 'cm'
# mpl.rcParams['mathtext.rm'] = 'serif'
# mpl.rcParams['axes.autolimit_mode'] = 'round_numbers'

print("For optimal usage set `plt.style.use('sciplot')`")