'''

Aluna: Polyana Bezerra da Costa
Essa classe representa o Dataset do sistema, que guarda informações sobre o nome do banco de imagens, a descrição e URL
do mesmo (se houver) e o caminho onde as imagens que fazem parte do dataset estão armazenadas. Essa classe também guarda
todas as anotações que foram salvas, bem como todos os objetos do tipo "Face" e "Geral" (objeto geral, que não é Face nem
Texto) que fazem parte dessas anotações.

'''
class Dataset(object):
	_instance = None

	'''
	Foi usado o padrão de projeto Singleton para que só haja uma única instância da classe Dataset enquando o programa estiver em
	execução. Caso ainda não haja uma instância, ao chamar "Dataset()", uma instância é criada; caso contrário, a instância exis-
	tente é retornada.
	Esse padrão foi usado para que as anotações, faces e objetos já inclusos no Dataset não sejam perdidos durante a execução do
	código.
	'''
	def __new__(cls):
		flag =  False
		if cls._instance is None:
			print('Creating the Dataset object')
			cls._instance = super(Dataset, cls).__new__(cls)
			flag = True
		return cls._instance, flag
		
	
	def config(self, id, name, path):
		'''
		Esse método permite a atribuição de valores às principais variáveis presentes na classe Dataset
		'''
		self.id = id
		self.name = name
		self.url = ""
		self.description = ""
		self.path = path
		self.annotations = []
		self.faces = []
		self.objects = []
		self.fileNames = []
		
	def getId(self):
		'''
		Retorna o numero identificador deste Dataset
		'''
		return self.id

	def setId(self,id):
		'''
		Atribui um valor ao identificador deste Dataset
		'''
		self.id = id

	def getName(self):
		'''
		Retorna o nome identificador deste Dataset
		'''
		return self.name

	def setName(self,name):
		'''
		Atribui um nome ao Dataset
		'''
		self.name = name

	def setFilePath(self,filepath):
		'''
		Define o caminho onde as imagens usadas no Dataset serão armazenadas
		'''
		self.path = filepath

	def getFilePath(self):
		'''
		Retorna o caminho onde as imagens usadas no Dataset estão armazenadas
		'''
		return self.path

	def getListofFiles(self, path):
		'''
		Retorna o nome de todas as imagens usadas no Dataset
		'''
		from os import walk
		fileNames = next(walk(path), (None, None, []))[2]
		return fileNames

	def addFace(self,face):
		'''
		Adiciona um objeto do tipo "Face" ao vetor de Faces
		'''
		self.faces.append(face)

	def removeFace(self,face):
		'''
		Remove um objeto do tipo "Face" do vetor de Faces
		'''
		self.faces.pop(face)

	def getFaces(self):
		'''
		Retorna todos os objetos "Face" presentes nas anotações salvas nesse Dataset
		'''
		return self.faces

	def addObject(self,obj):
		'''
		Adiciona um objeto do tipo "Geral" ao vetor de Objetos
		'''
		self.objects.append(obj)

	def removeObject(self,obj):
		'''
		Remove um objeto do tipo "Geral" do vetor de Objetos
		'''
		self.objects.pop(obj)

	def getObjects(self):
		'''
		Retorna todos os objetos do tipo "Geral" presentes nas anotações salvas nesse Dataset
		'''
		return self.objects

	def addAnnotation(self,annotation):
		'''
		Adiciona uma anotação ao Dataset
		'''
		self.annotations.append(annotation)

	def removeAnnotation(self,annotation):
		'''
		Remove uma anotação do Dataset
		'''
		self.annotations.pop(annotation)

	def clearAllAnnotations(self):
		'''
		Remove todas as anotações do Dataset
		'''
		self.annotations = []

	def getAnnotations(self):
		'''
		Retorna todas as anotações do Dataset
		'''
		return self.annotations
