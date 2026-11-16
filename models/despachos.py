from extensions import db

from servicos.conversao.data import agora

class Despacho(db.Model):

    __tablename__ = "despachos"

    id = db.Column(db.Integer, primary_key = True)

    pallet_id = db.Column(db.Integer, db.ForeignKey("pallets.id"), nullable = False)

    ordem_id = db.Column(db.Integer, db.ForeignKey("ordens_producao.id"), nullable = False)

# Aqui o default irá fazer o preenchimento, mas graças ao lambda só ocorrerá quando for requisitado, pois ele funciona semelhante a uma função, e graças ao time ele registra só HH:MM:SS
    horario = db.Column(db.Time, default = lambda: agora().time(), nullable = False)

    status = db.Column(db.String(20), default = "despachado", nullable = False)