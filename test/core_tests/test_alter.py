import unittest

import core.alter as alter

try:
    from vcf.parser import Reader
    from vcf.model import _Call
except ImportError:
    raise Exception("PyVCF is not installed. Try '$ sudo pip3 install pyvcf'")


class TestAlternator(unittest.TestCase):
    def setUp(self):
        self.alternator = alter.Alternator(Reader(filename='core_tests/files/XYZ123.vcf'))
        self.one_hom = next(self.alternator.rhandle)
        self.x_het = next(self.alternator.rhandle)
        self.x_monoploid = next(self.alternator.rhandle)
        self.y_monoploid = next(self.alternator.rhandle)
        self.fmt_string = self.x_het.FORMAT

    def test_create_empty_call_data(self):
        ecd = self.alternator.create_empty_call_data(self.fmt_string)
        self.assertEqual(ecd._fields[0], 'GT')
        self.assertEqual(ecd._types[0], 'String')
        self.assertEqual(ecd._types[-1], 'Integer')
        self.assertEqual(ecd._nums[0], 1)
        self.assertEqual(ecd._nums[-2], 2)
        self.assertIsInstance(ecd.AD, property)

    def test_create_call_data(self):
        cd = self.alternator.create_call_data(self.fmt_string)
        self.assertEqual(cd._fields[0], 'GT')
        self.assertEqual(cd._types[-1], 'Integer')
        self.assertEqual(cd._nums[-2], 2)
        self.assertIsInstance(cd.DP, property)

    def test_create_calls(self):
        sample_data = '1/0:.:PASS:433:470,433:470,433:41,44:-470,0,-433:-41,0,-44:48:25,23:23'
        cs = self.alternator.create_calls([sample_data], self.fmt_string, self.x_het)
        self.assertIsInstance(cs, list)
        self.assertIsInstance(cs[0], _Call)
        self.assertEqual(cs[0].data.GT, '1/0')
        self.assertEqual(cs[0].sample, 'XYZ123')

    if __name__ == '__main__':
        unittest.main()
