from extensions import db

class Pallet(db.Model):

    __tablename__ = "pallets"

    id = db.Column(db.Integer, primary_key = True)

    ordem_id = db.Column(db.Integer, db.ForeignKey("ordens_producao.id"), nullable = False)

    numero_pallet = db.Column(db.Integer, nullable = False)

# O __table_args__ permite  configurar regras e atributos especiais que vão além da definição individual de cada coluna, como nesse caso
# Aqui o UniqueConstraint garante a unicidade, ou seja, impede que certos valores se repitam, valores esses que são "ordem_id" e "numero_pallet" que participarão da regra, impedindo que uma sequência de mesmo NNº de pallet e OdP se repitam. O "uq_pallet_ordem_numero" serve para identificarmos a regra quando formos consultar o banco de dados afim de verificar erros ou criar migrações. E a , está ali pra considerar que tudo aquilo é uma espressão que deve ser operada, sem ela, em python, interpretariasse que os elementos dentro das aspas nas tuplas seriam apenas uma espressão entre parênteses, textos, e não tuplas de fato
    __table_args__ = (db.UniqueConstraint("ordem_id", "numero_pallet", name = "uq_pallet_ordem_numero"),)