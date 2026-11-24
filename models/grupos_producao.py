from extensions import db

class GrupoProducao(db.Model):
    __tablename__ = "grupos_producao"

    id = db.Column(db.Integer, primary_key = True)

    periodo_id = db.Column(db.Integer, db.ForeignKey("periodos_producao.id"), nullable = False)

    operador = db.Column(db.String(100), nullable = False)

    maquina = db.Column(db.String(100), nullable = False)

    meta = db.Column(db.Integer, nullable = True)

# Aqui o relacionamento é de N:1 em que um único período possui vários grupos
    periodo = db.relationship("PeriodoProducao", back_populates = "grupos")

# Aqui o relacionamento é de N:1 em que um grupo pode possui várias ocorrências, mas 1 ocorrência (Identificador do QRcode) só pertence a um grupo
    ordens = db.relationship("OrdemProducao", back_populates = "grupo")