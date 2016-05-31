#!./venv/bin/python
import argparse
import statistics

from vcf import Reader
import locale

enc = locale.getpreferredencoding()
VERSION = 'develop'


def parse_args():
    parser = argparse.ArgumentParser(prog='vcf-stats.py', description='Get useful stats from VCF file')
    parser.add_argument("input", help="VCF to be examined")
    parser.add_argument("-v", "--version", action='version', version='%(prog)s' + VERSION)
    arguments = parser.parse_args()
    return arguments


def _parse_args():
    """Create dummy args namespace"""
    parser = argparse.ArgumentParser(prog='test-vcf-stats.py', description="Dummy args")
    parser.add_argument("in", help="VCF to be examined")
    parser.add_argument("-v", "--version", action='version', version='%(prog)s' + VERSION)
    arguments = parser.parse_args(['/home/daniel/git/vcf-stats-ielis/vcf/test/example-4.2.vcf'])
    return arguments


def get_quals(record):
    return [s.data.GQ for s in record.samples]


def parse_vcf_quals(fpath):
    """Get dict with  of Vcf Genotype Quals, list per sample"""
    reader = Reader(filename=fpath, encoding=enc)
    samples_gq = {s: [] for s in reader.samples}
    num_samples = len(reader.samples)
    # TODO - doplnit aby bodku v no-calloch skiplo a znizilo pocet varaintov
    for record in reader:
        quals = get_quals(record)
        for i, id in zip(range(num_samples), reader.samples):
            samples_gq[id].append(quals[i])

    return samples_gq


def sample_text_record(data, id):
    """

    :param id:
    :return:
    """
    no_variants = len(data)
    mean = statistics.mean(data)
    stdev = statistics.stdev(data)
    median = statistics.median(data)

    print("################################################")
    print("\t### Sample: {}".format(str(id)))
    print("\t### Num of variants: {}".format(str(no_variants)))
    print("\t###### Genotype Quality (GQ)")
    print("\t#########   Mean: {}".format(mean))
    print("\t######### StdDev: {}".format(stdev))
    print("\t######### Median: {}".format(median))
    print("")


def samples_text_records(samples_quals):
    """

    :param samples_quals:
    :return:
    """
    for sample in samples_quals.keys():
        sample_text_record(samples_quals[sample], sample)


if __name__ == "__main__":
    args = parse_args()
    samples_quals = parse_vcf_quals(args.input)
    samples_text_records(samples_quals)
