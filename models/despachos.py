from extensions import db

from servicos.conversao.data import agora

class Despacho(db.Model):

    __tablename__ = "despachos"

    id = db.Column(db.Integer, primary_key = True)

    pallet_id = db.Column(db.Integer, db.ForeignKey("pallets.id"), nullable = False)


    data = db.Column(db.DateTime(timezone = True), default = agora, nullable = False)

    status = db.Column(db.String(20), default = "despachado", nullable = False)

    perfil_id = db.Column(db.Integer, db.ForeignKey("perfis_operacionais.id"), nullable = False)

# Aqui o relacionamento é de 1:N em que um pallet pode pouir mais de um despacho, no caso de cancelar e depachar de novo, por exemplo, já o despacho pertence a um único pallet
    pallet = db.relationship("Pallet", back_populates = "despacho")

# Aqui a relação é de 1:N pois um único perfil é responsável por fazer vários despachos, mas cada despacho é efetuado por somente 1 pessoa
    perfil = db.relationship("PerfilOperacional", back_populates = "despacho")