def identificar_blocos(aba):

    maquina = ""
    operador = ""
    turno = ""

    estado ="procurando_bloco"

# Para armazenar as informações do dicionário "dados"
    ordens=[]

    colunas = {}

    MAPEAMENTO = {
        "data": "DATA",
        "numero_pedido": "PEDIDO",
        "odp": "OdP",
        "cliente": "CLIENTE",
        "padrao": ["PADRÃO", "LARGURA  X MICRA"]
    }

# O .iter_rows() lê linha por linha do conteúdo que está conectado
    for linha in aba.iter_rows(): 

        try:

            valores = []

        except Exception as erro:

            raise

# Percorre as células da linha  
        for celula in linha:
            if celula.value is not None:

# O .append acrescenta na lista Valores, e o .strip separa o conteúdo por espaços 
                    valores.append(str(celula.value).strip())

# o len lê a quantidade, se a quantidade de celulas preenchidas for 1 continuará para descobrir a máquina e o operador
        if len(valores) == 1:
                
    # Guarda o primeiro valor da célula na variável texto
                texto = valores[0]

    # Primeiro verifica se é o título da ODP
                if texto.startswith("Ordem De Produção"):

                    if "Noite" in texto:
                        turno = "Noite"
                    elif "Manhã" in texto:
                        turno = "Manhã"

    # Só depois verifica máquina-operador
                elif " - " in texto:

                    maquina, operador = texto.split(" - ", 1)

                    maquina = maquina.strip()
                    operador = operador.strip()

# Descobrir o cabeçalho
        if "DATA" in valores and "PEDIDO" in valores and "OdP" in valores:
            estado = "lendo_ordens"


            if "PADRÃO" in valores:
                    origem = "PADRÃO"
                    coluna_padrao = "PADRÃO"
                    
            elif "LARGURA  X MICRA" in valores:
                    origem = "LARGURA  X MICRA"
                    coluna_padrao = "LARGURA  X MICRA"

# O indice é a posição, em que coluna está, e a celula a coordenada excel, como A15
            for indice, celula in enumerate(linha):
                if celula.value:

# Estrutura feita para que caso mudem alguma coluna de lugar essa linha se atualizará sozinha
                    colunas[str(celula.value).strip()] = indice

            continue

        if estado == "lendo_ordens":

            data = linha[colunas["DATA"]].value
            numero_pedido = linha[colunas["PEDIDO"]].value      

            if (data is not None and numero_pedido is not None):

                dados = {}

# O .items serve para organizar o dicionário em chave e valor
                for chave_programa,chave_planilha in MAPEAMENTO.items():

                    if chave_programa == "padrao":
                        dados[chave_programa] = linha[colunas[coluna_padrao]].value
                    else:
                        dados[chave_programa] = linha[colunas[chave_planilha]].value

# Aqui não precisa de , pq não é uma string, é uma tupla
                dados["operador"] = operador
                dados["maquina"] = maquina
                dados["observacao"] = ""
                dados["turno"] = turno

                dados["origem"] = origem

                ordens.append(dados)

            if   len(valores) == 1:
                if valores[0].startswith("OBS: "):
                    ordens[-1]["observacao"] = valores[0].replace("OBS: ","")
    print("3 - ORDENS INTERPRETADAS:", len(ordens))

    return ordens