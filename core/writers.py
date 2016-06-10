import datetime
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt


class PdfPlotWriter(object):
    """

    """

    # TODO - vymysliet aby reporty vyzerali pekne - A4 format, Uvedeny nazov vzorky, suvisiace grafy pri sebe atd
    def __init__(self, out_path):
        """"""
        self._out = out_path
        self._plots = []

    def add_plot(self, plot_object):
        # TODO - check if it is really some plot? Duck typing check?
        self._plots.append(plot_object)

    def write_out(self):
        """Create PDF as shown in pylab_examples code: multipage_pdf.py"""
        if not self._plots:
            raise Exception("No plot added, nothing to plot!")

        with PdfPages(self._out) as pdf:
            for fig in self._plots:
                pdf.savefig(fig)
