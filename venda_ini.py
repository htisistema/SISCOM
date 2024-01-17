from typing import List, Any

from PyQt6 import uic, QtWidgets, QtGui
from PyQt6.QtGui import QIcon, QGuiApplication, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QButtonGroup
from PyQt6.QtCore import QDateTime
from datetime import datetime
import keyboard
from hti_funcoes import conexao_banco
import hti_global as hg
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

hg.conexao_cursor.execute(f"SELECT codigo, descri FROM sactabpg ORDER BY codigo")
# Recupere o resultado
arq_sactabpg = hg.conexao_cursor.fetchall()
hg.conexao_bd.commit()

tela.cb_cond_pagamento.addItem("000 - DEFAULT")
for ret_sactabpg in arq_sactabpg:
    item = f"{ret_sactabpg[0]} - {ret_sactabpg[1]}".strip("(),")
    tela.cb_cond_pagamento.addItem(item)

tela.cb_cond_pagamento.setCurrentIndex(0)

rb_tipo_venda_group = QButtonGroup()
rb_tipo_venda_group.addButton(tela.rb_venda_normal, id=1)
rb_tipo_venda_group.addButton(tela.rb_venda_especial, id=2)
tela.rb_venda_normal.setChecked(True)

rb_tipo_pedido_group = QButtonGroup()
rb_tipo_pedido_group.addButton(tela.rb_pedido_normal, id=1)
rb_tipo_pedido_group.addButton(tela.rb_pedido_avaria, id=2)
tela.rb_pedido_normal.setChecked(True)


def fecha_tela():
    tela.close()
    return


def buscar_pedido(self):
    itens = f"       -              "
    tela.cb_pedido.addItem(itens)
    hg.conexao_cursor.execute(f"SELECT pnum_ped, sum(pquantd * pvlr_fat) FROM sacped_s "
                              f"WHERE sr_deleted = ' ' AND (ppag IS NULL OR ppag = ' ') group by 1")
    arq_ped = hg.conexao_cursor.fetchall()
    hg.conexao_bd.commit()
    for ret_ped in arq_ped:
        itens = f"{ret_ped[0]} - {ret_ped[1]}"
        tela.cb_pedido.addItem(itens)
    tela.cb_pedido.setCurrentIndex(0)


def buscar_orcamento(self):
    itens = f"       -              "
    tela.cb_orcamento.addItem(itens)
    hg.conexao_cursor.execute(f"SELECT pnum_PED, sum(pquantd * pvlr_fat) FROM sacorcam "
                              f"WHERE sr_deleted = ' ' AND (ppag IS NULL OR ppag = ' ') group by 1")
    arq_orca = hg.conexao_cursor.fetchall()
    hg.conexao_bd.commit()
    for ret_ped in arq_orca:
        itens = f"{ret_ped[0]} - {ret_ped[1]}"
        tela.cb_orcamento.addItem(itens)
    tela.cb_orcamento.setCurrentIndex(0)


def buscar_os(self):
    itens = f"       -                         "
    tela.cb_os.addItem(itens)
    hg.conexao_cursor.execute(f"SELECT num_os, (select razao from saccli cli where cli.cod_cli = os.cod_cli) "
                              f"FROM sacoss os WHERE (num_ped IS NULL OR num_ped = ' ')")
    arq_os = hg.conexao_cursor.fetchall()
    hg.conexao_bd.commit()
    for ret_ped in arq_os:
        itens = f"{ret_ped[0] - ret_ped[1]}"
        tela.cb_os.addItem(itens)
    tela.cb_os.setCurrentIndex(0)


def salvar_informacao():
    from venda import executar_consulta
    informacao_pedido = []
    mnum_pedido = '145082'
    mnum_os = m_num_os
    mcod_cliente = m_cod_cliente
    mcod_vendedor = m_cod_vendedor
    mtipo_venda = m_tipo_venda
    mcod_pagamento = m_cod_pagamento
    mpercentual_tab = m_percentual_tab
    mcod_representante = m_cod_representante
    mtipo_pedido = m_tipo_pedido
    # adicionar item no final da lista
    informacao_pedido.append(mnum_pedido)
    informacao_pedido.append(mnum_os)
    informacao_pedido.append(mcod_cliente)
    informacao_pedido.append(mcod_vendedor)
    informacao_pedido.append(mtipo_venda)
    informacao_pedido.append(mcod_pagamento)
    informacao_pedido.append(mpercentual_tab)
    informacao_pedido.append(mcod_representante)
    informacao_pedido.append(mtipo_pedido)
    informacao_pedido.append(mcod_cliente)
    executar_consulta(informacao_pedido)
    tela.close()
    return


def pedido_inicial():
    tela.pb_buscar_cliente.setIcon(icon_consulta)
    tela.pb_buscar_cliente.clicked.connect(salvar_informacao)

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

    tela.show()
    app.exec()


if __name__ == "__main__":
    pedido_inicial()
    hg.conexao_bd.close()
