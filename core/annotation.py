class Annotation:
	'''
	A classe Annotation guarda todos os dados anotados numa mesma imagem. Essa classe recebe como parâmetro um identificador para
	a anotação daquela imagem, o nome da imagem em si e uma instância do dataset em que aquela anotação será incluída. A classe
	ainda tem como parâmetro a variável "isFake", que diz se a imagem apresenta conteúdo falso ou não, além da variável "elements",
	um vetor que guarda AnnotationParts - informações sobre os objetos anotados e a região em que eles se encontram.
	'''
	def __init__(self, id, fileName, dataset):
		self.id = id
		self.fileName = fileName
		self.dataset = dataset
		self.isFake = False
		self.elements = []

	def getId(self):
		return self.id

	def setId(self,id):
		self.id = id

	def addElement(self,annotationPart):
		self.elements.append(annotationPart)

	def removeElement(self,annotationPart):
		self.elements.pop(annotationPart)
	
	def setFake(self,fake):
		self.isFake = fake

	def getElements(self):
		return self.elements