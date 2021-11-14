'''Common utility functions'''
import json


class CustomJSONEncoder(json.JSONEncoder):
    """
    Custom JSON encoder to convert class object to dictionary by stripping '_'
    """
    def default(self, o):
        return {k.lstrip('_'): v for k, v in vars(o).items()}


def convert_to_dict(obj):
    """
    Convert any class object to dictionary
    Args:
        obj: Any class object

    Returns: dictionary

    """
    return json.loads(json.dumps(obj, cls=CustomJSONEncoder))
