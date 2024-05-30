import fdb
import configparser
from PyQt6 import uic
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtGui import QIcon, QGuiApplication
from PyQt6.QtWidgets import QButtonGroup, QMessageBox, QLineEdit, QComboBox, QRadioButton
from datetime import date
import os
import hti_global as hg

titulo = "CONSULTA DE USUARIOS"
app = QtWidgets.QApplication([])
app.setStyleSheet(hg.style_sheet)
tela = uic.loadUi(f"{hg.c_ui}\\htiusuario.ui")
icon = QIcon(f"{hg.c_imagem}\\htiico.ico")
icon_cancelar = QIcon(f"{hg.c_imagem}\\cancelar.png")
icon_sair = QIcon(f"{hg.c_imagem}\\sair.png")
icon_salvar = QIcon(f"{hg.c_imagem}\\salvar.png")
icon_incluir = QIcon(f"{hg.c_imagem}\\incluir.png")
tela.setWindowIcon(icon)
# Centraliza a janela na tela
qt_rectangle = tela.frameGeometry()
center_point = app.primaryScreen().availableGeometry().center()
qt_rectangle.moveCenter(center_point)
tela.move(qt_rectangle.topLeft())

if hg.mtp_tela == 'G':
    primary_screen = QGuiApplication.primaryScreen()
    if primary_screen is not None:
        screen_geometry = primary_screen.geometry()
        tela.setGeometry(screen_geometry)

tela.setWindowTitle(titulo)
lbl_titulo_usuario = tela.findChild(QtWidgets.QLabel, "tit_usuario")
lbl_titulo_usuario.setText(titulo)

tela.statusBar = QtWidgets.QStatusBar()
tela.setStatusBar(tela.statusBar)
# PEGA O NOME DO ARQUIVO EM EXECUCAO
nome_file_com = os.path.basename(__file__)
nome_file, ext = os.path.splitext(nome_file_com)

tela.statusBar.showMessage(f"<< {nome_file} >>")

# hg.conexao_cursor.execute("SELECT * FROM sacsetup")
# # Recupere o resultado
# m_set = hg.conexao_cursor.fetchone()
# hg.conexao_bd.commit()

hg.conexao_cursor.execute("SELECT cidade, uf, cep FROM saccid ORDER BY cidade")
# Recupere o resultado
arq_cidade = hg.conexao_cursor.fetchall()
hg.conexao_bd.commit()

# COMBOX
tela.comboBox_2.addItems(hg.estados)
tela.comboBox_2.setCurrentIndex(16)  # coloca o focus no index

for ret_cidade in arq_cidade:
    item = f'{ret_cidade[0]} - {ret_cidade[1]}'.strip('(),')
    tela.comboBox.addItem(item)

tela.comboBox_3.addItems(["A->Administrador", "G->Gerente", "O->Operador", "V->Vendedor", "B->Bloqueado"])
tela.comboBox_3.setCurrentIndex(0)  # coloca o focus no index

tela.comboBox_4.addItems(["S->Siscom", "V->Venda", "C->Caixa", "M->Caixa e Venda"])
tela.comboBox_4.setCurrentIndex(0)  # coloca o focus no index

tela.comboBox_5.addItems([" ", "1", "2", "3", "4", "5", "6", "7", "8", '9'])
tela.comboBox_5.setCurrentIndex(0)  # coloca o focus no index

tela.comboBox_6.addItems([" ", "1", "2", "3", "4", "5", "6", "7", "8", '9'])
tela.comboBox_6.setCurrentIndex(0)  # coloca o focus no index




def on_close_event(event):
    tela.close()
    event.accept()
    # hg.conexao_cursor.close()
    tela.closeEvent = on_close_event


def fecha_tela():
    tela.close()
    tela.closeEvent = on_close_event
    return


def consulta_usuario(codigo_usuario):
    # PEGAR O ULTIMO NUMERO DOS usuario E ACRESCENTA 1
    hg.conexao_cursor.execute(f"SELECT * FROM insopera WHERE scod_op = {codigo_usuario}")
    # # Recupere o resultado
    arq_usu = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()
    tab_widget = tela.findChild(QtWidgets.QTabWidget, "tabWidget")
    tab_widget.setCurrentIndex(0)

    if arq_usu is None:
        QMessageBox.information(tela, "consulta de fornecedor", "Fornecedor nao CADASTRADO !")
        return

    if arq_usu[5] is None:
        data = QtCore.QDate(1900, 1, 1)
    else:
        data_str = arq_usu[5].strftime("%Y-%m-%d")
        data = QtCore.QDate.fromString(data_str, "yyyy-MM-dd")
        data = QtCore.QDateTime(data, QtCore.QTime(0, 0, 0))
    tela.msdata_cad.setDateTime(data)

    # if arq_usu[5] is None:
    #     data = QtCore.QDate(1900, 1, 1)
    # else:
    #     data = QtCore.QDateTime.fromString(arq_usu[5], "dd-MM-yyyy").date()
    # tela.msdata_cad.setDateTime(data)

    tela.mscod_op.setText(str(arq_usu[0]))
    tela.msnome.setText(str(arq_usu[1]).strip())
    # PROCURA A UF NO COMBOBOX
    for i in range(tela.comboBox_3.count()):
        item_text = tela.comboBox_3.itemText(i)
        if str(arq_usu[2]).strip() in item_text:
            tela.comboBox_3.setCurrentIndex(i)
            break

    for i in range(tela.comboBox_4.count()):
        item_text = tela.comboBox_4.itemText(i)
        if str(arq_usu[3]).strip() in item_text:
            tela.comboBox_4.setCurrentIndex(i)
            break

    for i in range(tela.comboBox_5.count()):
        item_text = tela.comboBox_5.itemText(i)
        if str(arq_usu[12][0]).strip() in item_text:
            tela.comboBox_5.setCurrentIndex(i)
            break

    for i in range(tela.comboBox_6.count()):
        item_text = tela.comboBox_6.itemText(i)
        if str(arq_usu[12][1]).strip() in item_text:
            tela.comboBox_6.setCurrentIndex(i)
            break

    tela.doubleSpinBox.setValue(float(arq_usu[6]))
    tela.doubleSpinBox_2.setValue(float(arq_usu[7]))
    tela.doubleSpinBox_3.setValue(float(arq_usu[8]))
    tela.doubleSpinBox_4.setValue(float(arq_usu[9]))
    tela.doubleSpinBox_5.setValue(float(arq_usu[17]))

    tela.memail.setText(str(arq_usu[33]).strip())
    tela.mendereco.setText(str(arq_usu[36]).strip())
    tela.mnumero.setText(str(arq_usu[37]).strip())
    tela.mcomplemento.setText(str(arq_usu[38]).strip())
    tela.mbairro.setText(str(arq_usu[39]).strip())
    for i in range(tela.comboBox.count()):
        item_text = tela.comboBox.itemText(i)
        if str(arq_usu[40]).strip() in item_text:
            tela.comboBox.setCurrentIndex(i)
            break
    for i in range(tela.comboBox_2.count()):
        item_text = tela.comboBox_2.itemText(i)
        if str(arq_usu[41]).strip() in item_text:
            tela.comboBox_2.setCurrentIndex(i)
            break
    tela.mfone.setText(str(arq_usu[42]).strip())
    tela.mcpf.setText(str(arq_usu[43]).strip())
    tela.mrg.setText(str(arq_usu[44]).strip())

    # RADIO BUTTON
    rb_alerta_doc_group = QButtonGroup()
    rb_alerta_doc_group.addButton(tela.rb_alerta_doc_sim, id=1)
    rb_alerta_doc_group.addButton(tela.rb_alerta_doc_nao, id=2)
    if arq_usu[27] == 'S':
        tela.rb_alerta_doc_sim.setChecked(True)
    else:
        tela.rb_alerta_doc_nao.setChecked(True)

    rb_alerta_estmin_group = QButtonGroup()
    rb_alerta_estmin_group.addButton(tela.rb_alerta_estmin_sim, id=1)
    rb_alerta_estmin_group.addButton(tela.rb_alerta_estmin_nao, id=2)
    if arq_usu[28] == 'S':
        tela.rb_alerta_estmin_sim.setChecked(True)
    else:
        tela.rb_alerta_estmin_nao.setChecked(True)

    rb_alerta_aniv_group = QButtonGroup()
    rb_alerta_aniv_group.addButton(tela.rb_alerta_aniv_sim, id=1)
    rb_alerta_aniv_group.addButton(tela.rb_alerta_aniv_nao, id=2)
    if arq_usu[34] == 'S':
        tela.rb_alerta_aniv_sim.setChecked(True)
    else:
        tela.rb_alerta_aniv_nao.setChecked(True)

    rb_pocket_group = QButtonGroup()
    rb_pocket_group.addButton(tela.rb_pocket_sim, id=1)
    rb_pocket_group.addButton(tela.rb_pocket_nao, id=2)
    if arq_usu[35] == 'S':
        tela.rb_pocket_sim.setChecked(True)
    else:
        tela.rb_pocket_nao.setChecked(True)
    tela.doubleSpinBox_6.setValue(float(arq_usu[48]))
    tela.doubleSpinBox_7.setValue(float(arq_usu[49]))

    tela.mscod_op.setDisabled(True)
    tela.msenha_atual.setDisabled(True)

    for widget in tela.findChildren((QLineEdit, QComboBox, QRadioButton)):
        widget.setEnabled(False)

    tab_widget.setTabOrder(tela.bt_sair, tela.bt_sair)
    tela.bt_sair.setFocus()

    tela.bt_sair.setFocus()
    tela.bt_salvar.setEnabled(False)
    # tela.bt_conta_apagar.clicked.connect()
    # tela.bt_movimento_produto.clicked.connect()
    tela.bt_sair.clicked.connect(fecha_tela)
    tela.bt_sair.setIcon(icon_sair)

    tela.show()


if __name__ == '__main__':
    from hti_funcoes import conexao_banco
    conexao_banco()
    consulta_usuario('002')
    app.exec()
    hg.conexao_bd.close()
