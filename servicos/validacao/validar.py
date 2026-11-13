from servicos.validacao.tratador_erros import NenhumArquivoEncontradoError, ArquivoInvalidoError

def validar_arquivo(arquivo):

    if not arquivo:
        raise NenhumArquivoEncontradoError()
        
    elif not arquivo.filename.lower().endswith(".pdf"):
        raise ArquivoInvalidoError()
    else:
        return True