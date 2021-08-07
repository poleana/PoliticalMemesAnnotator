from core.object import Object
'''
Aluna: Polyana Bezerra da Costa
Essa classe contém todas as informações dos objetos do tipo "Text", que sao usadas como elementos na classe AnnotationPart.
Um objeto do tipo Text guarda informações sobre a "label" ou "tag"(variável value) que representa a transcrição de um texto
presente na imagem, bem como o resultado do serviço de OCR (caso tenha sido aplicado na imagem).
Esta classe herda de Object.
'''
class Text(Object):
	def __init__(self, id, value,ocr):
		super().__init__(id, value)
		self.ocrResult = ocr
	def getOCRResult(self):
		return self.ocrResult