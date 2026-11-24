from extensions import db
from servicos.conversao.data import agora

class HistoricoProducao(db.Model):

    __tablename__ = "historicos_producao"

    id = db.Column(db.Integer, primary_key = True)

    ordem_id = db.Column(db.Integer, db.ForeignKey("ordens_producao.id"), nullable = False)

    pallet_id = db.Column(db.Integer, db.ForeignKey("pallets.id"), nullable = False)

    criado_em = db.Column(db.DateTime(timezone = True), default = agora, nullable = False)

    acao = db.Column(db.String(20), nullable = False)

    campo_alterado = db.Column(db.String(30), nullable = False)

    valor_anterior = db.Column(db.Text, nullable = True)

    valor_novo = db.Column(db.Text, nullable = True)

# Aqui o relacionamento é de 1:N em que um pallet possuindo vários registros históricos mas o histprico pertence só a um pallet
    pallet = db.relationship("Pallet", back_populates = "historico")

    ordem = db.relationship("OrdemProducao", back_populates = "historico")