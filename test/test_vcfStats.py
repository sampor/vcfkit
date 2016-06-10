import os
import unittest

from core.stats import get_instance_of_vcf_stats, StatsException, VcfStatsRunner
from vcf import Reader

fpath = 'files/XYZ123.vcf'


class TestVcfStats(unittest.TestCase):
    def setUp(self):
        self.reader = Reader(filename=fpath)
        self.vs = get_instance_of_vcf_stats(self.reader)
        self.cg_record = next(self.reader)
        for x in range(3):
            # Throw away uninteresting VCF records
            next(self.reader)
        self.ilm_record = next(self.reader)

    def tearDown(self):
        del (self.reader, self.vs, self.cg_record, self.ilm_record)

    def test__parse_header(self):
        """ The method gets called in VcfStats constructor so the self.vs object is being tested here"""
        self.assertEqual(self.vs.r_handle.samples[0], 'XYZ123')
        self.assertEqual(len(self.vs.nominal), 7)
        self.assertEqual(self.vs.nominal.count('GT'), 1)
        self.assertEqual(len(self.vs.ordinal), 30)
        self.assertEqual(self.vs.ordinal.count('GL'), 1)

    def test_run(self):
        interesting_fields = ['GT', 'DP', 'GQ', 'Dels']
        bad_input = 'GT:DP:GQ'
        self.assertRaises(AssertionError, self.vs.run, bad_input)

    def test__localise_good_input(self):
        gt_sites = self.vs._localise('GT')
        dp_sites = self.vs._localise('DP')
        af_sites = self.vs._localise('AF')
        self.assertEqual(gt_sites, 'formats')
        self.assertEqual(dp_sites, 'formats')  # formats has priority over infos, where the tag is also localised
        self.assertEqual(af_sites, 'infos')

    def test__localise_bad_input(self):
        self.assertRaises(StatsException, self.vs._localise, 'EVIL')

    @unittest.skip
    def test__get_values(self):
        interesting_fields = ['GT', 'DP', 'GQ', 'Dels']
        final = {'GT': '1/1', 'DP': 29, 'GQ': 99, 'Dels': 0.00}
        result = self.vs._get_values(interesting_fields, self.ilm_record)
        self.assertTrue(all([final[k] == result[k] for k in final.keys()]))

    def test__get_value(self):
        gt_formats = '0/1'
        gt = self.vs._get_value('GT', 'formats', self.ilm_record)
        self.assertEqual(gt, gt_formats)

        dels_infos = 0.00
        dels = self.vs._get_value('Dels', 'infos', self.ilm_record)
        self.assertEqual(dels, dels_infos)

        evil = self.vs._get_value('FOO', 'infos', self.ilm_record, missing='BAR')
        self.assertEqual(evil, 'BAR')


class TestVcfStatsRunner(unittest.TestCase):
    """

    """

    def setUp(self):
        """

        :return:
        """
        self.infile = fpath
        self.out_path = 'files/StatsRunner.pdf'
        if os.path.exists(self.out_path):
            os.remove(self.out_path)
        self.vsr = VcfStatsRunner(self.infile, self.out_path)

    def test_vsr_init(self):
        bad_in_path = 'files/EvilUnrealName.vcf'
        self.failUnlessRaises(AssertionError, VcfStatsRunner, bad_in_path, self.out_path)

    def test__parse_tags__separators(self):
        """Test good, faked good and bad input, values separated by ':' & ','"""
        good_tags_colon = 'GT:DP:GQ'
        good_tags_comma = 'GT,DP, GQ'
        res = ['GT', 'DP', 'GQ']
        other_tags_colon = 'GT:DP'
        other_res = ['DP', 'GT']
        self.assertListEqual(res, self.vsr._parse_tags(good_tags_colon), "Error parsing ':'separated values!")
        self.assertListEqual(res, self.vsr._parse_tags(good_tags_comma), "Error parsing ','separated values!")
        self.assertListEqual(other_res, self.vsr._parse_tags(other_tags_colon), "Error parsing ':'separated values!")

    def test__parse_tags_exceptions(self):
        """"""
        bad_sep = 'GT:DP,GQ'
        self.assertRaises(StatsException, self.vsr._parse_tags, bad_sep)

if __name__ == '__main__':
    unittest.main()
