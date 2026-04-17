import json


class _YamlLike:
    def safe_load(self, data):
        return {"data": data}

    def load(self, data, Loader=None):
        return {"data": data, "loader": Loader}


class SafeLoader:
    pass


yaml = _YamlLike()


def load_user_payload(user_data):
    obj1 = json.loads(user_data)
    obj2 = yaml.safe_load(user_data)
    obj3 = yaml.load(user_data, Loader=SafeLoader)
    return obj1, obj2, obj3
