# arquivos do Excel preservando sua estrutura.  
import os

from servicos.arquivos.planilha import preencher_planilha
from servicos.arquivos.zip import criar_zip
from servicos.interpretacao.interpretador import selecionar_interpretador
from servicos.producao.apontamento import agrupar_por_operador, selecionar_apontamento
from servicos.rastreabilidade.rastreabilidade import salvar_rastreabilidade
from servicos.progresso.progresso import atualizar_progresso

from servicos.entradas.google_sheets import validar_link, baixar_planilha
from servicos.arquivos.excel import abrir_planilha
from servicos.interpretacao.identificar_blocos import identificar_blocos
from servicos.rastreabilidade.rastreabilidade import gerar_identificador
from servicos.producao.odp import  preencher_odps
from servicos.etiquetas.etiqueta import preencher_etiqueta

def converter_google_sheets(link):

    atualizar_progresso(0)

    rastreabilidade = {}


    os.makedirs("temporario", exist_ok=True)

    atualizar_progresso(10)

    for nome in os.listdir("temporario"):
         caminho = os.path.join("temporario", nome)

         if os.path.isfile(caminho):

# Se começar com ODP_ seguirá reto e irá apagar o resto
              if nome.startswith("ODP_") and nome.endswith(".xlsx"):
                   continue

              try:
                os.remove(caminho)

              except PermissionError:
                   print(f"Não foi possível apagar {nome}")

# Valida se o link é do google docs ou não
    validar_link(link)
    atualizar_progresso(20)

# Variável que guarda a planilha em formato .xlsx que for criado
    caminho_arquivo = baixar_planilha(link)
    atualizar_progresso(30)

    planilha = abrir_planilha(caminho_arquivo)
    atualizar_progresso(40)

# Seleciona a aba ativa da planilha
    aba = planilha.active
         
    ordens = identificar_blocos(aba)
    atualizar_progresso(50)

    planilha.close()

    os.remove(caminho_arquivo)

    arquivos = []

    etiquetas_para_imprimir = []

    total_ordens = len(ordens)
    
    for indice,ordem in enumerate(ordens):
# Função chamada para analisar o padrão, e descobrir o filme e o peso do tubete. Além disso, dentro dela nota-se 2 padrao, o 1° é para encontrar a variável dentro do dicionário e o 2° é para encontrar a coluna caso ela se chame PADRÃO
        try:

                informacoes = selecionar_interpretador(ordem["padrao"], ordem["origem"])
             
                ordem["filme"] = informacoes["filme"]
                ordem["peso_tubete"] = informacoes["peso_tubete"]
                ordem["padrao"] = informacoes["padrao"]

                arquivo = preencher_planilha(ordem, indice)
             
                arquivos.append(arquivo)

# Essa conta é feita para que o progresso da criação de cada arquivo represente 15% do total e depois seja acrescentado aos 50% até se tornar
# É imporatante destacar que p + 1 está ali pois, se não tivesse, como o o 1º é sempre represebtado por 0, o 1° valor dessa conta seria 0, ou seja, na 1° volta não aumentaria a % e no final nunca daria 65%
                progresso = 50 + ((indice + 1) / total_ordens) * 15
                atualizar_progresso(progresso)
        
        except Exception as erro:

            raise

    grupos = agrupar_por_operador(ordens)

    total_operadores = len(grupos)

    contadores_etiquetas = {}

    for ordem in ordens:
        chave = f"{ordem['odp']}_{ordem['operador']}"
        contadores_etiquetas[chave] = contadores_etiquetas.get(chave, 0) + 1

    sequencia_etiquetas ={}
                    
    for indice, (operador,ordens_operador) in enumerate(grupos.items()):

        turno = ordens_operador[0]["turno"]

        arquivo = selecionar_apontamento(turno, operador, ordens_operador)
        arquivos.append(arquivo)

        for ordem in ordens_operador:

            chave = f"{ordem['odp']}_{ordem['operador']}"

            if chave not in sequencia_etiquetas:
                sequencia_etiquetas[chave] = 1
            else:
                sequencia_etiquetas[chave] += 1

            numero_etiqueta = sequencia_etiquetas[chave]
            total_etiquetas = contadores_etiquetas[chave]

# responsável por colocar um valor aleatório para a pessoa que tentar bipar a etiqueta sem ser pelo Transformer receber
            identificador = gerar_identificador()

# O identificador foi posto aqui para garantir que tanto preencher odp quanto eiquetas recebesse o mesmo,e não um independente cada um
            ordem["identificador"] = identificador

            arquivo_etiqueta = preencher_etiqueta(ordem,rastreabilidade,numero_etiqueta,total_etiquetas)
            arquivos.append(arquivo_etiqueta)

            etiquetas_para_imprimir.append(arquivo_etiqueta)

            progresso = 65 + ((indice + 1) / total_operadores) * 25
            atualizar_progresso(progresso)

    arquivo_odp = preencher_odps(ordens)
    arquivos.append(arquivo_odp)

    arquivo_zip = criar_zip(arquivos)

    salvar_rastreabilidade(rastreabilidade)

    return arquivo_zip,etiquetas_para_imprimir