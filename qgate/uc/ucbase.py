
from dotenv import dotenv_values

class UCBase:

    def __init__(self, environment, name):
        self._env=environment
        self._label=name
        self._config = self.load_env()

    @property
    def env(self):
        return self._env
    @property
    def label(self):
        return self._label

    @property
    def config(self):
        return self._config

    @staticmethod
    def str2bool(v):
        return v.lower() in ("yes", "true", "t", "1")

    @staticmethod
    def str2array(v):
        bulks = []
        for itm in v.split('|'):
            sub_itm = itm.split(',')
            if len(sub_itm)==2:
                bulk = [int(sub_itm[0]), int(sub_itm[1])]
            elif len(sub_itm)==3:
                bulk = [int(sub_itm[0]), int(sub_itm[1]), str(sub_itm[2]).strip()]
            else:
                bulk = []
            bulks.append(bulk)
        return bulks

    def load_env(self):

        pass
        # # load .env
        # perfsetup = dotenv_values(f"perfsetup-{self.env}.env")
        #
        # # replace global keys based on specific keys
        # lbl=f"{self.label}_"
        # for key in perfsetup.keys():
        #     if key.lower().startswith(lbl):
        #         extract=key[len(lbl):]
        #         perfsetup[extract]=perfsetup[key]
        # return perfsetup

