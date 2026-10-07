# Serve pra lidar com criação,validação ou leitura de arquivos
import os

# Serve para copiar ou mover arquivos
import shutil

# O os.getenv dá uma ordem ao Python de ir até o sistema operacional e procurar por uma variável, no caso AMBIENTE, se não achar,usa "local", no lugar
AMBIENTE = os.getenv("AMBIENTE", "local")

# Quando o ambiente for local o nome da pasta será "temporario", se for diferente, "storage"
PASTA_LOCAL = "temporario"
PASTA_STORAGE = "storage"

def pasta_arquivos():
    if AMBIENTE == "local":
        return PASTA_LOCAL
    return PASTA_STORAGE

# Salva o arquivo em um armazenamento adequado ao ambiente (local ou cloud)
def salvar_arquivo(caminho_origem,nome_arquivo):

# Guarda qual vai ser a pasta
    pasta = pasta_arquivos()

# Se a pasta temporario não existir, cria ela. Caso a pasta já tenha sido criada antes o exist_ok=True evita do programa dar erro
    os.makedirs(pasta, exist_ok = True)

# Junta o nome do arquivo e o nome da pasta em um único caminho, que será  destino do arquio
    destino = os.path.join(pasta, nome_arquivo)

# Copia o arquivo de origem para o destino, mantendo as informações do arquivo original. O copy2 é usado porque ele também tenta preservar os metadados do arquivo original (como a data de criação e modificação)
    shutil.copy2(caminho_origem,destino)

# Retorna o caminho onde o arquivo foi salvo
    return destino

# Retorna onde o arquivo deve ser retornado, pro local ou storage, que serve pro Render
# Ele se repete em algumas funções, mas é necessário, por questões de boas práticas, para que o código funcione corretamente, pois ele é usado em várias partes do código e não seria viável usar afunção salvar_arquivo, já que ela faz mais do que isso e assim gerar confusão
def caminho_arquivo(nome_arquivo):

# Guarda o caminho do arquivo
    return os.path.join(pasta_arquivos(), nome_arquivo)

# Verifica se o arquivo existe no armazenamento atual
def arquivo_existe(nome_arquivo):

# Retorna True se o arquivo existir e False se não existir, usando a função os.path.exists() que verifica se o caminho do arquivo existe ou não
    return os.path.exists(caminho_arquivo(nome_arquivo))

# Apaga um arquivo do armazenamento atual
def apagar_arquivo(nome_arquivo):

# Guarda na variável "caminho" o caminho do arquivo, obtido graças a função caminho_arquivo
    caminho = caminho_arquivo(nome_arquivo)

# Se o arquivo existir, ele será apagado e removido do sistema operacional
    if os.path.exists(caminho):
        os.remove(caminho)