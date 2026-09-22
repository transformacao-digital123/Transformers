import win32api
import win32print
import win32com.client

import os

def imprimir_etiqueta(caminho):

    print("CAMINHO:", os.path.abspath(caminho))
    print("ARQUIVO EXISTE?", os.path.exists(caminho))

# Esse comando descobre qual o nome da impressora padrão
    impressora = win32print.GetDefaultPrinter()

    print("IMPRESSORA:", impressora)

# O win32api.ShellExecute serve para acessar através da API do Windows a impressora padrão e executar os seguintes comandos:
# O 0 representa que aquele comando não precisa que seja dada importância a ele, no caso, o win32api.ShellExecute têm 6 exigências, e no caso apenas dissemos que essas, que são de abrir a janela da impressão, e a de abrir qualquer outra janela praauxiliar no processo, como bloco de notas, não são necessários aqui
# O "print" é literalmente o comando de imprimir
# /d serve para para forçar o Windows mandar o arquivo direto a impressora padrão, que está especificada ali, para que não apareça uma mensagem na tela perguntando qual impressora vc escolhe
# O "." serve apenas como um apoio, caso ele tenha alguma dúvida de algum processo ele consulta o diretório principal do Transformers
    win32api.ShellExecute(
        0,
        "print",
        caminho,
        f'/d:"{impressora}"',
        ".",
        0
    )