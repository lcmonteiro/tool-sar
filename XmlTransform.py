# -*- coding: utf-8 -*-
#
import re 
#
from xml.etree.ElementTree import fromstring
from collections import Counter
#
class XmlTransform:
#public
	@staticmethod
	def toVar(data):
		return XmlTransform.__toVar(
			fromstring(re.sub(
				'xsi:schemaLocation="[^"]+"', '', re.sub(' xmlns="[^"]+"', '', data, count=1), count=1)
			)
		)
#private
	@staticmethod
	def __toVar(root):
		'''Convert etree.Element into a dictionary'''
		value = dict()
		# process children
		children = [node for node in root if isinstance(node.tag, str)]
		# process attributs
		attrs = dict() 
		for attr, attrval in root.attrib.items():
			attrs[attr] = attrval
		if attrs:
			value['@'] = attrs
		# process text 
		if root.text:
			text = root.text.strip()
			if text:
				if len(children) == len(root.attrib) == 0:
					value = text
				else:
					value['#'] = text
		# process children
		count = Counter(child.tag for child in children)
		for child in children:
			if count[child.tag] == 1:
				value.update(XmlTransform.__toVar(child))
			else:
				result = value.setdefault(child.tag, list())
				result += XmlTransform.__toVar(child).values()
		return dict([(root.tag, value)])
	#
#
if __name__ == '__main__':    
    #
    with open("data/Dlog_ext_interfaces.arxml") as fd:
	    # xml to var
        print(XmlTransform.toVar(fd.read()))
    #
#