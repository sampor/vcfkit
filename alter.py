from vcf.model import make_calldata_tuple


def create_call(sample_id, **kwargs):
    keys = list(kwargs.keys())
    nt = make_calldata_tuple(keys)


if __name__ == '__main__':
    pass
