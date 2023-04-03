import unittest

class TestProjects(unittest.TestCase):

    def setUp(self):
        self.aa=""

    def tearDown(self):
        self.aa=None

    def test_root(self):
        print("aa")

