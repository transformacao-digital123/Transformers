import os

# O Config resúne as configurações da aplicação
class Config:

# Evita um mecanismo de monitoramento desnecessário
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Procura a conexão no ambiente, se não encontrar utiliza a conexão local
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:%40Luari123@localhost:5432/transformers_testing")