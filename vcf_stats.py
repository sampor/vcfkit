#!./vcfkit_venv/bin/python
import argparse
import sys

from core.stats import VcfStatsRunner


def parse_args():
    VERSION = 'develop'
    parser = argparse.ArgumentParser(description="Generate PDF with useful statistics from VCF file",
                                     prog="vcf_stats.py")
    parser.add_argument("in_vcf", help="Input VCF file", default=sys.stdin)
    parser.add_argument("pdf_path", help="Write PDF report to this path")
    parser.add_argument("-t", "--tags", help="VCF Format, Filter or Info tags to be analyzed",
                        default='GT,GQ,DP')  # TODO check ci zobrazuje default polia v CMD line
    parser.add_argument("-v", "--version", action='version', version='%(prog)s ' + VERSION)
    return parser.parse_args()




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
    ckor = VcfStatsRunner(in_file=args.in_vcf, pdf_path=args.pdf_path)
    ckor.analyze_tags(args.tags)
