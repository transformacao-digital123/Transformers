def extrair_filme(parte_esquerda):
    filme = parte_esquerda.split(" ")
    return filme[0]

def extrair_pesos(parte_direita):

# Validação dos pesos
    pesos = parte_direita.split(" + ")
    
    if len(pesos) > 1:
        peso_esquerdo = pesos[0]
        peso_direito = pesos[1]
    else:
        peso_esquerdo = pesos[0]
        peso_direito = ""
    
# Responsável por descobrir o valor do peso do filme
    peso_filme = peso_esquerdo.split(" ")
    peso_filme = peso_filme[0].replace("(", "")
    
    # Responsável por descobrir o valor do peso do tubete
    if len(pesos)> 1:
        peso_tubete = peso_direito.split(" ")
        peso_tubete = peso_tubete[0]
    else:
        peso_tubete = ""

    return peso_filme,peso_tubete

def extrair_padrao(peso_filme,peso_tubete):
# Responsável por descobrir o padrão
    if len(peso_tubete) > 0:
        padrao = f"{peso_filme} + {peso_tubete}"
    else:
        padrao = f"{peso_filme}"

    return padrao

def interpretar_largura_micra(texto):

    print("Entrei no interpretador de largura")

    informacoes = {
            "padrao":"",
            "filme": "",
            "peso_tubete": ""
    }

    return informacoes

def interpretar_padrao(texto):

# separação das partes
    partes = texto.split(" - ")

# Proteção para caso o PADRÃO  não tenha hífen
    if len(partes) > 2:
        return {
            "padrao": texto,
            "filme": "",
            "peso_tubete": ""
        }
    
    parte_esquerda  = partes[0]
    parte_direita = partes[1]

# Responsável por descobrir o valor do filme
    filme = extrair_filme(parte_esquerda)

# Responsável por descobrir o peso do filme e do tubete
    peso_filme,peso_tubete = extrair_pesos(parte_direita)


# Responsável por descobrir o padrão
    padrao = extrair_padrao(peso_filme,peso_tubete)
    
    informacoes = {
        "padrao": padrao,
        "filme": filme,
        "peso_tubete": peso_tubete
    }

    return informacoes

def selecionar_interpretador(texto, origem):

    if origem == "PADRÃO":
        print("Entrou em PADRÃO")
        return interpretar_padrao(texto)

    elif origem == "LARGURA  X MICRA":
        print("Entrou em LARGURA")
        return interpretar_largura_micra(texto)
    else:
        print("Nenhum if foi satisfeito")