from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment
from openpyxl.drawing.image import Image
import os
from datetime import datetime
from copy import copy

from servicos.validacao.exceptions import AbaNaoEncontradaError

ALINHAMENTO_PADRAO = Alignment(horizontal="center", vertical="center",wrap_text=True)

FONTE_PADRAO = Font(name="Arial", size=11)

def preencher_odps(ordens):

    primeira_ordem = ordens[0]

    planilha = load_workbook("modelos/OdP's de cada odp.xlsx")

# Assim fica especificado pro programa sempre usar de parâmetro a aba com o nome "Modelo"
    aba_modelo = planilha["Modelo"]

    data = primeira_ordem["data"].strftime("%d-%m-%Y")
    nome_aba = f"{data}_{primeira_ordem['turno']}"

    if nome_aba in planilha.sheetnames:
        aba = planilha[nome_aba]
    else:
        aba = planilha.copy_worksheet(aba_modelo)
        aba.title = nome_aba

    logo = Image("imagens/luari_logo_empresa.png")
    logo.width = 150
    logo.height = 60
    aba.add_image(logo, "B2")

# congela o painel a partir ca célula A6
    aba.freeze_panes = "A6"

# Cabeçalho

    aba["D3"] = primeira_ordem["data"]
    aba["D3"].number_format = "dd/mm/yyyy"

    aba["F3"] = primeira_ordem["turno"]

    for celula in ("D3","F3"):
        aba[celula].font = FONTE_PADRAO
        aba[celula].alignment = ALINHAMENTO_PADRAO

    linha = 6
    odp_anterior = None

    for ordem in ordens:

        if odp_anterior is not None and ordem["odp"] != odp_anterior:
            linha += 1

        aba[f"C{linha}"] = ordem["numero_pedido"]
        aba[f"D{linha}"] = ordem["odp"]

        # Valores que serão preenchidos na pesagem
        aba[f"E{linha}"] = ""
        aba[f"F{linha}"] = ""
        aba[f"G{linha}"] = ""
        aba[f"H{linha}"] = ""
        aba[f"I{linha}"] = ""

        aba[f"J{linha}"] = ordem["cliente"]
        aba[f"K{linha}"] = ordem["padrao"]
        aba[f"L{linha}"] = ordem["filme"]
        aba[f"M{linha}"] = ordem["peso_tubete"]
        aba[f"N{linha}"] = ordem.get("observacao","")
        aba[f"O{linha}"] = ordem["operador"]
        aba[f"P{linha}"] = ordem["maquina"]

        # Dados de rastreabilidade, para serem registrados no histórico
        aba[f"Q{linha}"] = ""
        aba[f"R{linha}"] = ""
        aba[f"S{linha}"] = ""
        aba[f"T{linha}"] = ordem["identificador"]
        aba[f"U{linha}"] = ""
        aba[f"V{linha}"] = ""
        aba[f"W{linha}"] = ""

# Essas letras todas são todas as colunas que tem informação na nossa tabela na qual aplicaremos alguma mudança
        for coluna in "CDEFGHIJKLMNOPQRSTUVW":

            aba[f"{coluna}{linha}"].font = FONTE_PADRAO
            aba[f"{coluna}{linha}"].alignment = ALINHAMENTO_PADRAO

    # OBS em vermelho
        aba[f"N{linha}"].font = Font(name="Arial", size=11, color="FF0000", bold=True)

        linha += 1

        odp_anterior = ordem["odp"]

# Remove a aba_modelo antes de salvar
    if aba_modelo.title in planilha.sheetnames:
        planilha.remove(aba_modelo)

    caminho_saida = os.path.join("temporario", f"{data}_{primeira_ordem['turno']}.xlsx")

    planilha.save(caminho_saida)
    planilha.close()

    print("SALVANDO O ARQUIVO:", os.path.abspath(caminho_saida))
    return caminho_saida

# A partir daqui comerça o trabalho para lidar com o apontamento

def localizar_odp(aba, odp):

# Aqui ele analisará cada linha desde a 1 até o final, mas devido ao python considerar que ele lerá somente até o valor antes do último colocamos o +1
    for linha in range(1, aba.max_row + 1):

# Se o valor da célula for igual a odp retornará linha
        if aba[f"D{linha}"].value == odp:
            return linha

# Se não retornará nada 
    return None

def preencher_expedição(aba,odp,numero_pallet,peso_total,peso_liquido,op_material,op_tubete):

    linha = localizar_odp(aba,odp)

    if linha is None:
        print(f"ODP não encontrada: {odp}")
        return False
    
    aba[f'E{linha}'] = numero_pallet
    aba[f'F{linha}'] = peso_total
    aba[f'G{linha}'] = peso_liquido
    aba[f'H{linha}'] = op_material
    aba[f'I{linha}'] = op_tubete

    return True

def localizar_fim_odps(aba):

# É igual a 0 pois caso a planilha esteja vazia, ou seja, não tenha linhas preenchidas, ele retornará 0
    ultima_linha = 0

# Começa da linha 6 e daí por diante olha todas as linhas preenchidas e soma + 1 pois se não o range fará ele parar de analisar 1 linha antes da última
    for linha in range(6, aba.max_row + 1):

# Se a ODP ainda estiver preenchida atualiza o valor da ultima_linha,quando retornar vazio,o ultimo valor será o que retornará para a próxima função
        if aba[f"D{linha}"].value is not None:
            ultima_linha = linha

    return ultima_linha

def localizar_pallet(aba,identificador,numero_pallet):

# Analisa todas as linhas,desde a linha 1 até a última, devido ao + 1
    for linha in range(1, aba.max_row + 1):

        identificador_linha = aba[f"T{linha}"].value
        pallet_linha = aba[f"E{linha}"].value

# Se o identificador linha for igual ao identificador do QRcode da etiqueta e o Nº do pallet  inserido for igual ao Nº do pallet que já tinha sido inserido antes...
# Devolve o Nº da linha em que parar
# Se não retorna None, por não ter achado nada
        if ( 
            str(identificador_linha) == str(identificador)
            and str(pallet_linha) == str(numero_pallet)
        ):
            return linha

    return None

def atualizar_odp(caminho_arquivo,nome_aba,linha,identificador,dados):

    planilha = load_workbook(caminho_arquivo)

    if nome_aba not in planilha.sheetnames:
        raise AbaNaoEncontradaError()

    aba = planilha[nome_aba]

    campos = {
        "numero_pallet": 'E',
        "peso_liquido": "F",
        "peso_total": "G",
        "op_material": "H",
        "op_tubete": "I"
    }
# Parte responsável por,caso o mesmo QRcode seja bipado mais de uma vez por possuir mais de um pallet dele
    numero_pallet = dados.get("numero_pallet")
    acao = dados.get("acao","pesagem")

# Se a ação for pesagem:
    if acao == "pesagem":

# Descobre através da função linha_pallet qual a linha que deve-se trabalhar
        linha_pallet = localizar_pallet(
            aba,identificador,numero_pallet
        )
# Se a linha_pallet não tretornou um valor vazio
        if linha_pallet is not None:

# Acrescente 1 valor a mais no valor da linha atual
            linha_nova = linha + 1

# Pegue o valor dessa linha, e adicione uma linha amais na planilha empurrando todas as outras linhas prea baixo, inclusive a linha original    
            aba.insert_rows(linha_nova)

# Analisa todas as colunas,desde a coluna 1 até a última, devido ao + 1
            for coluna in range(1, aba.max_column + 1):

# Pega os valores antigos e atuais das respectivas células respeitando as leis (x,y)
                origem = aba.cell(linha,coluna)
                destino = aba.cell(linha_nova,coluna)

# Guarda o valor que estiver em origem em destino
                destino.value = origem.value

# Se origem tiver alguma formatação de cor, borda, fonte diferente do padrão ele entra no if
# É uma forma de economizar memória do computador com o python apenas perguntando se ele têm estilos especificados, e não pedindo todos os tipos de estilos posssíveis
                if origem.has_style:

# Formatação de estilo,incluindo cor, borda, fonte diferente do padrão
# No _style o _ serve como uma medida de privacidade, é uma forma de garantir que usuários comuns não mexs, ou tentem copiar isso diretamente 
                    destino._style = copy(origem._style)

# Caso o if se cumpra o resto das condições são cumpridas automaticamente
# Formato do número (se é texto, moeda, quilos, data)
                destino.number_format = origem.number_format

# Alinhamento do texto (centralizado, esquerda, direita)   
                destino.alignment = copy(origem.alignment)

# Estilo do texto (tipo de letra, tamanho, negrito)
                destino.font = copy(origem.font)

# Cor de fundo da célula
                destino.fill = copy(origem.fill)

# As linhas de contorno (bordas) da célula
                destino.border = copy(origem.border)

# O valor de linha agora é o valor que antes pertencia só a linha_nova
            linha = linha_nova

# Esse serve para caso seja o 1º registro desse Pallet, assim ainda usando a linha original normalmente
        else:
            pass

# Esse é para caso a ação não seja pesagem
    else:
        pass

# Só mudará para True quando algum valor realmente for modificado
    houve_alteracao = False

# Usa a função para descobrir onde é o fim das odps adicionando 1 para limite
    inicio = localizar_fim_odps(aba) + 1

# Descobre qual a última linha preenchida e soma 1 para pegar a linha em branco
    linha_historico = aba.max_row + 1

# Um laço que verifica se a linha anterior na coluna Q já possui conteúdo. Se tiver, ele pula para a próxima linha disponível para garantir que o histórico não apague dados antigos.
# Nesse caso faz sentido o > porque linha_historico será maior que inicio visto que ele terá 1 linha em branco a mais do que ele
    while linha_historico > inicio and aba[f"Q{linha_historico - 1}"]. value is not None:
        linha_historico += 1

# Item faz uma lista onde campo é a chave e coluna valor
    for campo,coluna in campos.items():

# O .get() irá procurar se algum dos valores de campo está dados, se não tiver retornará None
        novo_valor = dados.get(campo)

# Se o operador não preencheu o campo ou deixou em branco, não altera nada, ele continua
        if novo_valor in (None,""):
            continue
# Acessa a célula exata da aba principal e lê o conteúdo dele através do .value()
        valor_anterior = aba[f"{coluna}{linha}"].value 

# Se os valores forem iguais o sistema continua, isso evita que o programa gaste processamento alterando valores iguais e acrescentando linhas de histórico inúteis 
        if str(valor_anterior) == str(novo_valor):
            continue

# Após passar pela filtragem as células da aba principal recebe o novo valor
        aba[f"{coluna}{linha}"] = novo_valor

# Serve pra indicar que quando passar pOr ele o flag será alterado, isso é importante pois masi pra frente haverá uma condição que só ocorrerá quando houve_alteracao for True
        houve_alteracao = True
            
        agora = datetime.now()

        aba[f"Q{linha_historico}"] = aba[f"D{linha}"].value
        aba[f"R{linha_historico}"] = agora.strftime("%d/%m/%Y")
        aba[f"S{linha_historico}"] = agora.strftime("%H:%M:%S")
        aba[f"T{linha_historico}"] = identificador
        aba[f"U{linha_historico}"] = dados.get("acao", "pesagem")
        aba[f"V{linha_historico}"] = valor_anterior
        aba[f"W{linha_historico}"] = novo_valor

        for coluna_historico in "QRSTUVW":
            aba[f"{coluna_historico}{linha_historico}"].font = FONTE_PADRAO
            aba[f"{coluna_historico}{linha_historico}"].alignment = ALINHAMENTO_PADRAO

# Caso o próximo campo também sofra alteração ele será inserido na linha de baixo, assim as 5 informações serão impressas uma em cima da outra
        linha_historico += 1

# Se houve_alteracao for True os novos dados da alteração serão salvos no arquivo
    if houve_alteracao:

        planilha.save(caminho_arquivo)

# Depois disso fecha o arquivo para liberar a memória do computador
    planilha.close()

# Retorna True se o arquivo foi modificado ou False se nada mudou. Quem chamou a função saberá se houve sucesso na alteração
    return houve_alteracao