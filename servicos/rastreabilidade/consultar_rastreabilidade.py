from servicos.rastreabilidade.rastreabilidade import buscar_rastreabilidade,localizar_aba

def consultar_rastreabilidade(identificador):

    dados = buscar_rastreabilidade(identificador)

    if dados is None:
        return None

    localizacao = localizar_aba(dados)

    if localizacao is None:
        return None

    return {
        "dados": dados,
        "localizacao": localizacao
    }
