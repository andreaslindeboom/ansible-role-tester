import sys
import yaml

class YamlFileLoader:
    @classmethod
    def load_yaml(self, filepath):
        try:
            config = open(filepath, 'r')
        except OSError:
            print("File {} not found".format(filepath))
            sys.exit(1)

        try:
            parsed_yaml = yaml.load(config)
        except yaml.YAMLError as err:
            print("Yaml file could not be loaded:\n {}".format(err))
            sys.exit(1)

        return parsed_yaml

