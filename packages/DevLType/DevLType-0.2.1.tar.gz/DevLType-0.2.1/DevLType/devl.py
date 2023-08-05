from . import OrderedDict,dumps

class DevLTypes:

	def __init__(self):
		pass

	def __str__(self):
		return dumps(self, indent=4, default=default, ensure_ascii=False)

	def __getitem__(self, item):
		return getattr(self, item)

def DevL_None(obj):
    if isinstance(obj, (list, tuple, set)):
        return type(obj)(DevL_None(x) for x in obj if x is not None)
    elif isinstance(obj, dict):
        return type(obj)((DevL_None(k), DevL_None(v)) for k, v in obj.items() if k is not None and v is not None)
    else:
        return obj


def default(o:DevLType):
    try:
        content = {i: getattr(o, i) for i in o.__slots__}

        return DevL_None(
            OrderedDict(
                [("_",o.__class__.__name__)]
                + [i for i in content.items()]
            )
        )
    except AttributeError:
        return repr(o)