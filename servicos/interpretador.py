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

    partes = texto.upper().strip().split()

    filme = partes[3]

    micra =partes[0]

    padrao = f"{filme} + {micra}"

    peso_tubete = ""

    informacoes = {
            "padrao":padrao,
            "filme": filme,
            "peso_tubete": peso_tubete
    }
    return informacoes

def interpretar_72x100(texto):
    partes = texto.upper().strip().split()

    filme = partes[1]

    padrao = partes[0]

    peso_tubete = ""

    informacoes = {
        "padrao": padrao,
        "filme": filme,
        "peso_tubete": peso_tubete
    }

    return informacoes

def interpretar_medidas(texto):

    padrao = texto

    partes = texto.split("x")

    filme =partes[-1].strip()
    peso_tubete = ""

    informacoes = {
        "padrao": padrao,
        "filme": filme,
        "peso_tubete": peso_tubete
    }
    return informacoes

def interpretar_padrao(texto):

# separação das partes
    partes = texto.split(" - ")

# Proteção para caso o PADRÃO  não tenha hífen
    if len(partes) != 2:
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

def interpretar_mic_pol(texto):

    esquerda,direita = texto.split("MIC -")

    filme = esquerda.strip()

    padrao =direita.strip()

    conteudo = direita.split("(")[1].replace(")", "")
    pesos = conteudo.split("+")
    peso_tubete = pesos[1].strip()

    informacoes = {
        "padrao": padrao,
        "filme": filme,
        "peso_tubete": peso_tubete
    }

    return informacoes

def interpretar_fita(texto):
    partes = texto.split()

    micragem = partes[-2].replace("(","")

    filme = f"{partes[0]} {micragem}"

    padrao = " ".join(partes[1:4])

    peso_tubete = ""

    informacoes = {
        "filme" : filme,
        "padrao" : padrao,
        "peso_tubete" : peso_tubete
    }

    return informacoes

def interpretar_manopla(texto):

    texto = texto.upper().strip()

    esquerda,direita = texto.split("-")

    filme = esquerda.strip()

    padrao = direita.strip()
    conteudo = padrao.split("(")[1].replace(")","")

    padrao = conteudo.strip()

    pesos = conteudo.split("+")

    peso_tubete = pesos[1].strip()

    informacoes = {
        "filme": filme,
        "padrao": padrao,
        "peso_tubete": peso_tubete
    }

def selecionar_interpretador(texto, origem):

    if origem == "PADRÃO":
            if texto.count("x") == 2:
                return interpretar_medidas(texto)
            else:
                return interpretar_padrao(texto)

    elif origem == "LARGURA  X MICRA":
            if "POL" in texto:
                return interpretar_mic_pol(texto)
            elif texto.startswith("MANOPLA"):
                return interpretar_manopla(texto)
            elif texto.startswith("FITA"):
                return interpretar_fita(texto)
            elif "MM" in texto:
                return interpretar_largura_micra(texto)
            else:
                return interpretar_72x100(texto)