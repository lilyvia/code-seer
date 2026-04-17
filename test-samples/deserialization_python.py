class _PickleLike:
    def loads(self, data):
        return data

    def load(self, stream):
        return stream


class _DillLike:
    def loads(self, data):
        return data

    def load(self, stream):
        return stream


class _YamlLike:
    def load(self, data):
        return data


class _MarshalLike:
    def loads(self, data):
        return data

    def load(self, stream):
        return stream


class _JsonpickleLike:
    def decode(self, data):
        return data


pickle = _PickleLike()
dill = _DillLike()
yaml = _YamlLike()
marshal = _MarshalLike()
jsonpickle = _JsonpickleLike()


def load_user_payload(user_data):
    obj1 = pickle.loads(user_data)
    obj2 = yaml.load(user_data)
    obj3 = dill.loads(user_data)
    obj4 = marshal.loads(user_data)
    obj5 = jsonpickle.decode(user_data)
    obj6 = pickle.load(user_data)
    obj7 = dill.load(user_data)
    obj8 = marshal.load(user_data)
    return obj1, obj2, obj3, obj4, obj5, obj6, obj7, obj8
