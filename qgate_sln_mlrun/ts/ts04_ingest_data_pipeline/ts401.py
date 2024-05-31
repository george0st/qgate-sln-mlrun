"""
  TS401: Ingest data & pipeline (Preview mode)
"""

from qgate_sln_mlrun.ts.tsbase import TSBase
from qgate_sln_mlrun.setup import Setup
import mlrun.feature_store as fstore
import pandas as pd
import glob
import os


class TS401(TSBase):

    def __init__(self, solution):
        super().__init__(solution, self.__class__.__name__)

    @property
    def desc(self) -> str:
        return "Ingest data & pipeline (Preview mode)"

    @property
    def long_desc(self):
        return "Ingest data & pipeline (Preview mode) from DataFrame Source"

    def prj_exec(self, project_name):
        """Data ingest"""

        pipelines = None
        if self.test_setting.get('pipeline'):
            if self.test_setting_pipeline.get('featuresets'):
                pipelines = self.test_setting_pipeline['featuresets']

        if pipelines:
            for featureset_name in self.get_featuresets(self.project_specs.get(project_name)):
                # processing only feature sets with pipelines
                if featureset_name in pipelines:
                    # create possible file for load
                    source_file = os.path.join(os.getcwd(),
                                               self.setup.model_definition,
                                               "02-data",
                                               self.setup.dataset_name,
                                               f"*-{featureset_name}.csv.gz")

                    # check existing data set
                    for file in glob.glob(source_file):
                        self._ingest_data(f"{project_name}/{featureset_name}", project_name, featureset_name, file)

    @TSBase.handler_testcase
    def _ingest_data(self, testcase_name, project_name, featureset_name, file):
        # get existing feature set (feature set have to be created in previous test scenario)
        featureset = fstore.get_feature_set(f"{project_name}/{featureset_name}")
        graph = featureset.graph

        # add pipelines
        setting=self.test_setting_pipeline['tests'][featureset_name]
        if setting:
            # add steps
            if setting["filter"]:
                graph.add_step("storey.Filter", name="filter", _fn=f"{setting['filter']}")
            if setting["extend"]:
                graph.add_step("storey.Extend",
                              name="extend",
                              _fn=f"{setting['filter']}")

        featureset.save()

        # ingest data with bundl/chunk
        for data_frm in pd.read_csv(file,
                                    sep=self.setup.csv_separator,
                                    header="infer",
                                    decimal=self.setup.csv_decimal,
                                    compression="gzip",
                                    encoding="utf-8",
                                    chunksize=Setup.MIN_BUNDLE):
            featureset.preview(data_frm)

