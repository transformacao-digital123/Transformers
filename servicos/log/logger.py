import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    "logs.txt", #  É o nome e caminho do arquivo principal onde os logs serão gravados inicialmente
    maxBytes= 5 * 1024 * 1024, # Guarda até 5 MB : 5 X 1024 = 5120 KB,5 X 1024 = 5 MB ou 5000 KB
    backupCount= 3, # Número máximo de arquivos que o sistema irá guardar podendo chegar a 20 MB se todos estiverem preenchidos, com o seu atual podendo guardar 5 MB masi os 5 dos outros 3 arquivos
    encoding= "utf-8" # Garante que o arquivo seja gravado usando a codificação UTF-8. Isso evita erros de formatação e permite que o sistema salve corretamente caracteres especiais, acentos e emojis nos logs.
)

logging.basicConfig(
    filename = "logs.txt",
    level= logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def registrar_info(mensagem):
    logging.info(mensagem)

def registrar_erro(mensagem):
    logging.error(mensagem)