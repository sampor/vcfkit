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


if __name__ == '__main__':
    args = parse_args()
    ckor = VcfStatsRunner(in_file=args.in_vcf, pdf_path=args.pdf_path)
    ckor.analyze_tags(args.tags)
