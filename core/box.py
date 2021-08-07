class Box:
    '''
    Aluna: Polyana Bezerra da Costa
    Essa classe guarda informações sobre as regiões da imagem ou bounding boxes onde os objetos anotados estão contidos.
    Recebe como parâmetros as posições x, y, largura e comprimento da região anotada, bem como uma cor para delimitar a
    região. Um objeto dessa classe é sempre usado ao criar uma AnnotationPart.
    '''

    def __init__(self, x, y, width, height, color):  
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def changeColor(self, color):
    	self.color = color