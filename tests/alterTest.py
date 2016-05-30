import unittest
import alter
from vcf.model import _Call


class CreateCallTest(unittest.TestCase):
    def setUp(self):
        self.sample_id = 'CKOR11'
        self.GT = '0/1'
        self.AD = ['10', '34']
        self.call = alter.create_call(self.sample_id, GT=self.GT, AD=self.AD)

    def call_instance_test(self):
        """

        :return:
        """
        self.assertIsInstance(self.call, _Call, "Object is not type _Call")

    def call_params_test(self):
        self.assertEqual(self.call.GT, self.GT)
        self.assertEqual(self.call.AD, self.AD)


if __name__ == '__main__':
    unittest.main()
