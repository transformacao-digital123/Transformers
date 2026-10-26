import os,json,re,tempfile

# A id_conversao identifica qual conversão estamos atualizando.

# O tempFile.gettempdir() serve pra descobrir o diretório temporário do sistema operaciona: Windows: C:\Users\Usuario\AppData\Local\Temp enquanto em Linux/Render: /tmp
# O os.path.join pega e combina e cria um único caminho com o DIRETORIO_ESTADOS sendo a pasta e transformers_estados sendo parte do caminho dela, então quando for chamada, DIRETORIO_ESTADOS = "/tmp/transformers_estados", e então o arquivo .json será posto dentro dessa pasta
DIRETORIO_ESTADOS =  os.path.join(tempfile.gettempdir(),"transformers_estados")

# O os.makedirs serve para então para criar de fato a pasta
# Caso a pasta já exista o exist_ok=True evita que gere erro por causa disso
os.makedirs(DIRETORIO_ESTADOS,exist_ok=True)

processamento_progresso = 0

# Essa função terá um chamado nos respectivos lugares que quiserem demarcar uma evolução, a cada chamado representa um aumento de porcentagem, por exemplo, quando chamarem ele nos 10%, esse 10 substituirá o valor que estiver em processamento_progresso, e assim por diante, até chegar a 100% que é o final do processo
def atualizar_progresso(id_conversao, valor, status = "processando", arquivo = None, erro = None):

# Aqui pegamos e criamos um caminho que se encaixará o arquivo .json na pasta do diretório,ex: "/tmp/transformers_estados/abcde.json"
    caminho = os.path.join(DIRETORIO_ESTADOS, f"{id_conversao}.json")

# Aqui é montado um dicionário em python com os dados de conversão
# Sendo valor o a % em que o Optimus se encontra do progresso da conversão; Status informa se está processando, concluída ou se deu erro; Arquivo guarda o caminho do arquivo quando for gerado no final; E erro guarda a mensagem de erro caso ocorra
    estado = {
        "progresso": valor,
        "status": status,
        "arquivo": arquivo,
        "erro": erro
    }

# Aqui será criada o arquivo_json que usará o caminho que criamos e será usado para guardar os dados transformados em .json, o "w" criará o arquivo caso não exista e o substituirá caso já exista
    with open(caminho, "w", encoding="utf-8") as arquivo_json:

# Transforma o dicionário em .json e guarda os dados no arquivo
# O ensure_ascii = False permite usar letras com acento e ç
        json.dump(estado, arquivo_json, ensure_ascii = False)  

    global processamento_progresso
    processamento_progresso = valor

# Ele retorn o valor que estiver em processamento_progresso e envia para a rota /progresso, que é o que o front-end vai usar para mostrar a evolução do processo
def obter_progresso():

    return processamento_progresso