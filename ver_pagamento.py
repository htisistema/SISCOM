from PyQt6 import uic
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication
from hti_funcoes import conexao_banco
import hti_global as hg

app = QApplication([])
app.setStyleSheet(hg.style_sheet)
tela_pg = uic.loadUi(f"{hg.c_ui}\\tipo_pagamento.ui")
icon = QIcon(f"{hg.c_imagem}\\htiico.ico")
tela_pg.setWindowIcon(icon)
icon_salvar = QIcon(f"{hg.c_imagem}\\confirma.png")
icon_sair = QIcon(f"{hg.c_imagem}\\sair.png")
tela_pg.setWindowIcon(icon)
tela_pg.setWindowTitle(f"DADOS DO CARTAO         {hg.SISTEMA}  Versao: {hg.VERSAO}")
# Centraliza a janela na tela_pg
qt_rectangle_pg = tela_pg.frameGeometry()
center_point_pg = app.primaryScreen().availableGeometry().center()
qt_rectangle_pg.moveCenter(center_point_pg)
tela_pg.move(qt_rectangle_pg.topLeft())
conexao_banco()
hg.conexao_cursor.execute(
    "SELECT codigo, descri, percent, cond, COALESCE(dia1, 0), COALESCE(dia2, 0) , "
    "COALESCE(dia3, 0), COALESCE(dia4, 0), COALESCE(dia5, 0), COALESCE(dia6, 0), "
    "COALESCE(dia7, 0), COALESCE(dia8, 0), COALESCE(dia9, 0), COALESCE(dia10, 0), "
    "COALESCE(dia11, 0), COALESCE(dia12, 0), COALESCE(dia13, 0), COALESCE(dia14, 0), "
    "COALESCE(dia15, 0) FROM sactabpg ORDER BY codigo"
)
# Recupere o resultado
arq_sactabpg = hg.conexao_cursor.fetchall()
hg.conexao_bd.commit()

tela_pg.cb_tipo_pg.addItem("000-DEFAULT                                     ")
for ret_sactabpg in arq_sactabpg:
    # print(f"{ret_sactabpg[2]:,.2f}".replace(",", " ").replace(".", ","))
    # formatar numero com tamanho de 8
    valor = "{:,.2f}".format(ret_sactabpg[2]).rjust(7)

    mdia1 = "{:,.0f}".format(ret_sactabpg[4]).rjust(3)
    mdia2 = "{:,.0f}".format(ret_sactabpg[5]).rjust(3)
    mdia3 = "{:,.0f}".format(ret_sactabpg[6]).rjust(3)
    mdia4 = "{:,.0f}".format(ret_sactabpg[7]).rjust(3)
    mdia5 = "{:,.0f}".format(ret_sactabpg[8]).rjust(3)
    mdia6 = "{:,.0f}".format(ret_sactabpg[9]).rjust(3)
    mdia7 = "{:,.0f}".format(ret_sactabpg[10]).rjust(3)
    mdia8 = "{:,.0f}".format(ret_sactabpg[11]).rjust(3)
    mdia9 = "{:,.0f}".format(ret_sactabpg[12]).rjust(3)
    mdia10 = "{:,.0f}".format(ret_sactabpg[13]).rjust(3)
    mdia11 = "{:,.0f}".format(ret_sactabpg[14]).rjust(3)
    mdia12 = "{:,.0f}".format(ret_sactabpg[15]).rjust(3)
    mdia13 = "{:,.0f}".format(ret_sactabpg[16]).rjust(3)
    mdia14 = "{:,.0f}".format(ret_sactabpg[17]).rjust(3)
    mdia15 = "{:,.0f}".format(ret_sactabpg[18]).rjust(3)
    # valor = f"{ret_sactabpg[0][2]:,.2f}".replace(",", " ").replace(".", ",")
    item_pg = (
        f"{ret_sactabpg[0]}-{ret_sactabpg[1]}-(%):{valor}-Cond: {ret_sactabpg[3][0]}+{ret_sactabpg[3][1:3]} "
        f"dias: {mdia1} {mdia2} {mdia3} {mdia4} {mdia5} {mdia6} {mdia7} {mdia8} {mdia9} {mdia10} "
        f"{mdia11} {mdia12} {mdia13} {mdia14} {mdia15}"
    )

    tela_pg.cb_tipo_pg.addItem(item_pg)


def confirma():
    tela_pg.close()
    mnumero = tela_pg.n_documento.text()
    print(mnumero)
    return mnumero
    # from venda_pdvcx import verifica_condicao
    # verifica_condicao()


def sair():
    tela_pg.close()
    return


def ver_pagamento(mno):
    tela_pg.cb_tipo_pg.setCurrentIndex(0)
    tela_pg.bt_confirma.clicked.connect(confirma)
    tela_pg.bt_confirma.setIcon(icon_salvar)
    tela_pg.bt_sair.clicked.connect(sair)
    tela_pg.bt_sair.setIcon(icon_sair)
    tela_pg.show()
