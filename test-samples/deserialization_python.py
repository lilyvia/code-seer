class _PickleLike:
    def loads(self, data):
        return data


class _DillLike:
    def loads(self, data):
        return data


class _YamlLike:
    def load(self, data):
        return data


pickle = _PickleLike()
dill = _DillLike()
yaml = _YamlLike()


def load_user_payload(user_data):
    obj1 = pickle.loads(user_data)
    obj2 = yaml.load(user_data)
    obj3 = dill.loads(user_data)
    return obj1, obj2, obj3
