from typing import List, Any

from PyQt6 import uic, QtWidgets, QtGui
from PyQt6.QtGui import QIcon, QGuiApplication, QPixmap
from PyQt6.QtWidgets import QApplication, QButtonGroup, QRadioButton

# import icecream as ic
from PyQt6.QtCore import QDateTime
from datetime import datetime
import keyboard
from hti_funcoes import conexao_banco
import hti_global as hg
from venda import executar_consulta
import os

app = QApplication([])
app.setStyleSheet(hg.style_sheet)
tela = uic.loadUi(f"{hg.c_ui}\\venda_ini.ui")
icon = QIcon(f"{hg.c_imagem}\\htiico.jpg")
tela.setWindowIcon(icon)
tela.setWindowTitle(f"PEDIDO DE VENDA         {hg.SISTEMA}  Versao: {hg.VERSAO}")
# Centraliza a janela na tela
qt_rectangle = tela.frameGeometry()
center_point = app.primaryScreen().availableGeometry().center()
qt_rectangle.moveCenter(center_point)
tela.move(qt_rectangle.topLeft())
icon_sair = QIcon(f"{hg.c_imagem}\\sair.png")
icon_salvar = QIcon(f"{hg.c_imagem}\\confirma.png")
icon_consulta = QIcon(f"{hg.c_imagem}\\consulta.png")
tela.setWindowIcon(icon)
# Centraliza a janela na tela
# AJUSTAR A TELA EM RELACAO AO MONITOR
qt_rectangle = tela.frameGeometry()
center_point = app.primaryScreen().availableGeometry().center()
qt_rectangle.moveCenter(center_point)
tela.move(qt_rectangle.topLeft())
lbl_produto = tela.findChild(QtWidgets.QLabel, "produto")
lbl_produto.setText("C A I X A   L I V R E ")
if os.path.exists(f"{hg.c_imagem}\\htifirma.jpg"):
    imagem = QPixmap(f"{hg.c_imagem}\\htifirma.jpg")
else:
    imagem = QPixmap(f"{hg.c_imagem}\\htifirma1.jpg")

pixmap_redimensionado = imagem.scaled(350, 50)  # redimensiona a imagem para 100x100
tela.empresa.setPixmap(pixmap_redimensionado)

lbl_forma_pagamento = tela.findChild(QtWidgets.QLabel, "lb_forma_pagamento")

conexao_banco()

hg.conexao_cursor.execute(f"SELECT cod_cli, razao, nome FROM saccli order by razao")
arq_cli = hg.conexao_cursor.fetchall()
hg.conexao_bd.commit()
for ret_cli in arq_cli:
    item = f"{str(ret_cli[0]).zfill(5)} - {ret_cli[1]} - {ret_cli[2]}".strip("(),")
    tela.cb_cliente.addItem(item)
tela.cb_cliente.setCurrentIndex(0)

hg.conexao_cursor.execute(f"SELECT scod_op, snome FROM insopera ORDER BY snome")
# Recupere o resultado
arq_usuario = hg.conexao_cursor.fetchall()
hg.conexao_bd.commit()
for ret_usuario in arq_usuario:
    item = f"{ret_usuario[0]} - {ret_usuario[1]}".strip("(),")
    tela.cb_vendedor.addItem(item)
    tela.cb_representante.addItem(item)

tela.cb_vendedor.setCurrentIndex(0)
tela.cb_representante.setCurrentIndex(0)

hg.conexao_cursor.execute(
    f"SELECT codigo, descri, percent, cond, COALESCE(dia1, 0), COALESCE(dia2, 0) , "
    f"COALESCE(dia3, 0), COALESCE(dia4, 0), COALESCE(dia5, 0), COALESCE(dia6, 0), COALESCE(dia7, 0), "
    f"COALESCE(dia8, 0), COALESCE(dia9, 0), COALESCE(dia10, 0), COALESCE(dia11, 0), COALESCE(dia12, 0), "
    f"COALESCE(dia13, 0), COALESCE(dia14, 0), COALESCE(dia15, 0) FROM sactabpg ORDER BY codigo"
)
# Recupere o resultado
arq_sactabpg = hg.conexao_cursor.fetchall()
hg.conexao_bd.commit()

tela.cb_cond_pagamento.addItem("000-DEFAULT                                     ")
for ret_sactabpg in arq_sactabpg:
    # print(f"{ret_sactabpg[2]:,.2f}".replace(",", " ").replace(".", ","))
    # formatar numero com tamanho de 8
    valor = "{:,.2f}".format(ret_sactabpg[2]).rjust(6)

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

    item = (
        f"{ret_sactabpg[0]}-{ret_sactabpg[1]}-(%):{valor}-Cond: {ret_sactabpg[3][0]}+{ret_sactabpg[3][1:3]} "
        f"dias: {mdia1} {mdia2} {mdia3} {mdia4} {mdia5} {mdia6} {mdia7} {mdia8} {mdia9} {mdia10} "
        f"{mdia11} {mdia12} {mdia13} {mdia14} {mdia15}"
    )

    tela.cb_cond_pagamento.addItem(item)

tela.cb_cond_pagamento.setCurrentIndex(0)

rb_tipo_venda_group = QButtonGroup()
rb_tipo_venda_group.addButton(tela.rb_av_ap_a, id=1)
rb_tipo_venda_group.addButton(tela.rb_av_ap_p, id=2)
tela.rb_av_ap_a.setChecked(True)


def fecha_tela():
    tela.close()
    return


def buscar_pedido():
    tela.cb_pedido.clear()
    itens = "Numero      Cliente  ValorR$"
    tela.cb_pedido.addItem(itens)
    hg.conexao_cursor.execute(
        f"SELECT pnum_ped, pcod_cli, sum(pquantd * pvlr_fat) FROM sacped_s "
        f"WHERE sr_deleted = ' ' AND (ppag IS NULL OR ppag = ' ') group by 1,2"
    )
    arq_ped = hg.conexao_cursor.fetchall()
    hg.conexao_bd.commit()
    for ret_ped in arq_ped:
        mcodigo_cliente = str(ret_ped[1]).zfill(5)
        itens = f"{ret_ped[0]} - {mcodigo_cliente} - {ret_ped[2]}"
        tela.cb_pedido.addItem(itens)
    tela.cb_pedido.setCurrentIndex(0)


def buscar_orcamento(self):
    tela.cb_orcamento.clear()
    itens = "Numero      Cliente  ValorR$"
    tela.cb_orcamento.addItem(itens)
    hg.conexao_cursor.execute(
        f"SELECT pnum_ped, pcod_cli, sum(pquantd * pvlr_fat) FROM sacorcam "
        f"WHERE sr_deleted = ' ' AND (ppag IS NULL OR ppag = ' ') group by 1,2"
    )
    arq_orca = hg.conexao_cursor.fetchall()
    hg.conexao_bd.commit()
    for ret_ped in arq_orca:
        itens = f"{ret_ped[0]} - {ret_ped[1]} - {ret_ped[2]}"
        tela.cb_orcamento.addItem(itens)
    tela.cb_orcamento.setCurrentIndex(0)


def buscar_os(self):
    tela.cb_os.clear()
    itens = "Numero      Cliente  ValorR$"
    tela.cb_os.addItem(itens)
    hg.conexao_cursor.execute(
        f"SELECT num_os, (select razao from saccli cli where cli.cod_cli = os.cod_cli) "
        f"FROM sacoss os WHERE (num_ped IS NULL OR num_ped = ' ')"
    )
    arq_os = hg.conexao_cursor.fetchall()
    hg.conexao_bd.commit()
    for ret_ped in arq_os:
        itens = f"{ret_ped[0] - ret_ped[1]}"
        tela.cb_os.addItem(itens)
    tela.cb_os.setCurrentIndex(0)


def salvar_informacao():
    # adicionar item no final da lista
    informacao_pedido = []
    mnum_ped = ""
    mnum_os = ""
    mnum_orcamento = ""
    mcod_cliente = ""
    mcod_cond_pg = ""
    mcod_vendedor = ""
    mav_ap = ""
    mcod_pagamento = ""
    mpercentual_tab = ""
    mavaria = ""

    index = tela.cb_pedido.currentIndex()
    mop = tela.cb_pedido.itemText(index)
    mnum_ped = mop[0:6]
    if mnum_ped == "Numero":
        mnum_ped = ""

    index = tela.cb_os.currentIndex()
    mop = tela.cb_os.itemText(index)
    mnum_os = mop[0:6]
    if mnum_os == "Numero":
        mnum_os = ""

    index = tela.cb_orcamento.currentIndex()
    mop = tela.cb_orcamento.itemText(index)
    mnum_orcamento = mop[0:6]
    if mnum_orcamento == "Numero":
        mnum_orcamento = ""

    index = tela.cb_cliente.currentIndex()
    mop = tela.cb_cliente.itemText(index)
    mcod_cliente = mop[0:48]

    index = tela.cb_vendedor.currentIndex()
    mop = tela.cb_vendedor.itemText(index)
    mcod_vendedor = mop[0:36]

    index = tela.cb_cond_pagamento.currentIndex()
    mop = tela.cb_cond_pagamento.itemText(index)
    mcod_pagamento = mop[0:70]

    if tela.rb_av_ap_a.isChecked():
        mav_ap = "A"
    elif tela.rb_av_ap_p.isChecked():
        mav_ap = "P"

    informacao_pedido.append(mnum_ped)
    informacao_pedido.append(mnum_os)
    informacao_pedido.append(mnum_orcamento)
    informacao_pedido.append(mcod_cliente)
    informacao_pedido.append(mcod_vendedor)
    informacao_pedido.append(mav_ap)
    informacao_pedido.append(mcod_pagamento)
    print(informacao_pedido)
    # executar_consulta(informacao_pedido)
    return


def ver_pedido():
    index = tela.cb_pedido.currentIndex()
    mop = tela.cb_pedido.itemText(index)
    mnum_ped = mop[0:6]
    m_cod_cliente = mop[13:18]
    if mnum_ped == "Numero":
        return

    if hg.m_set[4] == "S":
        tela.rb_av_ap_a.setDisabled(True)
        tela.rb_av_ap_p.setDisabled(True)

    if hg.m_set[45] == "S":
        tela.cb_cond_pagamento.setDisabled(True)

    ver_cliente()

    hg.conexao_cursor.execute(
        f"SELECT COALESCE(pnum_ped,''), COALESCE(pcod_cli,0), COALESCE(pcod_vend,''), "
        f"COALESCE(tipo_venda,''), COALESCE(pcod_tab,'')  FROM sacped_s "
        f"WHERE pnum_ped = {mnum_ped}"
    )
    arq_ped = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()
    if arq_ped is None:
        print("Pedido nao encontrado....")
        return

    for i in range(tela.cb_cliente.count()):
        item_text = tela.cb_cliente.itemText(i)
        if str(m_cod_cliente).strip() in item_text:
            tela.cb_cliente.setCurrentIndex(i)
            break

    for i in range(tela.cb_vendedor.count()):
        item_text = tela.cb_vendedor.itemText(i)
        if str(arq_ped[2]).strip() in item_text:
            tela.cb_vendedor.setCurrentIndex(i)
            break

    for i in range(tela.cb_cond_pagamento.count()):
        item_text = tela.cb_cond_pagamento.itemText(i)
        if str(arq_ped[4]).strip() in item_text:
            tela.cb_cond_pagamento.setCurrentIndex(i)
            break
        else:
            tela.cb_cond_pagamento.setCurrentIndex(0)
            break

    rb_av_ap = QButtonGroup()
    rb_av_ap.addButton(tela.rb_av_ap_a, id=1)
    rb_av_ap.addButton(tela.rb_av_ap_p, id=2)
    if arq_ped[3] == '1':
        tela.rb_av_ap_a.setChecked(True)
    else:
        tela.rb_av_ap_p.setChecked(True)

    # mnum_pedido = '145082'
    # informacao_pedido.append(mnum_ped)

    salvar_informacao()


def ver_cond_pagamento():
    index = tela.cb_cond_pagamento.currentIndex()
    mop = tela.cb_cond_pagamento.itemText(index)
    m_cod_cond_pg = mop[0:3]
    if m_cod_cond_pg == "   ":
        return
    hg.conexao_cursor.execute(
        f"SELECT COALESCE(percent,0), COALESCE(cond, '   '), COALESCE(dia1, 0), "
        f"COALESCE(dia2, 0) , "
        f"COALESCE(dia3, 0), COALESCE(dia4, 0), COALESCE(dia5, 0), COALESCE(dia6, 0), "
        f"COALESCE(dia7, 0), COALESCE(dia8, 0), COALESCE(dia9, 0), COALESCE(dia10, 0), "
        f"COALESCE(dia11, 0), COALESCE(dia12, 0), COALESCE(dia13, 0), COALESCE(dia14, 0), "
        f"COALESCE(dia15, 0)  FROM sactabpg where codigo = {m_cod_cond_pg}"
    )
    # Recupere o resultado
    ver_sactabpg = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()
    mpercentual = ver_sactabpg[0]
    if ver_sactabpg[1] == "   ":
        mcond = "000"
    else:
        mcond = ver_sactabpg[1]

    mcondicao = (
        f"Percentual (%): {mpercentual} - Entrada: {mcond[0:1]} + {mcond[1:3]} dias"
    )
    media_dias = (
        ver_sactabpg[2]
        + ver_sactabpg[3]
        + ver_sactabpg[4]
        + ver_sactabpg[5]
        + ver_sactabpg[6]
        + ver_sactabpg[7]
        + ver_sactabpg[8]
        + ver_sactabpg[9]
        + ver_sactabpg[10]
        + ver_sactabpg[11]
        + ver_sactabpg[12]
        + ver_sactabpg[13]
        + ver_sactabpg[14]
        + ver_sactabpg[15]
        + ver_sactabpg[16]
    )
    if float(mcond[1:3]) >= 1:
        mcondicao += f" Prazos: {ver_sactabpg[2]}"
    if float(mcond[1:3]) >= 2:
        mcondicao += f" {ver_sactabpg[3]}"
    if float(mcond[1:3]) >= 3:
        mcondicao += f" {ver_sactabpg[4]}"
    if float(mcond[1:3]) >= 4:
        mcondicao += f" {ver_sactabpg[5]}"
    if float(mcond[1:3]) >= 5:
        mcondicao += f" {ver_sactabpg[6]}"
    if float(mcond[1:3]) >= 6:
        mcondicao += f" {ver_sactabpg[7]}"
    if float(mcond[1:3]) >= 7:
        mcondicao += f" {ver_sactabpg[8]}"
    if float(mcond[1:3]) >= 8:
        mcondicao += f" {ver_sactabpg[9]}"
    if float(mcond[1:3]) >= 9:
        mcondicao += f" {ver_sactabpg[10]}"
    if float(mcond[1:3]) >= 10:
        mcondicao += f" {ver_sactabpg[11]}"
    if float(mcond[1:3]) >= 11:
        mcondicao += f" {ver_sactabpg[12]}"
    if float(mcond[1:3]) >= 12:
        mcondicao += f" {ver_sactabpg[13]}"
    if float(mcond[1:3]) >= 13:
        mcondicao += f" {ver_sactabpg[14]}"
    if float(mcond[1:3]) >= 14:
        mcondicao += f" {ver_sactabpg[15]}"
    if float(mcond[1:3]) >= 15:
        mcondicao += f" {ver_sactabpg[16]}"

    media_dias = float(media_dias) / float(mcond[1:3])
    media_dias = "{:,.0f}".format(media_dias).rjust(3)
    mcondicao += f" - Medias de dias: {media_dias}"

    lbl_forma_pagamento.setText(mcondicao)

    # print(mcondicao)


def ver_cliente():
    index = tela.cb_cliente.currentIndex()
    mop = tela.cb_cliente.itemText(index)
    mcodigo_cliente = mop[0:5]

    hg.conexao_cursor.execute(
        f"SELECT COALESCE(codvend,0), COALESCE(cod_cond, '   ') FROM saccli where cod_cli = {mcodigo_cliente}"
    )
    # Recupere o resultado
    vercliente = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()

    for i in range(tela.cb_vendedor.count()):
        item_text = tela.cb_vendedor.itemText(i)
        if str(vercliente[0]).strip() in item_text:
            tela.cb_vendedor.setCurrentIndex(i)
            break

    for i in range(tela.cb_cond_pagamento.count()):
        item_text = tela.cb_cond_pagamento.itemText(i)
        if str(vercliente[1]).strip() in item_text:
            tela.cb_cond_pagamento.setCurrentIndex(i)
            break
        else:
            tela.cb_cond_pagamento.setText('000')


def pedido_inicial():
    tela.cb_pedido.currentIndexChanged.connect(ver_pedido)
    tela.cb_cond_pagamento.currentIndexChanged.connect(ver_cond_pagamento)
    tela.cb_cliente.currentIndexChanged.connect(ver_cliente)
    # tela.cb_cond_pagamento.currentIndexChanged.connect(ver_cliente)

    tela.pb_buscar_cliente.setIcon(icon_consulta)
    # tela.pb_buscar_cliente.currentIndexChanged.connect()

    tela.pb_buscar_pedido.setIcon(icon_consulta)
    tela.pb_buscar_pedido.clicked.connect(buscar_pedido)

    tela.pb_buscar_os.setIcon(icon_consulta)
    tela.pb_buscar_os.clicked.connect(buscar_os)

    tela.pb_buscar_orcamento.setIcon(icon_consulta)
    tela.pb_buscar_orcamento.clicked.connect(buscar_orcamento)

    tela.bt_fecha.setIcon(icon_salvar)
    tela.bt_fecha.clicked.connect(salvar_informacao)

    tela.bt_sair.clicked.connect(fecha_tela)
    tela.bt_sair.setIcon(icon_sair)

    tela.cb_representante.setDisabled(True)
    if hg.m_set[151] == "S":
        tela.cb_representante.setDisabled(False)

    tela.rb_av_ap_a.setDisabled(True)
    tela.rb_av_ap_p.setDisabled(True)
    if hg.m_set[4] == "S":
        tela.rb_av_ap_a.setDisabled(False)
        tela.rb_av_ap_p.setDisabled(False)

    tela.cb_cond_pagamento.setDisabled(True)
    if hg.m_set[45] == "S":
        tela.cb_cond_pagamento.setDisabled(False)

    for i in range(tela.cb_cliente.count()):
        item_text = tela.cb_cliente.itemText(i)
        if str(hg.m_set[83]).zfill(5) in item_text:
            tela.cb_cliente.setCurrentIndex(i)
            break

    tela.show()
    app.exec()


if __name__ == "__main__":
    pedido_inicial()
    hg.conexao_bd.close()