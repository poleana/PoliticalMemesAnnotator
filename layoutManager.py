from imports import *
from mainController import *
from flask import Flask, send_from_directory


'''
Aluna: Polyana Bezerra da Costa
Esse arquivo contém o layout e componentes HTML referentes à interface do sistema.
'''



server = Flask(__name__)
@server.route("/download/<path:path>")
def download(path):
    '''
    Essa funçao disponiliza os arquivos .json para download
    '''
    fullPath = getFullWorkingPath(annotation_json_path)
    return send_from_directory (fullPath, path, as_attachment=True)

app = dash.Dash(server=server, external_stylesheets=[dbc.themes.BOOTSTRAP, 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'])

canvas_width = 500
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#edfafc",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}


def buildCanvas(filename, buttonsRow):
    global canvas_width    
    '''
    Essa função cria o canvas onde as imagens escolhidas pelo usuário serão renderizadas, permitindo que o usuário desenhe sobre
    elas
    '''
    canvas = html.Div([
        html.H6('Selecione o quadrado para desenhar na imagem.'),
        html.Div([
            dash_canvas.DashCanvas(id='canvas',
                tool = 'rectangle',
                lineWidth=5,
                lineColor='red',
                image_content=filename,
                width=canvas_width,
                json_data = None,
                hide_buttons=['line', 'zoom', 'pan', 'pencil'],
                goButtonTitle="Adicionar Forma"
            ),
        ], className="five columns"),
        html.Br(),
        buttonsRow
        ]
    )
    return canvas

def getMainDiv(img, buttons, tab ):
    '''
    Essa função retorna os componentes HTML referentes ao canvas e as 4 telas de funcionalidades do sistema (Anotar Imagem,
    Gerar OCR, Localizar Faces e Editar Anotações)
    '''
    canvas = buildCanvas(img, buttons)
    maindDiv = html.Div([
        html.Hr(),
        dbc.Row([
            dbc.Col(canvas),
            dbc.Col(tab)
        ]),
        html.Br(),       
    ])
    return maindDiv

sidebar = html.Div(
    [
        html.H3("Memes Annotator", style={'textAlign': 'center'}),
        html.Hr(),
        html.P(
            "Uma ferramenta de anotação para fake news em memes", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Anotação", href="/", active="exact"),
                dbc.NavLink("Sobre", href="/sobre", active="exact"),
            ],
            vertical=True,
            pills=True
        )
    ],
    style=SIDEBAR_STYLE
)
"""Esse modal define o popup que é mostrado quando o usuário adiciona uma bounding box à anotação"""
modalAnnotationPart = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader(
                    dbc.Alert("Conteúdo Salvo", color="info")
                ),
                dbc.ModalBody("A bounding box foi adicionada à anotação."),
                dbc.ModalFooter(
                    dbc.Button(
                        "Fechar", id="close",color="danger", className="ml-auto", n_clicks=0
                    )
                ),
            ],
            id="modal",
            size="sm",
            is_open=False,
        ),
    ]
)
"""Esse modal define o popup que é mostrado quando o usuário salva uma anotação"""
modalAnnotationSave = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.Alert("Conteúdo Salvo", color="success")),
                dbc.ModalBody("Anotação salva com sucesso."),
                dbc.ModalFooter(
                    dbc.Button(
                        "Fechar", id="close-message", color="danger", className="ml-auto", n_clicks=0
                    )
                ),
            ],
            id="modalAnnotationSave",
            size="sm",
            is_open=False,
        ),
    ]
)

"""Esse modal define o popup que é mostrado quando o usuário tenta salvar uma anotação, mas não preencheu todos os campos"""
modalAnnotationError = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.Alert("Erro ao salvar anotação!", color="danger")),
                dbc.ModalBody("Você provavelmente esqueceu de preencher algum campo."),
                dbc.ModalFooter(
                    dbc.Button(
                        "Fechar", id="close-error-message",color="danger", className="ml-auto", n_clicks=0
                    )
                ),
            ],
            id="modalAnnotationError",
            size="sm",
            is_open=False,
        ),
    ]
)
"""Esse modal define o popup que é mostrado quando o usuário salva uma anotação de texto gerada por OCR"""

modalAddText = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.Alert("Conteúdo Salvo", color="info")),
                dbc.ModalBody("Anotação textual salva com sucesso. Clique no botão 'Atualizar' quando terminar de incluir os resultados do OCR."),
                dbc.ModalFooter(
                    dbc.Button(
                        "Fechar", id="close-textModal", color="danger", className="ml-auto", n_clicks=0
                    )
                ),
            ],
            id="modalAddText",
            size="sm",
            is_open=False,
        ),
    ]
)
"""Esse modal define o popup que é mostrado quando o usuário salva uma anotação de face gerada pelo Face Detection"""
modalAddFace = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.Alert("Conteúdo Salvo", color="info")),
                dbc.ModalBody("Face incluída com sucesso. Clique no botão 'Atualizar' quando terminar de incluir as faces localizadas."),
                dbc.ModalFooter(
                    dbc.Button(
                        "Fechar", id="close-faceModal", color="danger", className="ml-auto", n_clicks=0
                    )
                ),
            ],
            id="modalAddFace",
            size="sm",
            is_open=False,
        ),
    ]
)
"""Esse modal define o popup que é mostrado quando o usuário edita ou apaga uma AnnotationPart já existente"""
modalEditPart = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.Alert("Alteração Salva", color="success")),
                dbc.ModalBody("Alteração salva com sucesso. Ao finalizar as alterações, clique no botão 'Atualizar' para ver a anotação resultante."),
                dbc.ModalFooter(
                    dbc.Button(
                        "Fechar", id="close-EditModal", color="danger", className="ml-auto", n_clicks=0
                    )
                ),
            ],
            id="modelEditPart",
            size="sm",
            is_open=False,
        ),
    ]
)

"""Essa div tem os componentes referenteas à View do upload de imagens"""
image_upload_div = html.Div(
    [
        
        html.P(
            "Escolha a pasta onde estão as imagens que se deseja anotar, ou imagens isoladas.", style={'textAlign': 'left'}
        ),
        dcc.Upload(
            id="upload-data_final",
            children=html.Div(
                ["Escolher arquivos"]
            ),
            style={
                "width": "50%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "auto",
            },
            multiple=True,
    )],
    style={"max-width": "500px"},
)



uploadCollapse = html.Div(
    [
        dbc.Button(
            "Upload de Imagens",
            id="collapse-upload-button",
            className="mb-3",
            color="primary",
            n_clicks=0,
        ),
        dbc.Collapse(
            image_upload_div,
            id="collapse-upload-card",
            is_open=False,
        )
    ]
)
"""Esse componentes contém os botões para avançar, retroceder na lista de imagens ou atualizar a imagem"""
buttonsRow = dbc.Row(
    [
        dbc.Col(html.Div(dbc.Button("<< Imagem Anterior", id="prev-image", outline=True, color="primary", className="mr-1")), width=4),
        dbc.Col(html.Div(dbc.Button("Atualizar", id="refresh",outline=True, color="success", className="mr-1"))),
        dbc.Col(html.Div(dbc.Button("Próxima Imagem >>", id="next-image", outline=True, color="primary", className="mr-1")), width=6),
    ]
)

"""Esse componente contém o seletor de cores para bounding boxes"""
color_picker = html.Div([
    daq.ColorPicker(
        id='color-picker',
        label='Cor do pincel',
        value=dict(hex='#FF0000')
    )],
    style={
        'textAlign': 'left'
    }
)

"""Esse componente contém as opções para sinalizar se a anotação apresenta conteúdo fake ou não"""
placeholder_br = html.Div([html.Br()])
annotation_fake = dbc.FormGroup(
    [
        dbc.Col(html.P("A imagem apresenta fake news?"), width=5),
        dbc.Col(
            dbc.RadioItems(
                id="fake-anotacao-radio",
                options=[
                    {"label": "Sim", "value": 1},
                    {"label": "Não", "value": 2}
                ],
            ),
            width=2,
        )
    ],
    row=True,
)
"""Esse componente apresenta o campo para inserção da tag da AnnotationPart"""
annotation_value = html.Div(
    [
        html.Hr(),
        html.P("Tag:",  style={'textAlign': 'left'}),
        dbc.Input(id="value-input", placeholder="Informe o valor ou tag da bounding box...", type="text"),
        html.Br()
    ]
)

"""Esse componente contém as opções de tipo de AnnotationPart"""
annotation_type = dbc.FormGroup(
    [
        dbc.Col(html.P("Tipo:"), width=1),
        dbc.Col(
            dbc.RadioItems(
                id="tipo-anotacao-radio",
                options=[
                    {"label": "Face", "value": 1},
                    {"label": "Texto", "value": 2},
                    {"label": "Geral", "value": 3}
                ],
            ),
            width=4,
        ),
        dbc.Col(color_picker, width=4)
    ],
    row=True,
)


"""Esse componente contém o botão para salvar a anotação e link para download do arquivo .json gerado"""
save_annotation = html.Div([html.Br(), dbc.Button("Salvar Anotação", id="save-annotation", outline=True, color="primary", className="mr-1")])
download_files = html.Div([
    html.Br(),
    html.Ul(id="file-list")
])

annotation_form = dbc.Form([placeholder_br,annotation_fake,annotation_value, annotation_type, save_annotation, download_files,modalAnnotationPart, 
modalAnnotationSave, modalAnnotationError, modalAddText, modalAddFace, modalEditPart])

####################### Tabs com as 4 Views de funcionalidades do sistema #####################################

"""Tab com a view para aplicar OCR sobre a imagem"""
tab2 = html.Div([
        dbc.Button("Gerar OCR", id="ocr-button", color="success"),
        html.Div(id="show-bbox-ocr")
    ]
)
tab2_content = dbc.Card(
    dbc.CardBody(tab2, id="tab2"),
    className="mt-3",
)

"""Tab com a view para aplicar localização de faces sobre a imagem"""
tab3 = html.Div([
        dbc.Button("Localizar Faces",id="face-button",color="success"),
        html.Div(id="showbboxFace")
    ]
)
tab3_content = dbc.Card(
    dbc.CardBody(tab3, id="tab3"),
    className="mt-3",
)

"""Tab com a view para selecionar AnnotationParts para editar ou apagar"""
tab4 = html.Div([
        dbc.Button("Selecionar Bounding Box",id="select-button",color="success"),
        html.Div(id="selectBBox")
    ]
)
tab4_content = dbc.Card(
    dbc.CardBody(tab4, id="tab4"),
    className="mt-3",
)

tabs = dbc.Tabs(
    [
        dbc.Tab(annotation_form, label="Anotar"),#tab com a view principal para anotação em imagens
        dbc.Tab(tab2_content, label="OCR"),
        dbc.Tab(tab3_content, label="Detecção de Face"),
        dbc.Tab(tab4_content, label="Editar Anotação"),
        
    ]
)


main_content = html.Div(id="page-content", style=CONTENT_STYLE)
canvas_content = html.Div(id="canvas-content", style=CONTENT_STYLE)
remainder_content = html.Div(id="buttons-content", style=CONTENT_STYLE)
canvas_show = html.Div(id="mainCanvas")

"""Adicionando todos os componentes criados ao layout da página principal"""
app.layout = html.Div([dcc.Location(id="url"), sidebar, main_content,canvas_content,canvas_show, remainder_content])