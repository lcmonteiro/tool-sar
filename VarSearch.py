# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------------------------
# dependencies
# -------------------------------------------------------------------------------------------------
from re import match as re_match
# -------------------------------------------------------------------------------------------------
# Var Search
# -------------------------------------------------------------------------------------------------
class VarSearch:
	#----------------------------------------------------------------------------------------------
	# public
	#----------------------------------------------------------------------------------------------
	@staticmethod
	def contains(pattern, doc):
		try:
			VarSearch.__contains(pattern, doc)
			return True
		except Exception as e:
			return False		
		#
	@staticmethod
	def match(pattern, doc):
		try:
			VarSearch.__assert(pattern, doc)
			return True
		except Exception as e:
			return False		
		#
	#----------------------------------------------------------------------------------------------
	# private
	# ---------------------------------------------------------------------------------------------
	@staticmethod
	def __assert(pattern, doc):
		if isinstance(doc, dict):
			for k in pattern:
				VarSearch.__assert(pattern[k], doc[k])
			#
		elif isinstance(doc, list):
			for d in doc:
				VarSearch.__assert(pattern, d)
			#
		else:
			if not re_match(pattern, doc):
				raise AssertionError()
			#
		#
	#	
	@staticmethod
	def __contains(pattern, doc):
		def __find(p, d):
			for k in d:
				if re_match(p, k):
					return k
				#
			raise AssertionError()
		#
		if isinstance(doc, dict):
			if isinstance(pattern, dict):
				for p in pattern:
					VarSearch.__contains(pattern[p], doc[__find(p, doc)])
			elif isinstance(p, list):
				for p in pattern:
					VarSearch.__contains({'.*':'.*'}, doc[__find(p, doc)])
			else:
				VarSearch.__contains({'.*':'.*'}, doc[__find(pattern, doc)])
		elif isinstance(doc, list):
			for d in doc:
				VarSearch.__contains(pattern, d)
			#
		else:
			if not re_match(pattern, doc):	
				raise AssertionError()
			#
		#
	#	
# -------------------------------------------------------------------------------------------------
# main
# -------------------------------------------------------------------------------------------------
if __name__ == '__main__':
	print(VarSearch.contains(
		{'.': {'.*':'.'}, '@': {'DEST': '.*'}}, 
		[	{'@': {'DEST': 'TRACEABLE'}, '#': 'DK_T3_1917'}, 
			{'@': {'DEST': 'TRACEABLE'}, '#': 'FZM_SC_SYS_PA_332'}, 
			{'@': {'DEST': 'TRACEABLE'}, '#': 'FZM_SC_SYS_PA_173'}, 
			{'@': {'DEST': 'TRACEABLE'}, '#': 'FZM_SC_SYS_PA_333'}]))
# -------------------------------------------------------------------------------------------------
# end
# -------------------------------------------------------------------------------------------------