from servicos.rastreabilidade.rastreabilidade import buscar_rastreabilidade,localizar_aba
from servicos.producao.odp import atualizar_odp

def atualizar_rastreabilidade(identificador,texto):
    dados = buscar_rastreabilidade(identificador)

    if dados is None:
        return {"Erro": "Identificador não encontrado"}, 404
      
    localizacao = localizar_aba(dados)

    if localizacao is None:
        return {"Erro": "ODP não encontrada"}, 404

    atualizar_odp (
            localizacao["arquivo"],
            localizacao["aba"],
            localizacao["linha"],
            identificador,
            texto)

    return {"mensagem": "Dados atualizados com sucesso",
            "resultado": localizacao}