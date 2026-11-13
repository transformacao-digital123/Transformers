from extensions import db
from datetime import datetime

class VersaoProducao(db.Model):

    __tablename__ = "versoes_producao"

    id = db.Column(db.Integer, primary_key = True)

    periodo_id = db.Column(db.Integer, db.ForeignKey("periodos_producao.id"), nullable = False)

    numero_versao = db.Column(db.Integer, nullable = False)

    criado_em = db.Column(db.DateTime, default = datetime.utcnow, nullable = False)

    motivo = db.Column(db.String(255), nullable = True)

    status = db.Column(db.String(20), default = "ativa", nullable = False)