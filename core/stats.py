cache = {}
loc_cache = {}

VCF_FIELD_TYPES = {'FILTER': 'filters', 'FORMAT': 'formats', 'INFO': 'infos'}
INV_VCF_FIELD_TYPES = {v: k for k, v in VCF_FIELD_TYPES.items()}


def get_instance(r_handle):
    if r_handle in cache:
        return cache[r_handle]
    else:
        cache[r_handle] = VcfStats(r_handle)
        return cache[r_handle]


class VcfStats(object):
    """

    """

    def __init__(self, reader_handle):
        # open VCF & parse header lines
        self.r_handle = reader_handle
        self.nominal, self.ordinal = self._parse_header()
        self.data = None

    def run(self, interest):
        assert isinstance(interest, list), "Fields must be passed in a list!"
        # TODO - sanity check - ci su zadane tagy definovane v VCF headeri
        self.data = {key: list() for key in interest}
        for record in self.r_handle:
            values = self._get_values(interest, record)
            [self.data[k].append(v) for k, v in values.items()]

            # TODO - analyse self.data!

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
                        "Problem parsing tag {} from {} field! The type is neither Integer nor String!".format(tag_id,
                                                                                                               k))
        return nominal, ordinal

    def _get_values(self, tags, record):
        loc = [self._localise(x) for x in tags]
        res = {t: self._get_value(t, l, record) for t, l in zip(tags, loc)}
        return res

    def _get_value(self, tag, loc, record, missing=None):
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


class StatsException(Exception):
    """Placeholder"""
    pass
