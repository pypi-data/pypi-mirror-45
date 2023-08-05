from . import OrderedDict,dumps

class DevLTypes(object):

	def default(self):
		L = {}
		for key, value in self.__dict__.items():
			if self.__dict__[key] is not None and isinstance(value,(int,str,list,dict)):
				L[key] = value
			elif  self.__dict__[key] is None:
				pass
			elif:
				L[key] = value.__class__.__name__
		return '%s(%s)' % (self.__class__.__name__,dumps(L, indent=4, sort_keys=True))