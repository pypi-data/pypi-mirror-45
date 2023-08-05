from . import OrderedDict,dumps

class DevLTypes(object):

	def default(self):
		L = {}
		for key, value in self.__dict__.items():
			if isinstance(value,object):
				value = value.__class__.__name__
			if self.__dict__[key] is not None:
				L[key] = value
		return '%s(%s)' % (self.__class__.__name__,dumps(L, indent=4, sort_keys=True))