from extensions import db
from servicos.conversao.data import agora

class LinkUtilizado(db.Model):

    __tablename__ = "links_utilizados"

    id = db.Column(db.Integer, primary_key = True)

    link = db.Column(db.Text, nullable = False, unique = True)

    utilizado_em = db.Column(db.DateTime(timezone = True), default = agora, nullable = False)