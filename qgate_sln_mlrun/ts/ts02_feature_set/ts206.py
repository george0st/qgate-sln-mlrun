"""
  TS206: Create feature set(s) & Ingest from Kafka source (one step)
"""
from qgate_sln_mlrun.ts.tsbase import TSBase
import mlrun
import mlrun.feature_store as fstore
from mlrun.data_types.data_types import ValueType
from mlrun.datastore.sources import KafkaSource
from qgate_sln_mlrun.ts.ts02_feature_set import ts201
import json
from qgate_sln_mlrun.helper.kafkahelper import KafkaHelper
import os
import glob


class TS206(TSBase):

    def __init__(self, solution):
        super().__init__(solution, self.__class__.__name__)
        self._kafka = KafkaHelper(self.setup)

    @property
    def desc(self) -> str:
        return "Create feature set(s) & Ingest from Kafka source (one step)"

    @property
    def long_desc(self):
        return ("Create feature set(s) & Ingest from Kafka source (one step, without save and load featureset)")

    def prj_exec(self, project_name):
        """ Create featuresets & ingest"""

        # It can be executed only in case that configuration is fine
        if not self._kafka.configured:
            return

        for featureset_name in self.get_featuresets(self.project_specs.get(project_name)):
            # Create topic only in case, that topic does not exist
            helper= self._kafka.create_helper(project_name, featureset_name)
            #if not self._kafka.helper_exist(helper):
            self._kafka.create_insert_data(helper, featureset_name,True)

            # create file with definition of vector
            source_file = os.path.join(os.getcwd(),
                                       self.setup.model_definition,
                                       "01-model",
                                       "02-feature-set",
                                       f"*-{featureset_name}.json")

            for file in glob.glob(source_file):
                # iterate cross all featureset definitions
                with open(file, "r") as json_file:
                    self._create_featureset_ingest(f'{project_name}/{featureset_name}', project_name, featureset_name, json_file)

    @TSBase.handler_testcase
    def _create_featureset_ingest(self, testcase_name, project_name, featureset_name, json_file):
        json_content = json.load(json_file)
        name, desc, lbls, kind = TSBase.get_json_header(json_content)

        if kind == "feature-set":

            # create feature set based on the logic in TS201
            ts= ts201.TS201(self._solution)
            featureset=ts.create_featureset_content(project_name, f"{self.name}-{name}", desc, json_content['spec'])


            # fstore.ingest(featureset,
            #               KafkaSource(brokers=self.setup.kafka,
            #                         topics=[self._kafka.create_helper(project_name, featureset_name)]),
            #               # overwrite=False,
            #               return_df=False,
            #               # infer_options=mlrun.data_types.data_types.InferOptions.Null)
            #               infer_options=mlrun.data_types.data_types.InferOptions.default())
