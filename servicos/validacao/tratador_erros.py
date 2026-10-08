from servicos.validacao.exceptions import (
    DataNaoEncontradoError,
    NumeroPedidoNaoEncontrado,
    ClienteNaoEncontradoError,
    PadraoNaoEncontradoerror,
    FilmeNaoEncontradoerror,
    OdpNaoEncontradaError,
    PlanilhaNaoEncontradaError,
    PlanilhaCorrompidaError,
    AbaNaoEncontradaError,
    RastreabilidadeNaoEncontradaError,
    RemessaNaoEncontradaError,
    NenhumaOdpNovaError
)

MENSAGENS = {
    DataNaoEncontradoError:
    "O campo data de entrega não foi encontrado",

    NumeroPedidoNaoEncontrado:
    "O campo número do pedido não foi encontrado",

    ClienteNaoEncontradoError:
    "O campo cliente não foi encontrado",

    PadraoNaoEncontradoerror:
    "O campo padrão não foi encontrado",

    FilmeNaoEncontradoerror:    
    "O campo filme não foi encontrado",

    OdpNaoEncontradaError:
    "O número da ODP não foi encontrado na planilha",

    PlanilhaNaoEncontradaError:
    "A planilha de rastreabilidade não foi encontrada,\nverifique se ela não está aberta em outra aba",

    PlanilhaCorrompidaError:
    "A planilha encontrada está corrompida ou não é um arquivo Excel válido",

    AbaNaoEncontradaError:
    "A aba solicitada não foi encontrada na planilha",

    RastreabilidadeNaoEncontradaError:
    "Não foi possível encontrar os dados de rastreabilidade",

    RemessaNaoEncontradaError:
    "Não existe uma remessa para essa data e turno. Crie uma nova remessa antes de tentar acrescentar ODPs",

    NenhumaOdpNovaError:
    "Nenhuma remessa nova foi incluída. todas as OdP's já estão na remessa"


}

def tratar_erro(erro):

# .get pergunta se tem uma chave em MENSAGENS que se relacione com esse erro
    return MENSAGENS.get(

# Se não tiver chave para esse erro, coloque essa mensagem
        type(erro),
        "Ocorreu um erro inesperado"
    )

# Sequencia lógica de como segue um erro

#extrator_pdf│
#       ▼
# raise ClienteNaoEncontradoError()
#       │
#       ▼
# conversor
#       │
#       ▼
# logger
#       │
#       ▼
# tratador_erros
#       │
#       ▼
# app.py
#       │
#       ▼
# HTML
#       │
#       ▼
# Usuário