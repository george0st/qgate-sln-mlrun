import unittest
import main
import os


class TestProjects(unittest.TestCase):

    INPUT_FILE = "qgate_sln_mlrun-sln-mlrun.env"

    @classmethod
    def setUpClass(cls):

        #os.chdir(os.path.dirname(os.getcwd()))

        # setup relevant path
        if not os.path.isfile(os.path.join(".", TestProjects.INPUT_FILE)):
            os.chdir(os.path.dirname(os.getcwd()))


    @classmethod
    def tearDownClass(cls):
        pass

    def test_main(self):
        main.run_testing()

