# -*- coding: utf-8 -*-
#
from boltons.iterutils import remap, default_enter, default_exit
#
class VarTransform:
	# public
	@staticmethod
	def outputs(data):

		def enter(path, key, value):
			print('enter=', path, key, value)
			return default_enter(path, key, value)

		def exit(path, key, old_parent, new_parent, new_items):
			print('exit=', path, key, old_parent,  new_parent, new_items)
			return default_exit(path, key, old_parent, new_parent, new_items)
		
		def visit(path, key, value):
			print('visit=', path, key, value)
			return False
		return remap(data, enter=enter, visit=visit, exit=exit)
		
		#return result
	# private
		
#
print(VarTransform.outputs({"a":1, "b":{'aa':11}, 'c':[{'bb':{'vvv':333,'hhh':888}}, {'jj':55}]}))