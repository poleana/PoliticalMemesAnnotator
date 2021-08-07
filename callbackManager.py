from layoutManager import *

'''
Aluna: Polyana Bezerra da Costa
Esse arquivo contém todas as callbacks referentes à interação do usuário com a interface do sistema.
Todas as informações que o usuário inseriu são coletadas por meio dessas callbacks e a resposta às
interações também são fornecidas por essas callbacks. 
As funções presentes nesse arquivo fazem uso de variáveis e funções presentes no controller mainController, 
que faz a mediação entre as Views e o Model.
'''

'''
Abaixo seguem algumas variáveis globais de controle usadas em algumas callbacks para controlar qual componente disparou a callback.
Algumas callbacks "assistem" vários componentes numa mesma função, então é preciso usar variáveis de controle para saber qual 
elemento disparou o evento. Isso foi feito porque a ferramenta usada para construir a página principal (Dash) permite que um 
componente do layout esteja relacionado a apenas uma callback.
'''
currentImageIndex = -1
filenames = []
prevButton = 0
nextButton = 0
refreshButton = 0
len_annotation = 0
closeAlertClicks = 0
clickSaveAnnotation = 0
closeSaveMessageClicks = 0
closeErrorMessageClicks = 0
currentResultSelected = None
currentFaceSelected = None
currentBBoxSelected = None
ocrResult = []
faceResult = []
addOcr = -1
addFace = -1
closeAddTextModal = 0
closeAddFaceModal = 0
closeFinalModel = 0
editButton = 0
deleteButton = 0
optionsBBox=[]
download_file = []


'''
Essa callback renderiza a página escolhida na navbar
'''
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return uploadCollapse
    elif pathname == "/sobre":
        return html.P("Essa ferramenta vista auxiliar no processo de anotação de imagens com o formato de meme, onde" + 
        "há texto sobrebondo uma imagem onde personalidades públicas podem aparecer. Além de permitir anotações de mão "+
        "livre, a ferramenta usa OCR e detecção de faces para automatizar o processo de anotar. Ao final, é possível "+
        "salvar e baixar a anotação resultante em um arquivo .json.")
        
    return dbc.Jumbotron(
        [
            html.H1("404: Pagina nao encontrada", className="text-danger"),
            html.Hr()
        ]
    )


'''
Essa callback mostra a view para fazer upload de imagens quando o usuário clica no botão "Upload de Imagens"
'''
@app.callback(
    Output("collapse-upload-card", "is_open"),[Input("collapse-upload-button", "n_clicks")],[State("collapse-upload-card", "is_open")])
def toggle_upload_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

'''
Essa callback recebe como entrada a lista de imagens escolhidas para upload pelo usuário e retorna uma view com a 
primeira imagem resultante do upload num canvas para desenho, seguida de 4 guias com as principais funcionalidades
do sistema
'''
@app.callback(
    [Output("canvas-content", "children")],[Input("upload-data_final", "filename"), Input("upload-data_final", "contents")])
def upload_images(uploaded_filenames, uploaded_file_contents):
    global currentImageIndex, filenames
    if uploaded_filenames is not None and uploaded_file_contents is not None:
        '''
        Ao selecionar imagens para upload, elas são salvas no local informado em "upload_images_path"
        e um objeto do tipo Annotation é criado para cada imagem
        '''
        clearFolders()
        filenames = []
        database.annotations = []
        index = 0
        for name, data in zip(uploaded_filenames, uploaded_file_contents):
            annotationTemp = annotation.Annotation(index, name, database)
            database.annotations.append(annotationTemp)
            filenames.append(name)
            save_image(name, data)
            index += 1

        currentImageIndex = 0
        imagePath = os.path.join(getFullWorkingPath(upload_images_path), filenames[currentImageIndex])
        img = Image.open(imagePath)
        """
        Uma view com o canvas contendo a primeira imagem do upload é mostrada, bem como as tabs com as 4 principais
        funcionalidades do sistema
        """
        maindDiv = getMainDiv(img, buttonsRow, tabs)
        return [maindDiv] 

    else:
        '''
        Caso nenhuma iamgem seja selecionada, a mensagem abaixo é mostrada
        '''
        return [html.Li("Nenhum arquivo selecionado (ainda)!")]


'''
Essa callback recebe qual botão foi acionado (Imagem Anterior, Imagem Seguinte, Atualizar) e mostra a imagem
correspondente no canvas
'''
@app.callback(
    [Output("canvas", "image_content"), Output("canvas", "tool"), Output("tab2", "children"), Output("tab3", "children"),
    Output("tab4", "children")],
    [Input("prev-image", "n_clicks"),Input("next-image", "n_clicks"), Input("refresh","n_clicks")])
def update_image_button_click(nPrev, nNext, nRefresh):
    global currentImageIndex, filenames, prevButton, nextButton, refreshButton, canvas_width
    """O índice da imagem selecionada é atualizado de acordo com o botão clicado"""

    if nPrev is not None:
        if nPrev != prevButton:
            prevButton = nPrev
            if currentImageIndex > 0:
                currentImageIndex -= 1
    
    if nNext is not None:
        if nNext != nextButton:
            nextButton = nNext
            if currentImageIndex < (len(filenames)-1):
                currentImageIndex += 1
                
    
    if nRefresh is not None:
        if nRefresh != refreshButton:
            refreshButton = nRefresh

    """A imagem atualizada é preparada para ser renderizada no canvas"""
    print("Current Index ", currentImageIndex)
    imagePath = os.path.join(getFullWorkingPath(upload_images_path), filenames[currentImageIndex])
    """se já houver anotações de bounding boxes relacionadas a essa imagem, elas são desenhadas na mesma """
    im = drawOnImage(imagePath, canvas_width, currentImageIndex)

    return im, 'rectangle', tab2, tab3, tab4


'''
Callback responsável por capturar a cor selecionada no seletor de cores e atualizar a variável correspondente no canvas
'''
@app.callback(Output('canvas', 'lineColor'),
            Input('color-picker', 'value'))
def update_canvas_color(value):
    if isinstance(value, dict):
        return value['hex']
    else:
        return value

'''
Callback responsável por adicionar uma AnnotationPart ao objeto Annotation referente à imagem renderizada no Canvas.
Essa callback é acionada toda vez que o usuário clica no botão "Adicionar Forma". Salvam-se informações sobre a 
bounding box desenhada na imagem e as informações inseridas nos campos de "tag" e "tipo" de objeto anotado.
Como resultado, é mostrado um popup avisando se a informação voi salva com sucesso.
'''
@app.callback(Output("modal", "is_open"),
    [Input('canvas', 'json_data'), Input('value-input', 'value'), Input('tipo-anotacao-radio', 'value'), Input("close", "n_clicks")],
    [State("modal", "is_open")])
def add_annotation_data(string, tag, annotationType, closeAlert, is_open):
    global currentImageIndex, filenames, len_annotation, canvas_width, closeAlertClicks
    
    if string:
        data = json.loads(string)
        imagePath = os.path.join(getFullWorkingPath(upload_images_path), filenames[currentImageIndex])
        im = Image.open(imagePath)
        factor = getScaleFactor(canvas_width, im)
    
        if(len(data['objects'][1:])!= len_annotation):#só entra aqui se o usuário desenhou alguma coisa no canvas
            len_annotation = len(data['objects'][1:])
            bbox = None
            '''Salvar as coordenadas da bounding box desenhada no canvas'''
            dt = data['objects'][1:][len(data['objects'][1:])-1]
            x = int(dt['left']*factor)
            y = int(dt['top']*factor)
            w  = int(dt['width']*factor)
            h = int(dt['height']*factor)
            bbox = box.Box(x,y,w,h,dt['stroke'])

            objTemp = None
            '''Criar um objeto de acordo com o tipo selecionado'''
            if int(annotationType) == 1:
                objTemp = face.Face(len_annotation-1, tag, imagePath, bbox)
            elif int(annotationType) == 2:
                objTemp = text.Text(len_annotation-1, tag, "None")
            else:
                objTemp = object.Object(len_annotation-1, tag)

            '''Adicionando uma annotationPart contendo a bounding box desenhada e o objeto informado'''
            database.annotations[currentImageIndex].addElement(annotationPart.AnnotationPart(len_annotation-1, bbox, objTemp))
            print('Quantidade de annotationParts: ',len(database.annotations[currentImageIndex].elements))
            is_open = True

        
    else:
        #se o usuário apertou o botão de "Adicionar Forma" sem desenhar nada no canvas, nada acontece
        raise PreventUpdate 
    
    if closeAlert is not None:
        if closeAlert != closeAlertClicks:
            closeAlertClicks = closeAlert
            is_open = False

    return is_open

def file_download_link(filename):
    """Preparando o link para fazer download de um arquivo"""
    location = "/download/{}".format(urlquote(filename))
    return html.A(filename, href=location)

'''
Ao clicar no botão "Salvar Anotação", essa callback salva a anotação e gera um arquivo .json, disponibilizando um link para 
download do mesmo. Como resultado, a callback mostra um popup informando se a anotação foi salva com sucesso ou não.
'''
@app.callback(
[Output("modalAnnotationSave", "is_open"), Output("modalAnnotationError", "is_open"), Output("file-list", "children")],
[Input("save-annotation", "n_clicks"), Input('fake-anotacao-radio', 'value'), Input("close-message", "n_clicks"), 
Input("close-error-message","n_clicks")],
[State("modalAnnotationSave", "is_open"), State("modalAnnotationError", "is_open")]
)
def save_annotation(clicks, isFake, closeModalSuccess, closeModalError, is_openSuccess, is_openError):
    global currentImageIndex, clickSaveAnnotation, closeSaveMessageClicks, closeErrorMessageClicks, download_file
    if clicks is not None:
        if clicks != clickSaveAnnotation:
            clickSaveAnnotation = clicks
            if isFake is not None:
                if int(isFake) == 1:
                    database.annotations[currentImageIndex].setFake = True
                if len(database.annotations[currentImageIndex].elements) > 0:
                    '''
                    ao salvar a anotação, todos os Objets presentes nas AnnotationParts são incluídos no dataset,
                    nos vetores objects e faces, respectivamente.
                    '''
                    addObjectsToDataset(currentImageIndex)
                    '''Escrevendo o arquivo json referente à anotação atual'''
                    fName = jsonManager.fileWriter(database.annotations[currentImageIndex])
                    print("Caminho onde o json foi salvo: ",jsonManager.path)
                    print("Nome do arquivo: ", fName)
                    '''Preparando o link para download do arquivo json'''
                    download_file = [html.Li(file_download_link(jsonName)) for jsonName in jsonManager.filenames]
                    #[html.Li(file_download_link(jsonName)) for jsonName in jsonManager.filenames]
                    #[html.Li(file_download_link(fName))]
                    
                    is_openSuccess = True
                else:
                    is_openError = True
            else:
                is_openError = True

    if closeModalSuccess is not None:
        if closeModalSuccess != closeSaveMessageClicks:
            closeSaveMessageClicks = closeModalSuccess
            is_openSuccess = False
    
    if closeModalError is not None:
        if closeModalError != closeErrorMessageClicks:
            closeErrorMessageClicks = closeModalError
            is_openError = False

    return is_openSuccess, is_openError, download_file

'''
Ao clicar no botão "Gerar OCR", essa callback mostra uma dropdown com as bounding boxes resultantes do processamento do OCR
'''
@app.callback(
    Output("show-bbox-ocr","children"), [Input("ocr-button", "n_clicks")]
)
def ocr_button_click(n):
    global filenames, currentImageIndex, ocrResult
    if n is not None:
        imagePath = os.path.join(getFullWorkingPath(upload_images_path), filenames[currentImageIndex])
        listOCR = getOCRResult(imagePath)#chamando a função de OCR do controller, que vai chamar a função do API Vision
        optionsSelect=[]
        for i in range(len(listOCR)):
            optionsSelect.append({"label":"Bounding Box "+str(i), "value": str(i)})
        ocrResult = listOCR
        ocrDiv = html.Div([
            html.Br(),
            dbc.Select(id="select-ocr",options=optionsSelect),
            html.Br(),
            html.Div(id="show-ocr-result")
                    
        ])

        return [ocrDiv]

'''
Quando o usuário seleciona uma opção da dropdown construída na callback anterior, esta callback renderiza uma imagem com 
a bounding box desenhada na mesma e o resultado do OCR é apresentado em um Input text. Se o usuário quiser incluir essa
AnnotationPart, basta clicar no botão "Incluir Anotação"
'''
@app.callback(
    Output("show-ocr-result","children"), [Input("select-ocr", "value")]
)
def ocr_result(value):
    global ocrResult, canvas_width, currentResultSelected, addOcr
    if value is not None:
        currentResultSelected =  ocrResult[int(value)]
        bbox = ocrResult[int(value)][0]
        tag = ocrResult[int(value)][1]
        imagePath = os.path.join(getFullWorkingPath(upload_images_path), filenames[currentImageIndex])
        im = Image.open(imagePath)
        draw = ImageDraw.Draw(im)
        factor = getScaleFactor(canvas_width, im)
        draw.rectangle((bbox.x, bbox.y, bbox.x+bbox.width, bbox.y+bbox.height),  outline=bbox.color, width=int(5*factor))
        bboxDiv = html.Div([
            html.Br(),
            html.Img(src=im, width=canvas_width),
            html.Hr(),
            html.P("Tag:",  style={'textAlign': 'left'}),
            dbc.Input(id="valueBBox-input", value=tag, type="text"),
            html.Br(),
            dbc.Button("Incluir Anotação", id="add-Anotacao", color="primary", className="mr-1")
        ])
        addOcr = 0
        return [bboxDiv]
            

'''
Se o usuário clicar no botão "Incluir Anotação", essa callback cria uma AnnotationPart e adiciona no objeto Annotation
referente à imagem atual. Se a AnnotationPart for incluída com sucesso, um popup é apresentado.
'''

@app.callback(
Output("modalAddText","is_open"),[Input("valueBBox-input", "value"), Input("add-Anotacao", "n_clicks"),
 Input("close-textModal", "n_clicks")], [State("modalAddText","is_open")])
def add_OCRResult(tagAnnotation, saveOCR, closeModal,  is_open):
    global addOcr, currentImageIndex, currentResultSelected, closeAddTextModal
   
    
    if tagAnnotation is not None :
        if saveOCR is not None:
            if saveOCR != addOcr:
                addOcr = saveOCR
                qdtAnnotation = len(database.annotations[currentImageIndex].elements)#número de annotation parts para essa imagem
                objTemp = text.Text(qdtAnnotation,tagAnnotation, currentResultSelected[1])
                database.annotations[currentImageIndex].addElement(annotationPart.AnnotationPart(qdtAnnotation, currentResultSelected[0], objTemp))
                print("****** Salvei a anotação *****")
                is_open = True

    if closeModal is not None:
        if closeModal != closeAddTextModal:
            closeAddTextModal = closeModal
            is_open = False
    return is_open


'''
Ao clicar no botão "Localizar Faces", essa callback mostra uma dropdown com as bounding boxes resultantes da
detecção de faces feita pela API Vision
'''

@app.callback(Output("showbboxFace","children"), Input("face-button", "n_clicks"))
def faces_button_click(nClicksFace):
    global filenames, currentImageIndex, faceResult
    
    if nClicksFace is not None:
        imagePath = os.path.join(getFullWorkingPath(upload_images_path), filenames[currentImageIndex])
        '''Chamando a função de localização de faces do controller, que vai chamar a função de face detection do API Vision'''
        listFaces = getFaceLocalizationResult(imagePath)
        optionsFaces=[]

        for faceIndex in range(len(listFaces)):
            optionsFaces.append({"label":"Bounding Box "+str(faceIndex), "value": str(faceIndex)})

        faceResult = listFaces
        faceDiv = html.Div([
            html.Br(),
            dbc.Select(id="select-faceLocalization",options=optionsFaces),
            html.Br(),
            html.Div(id="show-faces-result")
                    
        ])

        return [faceDiv]
  

'''
Quando o usuário seleciona uma opção da dropdown construída na callback anterior, esta callback renderiza uma imagem com 
a bounding box desenhada na mesma, na região da face detectada. Se o usuário quiser incluir essa Face na AnnotationPart, basta
informar uma label para essa face no Input text presente na view e clicar no botão "Incluir Anotação"
'''

@app.callback(
    Output("show-faces-result","children"), [Input("select-faceLocalization", "value")]
)
def faces_result(value):
    global faceResult, canvas_width, currentFaceSelected,addFace
    if value is not None:
        currentFaceSelected =  faceResult[int(value)]
        bbox = faceResult[int(value)]
        imagePath = os.path.join(getFullWorkingPath(upload_images_path), filenames[currentImageIndex])
        im = Image.open(imagePath)
        draw = ImageDraw.Draw(im)
        factor = getScaleFactor(canvas_width, im)
        '''Desenhando a face detectada na imagem original'''
        draw.rectangle((bbox.x, bbox.y, bbox.x+bbox.width, bbox.y+bbox.height),  outline=bbox.color, width=int(5*factor))
        bboxDiv = html.Div([
            html.Br(),
            html.Img(src=im, width=canvas_width),
            html.Hr(),
            html.P("Tag:",  style={'textAlign': 'left'}),
            dbc.Input(id="faceBBox-input", placeholder="Informe um nome/tag para esta face"),
            html.Br(),
            dbc.Button("Incluir Anotação", id="addFaceAnotacao", color="primary", className="mr-1")
        ])
        addFace = 0
        return [bboxDiv]
            
    

'''
Se o usuário clicar no botão "Incluir Anotação", essa callback cria uma AnnotationPart com um objeto do tipo Face
e adiciona no objeto Annotation referente à imagem atual. Se a AnnotationPart for incluída com sucesso, um popup é apresentado.
'''
@app.callback(
Output("modalAddFace","is_open"),[Input("faceBBox-input", "value"), Input("addFaceAnotacao", "n_clicks"),
 Input("close-faceModal", "n_clicks")], [State("modalAddFace","is_open")])
def add_FacesResult(tagAnnotation, saveFace, closeModal,  is_open):
    global addFace, currentImageIndex, filenames, currentFaceSelected, closeAddFaceModal
    if tagAnnotation is not None:
        if saveFace is not None:
            if saveFace != addFace:
                addFace = saveFace
                qdtAnnotation = len(database.annotations[currentImageIndex].elements)#number of annotation parts for this image
                imagePath = os.path.join(getFullWorkingPath(upload_images_path), filenames[currentImageIndex])
                '''Criando um objeto do tipo Face e incluindo na anotação'''
                faceTemp = face.Face(qdtAnnotation,tagAnnotation, imagePath, currentFaceSelected)
                database.annotations[currentImageIndex].addElement(annotationPart.AnnotationPart(qdtAnnotation, currentFaceSelected, faceTemp))
                is_open = True

    if closeModal is not None:
        if closeModal != closeAddFaceModal:
            closeAddFaceModal = closeModal
            is_open = False
    return is_open

'''
Ao clicar no botão "Selecionar Bounding Box", essa callback mostra uma dropdown com as bounding boxes já adicionadas na
anotação dessa imagem. Dessa forma, o usuário pode selecionar alguma bounding box já existente e editá-la, apagá-la ou deixar
como está.
'''
@app.callback(Output("selectBBox","children"), Input("select-button", "n_clicks"))
def selectAnnotation_button_click(nClicks):
    global currentImageIndex,optionsBBox
    
    if nClicks is not None:
        annotationParts = database.annotations[currentImageIndex].elements
        optionsBBox=[]

        for el in range(len(annotationParts)):
            optionsBBox.append({"label":"Bounding Box "+str(el), "value": str(el)})


        deleteDiv = html.Div([
            html.Br(),
            dbc.Select(id="select-bbox",options=optionsBBox),
            html.Br(),
            html.Div(id="show-select-result")
                    
        ])

        return [deleteDiv]

'''
Quando o usuário seleciona uma opção da dropdown construída na callback anterior, esta callback renderiza uma imagem com 
a bounding box desenhada na mesma, na região onde objeto está contido. O usuário pode alterar informações como o tipo da
AnnotationPart (Geral, Texto ou Face) e dar uma nova tag àquela bounding box. Se o usuário quiser incluir essas modificações,
basta clicar no botão "Salvar Edição". Também é possível apagar essa annotationPart clicando no botão "Apagar Anotação".
'''

@app.callback(
    Output("show-select-result","children"), [Input("select-bbox", "value")]
)
def selectDiv_result(value):
    global canvas_width, currentBBoxSelected, filenames, currentImageIndex, editButton, deleteButton
    if value is not None:
        currentBBoxSelected =  int(value)
        annPartTemp = database.annotations[currentImageIndex].elements[currentBBoxSelected]
        imagePath = os.path.join(getFullWorkingPath(upload_images_path), filenames[currentImageIndex])
        im = Image.open(imagePath)
        draw = ImageDraw.Draw(im)
        factor = getScaleFactor(canvas_width, im)
        draw.rectangle((annPartTemp.boundingBox.x, annPartTemp.boundingBox.y, annPartTemp.boundingBox.x+annPartTemp.boundingBox.width, 
        annPartTemp.boundingBox.y+annPartTemp.boundingBox.height),  outline=annPartTemp.boundingBox.color, width=int(5*factor))
        typeAnnotation = 3
        if type(annPartTemp.object) is face.Face:
            typeAnnotation = 1
        elif type(annPartTemp.object) is text.Text:
            typeAnnotation = 2
        typeAnnotation = dbc.FormGroup(
        [
            dbc.Label("Tipo:"),
            dbc.RadioItems(
                options=[
                    {"label": "Face", "value": 1},
                    {"label": "Texto", "value": 2},
                    {"label": "Geral", "value": 3},
                ],
                value=typeAnnotation,
                id="typeBbox",
                inline=True,
            ),
        ]
        )
        bboxResultDiv = html.Div([
            html.Br(),
            html.Img(src=im, width=canvas_width),
            html.Hr(),
            typeAnnotation,
            html.Br(),
            html.P("Tag:",  style={'textAlign': 'left'}),
            dbc.Input(id="tagEdit-input",value=str(annPartTemp.object.value)),
            html.Br(),
            dbc.Row([
                dbc.Col(dbc.Button("Salvar Edição", id="editAnotacao", color="success", className="mr-1")),
                dbc.Col(dbc.Button("Apagar Anotação", id="deleteAnotacao", color="danger", className="mr-1"))
            ])])
        resultingDiv = html.Div(children=bboxResultDiv, id="editingDiv")
        editButton = 0
        deleteButton = 0
        return [resultingDiv]


'''
Se o usuário clicar no botão "Salvar Edição", essa callback cria uma AnnotationPart com as novas informações
inseridas e atualiza essa AnnotationPart no vetor de elementos da anotação. Caso o usuário clique no botão "Apagar Anotação",
a annotationPart é apagado do vetor de elementos da anotação. Um popup é apresentado com a informação correspondente ao botão
selecionado.
'''

@app.callback([Output("modelEditPart", "is_open"), Output("select-bbox","options")],
[Input("tagEdit-input", "value"), Input("typeBbox", "value"), Input("editAnotacao", "n_clicks"), Input("deleteAnotacao", "n_clicks"),
Input("close-EditModal", "n_clicks")],[State("modelEditPart", "is_open")])
def editResult(tagAnnotation, typeAnnotation, editButton_clicks,  deleteButton_clicks, modalEdit_clicks, is_open):
    global closeFinalModel, editButton, deleteButton, currentBBoxSelected, filenames, currentImageIndex,optionsBBox

    if editButton_clicks is not None:
        if editButton_clicks != editButton:
            editButton = editButton_clicks
            objTemp = None
            lenAnnotationParts = len(database.annotations[currentImageIndex].elements)
            '''Atualizando a AnnotationPart com as novas informações inseridas'''
            bbox = database.annotations[currentImageIndex].elements[currentBBoxSelected].boundingBox

            if int(typeAnnotation) == 1:
                imagePath = os.path.join(getFullWorkingPath(upload_images_path), filenames[currentImageIndex])
                objTemp = face.Face(lenAnnotationParts, tagAnnotation, imagePath, bbox)
            elif int(typeAnnotation) == 2:
                objTemp = text.Text(lenAnnotationParts, tagAnnotation, database.annotations[currentImageIndex].elements[currentBBoxSelected].ocrResult)
            else:
                objTemp = object.Object(lenAnnotationParts, tagAnnotation)

            database.annotations[currentImageIndex].elements[currentBBoxSelected] = annotationPart.AnnotationPart(lenAnnotationParts, bbox, objTemp)
            is_open = True

    if deleteButton_clicks is not None:
        if deleteButton_clicks != deleteButton:
            deleteButton = deleteButton_clicks
            element = database.annotations[currentImageIndex].elements[currentBBoxSelected]
            '''Removendo o AnnotationPart selecionada'''
            optionsBBox.remove(optionsBBox[currentBBoxSelected])
            database.annotations[currentImageIndex].elements.remove(element)
            is_open = True

    if modalEdit_clicks is not None:
        if modalEdit_clicks != closeFinalModel:
            closeFinalModel = modalEdit_clicks
            is_open = False
            
    return is_open, optionsBBox
