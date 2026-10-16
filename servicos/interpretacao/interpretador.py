def extrair_filme(parte_esquerda):
    filme = parte_esquerda.split(" ")
    return filme[0]

def extrair_pesos(parte_direita):

# Validação dos pesos
    pesos = parte_direita.replace("(", "").split("+",1)
    
# Responsável por descobrir o valor do peso do filme
    for peso in pesos:
        if len(pesos) > 1:
            if "KG DE FILME" in peso:
                peso_filme = pesos[0].replace("KG DE FILME", "").strip()
        else:
            peso_filme = pesos[0].replace("KG DE FILME)", "").strip()

    if len(pesos) > 1:
        peso_tubete = pesos[1].replace("KG DE TUBETE)", "").strip()
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

def interpretar_padrao(texto):

# 25 MIC MAN - (3,5 KG DE FILME + 0,5 KG DE TUBETE)
# 40 MIC AUT - (10,2 KG DE FILME + 1,5 KG DE TUBETE)
# 40 MIC AUT - (10,2 KG DE FILME)
# 25 MIC MAN - (3 KG DE FILME)
# FILME PRETO MAN - (3 KG DE FILME + 0,5 KG DE TUBETE)

# separação das partes
    partes = texto.split("-")

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

def interpretar_largura_micra(texto):

# 520 MM X 0,50

    partes = texto.upper().strip().split()

    filme = partes[3]

    largura =partes[0]

    padrao = f"{filme} + {largura}"

    peso_tubete = ""

    informacoes = {
            "padrao":padrao,
            "filme": filme,
            "peso_tubete": peso_tubete
    }
    return informacoes

def interpretar_72x100(texto):

# 72x100 45 MIC

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

# 1500 x 1500 x 40

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

def interpretar_mic_pol(texto):

# 30 MIC - 1 POL - 5 CM (300 + 20)
# 25 MIC - 3 POL - 16,6 CM - 1,5 KG (1 KG + 0,500 G)

    texto = texto.upper().strip()

    if "DE FILME" in texto:

        partes = texto.split("(", 1)

        parte_padrao = partes[0].split("-", 1)[1].strip()

        if len(partes) > 1:
            conteudo = partes[1].replace(")", "").strip()
            pesos = conteudo.split("+")
        pesos = []

        filme = ""

        for peso in pesos:
            if len(pesos) > 1:
                if "KG DE FILME" in peso:
                    peso_filme = (pesos[0].replace("KG DE FILME", "").strip() if len(pesos) > 1 else "")
            else:
                peso_filme = (pesos[0].replace(")", "").strip() if len(pesos) > 1 else "")

# Se pesos for > 1, porque aqui foi separado em 2: pesos = parte_pesos.split("+")
        if len(pesos) > 1:
            peso_tubete = pesos[1].replace("KG DE TUBETE)", "").strip()
        else:
            peso_tubete = ""

        padrao = f"{parte_padrao} + {peso_filme} + {peso_tubete}"

        informacoes = {
            "padrao": padrao,
            "filme": filme,
            "peso_tubete": peso_tubete
        }

    else:

        partes = texto.split("MIC -", 1)

        esquerda = partes[0]
        direita = partes[1]

        if len(partes) > 1:
            filme = esquerda.strip()
        else:
            filme = esquerda.replace(")", "").strip()

        
        parte_padrao = direita.split("(",1)[0].strip()

        conteudo = direita.split("(")[1].replace(")", "")
        pesos = conteudo.split("+")

        for peso in pesos:
            if len(pesos) > 1:
                if "G DE FILME" in peso:
                    peso_filme = pesos[0].replace("G DE FILME", "").strip()
            else:
                peso_filme = pesos[0].replace(")", "").strip()

        if len(pesos) > 1:
            peso_tubete = pesos[1].replace("G DE TUBETE", "").strip()
        else:
            peso_tubete = ""

        padrao = f"{parte_padrao} + {peso_filme} + {peso_tubete}"

        informacoes = {
            "padrao": padrao,
            "filme": filme,
            "peso_tubete": peso_tubete
        }

    return informacoes

def interpretar_fita(texto):

# FITA ADESIVA ACRÍLICA 48 X 1200 (45 MIC)

    partes = texto.split("")

    micragem = partes[-2].replace("(","")

    filme = f"{partes[0]} {micragem}"

    padrao = " ".join(partes[1:5])

    peso_tubete = ""

    informacoes = {
        "filme" : filme,
        "padrao" : padrao,
        "peso_tubete" : peso_tubete
    }

    return informacoes

def interpretar_manopla(texto):

# MANOPLA - (180g + 20g)

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

    return informacoes

def interpretar_filme_pol(texto):

# 30 MIC - 1 POL - 5 CM - 320 GR (0,300 G DE FILME + 0,20 G DE TUBETE)

    partes = texto.split("(")

    parte_padrao = partes[0].split("-",1)[1].strip()

    filme = partes[0].split("MIC")[0].replace("FILME_", "").strip()

    pesos = partes[1].split("+")

    for peso in pesos:
        if len(pesos) > 1:
            if "G DE FILME" in peso:
                peso_filme = pesos[0].replace("G DE FILME", "").strip()
        else:
            peso_filme = pesos[0].replace(")", "").strip()

    if len(pesos) > 1:
        peso_tubete = pesos[1].replace("G DE TUBETE)", "").replace("G)", "").strip()
    else:
        peso_tubete = ""

    padrao = f"{parte_padrao} + {peso_filme} + {peso_tubete}"

    informacoes = {
        "filme": filme,
        "padrao": padrao,   
        "peso_tubete": peso_tubete
    }

    return informacoes

def interpretar_hotmelt(texto):

    texto = texto.upper().strip()

    partes = texto.split()

    padrao = partes[-1].strip()

    filme = " ".join(parte.strip() for parte in partes[:-1])

    peso_tubete = ""

    informacoes = {
        "filme": filme,
        "padrao": padrao,
        "peso_tubete": peso_tubete
    }
    return informacoes

def interpretar_filme_mm(texto):

    texto = texto.upper().strip()

    partes = texto.split("-")

    filme = partes[1].split("")[0]

    peso_tubete = partes[2].split("+")[1].replace("G)", "").strip()

    padrao = "-".join(parte.strip() for parte in partes[1:])

    informacoes = {
        "filme": filme,
        "padrao": padrao,
        "peso_tubete": peso_tubete
    }

    return informacoes

def interpretar_filme_750(texto):

# FILME_750 MM - 30 MIC AUT - (17 KG DE FILME + 2 KG DE TUBETE)

    texto = texto.upper().strip()

    partes = texto.split("-")

    filme = partes[1].replace("MIC AUT", "").strip()

    pesos = partes[2].replace("(", "").split("+",1) # Aqui foi definido que só haverá 1 separação

    esquerda = pesos[0].strip()
    direita = pesos[1].strip() if len(pesos) > 1 else ""

    for peso in pesos:
        if len(pesos) > 1:
            if "KG DE FILME" in peso:
                peso_filme = esquerda.replace("KG DE FILME", "").strip()
        else:
            peso_filme = esquerda.replace(")", "").strip()

    if "KG DE TUBETE)" in direita:
        peso_tubete = direita.replace("KG DE TUBETE)", "").strip()
    else:
        peso_tubete = ""

    padrao = f"{partes[0]} + {peso_filme} + {peso_tubete}".strip()

    informacoes = {
        "filme": filme,
        "padrao": padrao,
        "peso_tubete": peso_tubete
    }

    return informacoes

def interpretar_filme_sem_hifen(texto):

# FILME PRETO (3 KG DE FILME + 0,5 KG DE TUBETE)

    texto = texto.upper().strip()

    partes = texto.split("(", 1)

    filme = partes[0].strip()

    conteudo = partes[1].replace(")", "").strip()
    pesos = conteudo.split("+") 

    esquerda = pesos[0].strip()
    direita = pesos[1].strip() if len(pesos) > 1 else ""

    for peso in pesos:
        if len(pesos) > 1:
            if "KG DE FILME" in peso:
                peso_filme = esquerda.replace("KG DE FILME", "").strip()
            else:
                peso_filme = esquerda.replace(")", "").strip()

    if len(pesos) > 1:
        peso_tubete = direita.replace("KG DE TUBETE", "").strip()
    else:
        peso_tubete = ""

    if peso_tubete:
        padrao = f"{peso_filme} + {peso_tubete}".strip()
    else:
        padrao = peso_filme

    informacoes = {
        "filme": filme,
        "padrao": padrao,
        "peso_tubete": peso_tubete
    }

    return informacoes

def interpretar_filme_ou_pre(texto):

# PRE ESTIRADO - (2 KG DE FILME)
# FILME PRETO (3 KG DE FILME + 0,5 KG DE TUBETE)

    texto = texto.upper().strip()

    partes = texto.split("-")

    filme = partes[0].strip()

    pesos = partes[1].replace("(", "").split("+").strip()

    esquerda = partes[0].strip()
    direita = partes[1].strip() if len(pesos) > 1 else ""

    for peso in pesos:
        if len(pesos) > 1:
            if "KG DE FILME" in peso:
                peso_filme = esquerda.replace("KG DE FILME", "").strip()
        else:
            peso_filme = esquerda.replace(")", "").strip()

    peso_tubete = direita.replace("KG DE TUBETE)", "").strip()

    padrao = f"{peso_filme} + {peso_tubete}"

    informacoes = {
        "filme": filme,
        "padrao": padrao,
        "peso_tubete": peso_tubete
    }

    return informacoes

def selecionar_interpretador(texto, origem):

    if origem == "PADRÃO":
            if texto.count("x") == 2:
                return interpretar_medidas(texto)
            elif texto.count("-") == 3:
                return interpretar_filme_pol(texto)
            elif "FILME" in texto and "MM -" in texto and ("MIC AUT -" in texto or "MIC MAN -" in texto): # TEM DE CONSERTAR
                return interpretar_filme_750(texto)
            elif "MM" in texto:
                return interpretar_filme_mm(texto)
            elif "MIC" in texto:
                return interpretar_padrao(texto)
            else:
                return interpretar_filme_ou_pre(texto)

    elif origem == "LARGURA  X MICRA":
            if "POL" in texto:
                return interpretar_mic_pol(texto)
            elif texto.startswith("MANOPLA"):
                return interpretar_manopla(texto)
            elif texto.count("x") == 2:
                return interpretar_medidas(texto)
            elif texto.startswith("FITA"):
                return interpretar_fita(texto)
            elif "MM" in texto or "CM" in texto:
                return interpretar_largura_micra(texto)
            elif "HOTMELT" in texto:
                return interpretar_hotmelt(texto)
            else:
                return interpretar_72x100(texto)