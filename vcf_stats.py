#!/home/daniel/ielis/vcfkit/vcfkit_venv/bin/python
import argparse
import sys

from core.stats import VcfStatsRunner


def parse_args():
    VERSION = 'v0.0.1'
    parser = argparse.ArgumentParser(description="Generate PDF with useful statistics concerning VCF tags",
                                     prog="vcf_stats.py")
    parser.add_argument("in_vcf", help="Input VCF file", default=sys.stdin)
    parser.add_argument("pdf_path", help="Write PDF report to this path")
    parser.add_argument("-c", "--plot_config_file", help="YAML file with info for plotting (labels, scale, ...)",
                        default='config/plot_config.yaml')
    parser.add_argument("-t", "--tags", help="VCF Format, Filter or Info tags to be analyzed",
                        default='GT,GQ,DP')  # TODO check ci zobrazuje default polia v CMD line
    parser.add_argument("-v", "--version", action='version', version='%(prog)s ' + VERSION)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    ckor = VcfStatsRunner(in_file=args.in_vcf, out_path=args.pdf_path, plot_config_file=args.plot_config_file)
    ckor.analyze_tags(args.tags)
