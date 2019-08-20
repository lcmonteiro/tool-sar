# -*- coding: utf-8 -*-
#
from boltons.iterutils import remap, default_enter, default_exit
from VarSearch         import VarSearch
from Log               import Log
from SarBase           import SarBase
#
class SarTransform(SarBase):
	#
	#----------------------------------------------------------------------------------------------
	# public
	#----------------------------------------------------------------------------------------------
	#
	@staticmethod
	def prepare(data):
		data = SarTransform.__compress(data)
		data = SarTransform.__outputs(data)
		return data

	# 
	@staticmethod
	def insert(data, new):
		for d in new:
			if d in data:
				if data[d][SarBase.TYPE] != new[d][SarBase.TYPE]:
					Log.warning(
						"ObjectConflit = %s (%s != %s)"%(d,data[d][TYPE],new[d][TYPE])
					)
				#
			else:
				data[d] = new[d]
			#
		#
		return data
	#--------------------------------------------------------------------------
	# link output to input
	#--------------------------------------------------------------------------
	@staticmethod
	def link(data):
		# 
		def update(link, value):
			if SarBase.ILINK in link:
				link[SarBase.ILINK].update(value)
			else:
				link.update({SarBase.ILINK:value})
			#
		#
		for k in data:
			def visit(path, key, value):
				if key is SarBase.OLINK:
					for l in value:
						try:
							update(data[l], {k:data[k][SarBase.TYPE]})
						except:
							Log.warning("LinkNotFound = %s ( %s )"%(l, data[k][SarBase.TYPE]))
						#
					#
				#
				return True;
			#
			remap(data[k], visit=visit)
		#
		return data
	#
	#--------------------------------------------------------------------------
	# split to nodes and links 
	#--------------------------------------------------------------------------
	def split(data):
		nodes = []
		links = []
		#
		for d in data:
			nodes.append({
				'id': d,
				'type': data[d][SarBase.TYPE],
				'property': data[d][SarBase.PROPERTY]
			})
			#
			for t in [SarBase.CHILDREN, SarBase.OLINK]:
				try:
					for o in data[d][t]:
						if o in data:
							links.append(
								{'source' : d, 'target' : o, 'type' : t}
							)
						#
					#
				except:
					pass
				#
			#
		#
		return { 'nodes': nodes, 'links': links}
	#
	#----------------------------------------------------------------------------------------------
	# private
	#----------------------------------------------------------------------------------------------
	#
	@staticmethod
	def __outputs(data):
		#
		def update(link, value):
			if SarBase.OLINK in data[k]:
				link[SarBase.OLINK].update(value)
			else:
				link.update({SarBase.OLINK:value})
			#
		#
		for k in data:
			def visit(path, key, value):
				if VarSearch.match({'#':'^/.*','@':{'DEST':'.*'}}, value):
					if isinstance(value, list):
						links = {}
						for v in value:
							links.update({v['#']:v['@']['DEST']})
						#
						update(data[k], links)
					else:
						update(data[k], {value['#']:value['@']['DEST']})
					#
				return True
			#
			remap(data[k], visit=visit)
		#
		return data
	#
	@staticmethod
	def __compress(data):
		result={}
		def enter(path, key, value):
			curr = SarTransform.__path(path, key)
			if curr is '/' :
				result[curr] = {
					SarBase.PROPERTY : value.pop('@', {}),
					SarBase.TYPE     : value.pop('$', {})
				}
			else:
				prev = SarTransform.__path(path, None)
				#
				result[prev].update({
					SarBase.CHILDREN:{curr : value['$']}
				})
				#
				result[curr] = {
					SarBase.PROPERTY : value.pop('@', {}),
					SarBase.TYPE     : value.pop('$', {}),
					SarBase.PARENT   : {prev:result[prev]['$']}
				}
			#
			return default_enter(path, key, value)
		#
		remap(data, enter=enter)
		return result 
	#
	@staticmethod
	def __path(path, key):
		return '/'+'/'.join(filter(None, list(path) + [key]))
	#	
#