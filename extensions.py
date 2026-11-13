# Aqui é onde é inici   ado tanto o SQLAlchemy quanto o Migrate, para versionamento

from flask_sqlalchemy import SQLAlchemy # Cria a integração entre Flask e PostgreSQL
from flask_migrate import Migrate

# Nossa interface pra trabalhar com os dados
db = SQLAlchemy()

# Permite atualizar a estrutura do banco sem precisar recriá-lo
migrate = Migrate()