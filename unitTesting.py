import unittest
from unitTestingData import *
'''
Aluna: Polyana Bezerra da Costa
'''
class Tests(unittest.TestCase):
    
    #Testando a criação de um dataset
    def test_DatasetCreation(self):
        database = getTest_DatasetCreationData()
        self.assertEqual(database.name, "Political Memes", "A resposta deve ser Political Memes.")
    
    #Testando se o resultado do OCR da API Vision está correto
    def test_OCRResult(self):
        strOCR = getTest_OCRResultData()
        print("Resultado OCR: ", strOCR)
        self.assertEqual(strOCR, "BOULOS , SEM TETO MAS COM JATINHO ", "A resposta deve ser BOULOS , SEM TETO MAS COM JATINHO .")
    
    #Testando se a posição x da bounding box da face retornada pela API Vision é um inteiro (se estiver tudo correto, deve ser)
    def test_FaceDetection(self):
        posX = getTest_FaceDetetionData()
        print(isinstance(posX, int))
        self.assertTrue(isinstance(posX, int), "A resposta deveria ser True.")
    
    #Testando se o arquivo json de uma anotação é criado
    def test_CreateJson(self):
        jsonName, jsonFileName = getTest_CreateJson()
        self.assertTrue(jsonName == jsonFileName, "Os arquivos deveriam ter o mesmo nome.")

    #Testando se a conversão do conteúdo de um arquivo json em anotacao está correto
    def test_JsontoAnnotation(self):
        annotation1, annotation2 = getTest_JsonToAnnotationData()
        self.assertTrue(annotation1.fileName == annotation2.fileName, "Os objetos devem corresponder a mesma imagem.")
        
if __name__ == '__main__':
    unittest.main()

