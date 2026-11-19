# Aqui é a tabela relacional entre ordens_producao e grupos_producao

from extensions import db

class OrdemGrupo(db.Model):

    __tablename__ = "ordens_grupos"

    id = db.Column(db.Integer, primary_key = True)

    ordem_id = db.Column(db.Integer, db.ForeignKey("ordens_producao.id"), nullable = False)

    grupo_id = db.Column(db.Integer, db.ForeignKey("grupos_producao.id"), nullable = False)

# Aqui os relationship, diferente dos _id, que só são usados no banco de dados, servem para que os dados possam ser visualizados e manipulados no próprio Python. Em que ordem aponta para a classe OrdemProducao e black_populates relaciona o nome variável que está no arquivo que você quer relacionar, nesse caso grupos_associados está em ordens_producao.py
    ordem = db.relationship("OrdemProducao", back_populates = "grupos_associados")

    grupo = db.relationship("GrupoProducao", back_populates = "ordens_associadas")

    __table_args__ = (db.UniqueConstraint("ordem_id", "grupo_id", name = "uq_ordem_grupo"),)

# A razão de existir uma tabela intermediária é pra que possa fazer a relação corretamente de diferentes grupos com diferentes odp:

'''Grupo	    OdPs associadas
Grupo 1	        OdP 100, OdP 101
Grupo 2	        OdP 100, OdP 102'''

