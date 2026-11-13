from extensions import db

class GrupoProducao(db.Model):
    __tablename__ = "grupos_producao"

    id = db.Column(db.Integer, primary_key = True)

    versao_id = db.Column(db.Integer, db.ForeignKey("versoes_producao.id"), nullable = False)

    operador = db.Column(db.String(100), nullable = False)

    maquina = db.Column(db.String(100), nullable = False)

    meta = db.Column(db.Integer, nullable = True)