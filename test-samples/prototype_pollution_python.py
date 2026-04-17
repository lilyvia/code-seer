import pickle
import yaml

class PrototypePollutionPython:
    def vulnerable_setattr(self, obj, user_key, user_value):
        setattr(obj, user_key, user_value)

    def vulnerable_pickle_loads(self, user_input):
        return pickle.loads(user_input)

    def vulnerable_yaml_load(self, user_input):
        return yaml.load(user_input, Loader=yaml.Loader)
