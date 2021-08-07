
from core import dataset
from core import jsonFileManager
from core import annotationPart
from core import annotation
from core import text
from core import face
from core import object
from core import box
from googleVisionAPI import *

'''
Aluna: Polyana Bezerra da Costa
'''

testeImagePath = 'images/boulos1.png'
jsonFileName = ""
'''Criando uma instância de Dataset'''
def getTest_DatasetCreationData():
    database, flag = dataset.Dataset()
    if(flag):
        database.config(1,  "Political Memes", "C:/Users/polya/Downloads/FakeNewsImageAnnotator/images/")
    return database

'''Executando o OCR e pegando o resultado corresponde à primeira bounding box'''
def getTest_OCRResultData():
    boxes = detect_OCR(testeImagePath)
    if len(boxes):
        return boxes[0][1]#retornando o resultado do OCR da primeira bounding box
    return "None"

'''Executando a detecção de faces e pegando a posição x da bounding box da primeira face detectada'''
def getTest_FaceDetetionData():
    box = detect_faces(testeImagePath)
    if len(box):
        return box[0][0]#retornando o valor da posição x da primeira face detectada
    else:
        return None

'''Criando uma anotação com dados genéricos'''
def getAnnotation(database):
    obj = object.Object(1, "caneca")
    texto = text.Text(1, "hide the pain harold","ocr")
    faceBBox = face.Face(1, "Harold", "test.jpg", box.Box(556,4,208,217,"green"))
    annotationData = annotation.Annotation(1, "teste.jpg", database)
    annotationData.addElement(annotationPart.AnnotationPart(1, box.Box(565,293,101,134,"blue"), obj))
    annotationData.addElement(annotationPart.AnnotationPart(2, box.Box(9,440,939,99,"red"), texto))
    annotationData.addElement(annotationPart.AnnotationPart(3, box.Box(556,4,208,217,"green"), faceBBox))
    return annotationData

'''Criando uma instância de JsonFileManager'''
def createJsonFileManager(dataset):
    jsonManager, flag =  jsonFileManager.jsonFileManager()
    if(flag):
        jsonManager.config('C:/Users/polya/Downloads/FakeNewsImageAnnotator/jsonAnnotation/',dataset)
    return jsonManager

'''Escrevendo o conteudo de uma anotacao num arquivo json e recuperando o nome dos arquivos json no diretorio informado,
a fim de comparar se os nomes são iguais, comprovando assim que o arquivo .json foi mesmo criado'''
def getTest_CreateJson():
    global jsonFileName
    dataset = getTest_DatasetCreationData()
    jsonManager =  createJsonFileManager(dataset)
    
    annotationData = getAnnotation(dataset)
    #Escreve o arquivo json no disco e recebe o nome do arquivo
    fName = jsonManager.fileWriter(annotationData)
    jsonFileName = fName
    #Recupera o nome dos arquivos no diretorio informado
    jsonFile = dataset.getListofFiles('C:/Users/polya/Downloads/FakeNewsImageAnnotator/jsonAnnotation/')[0]
    return fName, jsonFile

'''Convertendo o conteúdo de um arquivo json num objeto do tipo Annotation e retornando o objeto resultante e o objeto original
que foi usado pra escrever o arquivo json'''
def getTest_JsonToAnnotationData():
    global jsonFileName
    dataset = getTest_DatasetCreationData()
    jsonManager =  createJsonFileManager(dataset)
    auxAnnotation = jsonManager.jsonToAnnotation(jsonFileName)
    annotationData = getAnnotation(dataset)
    return auxAnnotation, annotationData

