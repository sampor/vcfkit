#!./vcfkit_venv/bin/python
#  -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 18:21:47 2015

@author: Daniel Danis

Remove unnecessary format fields and move Genotype Quality to QUAL field
Process ONLY single sample VCF

"""

import vcf
import argparse
import locale
import sys
from vcf.model import make_calldata_tuple
from collections import OrderedDict

enc = locale.getpreferredencoding()

in_vcf = '/home/daniel/ielis/vcfkit/input/FH327.snp.vcf'
out_vcf = '/home/daniel/ielis/vcfkit/output/FH327.snp.vcf'


def parse_args():
    VERSION = 'develop'
    parser = argparse.ArgumentParser(description="Downsample Complete Genomics VCF to Jannovar.",
                                     prog="vcf-cg-2-jan.py")
    parser.add_argument("in_vcf", help="Input VCF file", default=sys.stdin)
    parser.add_argument("out_vcf", help="Write output to this path", default=sys.stdout)
    parser.add_argument("-v", "--version", action='version', version='%(prog)s ' + VERSION)
    return parser.parse_args()


class CompleteGenomics2Jannovar(object):
    """

    """

    def __init__(self, in_path, out_path):
        """

        """

        self.reader = vcf.Reader(filename=in_path, encoding=enc)
        self._update_header()
        self.new_format_fields = list(self.reader.formats.keys())
        self.writer = vcf.Writer(stream=open(out_path, mode='w', encoding=enc), template=self.reader)

    def _update_header(self):
        """

        """
        for k in self.reader.formats.keys():
            if not k == 'GT':
                del (self.reader.formats[k])

    def run(self):
        """"""
        for record in self.reader:
            new_record = self._update_record(record)
            self.writer.write_record(new_record)
        self.writer.close()
        sys.exit(0)

    def _update_record(self, record):
        assert len(record.samples) == 1, "Cannot process multisample VCF!"
        self._update_format(record)
        new_data = self._update_sample(record)
        record.samples[0].data = new_data
        return record

    def _update_sample(self, record):
        call = record.samples[0]
        data = call.data
        record.QUAL = float(self._get_min_value(data.CGA_CEHQ))
        data_tuple = make_calldata_tuple(self.new_format_fields)
        od = OrderedDict()
        for k in self.new_format_fields:
            od[k] = getattr(call.data, k)
        data = data_tuple._make(od.values())
        return data

    def _update_format(self, record):
        fmts = [k for k in record.FORMAT.split(':') if k in self.new_format_fields]
        record.FORMAT = ':'.join(fmts)

    def _get_min_value(self, vals):
        """ Return the smallest number from a list """
        assert type(vals) == list, "You must provide values in list!"
        no_nones = [x for x in vals if not any([x is None, x == '.'])]
        small = float(min(no_nones))
        if small == 0.0:
            return 1.0
        return small


if __name__ == '__main__':
    args = parse_args()
    cg2j = CompleteGenomics2Jannovar(args.in_vcf, args.out_vcf)
    cg2j.run()

c = CompleteGenomics2Jannovar(in_vcf, out_vcf)

r = next(c.reader)
# c._update_record(r)
