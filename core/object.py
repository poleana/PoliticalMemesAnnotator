'''
Aluna: Polyana Bezerra da Costa
Essa classe contém todas as informações dos objetos do tipo "Geral" (objeto geral, que não é Face nem Texto),
que sao usadas como elementos na classe AnnotationPart. Um Object guarda o número identificador de um objeto, 
o nome (value) e uma possível descrição(não é obrigatório informar uma descrição) para esse objeto. 
As subclasses "Face" e "Text" herdam de Object.
'''

class Object:
    def __init__(self, id, value):
        self.id = id
        self.value = value
        self.description = ""
    def setValue(self,value):
    	self.value = value
    def getValue(self):
    	return self.value
    def setDescription(self,description):
    	self.description = description
    def getDescription(self):
    	return self.description
