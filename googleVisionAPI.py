import os
from google.cloud import vision
import io
from PIL import Image, ImageDraw

'''
Esse arquivo contém as funções da API Vision do Google usadas nesse sistema para auxiliar no processo de anotação de memes.
Para que as funções possam ser executadas, é preciso fornecer uma APIKEY, contida no arquivo 'service_creds.json'.
Para gerar sua própria APIKEY, siga o tutorial em: https://cloud.google.com/vision/docs/quickstart-client-libraries. Ao obter
suas credenciais, substitua o arquivo 'service_creds.json' pelo arquivo .json gerado.
'''

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'service_creds.json'
client = vision.ImageAnnotatorClient()

def getBoxFromVertices(vertices):
    '''
    Essa função converte os vértices retornados pela API Vision em uma bounding box de coordenadas x, y, largura e altura
    '''
    w = abs(vertices[1].x - vertices[0].x)
    h = abs(vertices[2].y - vertices[1].y)
    x = vertices[0].x
    y = vertices[0].y
    if x < 0:
        x = 0
    if y < 0:
        y = 0
    return [int(x), int(y), int(w), int(h)]

def detect_OCR(path):
    '''
    Essa função recebe o caminho para uma imagem, aplica OCR e retorna as regiões onde foram encontrados textos, bem como
    a transcrição dos mesmos.
    '''
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)
    boxes_ocr = []

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            if block.confidence > 0.70:
                box = getBoxFromVertices(block.bounding_box.vertices)

                for paragraph in block.paragraphs:
                    paragraph_text = ""
                    for word in paragraph.words:
                        word_text = ''.join([symbol.text for symbol in word.symbols])
                        paragraph_text += word_text + " "
                    boxes_ocr.append([box,paragraph_text])
                
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    return boxes_ocr

    
def detect_faces(path):
    '''
    Essa função recebe o caminho para uma imagem, aplica a detecção de faces e retorna as regiões onde as faces foram encontradas
    '''
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.face_detection(image=image)
    faces = response.face_annotations
    boxes_faces = []

    for face in faces:
        box = getBoxFromVertices(face.bounding_poly.vertices)
        boxes_faces.append(box)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    return boxes_faces