import base64
import os
from urllib.parse import quote as urlquote 
from PIL import Image, ImageDraw

from core import object
from core import text
from core import face
from core import box
from core import annotationPart
from core import annotation

from core import dataset
from core import jsonFileManager
#from googleServices import googleVisionAPI
from googleVisionAPI import *

'''
Aluna: Polyana Bezerra da Costa
Esse arquivo representa o Controller que faz a mediação entre as Views do sistema (representadas no arquivo layoutManager)
e o Model (representado pelas classes do pacote Core e funções da API Vision), onde estão as regras de negócio do sistema.
'''


upload_images_path = "\\upload\\media\\images\\"#caminho onde serão salvas as imagens escolhidas para upload pelo usuário
annotation_json_path = "\\jsonAnnotation\\"#caminho onde serão salvos os arquivos .json


def getScaleFactor(canvas_width, image):
    '''
    Essa função retorna o fator de escala para que a imagem seja renderizada corretamente pelo Canvas
    '''
    width, height = image.size
    return width/canvas_width

def getFullWorkingPath(path):
    '''
    Essa função retorna o atual caminho do sistema (caminho completo)
    '''
    basePath = os.getcwd()
    return basePath + path
    

def getDataset():
    '''
    Essa função cria uma instância de Dataset caso não exista, ou retorna a instância existente
    '''
    database, flag = dataset.Dataset()
    if(flag):
        database.config(1,  "Political Memes", getFullWorkingPath(upload_images_path))
    return database

def addObjectsToDataset(index):
    '''
    Sempre que uma AnnotationPart é adicionada a uma Annotation, os objetos do tipo Object contidos em cada AnnotationPart
    são adicionados ao vetor de Objects do Dataset
    '''
    for element in database.annotations[index].elements:
        if type(element.object) is face.Face:
            database.faces.append(element.object)
        elif type(element.object) is object.Object:
            database.objects.append(element.object)
        
def drawOnImage(imagePath, canvas_width, index):
    '''
    Essa função é responsável por desenhar bounding boxes em uma imagem
    '''
    im = Image.open(imagePath)
    factor = getScaleFactor(canvas_width, im)
    db = getDataset()
    if len(db.annotations[index].elements):
        draw = ImageDraw.Draw(im)
        for el in db.annotations[index].elements:
            x = el.boundingBox.x
            y = el.boundingBox.y
            w = el.boundingBox.width
            h = el.boundingBox.height
            draw.rectangle((int(x), int(y), int((x+w)), int((y+h))), outline=el.boundingBox.color, width=int(5*factor))
    return im    

def createJsonManager(dataset):
    '''
    Essa função cria uma instância de jsonFileManager caso não exista, ou retorna a instância existente.
    O local onde que os arquivos .json serão salvos também é definido ao criar uma instância de jsonFileManager
    '''
    jsonManager, flag =  jsonFileManager.jsonFileManager()
    if(flag):
        jsonManager.config(getFullWorkingPath(annotation_json_path),dataset)
    return jsonManager

def clearFolders():
    '''
    Sempre ao renderizar a página de upload de imagens, as imagens que estiverem na página de upload são apagadas, bem como
    os arquivos .json resultantes de outras execuções do sistema
    '''

    fullPath = getFullWorkingPath(upload_images_path)
    for filename in os.listdir(fullPath):
        os.remove(fullPath+filename)

    fullPath = getFullWorkingPath(annotation_json_path)
    for fn in os.listdir(fullPath):
        os.remove(fullPath+fn)


def save_image(name, content):
    '''
    Essa função salva as imagens escolhidas para upload no local definido pela variável "upload_images_path"
    '''
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(getFullWorkingPath(upload_images_path), name), "wb") as fp:
        fp.write(base64.decodebytes(data))

def list_uploaded_images():
    '''
    Essa função lista todos os arquivos de que foi feito upload
    '''
    files = []
    for filename in os.listdir(upload_images_path):
        path = os.path.join(upload_images_path, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files

def getOCRResult(imagePath):
    '''
    Essa função chama a função de OCR da API Vision do Google, fornecendo como parâmetro o caminho da imagem.
    Esse caminho é definido no resultado de uma callback presente em callbackManager
    '''
    googleOCR = detect_OCR(imagePath)
    listOCR = []

    for bbox in googleOCR:
        listOCR.append([box.Box(bbox[0][0],bbox[0][1],bbox[0][2],bbox[0][3], "#ff0000"), bbox[1]])
    return listOCR

def getFaceLocalizationResult(imagePath):
    '''
    Essa função chama a função de detecção de Faces da API Vision do Google, fornecendo como parâmetro o caminho da imagem.
    Esse caminho é definido no resultado de uma callback presente em callbackManager
    '''
    listFaces = []
    googleFaces = detect_faces(imagePath)
    
    for bbox in googleFaces:
        listFaces.append(box.Box(bbox[0],bbox[1],bbox[2],bbox[3], "#00FF00"))
    return listFaces

'''
Criando as instâncias para Dataset e jsonFileManager que serão usadas por callbackManager
'''
database = getDataset()
jsonManager = createJsonManager(database)
