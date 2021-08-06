class AnnotationPart():
	'''
	Essa classe guarda informações sobre cada elemento (ou parte) de uma anotação, sendo composta de um objeto do tipo Box que
	representa a região onde o objeto anotado está e uma instância do objeto em si (Object, Text ou Face).
	'''
	def __init__(self, id, bbox, objeto):
		self.id = id
		self.boundingBox = bbox
		self.object = objeto

	def getId(self):
		return self.id

	def setId(self, id):
		self.id = id

	def getBBox(self):
		return self.boundingBox

	def addBBox(self,bbox):
		self.boundingBox = bbox

	def addObject(self,obj):
		self.object = obj