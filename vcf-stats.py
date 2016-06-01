import argparse
import os
import sys
from core.plot import create_boxplot, create_piechart, create_cumulative_distribution
from core.stats import get_instance
from vcf import Reader


def parse_args():
    VERSION = 'develop'
    parser = argparse.ArgumentParser(description="Generate PDF with useful statistics from VCF file",
                                     prog="vcf-stats.py")
    parser.add_argument("in_vcf", help="Input VCF file", default=sys.stdin)
    parser.add_argument("pdf_path", help="Write PDF report to this path")
    parser.add_argument("-t", "--tags", help="VCF Format, Filter or Info tags to be analyzed",
                        default='GT,GQ,DP')  # TODO check ci zobrazuje default polia v CMD line
    parser.add_argument("-v", "--version", action='version', version='%(prog)s ' + VERSION)
    return parser.parse_args()


class Statter(object):
    def __init__(self, in_file, pdf_path):
        assert os.path.exists(in_file), "File {} does not exist!".format(in_file)
        self._in_file = in_file
        self._pdf_path = pdf_path
        self._reader = Reader(filename=self._in_file)
        self._vs = get_instance(self._reader)
        self._data = self._vs.run()

    def run(self):
        # TODO - continue here!
        raise NotImplemented


# fpath = 'test/files/XYZ123.vcf'
# ordfp = 'figs/GTs.png'
# cdist = 'figs/GQcdf.png'
# ddist = 'figs/DPcdf.png'
# nomfp = 'figs/GQs.png'
# orddp = 'figs/DPs.png'
# large = 'input/E6.vcf'
# tags = ['GT', 'DP', 'GQ']
#
# r = Reader(filename=large)
# vs = get_instance(r)
# data = vs.run(tags)
#
# od = data['GQ']
# lod = ['GQ']
# dp = data['DP']
# ldp = ['DP']
# title = 'E6 Genotype Quality'
# create_boxplot(ordfp, od, lod, title=title)
# title = 'E6 Depth'
# create_boxplot(orddp, dp, ldp, title=title)
# title = 'E6 cumulative distribution of Genotype Quality'
# create_cumulative_distribution(cdist, od, title=title)
# title = 'E6 cumulative distribution of Depth'
# create_cumulative_distribution(ddist, dp, title=title)
#
# nd = data['GT']
# title = 'E6 Genotype piechart'
# create_piechart(nomfp, nd, title=title)
#

if __name__ == '__main__':
    args = parse_args()
