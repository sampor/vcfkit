import os

from vcf import Reader
from . import util
from . import plot
from .writers import PdfPlotWriter

cache = {}
loc_cache = {}

VCF_FIELD_TYPES = {'FILTER': 'filters', 'FORMAT': 'formats', 'INFO': 'infos'}
INV_VCF_FIELD_TYPES = {v: k for k, v in VCF_FIELD_TYPES.items()}


class VcfStats(object):
    """

    """

    def __init__(self, vcf_path):
        # open VCF & parse header lines
        self.r_handle = Reader(filename=vcf_path)
        self.nominal, self.ordinal = self._parse_header()

    def get_data_for_tags(self, interest):
        assert isinstance(interest, list), "Fields must be passed in a list!"
        # check tag presence in VCF
        self.check_tags(interest)
        data = {key: list() for key in interest}
        for record in self.r_handle:
            values = self._get_values(interest, record)
            [data[k].append(v) for k, v in values.items()]
        return data

    def choose_plot(self, tag):
        if tag in self.nominal:
            return [plot.get_piechart]
        elif tag in self.ordinal:
            return [plot.get_boxplot, plot.get_cumulative_distribution]
        else:
            raise StatsException("Cannot decide which plot to use for tag {}!".format(tag))

    def _parse_header(self):
        """Classify fields from FILTER, INFO and FORMAT columns as nominal or ordinal.

        Decide using type of values described in header:
        Nominal -> String, Flag
        Ordinal -> Integer, Float
        :return: (list(nominal_fields), list(ordinal_fields))
        """
        nominal = []
        ordinal = []
        for k, v in VCF_FIELD_TYPES.items():
            tag_dict = getattr(self.r_handle, v)
            # tags is Ordered Dict, continue if empty
            if not tag_dict:
                continue
            for tag_id, tag_vals in tag_dict.items():
                try:
                    t = getattr(tag_vals, 'type')
                    if t == 'Integer':
                        ordinal.append(tag_id)
                    elif t == 'Float':
                        ordinal.append(tag_id)
                    elif t == 'String':
                        nominal.append(tag_id)
                    elif t == 'Flag':
                        nominal.append(tag_id)
                    else:
                        raise StatsException(
                            "Problem parsing tag {} from {} field! "
                            "The type is neither Integer nor String!".format(tag_id, k))
                except AttributeError:
                    util.eprint("Tag {} is neither ordinal or nominal. Skipping..".format(tag_id))

        return nominal, ordinal

    def _get_values(self, tags, record):
        """Return dictionary with tags and their values"""
        loc = [self._localise(x) for x in tags]
        res = {t: self._get_value(t, l, record) for t, l in zip(tags, loc)}
        return res

    def _get_value(self, tag, loc, record, missing=None):
        """Return tag value from _Record. Return missing if tag not present in _Record.
        :param tag: Tag string to be found
        :param loc: Place in VCF _Record (filters, formats, infos)
        :param record: VCF _Record object
        :param missing: Return this value if Tag is not present in _Record
        :return: Tag value or missing
        """
        if loc == 'infos':
            # Get dictionary with vcf INFO fields
            i = getattr(record, INV_VCF_FIELD_TYPES[loc])
            try:
                return i[tag]
            except KeyError:
                return missing
        elif loc == 'filters':
            # TODO - implememnt me ;)
            raise NotImplemented
        elif loc == 'formats':
            if len(record.samples) > 1:
                raise StatsException("Multisample VCFs are not yet supported!")
            # Get CallData object
            cd = record.samples[0].data
            try:
                return getattr(cd, tag)
            except AttributeError:
                return missing
        else:
            raise NotImplemented

    def _localise(self, tag):
        """Return attribute of Reader handle where the tag is localised.

        Attribute priority is in this order: formats > infos > filters
        :param tag: Tag string
        :return: Reader attribute string. E.g. 'infos'
        """

        if tag in loc_cache:
            return loc_cache[tag]
        else:
            priority = ['formats', 'infos', 'filters']
            for site in priority:
                od = getattr(self.r_handle, site)
                if tag in od.keys():
                    loc_cache[tag] = site
                    return loc_cache[tag]

            raise StatsException("This shouldn't happen!")

    def check_tags(self, tag_list):
        """Check tag presence in VCF file. Raise StatsException if a tag is not present in VCF."""
        # TODO - we may continue even if one tag is not present. Just leave it and process the others
        for t in tag_list:
            if not self._check_tag(t):
                raise StatsException("Tag {} is not present in VCF file!".format(t))
        return True

    def _check_tag(self, tag):
        if tag not in self.nominal + self.ordinal:
            return False
        return True


class VcfStatsRunner(object):
    def __init__(self, in_file, pdf_path):
        assert os.path.exists(in_file), "File {} does not exist!".format(in_file)
        self._in_file = in_file
        self._pdf_path = pdf_path

    def analyze_tags(self, tags):
        tg = parse_tags(tags)
        vs = VcfStats(self._in_file)
        data = vs.get_data_for_tags(tg)
        pdf_writer = PdfPlotWriter(self._pdf_path)
        for t in tg:
            # TODO - Create class for choosing plot type - based on VCF Header and tag
            cp = vs.choose_plot(t)
            # cp may be more methods
            figs = [p(data[t]) for p in cp]
            [pdf_writer.add_plot(fig) for fig in figs]

        pdf_writer.write_out()

    def get_data(self, tags):
        pass


def parse_tags(tag_string):
    separators = [',', ':']
    if ',' in tag_string and ':' in tag_string:
        raise StatsException("Tags cannot be separated both with comma & colon!")

    for sep in separators:
        if sep in tag_string:
            ts = tag_string.split(sep)
            return [t.strip() for t in ts]
    # separator is not present, probably single tag input string (e.g. 'GT')
    return [tag_string]


class StatsException(Exception):
    """Placeholder"""
    pass
