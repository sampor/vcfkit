from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np

# generate numbers to plt.figure
numgen = (x for x in range(30))


def create_boxplot(fpath, ordinal_data, labels, title='Default boxplot title'):
    """Create boxplot from ordinal data"""
    if _typecheck(ordinal_data, list):
        pass
    fig = plt.figure(next(numgen), figsize=(6, 15))
    ax = fig.add_subplot(111)
    plt.grid(True)
    ax.set_title(title)
    bp = ax.boxplot(ordinal_data, patch_artist=True)
    ax.set_xticklabels(labels)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ax.text()
    fig.savefig(fpath, bbox_inches='tight')


def create_piechart(fpath, nominal_data, title='Default piechart title'):
    """Create piechart from nominal data"""
    if _typecheck(nominal_data, list):
        pass
    total = len(nominal_data)
    nums = defaultdict(int)
    for v in nominal_data:
        nums[v] += 1

    fract = {k: float(v / total) for k, v in nums.items()}
    vals = list(fract.values())
    labs = list(fract.keys())
    fig = plt.figure(next(numgen), figsize=(9, 6))
    ax = fig.add_subplot(111)
    ax.set_title(title)
    p = ax.pie(vals, labels=labs, shadow=True)
    fig.savefig(fpath, bbox_inches='tight')


def create_cumulative_distribution(fpath, ordinal_data, title='Default cumulative histogram title'):
    n_bins = 50
    n_ordinal_data = len(ordinal_data)
    values, base = np.histogram(ordinal_data, bins=n_bins)
    cumulative = np.cumsum(values)
    fig = plt.figure(next(numgen), figsize=(9, 6))
    plt.grid(True)
    ax = fig.add_subplot(111)
    ax.set_title(title)
    ax.plot(base[:-1], cumulative, c='blue')
    fig.savefig(fpath, bbox_inches='tight')


def _typecheck(data, data_type):
    """"""
    if isinstance(data, data_type):
        return True
    raise TypeError("Please provide data in a {}!".format(data_type))
