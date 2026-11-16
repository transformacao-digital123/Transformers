from extensions import db

class PesagensProducao(db.Model):

    __tablename__ = "pesagens_producao"

    id = db.Column(db.Integer, primary_key = True)

    pallet_id = db.Column(db.Integer, db.ForeignKey("pallets.id"), nullable = False, unique = True)

    peso_liquido = db.Column(db.Numeric(10, 2), nullable = True)

    peso_bruto = db.Column(db.Numeric(10, 2), nullable = True)

    peso_palete = db.Column(db.Numeric(10, 2), nullable = True)

    peso_total = db.Column(db.Numeric(10, 2), nullable = True)

    op_material = db.Column(db.Integer, nullable = True)

    op_tubete = db.Column(db.Integer, nullable = True)