from extensions import db
from servicos.conversao.data import agora

class PerfilOperacional(db.Model):

    __tablename__ = "perfis_operacionais"

    id = db.Column(db.Integer, primary_key = True)

    nome = db.Column(db.String(150), nullable = False)

    cargo = db.Column(db.String(50), nullable = False)

    criado_em = db.Column(db.DateTime(timezone = True), default = agora, nullable = False)

# Aqui a relação é de 1:N pois um único perfil é responsável por fazer vários despachos, mas cada despacho é efetuado por somente 1 pessoa
    despacho = db.relationship("Despacho", back_populates = "perfil")

