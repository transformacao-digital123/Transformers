def validar_arquivo(arquivo):

    if not arquivo:
        print("Nenhum arquivo recebido")
        
    elif not arquivo.filename.lower().endswith(".pdf"):
        print("Arquivo inválido")
    else:
        print("PDF recebido!")
        return True