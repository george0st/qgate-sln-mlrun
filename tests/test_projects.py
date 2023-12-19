import unittest
import main
import os


class TestProjects(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

        #os.chdir(os.path.dirname(os.getcwd()))

        # setup relevant path
        # prefix = "."
        # if not os.path.isfile(path.join(prefix, TestCaseBasic.INPUT_FILE)):
        #     prefix=".."

    @classmethod
    def tearDownClass(cls):
        pass

    def test_main(self):
        main.run_testing()

