from flask import Flask, render_template, request, send_file

#importações vindas de outros arquivos
from servicos.conversor import converter_pdf
from servicos.google_sheet import converter_google_sheets
from servicos.tratador_erros import tratar_erro

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
                        arquivo_excel = converter_pdf(arquivo)

                    elif link:
                          arquivo_excel = converter_google_sheets(link)
                    else:
                          render_template("index.html", erro = "Selecione um PDF ou insira um link dom google-sheet")
                
#Ele lança o arquivo no sistema
                    return send_file(arquivo_excel)

            except Exception as erro:
                    mensagem  = tratar_erro(erro)

            return render_template("index.html", erro = mensagem)
                

#Enquanto nada for enviado ainda será um GET, logo, enquanto isso, afim de evitar erro, o programa pula para as linha anteriores para que a página possa ser aberta, carregando a página através do arquivo HTML
    return render_template(
        "index.html")

if __name__ == "__main__":
    app.run(debug=True)