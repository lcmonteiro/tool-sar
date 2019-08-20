# -*- coding: utf-8 -*-
#
from os import walk
from os import sep
from re import match
#
#
class FileSearch:
	# public
	@staticmethod
	def find(path, pattern):
		result = []
		for root, f, files in walk(path):
			for f in [root + sep + f for f in files if match(pattern, f)]:
				result.append(f)
			#
		#
		return result
	#
#