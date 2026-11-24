from extensions import db

from servicos.conversao.data import agora

# Aqui a classe PeriodoProducao herda db.Model e então informa ao SQLAlchemy que esta classe representa uma tabela no banco de dados
class PeriodoProducao(db.Model):

# Define o nome da tabela no banco de dados
    __tablename__ = "periodos_producao"

# A partir daqui é criado as colujnas das tabelas

# Aqui será chave primária e Integer define a coluna só com Nº inteiros e 
    id = db.Column(db.Integer, primary_key = True)

# O nullable = False faz o preenchimento ser obrigatório, não permitindo essa coluna ficar vazia, e o .Date faz com que seja gravada somente a data e não a hora, diferente do datetime, que também registra a hora
    data = db.Column(db.Date, nullable = False)

    turno = db.Column(db.String(20), nullable = False)

# Aqui o default define uma valor automático quando um registro é criado, nesse caso, define a data e hora automaticamente com o padrão UTC
    criado_em = db.Column(db.DateTime(timezone = True), default = agora, nullable = False)

# O onupdate atualizará o registro com uma nova data e hora toda vez que o registro sofrer alguma alteração no banco
    atualizado_em = db.Column(db.DateTime(timezone = True), default = agora, onupdate = agora, nullable = False)

# Aqui o relacionamento é de 1:N com um único período podendo possuir várias grupos
    grupos = db.relationship("GrupoProducao", back_populates = "periodo")

    __table_args__ = (db.UniqueConstraint("data", "turno", name = "uq_periodo_data_turno"),)