

class BaseHelper:

    @property
    def prefix(self):
        raise NotImplemented()

    def convert_featureset_name(self, featureset_name):
        """Convert featureset name to the name of helper (e.g. DB table name, kafka topic name, etc.).

        :param featureset_name:     Feature set name
        :return:                    The name of helper (DB table name, kafka topic name, etc.) with relevant prefix
        """
        return f"{self.prefix}{featureset_name}".replace('-', '_')

    def create_insert_data(self, featureset_name, drop_if_exist = False):
        raise NotImplemented()