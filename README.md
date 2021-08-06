# FakeNewsMemesAnnotator
Este repositório apresenta o código e a documentação de um anotador web para um base de imagens de *Fake News* em *memes*. A ferramenta permite o upload e carregamento de imagens, a visualização das mesmas, a anotação das faces e do texto presente nas imagens - ressaltando essas regiões de interesse através de *bounding boxes* e a anotação da classificação do conteúdo da imagem em real ou falso. Além disso, o anotador salvar as anotações em um arquivo .json (permitindo o download do mesmo), e também permite a alteração do conteúdo de anotações já salvas, ou que as mesmas sejam apagadas.

Para facilitar o processo de anotação, há um módulo de OCR (*Optical Character Recognition*) para detectar as regiões da imagem onde há texto, transcrevendo-os. Caso haja algum erro, o usuário precisa apenas corrigir ou confirmar se a detecção dos caracteres está correta. Além disso, para facilitar o processo de anotação das faces, também há um módulo de localização de faces, onde dada uma imagem, serão identificadas as regiões que apresentam rostos. Ambos os módulos usam a [API Vision do Google](https://cloud.google.com/vision). Para executar o código e ter acessos aos módulos da API Vision, é preciso gerar uma APIKEY. É possível gerar uma chave seguindo esses [passos](https://cloud.google.com/vision/docs/quickstart-client-libraries). Após obter suas credencias, coloque-as no arquivo service_creds.json.

# Projeto Final de Programação
 
Aluna: Polyana Bezerra da Costa

Matrícula: 2012409

Orientador: Sérgio Colcher

O PDF com toda a documentação do projeto (finalidade, escopo, requisitos, projeto, arquitetura do sistema, testes e manual do usuário) pode ser encontrado na pasta documentation/documentacaoProjetoFinalProgramacao.pdf ou clicando [aqui](documentation/documentacaoProjetoFinalProgramacao.pdf).
Qualquer dúvida, entrar em contato com *polyanabcosta@gmail.com*.
