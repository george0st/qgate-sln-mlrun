

class BaseHelper:

    @property
    def prefix(self):
        raise NotImplemented()

    def create_helper_name(self, project_name, featureset_name):
        """Convert project name and featureset name to the name of helper (e.g. DB table name, kafka topic name, etc.).

        :param featureset_name:     Feature set name
        :return:                    The name of helper (DB table name, kafka topic name, etc.) with relevant prefix
        """
        return f"{self.prefix}{project_name}_{featureset_name}".replace('-', '_')

    def create_insert_data(self, project_name, featureset_name, drop_if_exist = False):
        raise NotImplemented()