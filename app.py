from flask import Flask, render_template, request, send_file
from openpyxl import load_workbook
import os 
import traceback
from datetime import datetime

#importações vindas de outros arquivos
from servicos.conversao.conversor import converter_pdf
from servicos.orquestradror.google_sheet import converter_google_sheets
from servicos.validacao.tratador_erros import tratar_erro
from servicos.progresso.progresso import obter_progresso
from servicos.rastreabilidade.consultar_rastreabilidade import consultar_rastreabilidade
from servicos.rastreabilidade.atualizar_rastreabilidade import atualizar_rastreabilidade
from servicos.rastreabilidade.rastreabilidade import localizar_por_identificador
from servicos.validacao.exceptions import RastreabilidadeNaoEncontradaError

from servicos.rastreabilidade.despacho import preencher_despacho

AMBIENTE = os.getenv("AMBIENTE","local")

app = Flask(__name__)

@app.route("/progresso")
def progresso():
    return {"progresso": obter_progresso()}

# Estão aqui e não no home para que não sejam reiniciados para estarem vazios toda vez que a função roda, nesse caso ele só será acrescentado sendo chamado apenas quando convém
etiquetas_geradas = []
arquivo_gerado = None

# Comandos padrão do Flask para organizar o acesso a página Web
@app.route("/", methods = ["GET", "POST"])
def home():

    global arquivo_gerado

    if request.method == "POST":
            
# Linhas responsáveis por determinar que somente arquivos PDF e linhas do DOCS serão importados, ou seja, faz a filtragem, apenas se atender a esses 3 requisitos é que o processamento começa
            arquivo = request.files.get("pdf")

            link = request.form.get("link")

            acrescentar = request.form.get("acrescentar") == "sim"
            
# Esse try e execpt são uma prevenção, caso o usuário envie algum arquivo que não seja correspondente ao que queremos, ele enviará essa mensagem de erro e o programa continuará a funcionar normalmente            
            try:

# Condicionamento para ver se será arquivo ou google sheet
                    if arquivo:

# Comando, com uma nova "variável arquivo_excel" que puxa do conversor o arquivo já pronto e lapidado e só espera ser chamado para lançado no sistema
                        arquivo_gerado = converter_pdf(arquivo)

                    elif link:
                        arquivo_gerado, etiquetas = converter_google_sheets(link, acrescentar)

                        etiquetas_geradas.clear()
                        etiquetas_geradas.extend(etiquetas)

                    else:
                        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                             return {
                                  "sucesso": False,
                                  "erro": "Selecione um PDF ou insira um link do google-sheet"
                                  }, 400

                        return render_template("index.html",
                                               erro = "Selecione um PDF ou insira um link do google-sheet",
                                               ambiente = AMBIENTE)

# Condicionamento para ver se a requisição é AJAX ou não, caso seja, ele retorna um JSON com a mensagem de sucesso, caso contrário, ele retorna o arquivo para download
                    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                        return {"sucesso": True}
              
# Ele lança o arquivo no sistema
                    return send_file(arquivo_gerado)

            except Exception as erro:

                    traceback.print_exc()
                    print(type(erro))
                    print(erro)
                    
                    mensagem  = tratar_erro(erro)

                    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                        return {
                            "sucesso": False,
                            "erro": mensagem}, 400

            return render_template("index.html",
                                   erro = mensagem,
                                   ambiente = AMBIENTE)
                

# Enquanto nada for enviado ainda será um GET, logo, enquanto isso, afim de evitar erro, o programa pula para as linha anteriores para que a página possa ser aberta, carregando a página através do arquivo HTML
    return render_template(
        "index.html",
        ambiente = AMBIENTE)

@app.route("/baixar-arquivo", methods = ["GET"])
def baixar_arquivo():

    if arquivo_gerado is None:
        return {"Erro": "Nenhum arquivo foi gerado"}, 404

    if not os.path.exists(arquivo_gerado):
        return{"Erro": "Arquivo não encontrado"},404

    return send_file(
        arquivo_gerado,
        as_attachment=True,
        download_name=os.path.basename(arquivo_gerado)
    )

@app.route("/imprimir-etiquetas", methods = ["POST"])
def imprimir_etiquetas():

    try:

# Essa importação, em Windows, está dentro dessa função porque assim, quando estiver no Render, que funciona em Linux, não dá problema,já que ela está aqui para ser importada somente quando for solicitada
        from servicos.etiquetas.imprimir_etiqueta import imprimir_etiqueta

        for etiqueta in etiquetas_geradas:
            imprimir_etiqueta(etiqueta)

        return {
            "sucesso": True
        }
    except Exception as erro:

        traceback.print_exc()

        mensagem = tratar_erro(erro)

        return {
            "sucesso": False,
            "erro": mensagem  
        }, 400

@app.route("/camera")
def camera():
    return render_template("camera.html")

@app.route("/despacho")
def despacho():
    return render_template("despacho.html")

@app.route("/registrar-despacho", methods = ["POST"])
def registrar_despacho():

    dados = request.get_json()
    identificador = dados.get("identificador")

    print(f"IDENTIFICADOR: {identificador}")

    localizacao = localizar_por_identificador(identificador)

    if localizacao is None:
        return {
            "sucesso": False,
                "erro": "identificador não encontrado"
        }, 404

    resultado = preencher_despacho(
        localizacao["arquivo"],
        localizacao["aba"],
        localizacao["linha"]
    )

# Aqui é que se o valor de novo for false porque if not True: = if False:
    if not resultado["novo"]:
        return {
            "sucesso": True,
            "ja_despachado": True,
            "hora_despacho": resultado["hora_despacho"]
        }
# Se for true
    return {
        "sucesso": True,
        "hora_despacho": resultado["hora_despacho"]
    }

@app.route("/buscar-rastreabilidade",methods = ["POST"])
def buscar_rastreabilidade_api():

# Transforma os dados recebidos em JSON e transforma em um dicionário python
    texto = request.get_json()

    identificador = texto["identificador"]

    resultado = consultar_rastreabilidade(identificador)

    if resultado is None:
        raise RastreabilidadeNaoEncontradaError()

    dados = resultado["dados"]
    localizacao = resultado["localizacao"]

# Ao dar o último return o Flask sempre irá transformar o texto novamente em string para que ele possa navegar pela rede
    return {
          "odp": dados["odp"],
          "operador": dados["operador"],
          "maquina": dados["maquina"],
          "data": dados["data"],
          "turno": dados["turno"],
          "cliente": dados["cliente"],
          "numero_pedido": dados["numero_pedido"],
          "arquivo": localizacao["arquivo"],
          "aba": localizacao["aba"],
          "linha": localizacao["linha"]
    }

@app.route("/atualizar-rastreabilidade",methods=["POST"])
def atualizar_rastreabilidade_api():

# Ele recebe todos os dados q1ue o servidor enviar e converte de JSON para dicionário do python para que o seu programa possa usá-lo
    texto = request.get_json()

    identificador = texto["identificador"]

    resultado = atualizar_rastreabilidade(identificador,texto)

    if resultado is None: 
        return {"Erro": "não foi possível localizar a rastreabilidade"}, 404

    localizacao = resultado["resultado"]

    return {
         "mensagem": "Dados atualizados com sucesso",
         "resultado": localizacao
    }

@app.route("/acompanhamento")
def acompanhamento():
    return render_template("acompanhamento.html")

@app.route("/dados-acompanhamento")
def dados_acompanhamento():

    arquivo = request.args.get("arquivo")

    if not arquivo or not os.path.exists(arquivo):
        return {"Erro": "Arquivo não encontrado"}, 404

    planilha = load_workbook(arquivo, data_only=True)

    dados = []

    for aba in planilha.worksheets:

        for linha in range(6, aba.max_row + 1):

            valores = []

            for coluna in range(3, 24):  # C até W
                valores.append(aba.cell(linha, coluna).value)

            # ignora linhas completamente vazias
            if any(valor is not None for valor in valores):
                dados.append({
                    "aba": aba.title,
                    "linha": linha,
                    "valores": valores
                })

    planilha.close()

    return {"dados": dados}

@app.route("/arquivos-acompanhamento")
def arquivos_acompanhamento():

    arquivos = []

    for nome in os.listdir("temporario"):

        if nome.endswith(".xlsx"):

            arquivos.append(nome)

    return {"arquivos": arquivos}

@app.route("/rastreabilidade")
def rastreabilidade():
    return render_template("rastreabilidade.html")

@app.route("/baixar-acompanhamento")
def baixar_acompanhamento():

    print("ENTROU NA ROTA DE DOWNLOAD")

    nome_arquivo = request.args.get("arquivo")

    if not nome_arquivo:
        return {"Erro": "Arquivo não informado"}, 400

    arquivo = nome_arquivo

    print("ARQUIVO RECEBIDO:", nome_arquivo)
    print("CAMINHO PROCURADO:", arquivo)

    if not os.path.exists(arquivo):
        return {"Erro": "Arquivo não encontrado"}, 404

    return send_file(
        arquivo,
        as_attachment=True,
        download_name=nome_arquivo
    )

if __name__ == "__main__":
    app.run(debug=True)