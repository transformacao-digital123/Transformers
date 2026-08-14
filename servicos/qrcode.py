import qrcode
from openpyxl.drawing.image import Image
from openpyxl.styles import Font,Alignment
from openpyxl import load_workbook
import os
import json
import secrets

FONTE_PADRAO = Font(name="Arial", size=11)

ALINHAMENTO_PADRAO = Alignment(horizontal="center",vertical="center",wrap_text=True)

rastreabilidade = {}

# O texto servirá como parâmetro no lugar de texto_qr onde ODP, data, turno e operador são parâmetros obrigatórios pois são eles que nos ajudarão a encontrar o caminho até ao arquivo, aba e linha onde está nossa odp
def gerar_qrcode(texto):

# Pegue o conteúdo recebido em odp e transforme-o em uma imagem de QR Code.
        qr = qrcode.make(texto)

# Agora que o qr já foi criado podemos voltar a transformar a variável em biblioteca de novo para que possamos a continuar a usar a variável odp pro resto do programa
        dados = json.loads(texto)
        odp = dados["odp"]

        odp_limpo = odp.replace("/","-")

 # Aqui você aproveitou a própria ODP para criar um nome único para a imagem       
        test = f"QR_{odp_limpo}.png"

        caminho = os.path.join("temporario", test)

# Agora a imagem que está na variável qr é realmente gravada no computador
        qr.save(caminho)

# A função não retorna o QR Code em si. Ela retorna o endereço onde a imagem foi salva
        return caminho

def interpretar_qrcode(texto_lido):
        dados = json.loads(texto_lido)

        print(f"ODP: {dados['odp']}")
        print(f"OPERADOR: {dados['operador']}")
        print(f"DATA: {dados['data']}")
        print(f"TURNO: {dados["turno"]}")

        return dados

def preencher_etiqueta(ordem):

# token_hex(4): Pede para o sistema gerar 4 bytes, cada byte representa um caracter, de dados aleatórios e transformá-los em uma string no formato hexadecimal (que usa números de 0 a 9 e letras de A a F).
        identificador = "LUARI-" + secrets.token_hex(4).upper()

        dados_identificador = {
                "odp": ordem["odp"],
                "operador": ordem["operador"],
                "maquina": ordem["maquina"],
                "turno": ordem["turno"],
                "data": ordem["data"]
        }

        rastreabilidade[identificador] = dados_identificador

# Carrega a planilha que queremos
        planilha = load_workbook("modelos/Modelo_Etiqueta_Luari.xlsx")

# Abre na 1º aba do arquivo
        aba = planilha.active

        aba["B6"] = ordem["odp"]
        aba["B6"].font = FONTE_PADRAO
        aba["B6"].alignment = ALINHAMENTO_PADRAO

        aba["B7"] = ordem["operador"]
        aba["B7"].font = FONTE_PADRAO
        aba["B7"].alignment = ALINHAMENTO_PADRAO

        aba["B8"] = ordem["maquina"]
        aba["B8"].font = FONTE_PADRAO
        aba["B8"].alignment = ALINHAMENTO_PADRAO

        aba["B9"] = ordem["data"]
        aba["B9"].number_format = "dd/mm/yy"
        aba["B9"].font = FONTE_PADRAO
        aba["B9"].alignment = ALINHAMENTO_PADRAO

# Serve para encontrar a odp na aba e arquivo corretos
        dados_qr = {
                "odp": ordem["odp"],
                "data": ordem["data"].strftime("%d-%m-%Y"),
                "turno": ordem["turno"],
                "operador": ordem["operador"]
        }

# Aqui ele pega e transforma o texto em uma linguagem que o programa do QR code consiga ler,no caso formato de texto, esse comando ensure_ascii= False serve para caso seja escrito uma palavra com ~ ou ç o programa faça o texto ficar normal e não um conjunto de letras estranhas
        texto_qr = json.dumps(dados_qr, ensure_ascii= False)

# Usa a função Gerar_qrcode para gerar o caminho da imagem PNG do QRcode
        caminho_qr = gerar_qrcode(texto_qr)

# Cria um objeto que pode ser inserido na planilha
        qr = Image(caminho_qr)

# Define os tamahos 406x240(valores do espaço onde o QR code está inserido)
        qr.height = 200
        qr.width = 200

# Adiciona a imagem começando na célula especificada
        aba.add_image(qr,"B12")

        odp_limpo = ordem["odp"].replace("/","-")

# Camiho da saída do nvo arquivo das etiqueta
        caminho = f"Etiqueta_{odp_limpo}.xlsx"

        caminho_saida = os.path.join("temporario", caminho)

        planilha.save(caminho_saida)

        return caminho_saida