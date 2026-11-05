from openpyxl import load_workbook
import os
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

def extrair_imagens(caminho_excel):

    planilha = load_workbook(caminho_excel)
    aba = planilha.active

    imagens = []

# Aqui _images pega a imagem que está em aba, no caso a principal, e a guarda, então dados guarda o valor dos dados da imagem obtidos em _data() que logo são inseridos em imagens os dados de cada imagem que lhe for passado como uma lista
    for imagem in aba._images:
        dados = imagem._data()
        imagens.append(dados)

    return imagens

def criar_pdf(caminho_pdf):

# Aqui está convertendo centímetro pra pontos, unidade de medida do ReportLab
    largura_pagina = 10.73 * 72 / 2.54
    altura_pagina = 15.88 * 72 / 2.54

# Cria o documento PDF com as dimensões definidas
    pdf = canvas.Canvas(caminho_pdf, pagesize = (largura_pagina, altura_pagina))

    return pdf

def adicionar_etiqueta_pdf(pdf, caminho_qrcode, caminho_logo, odp, operador, maquina, data, cliente):

# Aqui está convertendo centímetro pra pontos, unidade de medida do ReportLab
    largura_pagina = 10.73 * 72 / 2.54
    altura_pagina = 15.88 * 72 / 2.54

# Aqui converte de px pra pontos, que é a forma que o reportlab trabalha, então 72/96 é a proporção de px pra pontos
    escala = 72/96

    x_logo = 67 * escala
    x_qrcode = 15 * escala

    y_logo = 30 * escala
    y_qrcode = 250 * escala

    largura_logo = 160
    altura_logo = 50

# Aqui renderiza a imagem da Logo no PDF junto com sua posição e dimensão, mais o mask='auto' que serve para remover o fundo branco da imagem, caso ela tenha, por ser PNG
    pdf.drawImage(caminho_logo,x = x_logo, y = altura_pagina - y_logo - altura_logo, width = largura_logo, height = altura_logo, mask='auto')

    largura_qrcode = 280
    altura_qrcode = 280

# Aqui renderiza a imagem do QR Code no PDF junto com sua posição e dimensão
    pdf.drawImage(caminho_qrcode, x = x_qrcode, y = altura_pagina - y_qrcode - altura_qrcode, width = largura_qrcode, height = altura_qrcode, mask='auto')

# Aqui vai começar do canto inferior esquerdo e traçar uma linha pra servir como borda, tendo uma distância de 5 pontos tanto em x quanto em y da margem da folha
# Por ter essa distância de 5 pontos, é necessário descontar 10 para que o contorno seja feito dentro e no devido lugar da folha, caso contrário ele só seria completado fora dela visto que começaria com 5 pontos de diferença dos pontos da folha
    pdf.rect(5,5, largura_pagina - 10, altura_pagina - 10)

# define que a tabela começará a 5 pontos de distância da margem, no caso com sua borda se unindo a borda da folha
    x_tabela = 5

# Define de baixo pra cima onde a tabela vai começar
    y_tabela = 240

# Carcula a largura da tabela subtraindo a largura da página pelos 5 pontos de cada lado
    largura_tabela = largura_pagina - 10

# Altura de cada linha da tabela
    altura_linha = 25

# Quantidade de linhas, como o próprio nome diz
    quantidade_linhas = 5

# Aqui é feito o desenho do contorno da tabela, encontrando 1º a ordeda de onde começar e depois a dimensão
# Além de altura_linha * quantidade_linhas fazer com que a altura da tabela seja 125 pontos, visto que multiplicará 25, altura_linha, por 5, quantidade de linhas
    pdf.rect(x_tabela, y_tabela, largura_tabela, altura_linha * quantidade_linhas)

# Aqui é a localização da linha de separação entre chave e valor
    x_divisao = x_tabela + 70

# É aqui que é feito o loop para que cada linha de chave valor tenha uma linha horizontal os separando
    for i in range(1, quantidade_linhas):

# Calcula a localização da linha horizontal de separação de cada chave e valor
        y = y_tabela + i * altura_linha

# Aqui é feito a linha de separação horizontal
        pdf.line(x_tabela, y, x_tabela + largura_tabela, y)

    campos = [
        ("OdP:", odp),
        ("Operador:", operador),
        ("Máquina:", maquina),
        ("Data:", data),
        ("Cliente:", cliente)]

# Aqui ele vai percorrer cada um dos textos dentro de campos e os posicionar em seus repectivos lugares, x e y
    for i, (chave, valor) in enumerate(campos):

# Aqui é onde calcula a localização y dentro de suas respectivas células
# Como em ReprtLab a leitura é feita de baixo pra cima usamos quantidade_linhas - 1 - i para que a primeira linha seja a de cima e a última a de baixo
        y_linha = (y_tabela + altura_linha * (quantidade_linhas - 1 - i))

# Essa é a cor que será preenchida as células das chaves
        pdf.setFillColor("#EAEAEA")

# Aqui 1º é encontrado a localização de onde começa a pintar, com 100 de largura e 25 de altura, fill fala pra preencher com a cor que estiver ativa, no caso o cinza
        pdf.rect(x_tabela, y_linha, 70, altura_linha, fill = 1)

# Troca a cor ativa para preto, que é a cor que será usada para escrever os textos
        pdf.setFillColor("#000000")

# Aqui encontramos a localização pra centralizar y, em que somamos o valor da base da linha y + 9.5, devido a fonte hauvética ter um preenchimento invisível, por isso não é 7.5
# No caso a fonte é pra ter tamanho 10, então se o espaçamento é 25, - 10 = 15, /2 = 7.5, e se considerar o espaçamento invisível que falei, 9.5
        y_texto = y_linha + 9.5

# Aqui é escrito os valores das chaves de campos em seus respectivos lugares, que é a linha de separação vertical de chave e valor
# No caso, graças ao drawCentredString o texto é centralizado somando sua coordenada x + 50 de largura que tem essa célula
        pdf.drawCentredString(x_tabela + 35, y_texto, chave)

# Já aqui é escrito os valores dos valores dos campos em seus respectivos lugares, que é a linha de separação vertical de chave e valor
# No caso subtraímos a largura total da tabela pelo valor da largura da chave, pra considerar apenas valor, então dividimos esse valor por 2 pra chegar na metade, e pra garantir que não fique encostado na lateral somamos a x_divisao
        pdf.drawCentredString(x_divisao + (largura_tabela - 70) / 2, y_texto, str(valor))

# Aqui é onde é feito a linha de separação vertical de chave e valor
    pdf.line(x_divisao, y_tabela, x_divisao, y_tabela + altura_linha * quantidade_linhas)


if __name__ == "__main__":

    caminho = "temporario/Etiqueta_26-02187_Mateus.xlsx"

# cria a pasta onde guardamos as imagens
    os.makedirs("temporario/imagens",exist_ok=True)

    planilha = load_workbook(caminho)

    aba = planilha.active

# O enumerate percorre as imagens e numera cada uma
    for i,imagem in enumerate(aba._images, start=1):

        dados = imagem._data()

        caminho = f"temporario/imagens/imagem_{i}.png"

# Cria um arquivo em modo de escrita binária, isso se dá porque transformamos nossa imagem em _data pra extrair seus dados
        with open(caminho, "wb") as arquivo:

# Grava a imagem no computador
            arquivo.write(dados)

        print(f"Imagem {i} salva em {caminho}")

    print(f"Quantidade de imagens: {len(aba._images)}")

# Cria o documento com as dimensões especificadas
    pdf = criar_pdf("temporario/Etiquetas.pdf")

# Pega o documento criado e desenha a etiqueta dele
    adicionar_etiqueta_pdf(pdf,
                        "temporario/imagens/imagem_1.png",
                        "temporario/imagens/imagem_2.png",
                        "26/02299",
                        "Mateus",
                        12,
                        "16/07/2026",
                        "SENIR")

# Pega o documento completo
    pdf.save()
    #     print(f"Imagem: {i}")
    #     print(f"Tamanho: {len(dados)} bytes")
    #     print(f"Posição: {imagem.anchor._from.col}, {imagem.anchor._from.row}")
    #     print(f"Dimensões: {imagem.width} x {imagem.height}")

    # print(f"\nCONFIGURAÇÃO DA PÁGINA")

    # print(f"Orientação: {aba.page_setup.orientation}")
    # print(f"Papel: {aba.page_setup.paperSize}")
    # print(f"Área de impressão: {aba.print_area}")

    # print(f'\nDIMENSÕES DAS COLUNAS')
    # for coluna, dimensao in aba.column_dimensions.items():
    #     print(coluna, dimensao.width)

    # print(f"\nALTURA DAS LINHAS")

    # for linha,dimensao in aba.row_dimensions.items():
    #     print(linha,dimensao.height)