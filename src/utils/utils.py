import json


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        return {k.lstrip('_'): v for k, v in vars(o).items()}


def convert_to_dict(obj):
    return json.loads(json.dumps(obj, cls=CustomJSONEncoder))
