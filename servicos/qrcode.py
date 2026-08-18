import qrcode
from openpyxl.drawing.image import Image
from openpyxl.styles import Font,Alignment
from openpyxl import load_workbook
import os
import json
import secrets

from servicos.apontamento import localizar_odp

FONTE_PADRAO = Font(name="Arial", size=11)

ALINHAMENTO_PADRAO = Alignment(horizontal="center",vertical="center",wrap_text=True)

# O texto servirá como parâmetro no lugar de texto_qr onde ODP, data, turno e operador são parâmetros obrigatórios pois são eles que nos ajudarão a encontrar o caminho até ao arquivo, aba e linha onde está nossa odp
def gerar_qrcode(texto,odp):

# Pegue o conteúdo recebido em odp e transforme-o em uma imagem de QR Code.
        qr = qrcode.make(texto)

        odp_limpo = odp.replace("/","-")

 # Aqui você aproveitou a própria ODP para criar um nome único para a imagem       
        test = f"QR_{odp_limpo}.png"

        caminho = os.path.join("temporario", test)

# Agora a imagem que está na variável qr é realmente gravada no computador
        qr.save(caminho)

# A função não retorna o QR Code em si. Ela retorna o endereço onde a imagem foi salva
        return caminho

def interpretar_qrcode(identificador,rastreabilidade):
        dados = rastreabilidade[identificador]

        print(f"ODP: {dados['odp']}")
        print(f"OPERADOR: {dados['operador']}")
        print(f"DATA: {dados['data']}")
        print(f"TURNO: {dados["turno"]}")

        return dados

def preencher_etiqueta(ordem,rastreabilidade):

# token_hex(4): Pede para o sistema gerar 4 bytes, cada byte representa um caracter, de dados aleatórios e transformá-los em uma string no formato hexadecimal (que usa números de 0 a 9 e letras de A a F).
        identificador = "LUARI-" + secrets.token_hex(4).upper()

        dados_identificador = {
                "odp": ordem["odp"],
                "operador": ordem["operador"],
                "maquina": ordem["maquina"],
                "turno": ordem["turno"],
                "data": ordem["data"].strftime("%d%m%Y")
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

# Aqui ele pega e transforma o texto em uma linguagem que o programa do QR code consiga ler,no caso formato de texto, esse comando ensure_ascii= False serve para caso seja escrito uma palavra com ~ ou ç o programa faça o texto ficar normal e não um conjunto de letras estranhas
        texto_qr = identificador

# Usa a função Gerar_qrcode para gerar o caminho da imagem PNG do QRcode. A odp aí é apenas pq a função gerar-qrcode exige esses 2 parâmetros
        caminho_qr = gerar_qrcode(texto_qr,ordem["odp"])

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

def salvar_rastreabilidade(rastreabilidade):

        caminho = "temporario/rastreabilidade.json"

        with open( caminho, "w", encoding= "utf-8") as arquivo:
                json.dump(rastreabilidade,arquivo,ensure_ascii=False,indent=4)

def carregar_rastreabilidade():

    caminho = "temporario/rastreabilidade.json"

    if not os.path.exists(caminho):
        return {}

    with open(caminho, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)

def buscar_rastreabilidade(identificador):

    rastreabilidade = carregar_rastreabilidade()

    if identificador not in rastreabilidade:
        return None
       
    return rastreabilidade[identificador]

def formatar_data_aba(data):

    return(
              data[:2] + "-" +
              data[2:4] + "-" +
              data[4:]
       )

def localizar_aba(dados):
    data = formatar_data_aba(dados["data"])

    nome_aba = f"{data}_{dados['turno']}"

    caminho_saida = f"temporario/ODP_{dados['operador']}.xlsx"

    planilha = load_workbook(caminho_saida)

    if nome_aba in planilha.sheetnames:
        aba = planilha[nome_aba]

        linha = localizar_odp(aba,dados["odp"])

        return {
            "arquivo": caminho_saida,
            "aba": nome_aba,
            "linha": linha
		}
    else:
        return None

def localizar_por_identificador(identificador):

	dados = buscar_rastreabilidade(identificador)

	if dados is None:
		return None

	localizacao = localizar_aba(dados)

	if localizacao is None:
		return None

	return localizacao

	