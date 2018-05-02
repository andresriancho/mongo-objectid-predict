import unittest

from mongo_objectid_predict.object_id import ObjectId


class TestObjectId(unittest.TestCase):

    SAMPLE = '5ae9bcaa2c144b9def01ec3e'

    def test_parse_str(self):
        o = ObjectId(self.SAMPLE)
        self.assertEqual(str(o), self.SAMPLE)

    def test_looks_like(self):
        self.assertTrue(ObjectId.looks_like(self.SAMPLE))
