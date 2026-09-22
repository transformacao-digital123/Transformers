processamento_progresso = 0

# Essa função terá um chamado nos respectivos lugares que quiserem demarcar uma evolução, a cada chamado representa um aumento de porcentagem, por exemplo, quando chamarem ele nos 10%, esse 10 substituirá o valor que estiver em processamento_progresso, e assim por diante, até chegar a 100% que é o final do processo
def atualizar_progresso(valor):
    global processamento_progresso
    processamento_progresso = valor

# Ele retorn o valor que estiver em processamento_progresso e envia para a rota /progresso, que é o que o front-end vai usar para mostrar a evolução do processo
def obter_progresso():
    return processamento_progresso