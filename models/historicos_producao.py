from extensions import db
from servicos.conversao.data import agora

class HistoricoProducao(db.Model):

    __tablename__ = "historicos_producao"

    id = db.Column(db.Integer, primary_key = True)

    ordem_id = db.Column(db.Integer, db.ForeignKey("ordens_producao.id"), nullable = False)

    pallet_id = db.Column(db.Integer, db.ForeignKey("pallets.id"), nullable = False)

    data_pesagem = db.Column(db.Date, default = lambda: agora().date(), nullable = False)

    horario_pesagem = db.Column(db.Time, default = lambda: agora().time(), nullable = False)

    acao = db.Column(db.String(20), nullable = False)

    campo_alterado = db.Column(db.String(30), nullable = False)

    valor_anterior = db.Column(db.String(30), nullable = True)

    valor_novo = db.Column(db.String(30), nullable = True)

# Aqui o relacionamento é de 1:N em que um pallet possuindo vários registros históricos mas o histprico pertence só a um pallet
    pallet = db.relationship("Pallet", back_populates = "historico")

    ordem = db.relationship("OrdemProducao", back_populates = "historico")