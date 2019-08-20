# -*- coding: utf-8 -*-
#
#
class TreeTransform:
	def __init__(self, key):
		self.__key = key
	# public
	def run(self, data):
		result = {}
		p = self.__next('', data, result)
		if p:
			result['@']=p
		return result
	# private
	def __next(self, tag,  doc, result):	
		data = None
		if isinstance(doc, dict):
			data={}
			data.update(self.__process(tag, doc, result))
		elif isinstance(doc, list):
			data=[]
			for d in doc:
				n = self.__next(tag, d, result)
				if n:
					data.append(n)
				#
			#
		else:
			data=doc
		#
		return data
	#
	def __process(self, tag, doc, result):
		props={}
		try:
			key = doc.pop(self.__key) 
			# update data
			data = {} 
			for k in doc:
				p = self.__next(k, doc[k], data)
				if p:
					props[k] = p
				#
			# update properties
			if props:
				data['@']=props
			# update tag
			if tag:
				data['$']=tag
			# update result
			result[key]=data
			# empty props
			return {}
		except:
			for k in doc:
				p=self.__next(k, doc[k], result)
				if p:
					props[k]=p
				#
			#
			return props
		#
	#	
#