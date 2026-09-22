import pdfplumber

#importações vindas de outros arquivos
from servicos.validacao.exceptions import(
    DataNaoEncontradoError,
    NumeroPedidoNaoEncontrado,
    ClienteNaoEncontradoError,
    PadraoNaoEncontradoerror,
    FilmeNaoEncontradoerror,
)

def pegar_cliente(linhas):
                
    for linha in linhas:
        if "Cliente" in linha:

# Comando para saber as posições das variáveis

            posicao = linha.find("Cliente")
            inicio = posicao + len("Cliente ")

            cliente = linha[inicio:]

            return cliente
    raise ClienteNaoEncontradoError()
        
def pegar_data(linhas):
                
    for linha in linhas:
        if "data de entrega" in linha:
            
            # Outro exemplo de como fazer a mesma coisa

            inicio = linha.find("data de entrega")
            inicio += inicio + len("data de entrega ")

            data = linha[inicio:]

            return data
    raise DataNaoEncontradoError()
        
def pegar_numero_pedido(linhas):
                
    for linha in linhas:
        if "Pedido de Venda" in linha:

            posicao = linha.find("Pedido de Venda")
            inicio = posicao + len("Pedido de Venda ")

            numero_pedido = linha[inicio:]

            return numero_pedido
    raise NumeroPedidoNaoEncontrado()
        
def pegar_filme(linhas):

    #filme = ""
                
    for linha in linhas:
        if "FILME" in linha:

            posicao = linha.find("FILME")
            inicio = posicao + len("FILME ")

            filme = linha[inicio:inicio+3] + "A"

            return filme
    raise FilmeNaoEncontradoerror()
        
def pegar_peso_tubete(linhas):

 #Variável vazia para que caso o valor não seja encontrado não seja convertido em none e dê erro no programa   
    peso_tubete = ""
                
    for linha in linhas:
        if "FILME +" in linha:

            posicao = linha.find("FILME +")
            inicio = posicao + len("FILME + ")

            peso_tubete = linha[inicio:inicio+2] + "KG"

            return peso_tubete

#TALVEZ EU TENHA ERRADO
      
def pegar_padrao(linhas):
    padrao = ""
    palavra2 = ""
         
    for linha in linhas:
        if "- (" in linha:
            palavras = linha.split(" ")
        
            for palavra in palavras:

 #Retira os parênteses que estão ligados aos numeros por valores vazios
                palavra1 = palavra.replace("(", "")
                palavra2 = palavra.replace(")", "")

#se palavara é um digito
                if palavra.isdigit():

                    padrao = palavra1 + " + " + palavra2

                    return padrao
    raise PadraoNaoEncontradoerror()


# Função extrair os dados e lapidá-los para serem postos na planilha do Excel
def processar_pdf(arquivo):

# Abre o arquivo PDF na variável pdf
        with pdfplumber.open(arquivo) as pdf:

# Abre a página que for solicitada
                    pagina = pdf.pages[0]
# Abre o conteúdo que estiver nessa página                
                    texto = pagina.extract_text()

# Separação de conteúdo por linha
                    linhas = texto.split("\n")

# Dados do PDF
                    data = pegar_data(linhas)

                    numero_pedido = pegar_numero_pedido(linhas)

                    cliente = pegar_cliente(linhas)
                    
                    padrao = pegar_padrao(linhas)

                    filme = pegar_filme(linhas) #+ "A"

                    peso_tubete = pegar_peso_tubete(linhas) #+ "KG"

                    dados = {
                                "data": data,
                                "numero_pedido": numero_pedido,
                                "cliente": cliente,
                                "padrao": padrao,
                                "filme": filme,
                                "peso_tubete": peso_tubete
                            }

                    return dados
    
        raise