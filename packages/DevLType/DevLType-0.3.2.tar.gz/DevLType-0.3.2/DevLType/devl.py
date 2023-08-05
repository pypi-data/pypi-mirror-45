from . import OrderedDict,dumps

class DevLTypes(object):

	def to_dict(obj):
		if isinstance(obj, (list, tuple, set)):
			return type(obj)(to_dict(x) for x in obj if x is not None)
		elif isinstance(obj, dict):
			return type(obj)((to_dict(k), to_dict(v)) for k, v in obj.items() if k is not None and v is not None)
		else:
			return obj

	def default(self):
		return dumps(self, indent=4, default=self.to_json, ensure_ascii=False)

	def to_json(self):
		try:
			content = {i: getattr(self.__dict__, i) for i in self.__dict__}
			return to_dict(
				OrderedDict(
					[("_", "DevLGram." + self.__class__.__name__)]
					+ [i for i in content.items()]
					)
				)
		except AttributeError:
			return repr(self),'error'
