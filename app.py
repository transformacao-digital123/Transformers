from flask import Flask, render_template, request, send_file

import traceback

#importações vindas de outros arquivos
from servicos.conversor import converter_pdf
from servicos.google_sheet import converter_google_sheets, criar_zip
from servicos.tratador_erros import tratar_erro
from servicos.qrcode import buscar_rastreabilidade, localizar_aba
from servicos.apontamento import atualizar_odp

app = Flask(__name__)

# Comandos padrão do Flask para organizar o acesso a página Web
@app.route("/", methods = ["GET", "POST"])
def home():

    if request.method == "POST":
            
# Linhas responsáveis por determinar que somente arquivos PDF e linhas do DOCS serão importados 
            arquivo = request.files.get("pdf")

            link = request.form.get("link")
            
# Esse try e execpt são uma prevenção, caso o usuário envie algum arquivo que não seja correspondente ao que queremos, ele enviará essa mensagem de erro e o programa continuará a funcionar normalmente            
            try:

# Condicionamento para ver se será arquivo ou google sheet
                    if arquivo:

# Comando, com uma nova "variável arquivo_excel" que puxa do conversor o arquivo já pronto e lapidado e só espera ser chamado para lançado no sistema
                        arquivo_saida = converter_pdf(arquivo)

                    elif link:
                          arquivo_saida = converter_google_sheets(link)
                    else:
                          render_template("index.html", erro = "Selecione um PDF ou insira um link do google-sheet")
                
#Ele lança o arquivo no sistema
                    return send_file(arquivo_saida)

            except Exception as erro:

                    traceback.print_exc()
                    print(type(erro))
                    print(erro)
                    
                    mensagem  = tratar_erro(erro)

            return render_template("index.html", erro = mensagem)
                

#Enquanto nada for enviado ainda será um GET, logo, enquanto isso, afim de evitar erro, o programa pula para as linha anteriores para que a página possa ser aberta, carregando a página através do arquivo HTML
    return render_template(
        "index.html")

@app.route("/camera")
def camera():
    return render_template("camera.html")

@app.route("/buscar-rastreabilidade",methods = ["POST"])
def buscar_rastreabilidade_api():

# Transforma os dados recebidos em JSON e transforma em um dicionário python
    texto = request.get_json()

    print("=== BUSCAR RASTREABILIDADE ===")
    print("JSON RECEBIDO:", texto)

    identificador = texto["identificador"]
    print("IDENTIFICADOR RECEBIDO:", identificador)

    dados = buscar_rastreabilidade(identificador)
    print("DADOS ENCONTRADOS:", dados)

    if dados is None:
          return {"Erro": "identificador não encontrado"}, 404

    localizacao = localizar_aba(dados)

    print("LOCALIZAÇÃO ENCONTRADA: ", localizacao)

    if localizacao is None:
          return {"Erro": "não foi possível localizar a OdP"}, 404

    print("DADOS:", dados)
    print("LOCALIZAÇÃO:", localizacao)

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

    print("=== ATUALIZAÇÃO RECEBIDA ===")
    print("DADOS:", texto)

    identificador = texto["identificador"]

    print("IDENTIFICADOR:", identificador)

    dados = buscar_rastreabilidade(identificador)

    print("DADOS ENCONTRADOS:", dados)

    if dados is None:
        print("ERRO: IDENTIFICADOR NÃO ENCONTRADO")
        return {"Erro": "Identificador não encontrado"}, 404
      
    localizacao = localizar_aba(dados)

    print("LOCALIZAÇÃO:", localizacao)

    if localizacao is None:
        print("ERRO: ODP NÃO ENCONTRADA")
        return {"Erro": "ODP não encontrada"}, 404

    print("CHAMANDO ATUALIZAR_ODP")

    atualizar_odp (
        localizacao["arquivo"],
        localizacao["aba"],
        localizacao["linha"],
        identificador,
        texto
    )

    return {
         "mensagem": "Dados atualizados com sucesso",
         "arquivo": localizacao["arquivo"],
         "aba": localizacao["aba"],
         "linha": localizacao["linha"]
    }
if __name__ == "__main__":
    app.run(debug=True)
