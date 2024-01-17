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


def salvar_informacao():
    from venda import executar_consulta
    informacao_pedido = []
    mnum_ped = ''
    # adicionar item no final da lista
    informacao_pedido.append(mnum_ped)
    executar_consulta()
    tela.close()
    return


def pedido_inicial():
    tela.pb_buscar_cliente.clicked.connect(salvar_informacao)
    tela.pb_buscar_cliente.setIcon(icon_consulta)
    tela.bt_fecha.clicked.connect(salvar_informacao)
    tela.bt_fecha.setIcon(icon_salvar)
    tela.bt_sair.clicked.connect(fecha_tela)
    tela.bt_sair.setIcon(icon_sair)

    tela.show()
    app.exec()


if __name__ == "__main__":
    pedido_inicial()
    hg.conexao_bd.close()
