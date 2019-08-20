# -*- coding: utf-8 -*-
#
from XmlTransform  import XmlTransform
from FileSearch    import FileSearch
from SarBase       import SarBase
#
class SarFiles(SarBase):
#--------------------------------------------------------------------------------------------------
# public
#--------------------------------------------------------------------------------------------------
	def __init__(self, path):
		self.__path = path
	#
	def process(self):
		result = {}
		# find all arxml
		for f in self.__findFiles():
			# parse
			try:
				result[f] = self.__parseFile(f)
			except:
				pass
		return result
	#
#--------------------------------------------------------------------------------------------------
#private
#--------------------------------------------------------------------------------------------------
	def __parseFile(self, path):
		#
		result = {}
		with open(path) as fd:
			# xml to var
			result = XmlTransform.toVar(fd.read())
		#
		return result
	#
	def __findFiles(self):
		if isinstance(self.__path, list):
			return self.__path
		else:
			return FileSearch.find(self.__path, '.*\\.arxml$')
		#
	#
#