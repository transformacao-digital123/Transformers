import secrets
from openpyxl import load_workbook
import os
import json
from zipfile import BadZipFile

from servicos.validacao.exceptions import OdpNaoEncontradaError,PlanilhaNaoEncontradaError,PlanilhaCorrompidaError

def gerar_identificador():

# token_hex(4): Pede para o sistema gerar 4 bytes, cada byte representa um caracter, de dados aleatórios e transformá-los em uma string no formato hexadecimal (que usa números de 0 a 9 e letras de A a F).
    return "LUARI - " + secrets.token_hex(4).upper()

def salvar_rastreabilidade(rastreabilidade):

        caminho = "temporario/rastreabilidade.json"

        with open( caminho, "w", encoding= "utf-8") as arquivo:
                json.dump(rastreabilidade,arquivo,ensure_ascii=False,indent=4)

def carregar_rastreabilidade():

    caminho = "temporario/rastreabilidade.json"

    print("BUSCANDO RASTREABILIDADE EM:", os.path.abspath(caminho))
    print("ARQUIVO EXISTE?", os.path.exists(caminho))

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

    turno = dados["turno"]

    nome_arquivo = f"{data}_{turno}.xlsx"

    caminho_saida = os.path.join(f"temporario",nome_arquivo)

    if not os.path.exists(caminho_saida):

        raise PlanilhaNaoEncontradaError()

    try:
    
        planilha = load_workbook(caminho_saida)

    except BadZipFile:
         raise PlanilhaCorrompidaError()

    aba = planilha.active

    for aba in planilha.worksheets:

        for linha in range(6, aba.max_row + 1):                

            if str(aba[f"D{linha}"].value) == str(dados["odp"]).strip():
                    print("ODP encontrada na linha:", linha)

                    return {
                            "arquivo": caminho_saida,
                            "aba": aba.title,
                            "linha": linha
                            }
        raise OdpNaoEncontradaError()

def localizar_por_identificador(identificador):

	dados = buscar_rastreabilidade(identificador)

	if dados is None:
		return None

	localizacao = localizar_aba(dados)

	if localizacao is None:
		return None

	return localizacao