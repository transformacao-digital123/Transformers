from extensions import db

class OrdemProducao(db.Model):

    __tablename__ = "ordens_producao"

    id = db.Column(db.Integer, primary_key = True)

    grupo_id = db.Column(db.Integer, db.ForeignKey("grupos_producao.id"), nullable = False)

# Aqui é string devido a / ou - da OdP

    pedido = db.Column(db.String(20), nullable = False)

    odp = db.Column(db.String(20), nullable = False, unique = True)

    cliente = db.Column(db.String(255), nullable = False)

    padrao = db.Column(db.String(60), nullable = False)

    filme = db.Column(db.String(40), nullable = False)

    peso_tubete = db.Column(db.String(10), nullable = False)

    observacoes = db.Column(db.Text, nullable = True)

    identificador = db.Column(db.String(30), nullable = False, unique = True)

