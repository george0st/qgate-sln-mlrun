

class BaseHelper:

    @property
    def prefix(self):
        raise NotImplemented()

    def create_helper(self, project_name, featureset_name) -> str:
        """Convert project name and featureset name to the name of helper (e.g. DB table name, kafka topic name, etc.).

        :param project_name:        project name
        :param featureset_name:     Feature set name
        :return:                    The name of helper (DB table name, kafka topic name, etc.) with relevant prefix
        """
        return f"{self.prefix}{project_name}_{featureset_name}".replace('-', '_')

    def create_insert_data(self, helper, featureset_name, drop_if_exist = False):
        raise NotImplemented()

    def helper_exist(self, helper) -> bool:
        raise NotImplemented()

    def remove_helper(self, start_with):
        raise NotImplemented()