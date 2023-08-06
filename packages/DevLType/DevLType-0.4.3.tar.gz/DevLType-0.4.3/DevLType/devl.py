from . import OrderedDict,dumps

class DevLTypes(object):

	def to_dict(self,obj):
		if isinstance(obj, (list, tuple, set)):
			return type(obj)(self.to_dict(x) for x in obj if x is not None)
		elif isinstance(obj, dict):
			return type(obj)((self.to_dict(k), self.to_dict(v)) for k, v in obj.items() if k is not None and v is not None)
		else:
			return obj

	def default(self):
		return dumps(self, indent=4, default=to_json, ensure_ascii=False)

def to_json(o:DevLTypes):
		try:
			content = {i: getattr(o, i) for i in o.__dict__}
			return o.to_dict(
				OrderedDict([i for i in content.items()]
				)
			)
		except AttributeError as e:
			return repr(o),f'{e}'
