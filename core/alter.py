from vcf import Reader
from vcf.model import make_calldata_tuple, _Call
from vcf.parser import RESERVED_FORMAT


class Alternator(object):
    """Class for convenient altering of VCF records, especially _Call and _CallData objects

    As _Call and CallData objects are immutable this class simplifies creation of new Calls and CallDatas. It may be
    useful for reorganizing and formatting VCF records, e.g. moving important values from custom format fields
    to more common fields which are recognized by most software. (E.g. CGA_CEHQ to HQ in case of Complete Genomics
    VCF files."""

    def __init__(self, reader_handle):
        self.rhandle = reader_handle

    # def

    def create_empty_call_data(self, samp_fmt_s):
        """Create CallData object as in method vcf.parser._parse_samples
        :param samp_fmt_s: VCF Record format string
        :return: CallData named tuple
        """
        samp_fmt = make_calldata_tuple(samp_fmt_s.split(':'))

        for fmt in samp_fmt._fields:
            try:
                entry_type = self.rhandle.formats[fmt].type
                entry_num = self.rhandle.formats[fmt].num
            except KeyError:
                entry_num = None
                try:
                    entry_type = RESERVED_FORMAT[fmt]
                except KeyError:
                    entry_type = 'String'
            samp_fmt._types.append(entry_type)
            samp_fmt._nums.append(entry_num)
        return samp_fmt

    def create_call_data(self, samp_fmt):
        """Create CallData object to hold values of samples' FORMAT field

        :param samp_fmt: FORMAT string
        :return:
        """
        if samp_fmt not in self.rhandle._format_cache:
            self.rhandle._format_cache[samp_fmt] = self.create_empty_call_data(samp_fmt)
        samp_fmt = self.rhandle._format_cache[samp_fmt]
        return samp_fmt

    def create_calls(self, samples, samp_fmt, site):
        """Create a list of _Call object as it is found in vcf.model._Record.data attribute.

        Method is not very inovative, it repeats vcf.parser._parse_samples .
        :param samples: list of strings with samples' data (vcf columns 9+)
        :param samp_fmt: vcf FORMAT string
        :param site: _Record object
        :return: list of _Call objects
        """
        smp_fmt = self.create_call_data(samp_fmt)

        samp_data = []
        _map = self.rhandle._map
        nfields = len(smp_fmt._fields)

        for name, sample in zip(self.rhandle.samples, samples):

            sampdat = [None] * nfields

            for i, vals in enumerate(sample.split(':')):

                if smp_fmt._fields[i] == 'GT':
                    sampdat[i] = vals
                    continue
                elif not vals or vals == '.':
                    sampdat[i] = None
                    continue

                entry_num = smp_fmt._nums[i]
                entry_type = smp_fmt._types[i]

                # we don't need to split single entries
                if entry_num == 1 or ',' not in vals:

                    if entry_type == 'Integer':
                        try:
                            sampdat[i] = int(vals)
                        except ValueError:
                            sampdat[i] = float(vals)
                    elif entry_type == 'Float':
                        sampdat[i] = float(vals)
                    else:
                        sampdat[i] = vals

                    if entry_num != 1:
                        sampdat[i] = (sampdat[i])

                    continue

                vals = vals.split(',')

                if entry_type == 'Integer':
                    try:
                        sampdat[i] = _map(int, vals)
                    except ValueError:
                        sampdat[i] = _map(float, vals)
                elif entry_type == 'Float' or entry_type == 'Numeric':
                    sampdat[i] = _map(float, vals)
                else:
                    sampdat[i] = vals

            # create a call object
            call = _Call(site, name, smp_fmt(*sampdat))
            samp_data.append(call)

        return samp_data

    def add_header_line(self, meta_type, meta_id=None, number=None, data_type=None, description=None):
        """

        :param meta_type:
        :param meta_id:
        :param number:
        :param data_type:
        :param description:
        :return:
        """
        # TODO - dopln metodu na upravenie pola v ramci headeru
        raise NotImplemented

if __name__ == '__main__':
    pass

in_vcf = '/home/daniel/ielis/vcfkit/input/FH327.snp.vcf'
alt = Alternator(Reader(filename=in_vcf))
fmt = 'GT:AD:DP:PL'
r = alt.rhandle
