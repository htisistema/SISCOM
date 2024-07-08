# from PyQt6.QtCore import QDate
# import hti_global as hg
#
# # Suponha que hg.mdata_sis seja uma string no formato "YYYY-MM-DD"
# print(hg.mdata_sis)
# # mdata_sis = hg.mdata_sis.strftime("%Y/%m/%d")
# # Converte a string para um objeto QDate
# mdata_sis = QDate.fromString(hg.mdata_sis, "yyyy-MM-dd")
# print(mdata_sis)
# # Verifique se a conversão foi bem-sucedida
# if not mdata_sis.isValid():
#     raise ValueError(f"Data inválida: {hg.mdata_sis}")
#
# # Adiciona os dias ao QDate
# mdia = 10  # Exemplo de número de dias a adicionar
# mdata_f = mdata_sis.addDays(mdia)
# print(mdata_f)
# # Imprime a nova data
# mdata_sis = mdata_f.toString("yyyy-MM-dd")
# print(mdata_sis)
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm


def mm2p(milimetros):
    return milimetros * mm


# Cria o canvas
c = canvas.Canvas(f"c:\\hti\\python\siscom\\teste.pdf", pagesize=A4)

# Define um texto para a primeira página
c.drawString(mm2p(20), mm2p(280), "Este é o texto da primeira página.")

# Ejetar a primeira página e iniciar uma nova
c.showPage()

# Define um texto para a segunda página
c.drawString(mm2p(20), mm2p(280), "Este é o texto da segunda página.")

# Ejetar a segunda página e iniciar uma nova (se necessário)
c.showPage()

# Define um texto para a terceira página
c.drawString(mm2p(20), mm2p(280), "Este é o texto da terceira página.")

# Fecha o canvas
c.save()
