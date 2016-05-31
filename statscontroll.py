from core.stats import get_instance
from vcf import Reader

fpath = 'test/files/XYZ123.vcf'
tags = ['GT', 'DP', 'GQ', 'Dels', 'FT']

r = Reader(filename=fpath)
vs = get_instance(r)
vs.run(tags)

print('Finish!')
#
# cg_record = next(r)
# for x in range(3):
#     # Throw away uninteresting VCF records
#     next(r)
# ilm_record = next(r)
# vs._get_values(tags, ilm_record)
