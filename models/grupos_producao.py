from extensions import db

class GrupoProducao(db.Model):
    __tablename__ = "grupos_producao"

    id = db.Column(db.Integer, primary_key = True)

    versao_id = db.Column(db.Integer, db.ForeignKey("versoes_producao.id"), nullable = False)

    operador = db.Column(db.String(100), nullable = False)

    maquina = db.Column(db.String(100), nullable = False)

    meta = db.Column(db.Integer, nullable = True)

    versao = db.relationship("VersaoProducao", back_populates = "grupos")

# Aqui o relacionamento é de N:N em que um grupo pode possui várias odp assim como uma única odp pode pertencer a vários grupos, criando assim a tabela intermediária entre eles
    ordens_associadas = db.relationship("OrdemGrupo", back_populates = "grupo")