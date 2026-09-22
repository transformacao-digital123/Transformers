import qrcode
import os


# O texto servirá como parâmetro no lugar de texto_qr onde ODP, data, turno e operador são parâmetros obrigatórios pois são eles que nos ajudarão a encontrar o caminho até ao arquivo, aba e linha onde está nossa odp
def gerar_qrcode(texto,odp,operador):

# Pegue o conteúdo recebido em odp e transforme-o em uma imagem de QR Code.
        qr = qrcode.make(texto)

        odp_limpo = odp.replace("/","-")

        operario = operador

 # Aqui você aproveitou a própria ODP para criar um nome único para a imagem       
        test = f"QR_{odp_limpo}_{operario}.png"

        caminho = os.path.join("temporario", test)

# Agora a imagem que está na variável qr é realmente gravada no computador
        qr.save(caminho)

# A função não retorna o QR Code em si. Ela retorna o endereço onde a imagem foi salva
        return caminho

def interpretar_qrcode(identificador,rastreabilidade):
        dados = rastreabilidade[identificador]

        print(f"ODP: {dados['odp']}")
        print(f"OPERADOR: {dados['operador']}")
        print(f"DATA: {dados['data']}")
        print(f"TURNO: {dados["turno"]}")

        return dados




	