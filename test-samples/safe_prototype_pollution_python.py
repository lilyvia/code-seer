import yaml

class SafePrototypePollutionPython:
    ALLOWED_KEYS = {'name', 'email', 'age'}

    def safe_setattr(self, obj, key, value):
        if key in self.ALLOWED_KEYS:
            setattr(obj, key, value)

    def safe_yaml_load(self, user_input):
        return yaml.safe_load(user_input)
