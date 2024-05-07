from qgate_sln_mlrun.ts.tsbase import TSBase
from qgate_sln_mlrun.ts.tshelper import TSHelper
from qgate_sln_mlrun.setup import Setup


class KafkaHelper():

    # Prefix of table with sources
    TOPIC_SOURCE_PREFIX = "tmp_"

    def __init__(self,setup: Setup):
        self._setup = setup