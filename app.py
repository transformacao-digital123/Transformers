from flask import Flask, render_template, request, send_file
from openpyxl import load_workbook
import os
import traceback
from datetime import datetime
import uuid

#importações vindas de outros arquivos
from servicos.conversao.conversor import converter_pdf
from servicos.orquestradror.google_sheet import converter_google_sheets
from servicos.validacao.tratador_erros import tratar_erro
from servicos.progresso.progresso import (obter_progresso,atualizar_progresso)
from servicos.rastreabilidade.consultar_rastreabilidade import consultar_rastreabilidade
from servicos.rastreabilidade.atualizar_rastreabilidade import atualizar_rastreabilidade
from servicos.rastreabilidade.rastreabilidade import localizar_por_identificador
from servicos.validacao.exceptions import RastreabilidadeNaoEncontradaError
from servicos.rastreabilidade.despacho import preencher_despacho
from servicos.armazenamento import pasta_arquivos

AMBIENTE = os.getenv("AMBIENTE","local")

app = Flask(__name__)

@app.route("/progresso")
def progresso():

# O args aqui serve para capturar os valores que estiverem depois do ? em uma URL, ex: ?id_conversao=123456
    id_conversao = request.args.get("id_conversao")

    if not id_conversao or  len(id_conversao) != 32 or any(
        caractere not in "0123456789abcdef"
        for caractere in id_conversao
    ):
        return {"erro": "Identificador de conversão inválido"}, 400

    estado = obter_progresso(id_conversao)

    if estado is None:
        return {"erro": "Conversão não encontrada"}, 404
    
    return estado

# Estão aqui e não no home para que não sejam reiniciados para estarem vazios toda vez que a função roda, nesse caso ele só será acrescentado sendo chamado apenas quando convém
etiquetas_geradas = []
arquivo_gerado = None

# Comandos padrão do Flask para organizar o acesso a página Web
@app.route("/", methods = ["GET", "POST"])
def home():

    global arquivo_gerado

    if request.method == "POST":

# O request.form contém os campos enviados pelo formulário, como o do input, e .get("id_conversao") serve pra procurar o campo com esse nome
            id_conversao = request.form.get("id_conversao")

# Verifica se o id_conversao está ausente ou vazio ou se o Nº de caracteres é diferente de 32, que é o formato do uuid.uuid4().hex, ou se algum dos caracteres está fora do conjunto permitido
            if not id_conversao or len(id_conversao) != 32 or any(

# Aqui ele faz uma verificação procuranado por cada caractere dentro de id_conversao, se um estiver fora do padrão como "g" retrona False, caso contrário True e atualiza o progresso
# Isso acontece da seguinte forma o 2º caractere avalia cada caractere em id_conversao, já o 1° avalia se em caractere está algum valor que não seja "0123456789abcdef"
                caractere not in "0123456789abcdef"
                for caractere in id_conversao
            ):
                return {"sucesso": False, "erro": "Identificador de conversão inválido"}, 404

# Aqui essa função será responsável por criar o .json para aquela conversão com progresso inicial de 0% e status "processando"
            atualizar_progresso(id_conversao,0)
            
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
                        arquivo_gerado, etiquetas = converter_google_sheets(link, id_conversao, acrescentar)

                        etiquetas_geradas.clear()
                        etiquetas_geradas.extend(etiquetas)

                    else:

                        mensagem = "Selecione um PDF ou um link do Google-Sheets"

                        atualizar_progresso(id_conversao,0,status="erro",erro=mensagem)

                        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                             return {
                                  "sucesso": False,
                                  "erro": mensagem
                                  }, 400

                        return render_template("index.html",
                                               erro = mensagem,
                                               ambiente = AMBIENTE,
                                               id_conversao = id_conversao)

# Aqui Vamos não só gravar o estado atualizado no JSON da conversão como vamos deixar o caminho do arquivo absoluto, se antes estava temporario/resultado.zip, agora ficará algo como C:\\Projetos\\Transformers\\temporario\\resultado.zip
                    atualizar_progresso(id_conversao,100,status="concluido", arquivo = os.path.abspath(arquivo_gerado))

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

# Aqui informaremos o atualizador de progresso caso o sistema falhe
                    atualizar_progresso(id_conversao, 0, status = "erro", erro=mensagem)

                    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                        return {
                            "sucesso": False,
                            "erro": mensagem}, 400

            return render_template("index.html",
                                   erro = mensagem,
                                   ambiente = AMBIENTE)

#Aqui, enquanto o método é GET,já que nada foi enviado ainda, podemos deixá-lo aqui, pois GET representa os valores que o programa envia, e não que nós enviamos
# Gera um identificador de 32 caracteres na versão 4
    id_conversao = uuid.uuid4().hex

# Se não fosse por essa função se encontrar aqui o programa faria a consulta por progresso a cada 500ms, e caso o programa nãop tivesse começado ainda, daria um erro 404
    atualizar_progresso(id_conversao, 0)

# Enquanto nada for enviado ainda será um GET, logo, enquanto isso, afim de evitar erro, o programa pula para as linha anteriores para que a página possa ser aberta, carregando a página através do arquivo HTML
    return render_template(
        "index.html",
        ambiente = AMBIENTE,
        id_conversao = id_conversao)

@app.route("/baixar-arquivo", methods = ["GET"])
def baixar_arquivo():

    id_conversao = request.args.get("id_conversao")

# Se o id_conversao estiver vazio, não contiver nenhum dos 16 caracteres ou não tiver 32 digitos retorna o erro
    if not id_conversao or len(id_conversao) != 32 or any(
        caractere not in "0123456789abcdef"
        for caractere in id_conversao
    ):
        return {"erro": "Identificador de conversão inválido"},400

# Guarda em .json os dados do progresso
    estado = obter_progresso(id_conversao)

# Se estado estiver vazio dá erro
    if estado is None:
        return {"erro": "Conversão nãoencontrada"},404

# Se em estado o status não for concluido dá erro
    if estado.get("status") != "concluido":
        return { "erro": "A conversão ainda não foi concluída"}, 404

# Em estado o "arquivo" contém o caminho absoluto do arquivo, ou seja, completo
    caminho_arquivo = estado.get("arquivo")

# Se o caminho_arquivo estiver vazio ou se não existir dá erro
    if not caminho_arquivo or not os.path.isfile(caminho_arquivo):
        return {"erro": "Arquivo não encontrado"},404

# Envia a pasta contendo o arquivo para a interface do usuário
    return send_file(
        caminho_arquivo,
        as_attachment=True,
        download_name=os.path.basename(caminho_arquivo)
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

    dados = request.get_json(silent=True) or {}

    identificador = dados.get("identificador")
    numero_pallet = dados.get("numero_pallet")

    print(f"IDENTIFICADOR: {identificador}")
    print(f"NUMERO_PALLET: {numero_pallet}")

    cancelar = dados.get("cancelar", False)

    if not identificador or not numero_pallet:
        return {
            "sucesso": False,
            "erro": "Identificador ou número do pallet não informado"
        }, 404

    print(f"ROTA: {repr(numero_pallet)}")

    localizacao = localizar_por_identificador(identificador, numero_pallet)

    if localizacao is None:
        return {
            "sucesso": False,
                "erro": "identificador não encontrado"
        }, 404

    resultado = preencher_despacho(
        localizacao["arquivo"],
        localizacao["aba"],
        localizacao["linha"],
        cancelar = cancelar
    )

    if resultado.get("cancelado"):
        return{
            "sucesso": True,
            "cancelado": True,
            "hora_despacho": "",
            "numeroPallet": numero_pallet,
            "identificadorAtual": identificador
        }

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

    planilha = load_workbook(localizacao["arquivo"], data_only=True)
    aba = planilha[localizacao["aba"]]
    linha = localizacao["linha"]

    op_material = aba[f"I{linha}"].value
    op_tubete = aba[f"J{linha}"].value

    planilha.close()

# Ao dar o último return o Flask sempre irá transformar o texto novamente em string para que ele possa navegar pela rede
    return {
          "odp": dados["odp"],
          "operador": dados["operador"],
          "maquina": dados["maquina"],
          "data": dados["data"],
          "turno": dados["turno"],
          "cliente": dados["cliente"],
          "numero_pedido": dados["numero_pedido"],
          "op_material": op_material,
          "op_tubete": op_tubete,
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

# Serve para ser usado como o filtrador da data e turno quando for solicitado a visualização da planilha
@app.route("/opcoes-acompanhamento")
def opcoes_acompanhamento():
    arquivos = []

# Aqui será feito uma verificação, através do nome do caminho, de todos os caminhos dos arquivos
    for nome in os.listdir(pasta_arquivos()):

# Se, tudo em minúsculo, o caminho terminar em ".xlsx" ou começar com "~$", representa arquivos temporários ocultos que o próprio excel cria quando está aberto, simplesmente continue
        if not nome.lower().endswith(".xlsx") or nome.startswith("~$"):
            continue

# Pega e faz a separação do nome do arquivo com sua terminação(.xlsx), em que ele pegará pra guardar apenas o 1° valor
        base = os.path.splitext(nome)[0]

# Aqui ele irá separar o texto em 3 partes através do "_", a data, o próprio _, e o turno
        data_texto, separador, turno = base.partition("_")

# aqui verificará se tem o separador("_") e o turno depois dele, caso esteja fora do padrão ele apenas dará continue e seguirá reto
        if not separador or not turno:
            continue

# Aqui faremos uma verificação, se a sata que for passada for uma data convencional n~so acontecerá nada demais, caso contrário, caso haja algo como dia 32 ela dará erro
# Aqui há 2 formatações de data,isso se deve porque a 1º está ali para a nossa visualização, já que usamos o método brasileiro, enquanto o 2º serve para enviar para o servidor qual a data, pois o sistema funciona no método americano, mas isso não afetará nada no nosso cotidiano, é apenas uma forma de evitar bug
        try:
            data = datetime.strptime(
                data_texto, "%d-%m-%Y"
            ).strftime("%Y-%m-%d")
        except ValueError:
            continue

# Guarda em arquivos o nome, data e turno do arquivo
        arquivos.append({
            "nome": nome,
            "data": data,
            "turno": turno
        })

# Retorna em um formato que o.json consiga entender para que quem o chamou possa processar os dados
    return {"arquivos": arquivos}

@app.route("/dados-acompanhamento")
def dados_acompanhamento():

# Aqui ele pegará o URL que está no momento, por exemplo /dados-acompanhamento?arquivo=planilha_manha.xlsx, e pegará tudo o que tiver depois de arquivo e guardará na nova variável arquivo
    nome_arquivo = request.args.get("arquivo")

# Aqui é uma verificação, se não houver nem o nome do arquivo nem se existe um arquivo com esse nome no servidor, retornará erro, se não apenas irá continuar reto
    if not nome_arquivo:
        return {"Erro": "Arquivo não encontrado"}, 404

    caminho = (os.path.join(pasta_arquivos(), nome_arquivo))

    planilha = load_workbook(caminho, data_only=True)

    dados = []

# Aqui ele verificará todas as abas daquele arquivo,no caso só 1
    for aba in planilha.worksheets:

# Irá analisar todas as linhas, começando da 6 até a última linha preenchida (isso devido ao + 1)
        for linha in range(6, aba.max_row + 1):

            valores = []

# Aqui irá fazer uma análise de C a X e acrescentará em valores os valores que estiverem nas células analisadas
            for coluna in range(3, 25):  # C até X
                valores.append(aba.cell(linha, coluna).value)

# Se a linha tiver ao menos 1 valor em valores ele seguirá seu rumo como deveria, se não dará erro
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

    for nome in os.listdir(pasta_arquivos()):

        if nome.endswith(".xlsx"):

            arquivos.append(nome)

    return {"arquivos": arquivos}

@app.route("/rastreabilidade")
def rastreabilidade():
    return render_template("rastreabilidade.html")

@app.route("/baixar-acompanhamento")
def baixar_acompanhamento():

    nome_arquivo = request.args.get("arquivo")

    if not nome_arquivo:
        return {"Erro": "Arquivo não informado"}, 400

    caminho = os.path.join(pasta_arquivos(), nome_arquivo)

    if not os.path.exists(caminho):
        return {"Erro": "Arquivo não encontrado"}, 404

    return send_file(
        caminho,
        as_attachment=True,
        download_name=nome_arquivo
    )

if __name__ == "__main__":
    app.run(debug=True)