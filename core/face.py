from core.object import Object
from PIL import Image

'''
Essa classe contém todas as informações dos objetos do tipo "Face", que sao usadas como elementos na classe AnnotationPart.
Um objeto do tipo Face guarda informações sobre a imagem em que aquela face foi anotada e a região da imagem onde a referida
face está.
Por herdar da classe Object, essa classe também guarda informação sobre a "label" ou "tag" dessa face.
'''

class Face(Object):
	def __init__(self, id, value, file, bbox):
		super().__init__(id, value)
		self.associatedFile = file
		self.boundingBox = bbox

	'''
	Retorna somente a região da imagem onde a face está
	'''
	def getFacePicture(self):
		im = Image.open(self.associatedFile)
		im1 = im.crop((self.boundingBox.x, self.boundingBox.y, self.boundingBox.x+self.boundingBox.width, 
		self.boundingBox.y+self.boundingBox.height))
		return im1