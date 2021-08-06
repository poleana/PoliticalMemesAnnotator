from core.dataset import Dataset
from core.annotation import Annotation
from core.annotationPart import AnnotationPart
from core.object import Object
from core.text import Text
from core.face import Face
from core.box import Box
import json
import os
import random

'''

Aluna: Polyana Bezerra da Costa
Essa classe representa o gerenciador de arquivos json do sistema, responsável por gerar os .jsons referentes às anotações,
escrevê-los ou apagáa-los do disco, bem como ler um arquivo .json e gerar o objeto do tipo Annotation correspondente.
A classe recebe como parâmetro o local onde os arquivos .json serão armazenados e uma instância de Dataset, que contém todas
as informações sobre as anotações salvas.

'''

class jsonFileManager(object):

	_instance = None
	'''
	Foi usado o padrão de projeto Singleton para que só haja uma única instância da classe jsonFileManager enquando o programa
	estiver em execução. Caso ainda não haja uma instância, ao chamar "jsonFileManager()", uma instância é criada; caso contrário,
	a instância existente é retornada.
	Esse padrão foi usado para que as anotações, o caminho onde os arquivos json são temporariamente salvos e os nomes dos arquivos
	.json não sejam perdidos durante atualizações.
	'''
	def __new__(cls):
		flag =  False
		if cls._instance is None:
			print('Creating the JsonFileManager object')
			cls._instance = super(jsonFileManager, cls).__new__(cls)
			flag = True
		return cls._instance, flag
	
	def config(self, path, dataset):
		self.path = path
		self.filenames = []
		self.annotations = []
		self.dataset = dataset

	def getObjectType(self,obj):
		'''
		Recebe um objeto da superclasse Objet e retorna qual é seu tipo específico
		'''
		if isinstance(obj, Face):
			return "face"
		elif isinstance(obj, Text):
			return "texto"
		else:
			return "geral"

	

	def fileWriter(self,annotation):
		'''
		Recebe um objeto do tipo Annotation e escreve o conteúdo da mesma num arquivo .json, salvando-o no disco
		'''
		
		data = {}
		data["filename"] = annotation.fileName
		data["path"] = annotation.dataset.path
		data["source"] = {
			'database': annotation.dataset.name,
			'url': annotation.dataset.url
		}
		data["isFake"] = annotation.isFake,
		data["annotations"] = []
		for element in annotation.elements:
			data["annotations"].append({
				"id" : element.object.id,
				"type": self.getObjectType(element.object),
				"value": element.object.value,
				"coordinates": {
					"x": element.boundingBox.x,
					"y":  element.boundingBox.y,
					"width":  element.boundingBox.width,
					"height":  element.boundingBox.height,
					"color": element.boundingBox.color
				}
			})

		jsonName = os.path.splitext(data["filename"])[0] + ".json"
		
		with open(self.path + jsonName, 'w') as outfile:
			json.dump(data, outfile)
		self.filenames.append(jsonName)

		return jsonName

	def writeAll(self,annotations):
		'''
		Escreve arquivos .json para todas as anotações presentes no dataset
		'''
		for a in annotations:
			self.filenames.append(self.fileWriter(a))

	def deleteJsonFile(self,filename):
		'''
		Apaga do disco o arquivo .json especificado
		'''
		os.remove(self.path+filename)
		self.filenames.pop(filename)

	def jsonToAnnotation(self,filename):
		'''
		Carrega um arquivo .json do disco e retorna um objeto do tipo Annotation com as informações salvas no .json
		'''
		annotation = None
		filePath = self.path + filename

		with open(filePath) as json_file:
			data = json.load(json_file)
			annotation = Annotation(self.filenames.index(filename), data["filename"], self.dataset)
			countAnnotations = 0

			for a in data["annotations"]:
				bbox = Box(a["coordinates"]["x"],a["coordinates"]["y"],a["coordinates"]["width"],a["coordinates"]["height"],a["coordinates"]["color"])
				object =   None
				
				if a["type"] == "texto":
					object = Text(a["id"], a["value"],"")
				elif a["type"] == "face":
					object = Face(a["id"], a["value"], data["filename"], bbox)
				else:
					object = Object(a["id"], a["value"])

				annotation.addElement(AnnotationPart(countAnnotations, bbox, object))
				countAnnotations += 1

		return annotation

	def getAllJson(self):
		'''
		Para cada arquivo .json salvo, gera o objeto do tipo Annotation correspondente, retornando uma lista de Annotations
		'''
		annotationList = []
		
		filenames = self.dataset.getListofFiles(self.path)
		for fname in filenames:
			annotationList.append(self.jsonToAnnotation(fname))
		self.filenames = filenames
		self.annotations = annotationList
		return self.annotations

	def changePath(self, newPath):
		'''
		Muda o caminho onde os arquivos .json serão salvos
		'''
		self.path = newPath

	def getPath(self):
		'''
		Retorna o caminho onde os arquivos .json serão salvos
		'''
		return self.path