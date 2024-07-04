from reportlab.pdfgen import canvas
from reportlab.lib.units import mm


def mm2p(milimetros):
    return milimetros * mm

# Caminho absoluto para a imagem
imagem_caminho = r"C:\HTI\PYTHON\SISCOM\imagem\001.jpg"

# Cria o canvas
c = canvas.Canvas("example.pdf")

# Desenha uma string
c.drawString(mm2p(5), mm2p(280), "Exemplo de Texto")

# Desenha uma imagem
try:
    # Coordenadas (x, y) e dimensões (largura, altura)
    c.drawImage(imagem_caminho, mm2p(5), mm2p(230), width=mm2p(15), height=mm2p(15))
except IOError:
    print(f"Erro ao abrir o arquivo de imagem: {imagem_caminho}")

# Fecha o canvas
c.showPage()
c.save()
