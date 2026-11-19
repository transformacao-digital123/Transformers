from extensions import db

class Pallet(db.Model):

    __tablename__ = "pallets"

    id = db.Column(db.Integer, primary_key = True)

    ordem_id = db.Column(db.Integer, db.ForeignKey("ordens_producao.id"), nullable = False)

    numero_pallet = db.Column(db.Integer, nullable = False)

# O uselist=False informa que palete.pesagem deve retornar um único objeto, e não uma lista, no caso retornar os pesos ligados aquele pallet e não todos os pesos que já foram catalogados anteriormente
# Aqui o relacionamento é de 1:1 em que um único pallet pertence a uma única pesagem
    pesagem = db.relationship("PesagemProducao", back_populates = "pallet", uselist = False)

# Aqui o relacionamento é de 1:N em que um pallet pode pouir mais de um despacho, no caso de cancelar e depachar de novo, por exemplo, já o despacho pertence a um único pallet
    despacho = db.relationship("Despacho", back_populates = "pallet")

# Aqui o relacionamento é de 1:N em que um pallet possuindo vários registros históricos mas o histoprico pertence só a um pallet
    historico = db.relationship("HistoricoProducao", back_populates = "pallet")

# Aqui a relaçã é de 1:N pois um pallet faz referência a uma única odp, já uma odp pode possui vários pallets
    ordem = db.relationship("OrdemProducao", back_populates = "pallet")

# O __table_args__ permite  configurar regras e atributos especiais que vão além da definição individual de cada coluna, como nesse caso
# Aqui o UniqueConstraint garante a unicidade, ou seja, impede que certos valores se repitam, valores esses que são "ordem_id" e "numero_pallet" que participarão da regra, impedindo que uma sequência de mesmo NNº de pallet e OdP se repitam. O "uq_pallet_ordem_numero" serve para identificarmos a regra quando formos consultar o banco de dados afim de verificar erros ou criar migrações. E a , está ali pra considerar que tudo aquilo é uma espressão que deve ser operada, sem ela, em python, interpretariasse que os elementos dentro das aspas nas tuplas seriam apenas uma espressão entre parênteses, textos, e não tuplas de fato
    __table_args__ = (db.UniqueConstraint("ordem_id", "numero_pallet", name = "uq_pallet_ordem_numero"),)