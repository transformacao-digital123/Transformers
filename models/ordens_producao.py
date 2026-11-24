from extensions import db

class OrdemProducao(db.Model):

    __tablename__ = "ordens_producao"

    id = db.Column(db.Integer, primary_key = True)

# O relacionamento entre grupos e ordens_producao está em ordens_grupos.py

# Aqui é string devido a / ou - da OdP

    pedido = db.Column(db.String(20), nullable = False)

    odp = db.Column(db.String(20), nullable = False)

    cliente = db.Column(db.String(255), nullable = False)

    padrao = db.Column(db.String(60), nullable = False)

    filme = db.Column(db.String(40), nullable = False)

    peso_tubete = db.Column(db.Numeric(10,2), nullable = False)

    observacoes = db.Column(db.Text, nullable = True)

# Identificador 
    chave_origem = db.Column(db.String(36), nullable = False, unique = True)

# Identificador da ocorrência por meio do QRcode, representando todas as OdP ligadas aquele QR, independente de quantos pallets aja
    identificador = db.Column(db.String(30), nullable = False)

# Aqui o relacionamento é de N:1 em que um grupo pode possui várias ocorrências, mas 1 ocorrência (Identificador do QRcode) só pertence a um grupo
    grupo_id = db.Colum(db.Integer, db.ForeignKey("grupos_producao.id"), nullable = False)

    grupo = db.relationship("GrupoProducao", back_populates = "ordens")

# Aqui a relaçã é de 1:N pois um pallet faz referência a uma única odp, já uma odp pode possui vários pallets
    pallet = db.relationship("Pallet", back_populates = "ordem")

    historico = db.relationship("HistoricoProducao", back_populates = "ordem")

