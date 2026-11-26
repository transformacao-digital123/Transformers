from collections import Counter

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

def criar_assinatura(ordem):
    campos = (
         "data",
         "turno",
         "numero_pedido",
         "odp",
         "cliente",
         "padrao",
         "operador",
         "maquina",
         "observacao",
         "origem"
    )

# Retorna os 10 valores pegos da ordem só que em uma nova tupla
    return tuple(

# O str transforma tudo em string, o .get pega o dicionário ordem do valor correspondente a chave atual, o campo, no caso, se lá houver data, ele preencherá o valor da data no lugar do campo da data sem espaçamentos desnecessários e tudo em maiúsculo, e se não houver nada retorna ""
        str(ordem.get(campo) or "").strip().upper()

# Inicia o laço de repetição
        for campo in campos
    )

def contar_assinaturas(ordens):

# Retorna a contagem das assinaturas
    return Counter(

# Chama a função que cria a assinatura
        criar_assinatura(ordem)

# Inicia o laço de repetição com cada OdP
        for ordem in ordens
    )

def identificar_novas_ordens(ordens_novas, ordens_existentes):

# Chama as assinaturas que foram contada já
    contagens_existentes = contar_assinaturas(ordens_existentes)

    novas_ocorrencias = []

    for ordem in ordens_novas:

# Aqui ele refaz a criação das assinaturas, para caso tenha sido criado uma nova
        assinatura = criar_assinatura(ordem)

# Faz uma comparação de quantas assinaturas contagens_existentes e assinaturas tem em comum
# Aqui ele faz a comparação de uma odp por vez, ou seja, se for solicitado a análise ele fará a comparação entre ambos, caso já aja aquela odp na planilha original o Nº do contador será 1, ou seja, maior que 0
        if contagens_existentes[assinatura] > 0:

# Caso isso ocorra, o Nº dessa contagem é zerado pois, quando for feita a análise da próxima odp, caso ela seja nova, se não descontar 1 do contador ele ficará 2, assimele sempre será maior que 0 e nunca dará pra determinar se uma OdP é nova ou não
            contagens_existentes[assinatura] -= 1

# Aqui é caso o Nº de ordens iguais for = 0 ele acrescentará a variável novas_ocorrencias e então retornar pra quem chamou
        else:
            novas_ocorrencias.append(ordem)

    return novas_ocorrencias