from extensions import db

from servicos.conversao.data import agora

class VersaoProducao(db.Model):

    __tablename__ = "versoes_producao"

    id = db.Column(db.Integer, primary_key = True)

    periodo_id = db.Column(db.Integer, db.ForeignKey("periodos_producao.id"), nullable = False)

    numero_versao = db.Column(db.Integer, nullable = False)

    criado_em = db.Column(db.DateTime(timezone = True), default = agora, nullable = False)

    motivo = db.Column(db.String(255), nullable = True)

    status = db.Column(db.String(20), default = "ativa", nullable = False)

# Aqui a relação é de 1:N com cada versao podendo possuir vários grupos mas cada grupo pertencendo a somente 1 versao
    grupos = db.relationship("GrupoProducao", back_populates = "versao")

# Aqui o relacionamento é de 1:N com um único período podendo possuir várias versões
    periodo = db.relationship("PeriodoProducao", back_populates = "versoes")

    __table_args__ = (db.UniqueConstraint("periodo_id", "numero_versao", name = "uq_versao_periodo_numero"),)