from models.periodos_producao import PeriodoProducao
from models.grupos_producao import GrupoProducao
from models.ordens_producao import OrdemProducao

from extensions import db

def agrupar_por_grupo_producao(ordens):

# Dicionário vazio pra armazenar os grupos
    grupos = {}

# Aqui será feito um laço de repetição pra cada ordem, em que, pra cada ordem que passar por aqui, independente se passar mais de uma vez por N motivos, terá a sua própria chave que a represente
    for ordem in ordens:

# Aqui é feita uma tupla pra identificar o grupo, essa identificação conterá data, turno, operador e máquina
        chave = (
            ordem["data"],
            ordem["turno"],
            ordem["operador"],
            ordem["maquina"]
        )

# Se for a 1º da chave aqui, ela ainda não terá um grupo que a represente então aqui sertá criada uma lista vazia a ele
        if chave not in grupos:
            grupos[chave] = []

# Criada a lista, as próximas vezes que a chave passar pela condição anterior, caso ele já possua um grupo ele pulará pra cá, onde se encaixará no grupo que ele pertence
        grupos[chave].append(ordem)

# Devolve um dicionário com todos os grupos
    return grupos


def obter_ou_criar_periodo(data, turno):

# Aqui é feita uma consulta na tabela PeriodoProducao, filtrando somente por data e turno e pegando o 1º valor, visto que todas as odp desse periodo usarão a mesma data e turno. Lembrando que o first() pode tanto retornar um objeto PeriodoProducao quanto None, devido a por algum motivo o período ainda não ter sido registrado no banco por ser o 1º registro do dia por exemplo
    periodo = PeriodoProducao.query.filter_by(

# Aqui nomearemos de data aquilo que encontramos que tiver o nome de data, e o mesmo vale pro tuno
        data = data,
        turno = turno
    ).first()

# Caso retorne None, nós criamos uma data e período pra ele
    if periodo is None:
        periodo = PeriodoProducao(
            data = data,
            turno = turno
        )

# Adiciona o objeto ao SQL
        db.session.add(periodo)

# Aqui é preenchido valores que não foram informados, no caso, o flush aqui é responsável por o periodo ter o ID preenchido
        db.session.flush()

    return periodo


def obter_ou_criar_grupo(periodo, operador, maquina):

    grupo = GrupoProducao.query.filter_by(
        periodo_id = periodo.id,
        operador = operador,
        maquina = maquina
    ).first()

    if grupo is None:
        grupo = GrupoProducao(
            periodo_id = periodo.id,
            operador = operador,
            maquina = maquina
        )

        db.session.add(grupo)
        db.session.flush()

    return grupo

def obter_ou_criar_odp(ordem, grupo, chave_origem):

# Devemos fazer a busca exclusivamente pela chave_origem, pois ela define cada linha de pedido, se ela não existir pula pro próximo bloco que então a cria para aquele pedido
# É bom destacar que o motivo de haver essa variável aqui é que, apesar de não ter como chave_origem se repetir porque cada uma é única, caso venha acontecer posteriormente algum acréscimo de odp na planilha, ele identificará os que já foram constatados e obterá seu valor que já havia sido preenchido e então fará isso até encontrar as novas OdP, que esses sim pularão ao bloco seguinte por retornarem None
    odp = OrdemProducao.query.filter_by(
        chave_origem = chave_origem
    ).first()

    if odp is None:
        odp = OrdemProducao(
            pedido = ordem["numero_pedido"],
            odp = ordem["odp"],
            cliente = ordem["cliente"],
            padrao = ordem["padrao"],
            filme = ordem["filme"],
            peso_tubete = ordem["peso_tubete"],
            observacoes = ordem.get("observacao"), # Aqui ficou observacoes por causa que é assim que está no banco de dados e o .get() está aí pois, já que observacao é uma valor que pode vir vazio, caso venha vazio, ao invés de dar erro como os outros, apenas virá como null
            identificador = ordem["identificador"],
            grupo_id = grupo.id,
            chave_origem = chave_origem
        )

        db.session.add(odp)
        db.session.flush()

    return odp