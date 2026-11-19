from extensions import db

class PesagemProducao(db.Model):

    __tablename__ = "pesagens_producao"

    id = db.Column(db.Integer, primary_key = True)

    pallet_id = db.Column(db.Integer, db.ForeignKey("pallets.id"), nullable = False, unique = True)

    peso_liquido = db.Column(db.Numeric(10, 2), nullable = True)

    peso_bruto = db.Column(db.Numeric(10, 2), nullable = True)

    peso_palete = db.Column(db.Numeric(10, 2), nullable = True)

    peso_total = db.Column(db.Numeric(10, 2), nullable = True)

    op_material = db.Column(db.Integer, nullable = True)

    op_tubete = db.Column(db.Integer, nullable = True)

# Aqui o relacionamento é de 1:1 em que um único pallet pertence a uma única pesagem
    pallet = db.relationship("Pallet", back_populates = "pesagem")