from extensions import db

class Usuario(db.Model):

    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key = True)

    senha_hash = db.Column(db.String(255), nullable = False)

    usuario = db.Column(db.String(20), nullable = False, unique = True)