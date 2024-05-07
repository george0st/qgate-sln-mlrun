

class BaseHelper:

    @property
    def prefix(self):
        return ""

    def convert_featureset_name(self, featureset_name):
        """Convert featureset name to the name of helper.

        :param featureset_name:     Feature set name
        :return:                    The name of helper (db table, kafka topic, etc.) with relevant prefix
        """
        return f"{self.prefix}{featureset_name}".replace('-', '_')