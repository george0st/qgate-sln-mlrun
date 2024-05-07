from qgate_sln_mlrun.ts.tsbase import TSBase
from qgate_sln_mlrun.ts.tshelper import TSHelper
from qgate_sln_mlrun.setup import Setup


class KafkaHelper():

    # Prefix of table with sources
    TOPIC_SOURCE_PREFIX = "tmp_"

    def __init__(self,setup: Setup):
        self._setup = setup

    @property
    def setup(self) -> Setup:
        return self._setup

    @property
    def configured(self):
        """Return None if not configured or connection string (based on setting QGATE_MYSQL in *.env file)."""
        return self.setup.kafka

    def create_insert_data(self, featureset_name, drop_if_exist = False):
        """Create table and insert data"""

        return