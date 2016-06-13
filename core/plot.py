from collections import defaultdict

try:
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError:
    print("Matplotlib or numpy is not installed! Try 'pip3 install matplotlib && pip3 install numpy")
    raise

# generate numbers to plt.figure
numgen = (x for x in range(30))


def get_boxplot(data, title='Default boxplot title', xlabel='Default X label',
                ylabel="Default Y label", yscale='linear', **kwargs):
    """Create boxplot from ordinal data"""
    if _typecheck(data, list):
        pass
    fig = plt.figure(next(numgen), figsize=(6, 15))
    ax = fig.add_subplot(111)
    ax.set_title(title)
    bp = ax.boxplot(data, patch_artist=True)
    # ax.set_xticklabels(labels)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ax.set_yscale(yscale, nonposy='clip')
    plt.grid(True, axis='both', which='both')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    return fig


def get_piechart(data, title='Default piechart title', **kwargs):
    """Create piechart from nominal data"""
    if _typecheck(data, list):
        pass
    total = len(data)
    nums = defaultdict(int)
    for v in data:
        nums[v] += 1

    fract = {k: float(v / total) for k, v in nums.items()}
    vals = list(fract.values())
    labs = list(fract.keys())
    fig = plt.figure(next(numgen), figsize=(9, 6))
    ax = fig.add_subplot(111)
    ax.set_title(title)
    p = ax.pie(vals, labels=labs, shadow=True)
    return fig


def get_cumulative_distribution(data, title='Default cumulative histogram title',
                                xlabel="Default X label", ylabel="Default Y label",
                                xscale='linear', yscale='linear', **kwargs):
    n_bins = 50
    # n_ordinal_data = len(ordinal_data)
    values, base = np.histogram(data, bins=n_bins)
    cumulative = np.cumsum(values)
    fig = plt.figure(next(numgen), figsize=(9, 6))
    ax = fig.add_subplot(111)
    ax.set_title(title)
    ax.set_xscale(xscale, nonposx='clip')
    ax.set_yscale(yscale, nonposy='clip')
    ax.plot(base[:-1], cumulative, c='blue')
    plt.grid(True, axis='both', which='both')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    return fig


def _typecheck(data, data_type):
    """"""
    if isinstance(data, data_type):
        return True
    raise TypeError("Please provide data in a {}!".format(data_type))


plot_2_method = {'boxplot': get_boxplot,
                 'piechart': get_piechart,
                 'cumulative_distribution': get_cumulative_distribution}


def get_plot_callable(plottype):
    """Factory method for choosing the plot method"""
    try:
        return plot_2_method[plottype]
    except ValueError:
        raise Exception("Cannot pair plot type {} with plotting method!".format(plottype))
