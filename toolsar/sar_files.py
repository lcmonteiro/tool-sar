# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------------------------
# dependencies
# -------------------------------------------------------------------------------------------------
from toolsar.xml_transform  import XmlTransform
from toolsar.file_search    import FileSearch
from toolsar.sar_base       import SarBase
# -------------------------------------------------------------------------------------------------
# Sar Files
# -------------------------------------------------------------------------------------------------
class SarFiles(SarBase):
# -------------------------------------------------------------------------------------------------
# public
# -------------------------------------------------------------------------------------------------
    # initialization
    # -------------------------------------------------------------------------
	def __init__(self, path):
		self.__path = path
	# ------------------------------------------------------------------------- 
    # process
    # -------------------------------------------------------------------------
	def __call__(self):
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
# -------------------------------------------------------------------------------------------------
# private
# -------------------------------------------------------------------------------------------------
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
			return file_search.find(self.__path, '.*\\.arxml$')
		#
	#
# -------------------------------------------------------------------------------------------------
# end
# -------------------------------------------------------------------------------------------------
