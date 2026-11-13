#importações vindas de outros arquivos
from servicos.validacao.validar import validar_arquivo
from servicos.interpretacao.extrator_pdf import processar_pdf
from servicos.arquivos.planilha import preencher_planilha
from servicos.log.logger import registrar_info, registrar_erro
from servicos.progresso.progresso import atualizar_progresso
from servicos.validacao.tratador_erros import NaoAcrescentarOdpEmArquivoPdfError

def converter_pdf(arquivo, id_conversao, acrescentar = False):

    atualizar_progresso(id_conversao, 0)
            
    try:

        if acrescentar:
            raise NaoAcrescentarOdpEmArquivoPdfError()

# Comandos para executar as análises dos dados do PDF e o preenchimento do Excel
        validar_arquivo(arquivo)
        dados = processar_pdf(arquivo)
        arquivo_excel = preencher_planilha(dados)

        registrar_info(
            f"Conversão do {arquivo.filename} realizada com sucesso!"
        )

        return arquivo_excel
    
    except Exception as erro:

# Registra o erro e envia para o logger afim de que o desenvolvedor saiba qual o erro   
        registrar_erro(str(erro))
        raise