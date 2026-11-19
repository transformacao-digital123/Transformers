from extensions import db

class Usuario(db.Model):

    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key = True)

    senha = db.Column(db.Text, nullable = False)

    usuario = db.Column(db.String(20), nullable = False, unique = True)