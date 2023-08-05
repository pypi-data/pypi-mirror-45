# -*- encoding: utf-8 -*-
"""Compare different correction techniques using data generated
according to the Bennett et al. model.

Author: Tuomas Puoliväli
Email: tuomas.puolivali@helsinki.fi
Last modified: 11th September 2018
License: Revised 3-clause BSD
"""

from data import two_class_grid_model

from fdr import lsu, qvalue
from fwer import sidak

from viz import plot_grid_model

"""Generate the test data."""
nl, sl = 100, 60
N, delta = 25, 0.5
X = two_class_grid_model(nl, sl, N)

"""Apply each correction technique to the generated dataset."""
Y_sidak = sidak(X.flatten(), alpha=0.05)
Y_sidak = Y_sidak.reshape(nl, nl)

Y_fdr = lsu(X.flatten(), q=0.05)
Y_fdr = Y_fdr.reshape(nl, nl)

Y_qvalue, _ = qvalue(X.flatten(), threshold=0.05)
Y_qvalue = Y_qvalue.reshape(nl, nl)

"""Visualize the results."""
fig_sidak = plot_grid_model(Y_sidak, nl, sl)
fig_sidak.axes[0].set_title('Sidak')

fig_fdr = plot_grid_model(Y_fdr, nl, sl)
fig_fdr.axes[0].set_title('FDR')

fig_qvalue = plot_grid_model(Y_qvalue, nl, sl)
fig_qvalue.axes[0].set_title('Q-value')

import matplotlib.pyplot as plt
plt.show()
