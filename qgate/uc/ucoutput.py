import os


class UCOutput:
    """
    Management reports/outputs from use cases
    """

    def __init__(self, output_dir: str):

        self._output_dir=output_dir
        if not os.path.exists(self._output_dir):
            os.makedirs(self._output_dir)

        self._file = open(os.path.join(self._output_dir, "qgate-sln-mlrun.txt"), 'w+t')

    def __del__(self):
        self._file.close()

    def _headr(self):
        pass

    def output(self, uc_name, *args, **kwargs):
        self._file.write(uc_name + str.format(args, kwargs) + '\n')


