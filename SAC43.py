# CONSULTA FORNECEDOR

from PyQt6 import uic
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtGui import QIcon, QGuiApplication
from PyQt6.QtWidgets import QButtonGroup, QMessageBox, QLineEdit, QComboBox, QRadioButton
from datetime import date
import os
import hti_global as hg

titulo = "CONSULTA DE FORNECEDOR"
app = QtWidgets.QApplication([])
app.setStyleSheet(hg.style_sheet)
tela = uic.loadUi(f"{hg.c_ui}\\htifornecedor.ui")
tela.setWindowTitle(titulo)
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

tela.statusBar = QtWidgets.QStatusBar()
tela.setStatusBar(tela.statusBar)

lbl_titulo_fornecedor = tela.findChild(QtWidgets.QLabel, "tit_fornecedor")
lbl_titulo_fornecedor.setText(titulo)

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

hg.conexao_cursor.execute("SELECT codigo, desc1 FROM sacdesp ORDER BY codigo")
# Recupere o resultado
arq_desp = hg.conexao_cursor.fetchall()
hg.conexao_bd.commit()

# COMBOX
tela.comboBox_3.addItems(hg.estados)
tela.comboBox_3.setCurrentIndex(16)  # coloca o focus no index

for ret_desp in arq_desp:
    item = f'{ret_desp[0]} - {ret_desp[1]}'.strip('(),')
    tela.comboBox.addItem(item)
tela.comboBox.setCurrentIndex(0)

for ret_cidade in arq_cidade:
    item = f'{ret_cidade[0]} - {ret_cidade[1]}'.strip('(),')
    tela.comboBox_2.addItem(item)




def on_close_event(event):
    tela.close()
    event.accept()
    # hg.conexao_cursor.close()
    tela.closeEvent = on_close_event


def consulta_fornecedor(codigo_fornecedor):
    hg.conexao_cursor.execute(f"SELECT * FROM sacforn WHERE cod_forn = {codigo_fornecedor}")
    arq_forn = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()
    tab_widget = tela.findChild(QtWidgets.QTabWidget, "tabWidget")
    tab_widget.setCurrentIndex(0)
    if arq_forn is None:
        QMessageBox.information(tela, "alteracao de fornecedor", "Fornecedor nao CADASTRADO !")
        return

    if arq_forn[3] is None:
        data = QtCore.QDate(1900, 1, 1)
    else:
        data_str = arq_forn[3].strftime("%Y-%m-%d")
        data = QtCore.QDate.fromString(data_str, "yyyy-MM-dd")
        data = QtCore.QDateTime(data, QtCore.QTime(0, 0, 0))
    tela.mdata_cad.setDateTime(data)

    tela.mcod_forn.setText(str(arq_forn[0]))
    tela.mrazao.setText(str(arq_forn[1]).strip())
    tela.mcgc.setText(str(arq_forn[15]))
    tela.mfantasia.setText(str(arq_forn[34]).strip())

    # ENVIA PARA POCKET
    rb_app_group = QButtonGroup()
    rb_app_group.addButton(tela.rb_pocket_sim, id=1)
    rb_app_group.addButton(tela.rb_pocket_nao, id=2)
    if arq_forn[33] == 'S':
        tela.rb_pocket_sim.setChecked(True)
    else:
        tela.rb_pocket_nao.setChecked(True)

    for i in range(tela.comboBox.count()):
        item_text = tela.comboBox.itemText(i)
        if str(arq_forn[2]).strip() in item_text:
            tela.comboBox.setCurrentIndex(i)
            break

    tela.minsc.setText(str(arq_forn[16]).strip())
    tela.mcpf.setText(str(arq_forn[17]).strip())

    tela.mendereco.setText(str(arq_forn[5]).strip())
    tela.mbairro.setText(str(arq_forn[6]).strip())
    # PROCURA A CIDADE NO COMBOBOX
    for i in range(tela.comboBox_2.count()):
        item_text = tela.comboBox_2.itemText(i)
        if str(arq_forn[7]).strip() in item_text:
            tela.comboBox_2.setCurrentIndex(i)
            break

    # PROCURA A UF NO COMBOBOX
    for i in range(tela.comboBox_3.count()):
        item_text = tela.comboBox_3.itemText(i)
        # print(str(arq_forn[24]).strip())
        if str(arq_forn[8]).strip() in item_text:
            tela.comboBox_3.setCurrentIndex(i)
            break

    tela.mcep.setText(str(arq_forn[9]).strip())
    tela.mlocal.setText(str(arq_forn[32]).strip())
    tela.memail.setText(str(arq_forn[11]).strip())
    tela.mtel1.setText(str(arq_forn[12]).strip())
    tela.mtel2.setText(str(arq_forn[13]).strip())
    tela.mfax.setText(str(arq_forn[14]).strip())

    tela.mprazo_pag.setText(str(arq_forn[20]).strip())

    tela.doubleSpinBox.setValue(float(arq_forn[25]))

    tela.mct_cobran.setText(str(arq_forn[24]).strip())
    tela.mct_gerente.setText(str(arq_forn[21]).strip())
    tela.mct_fatura.setText(str(arq_forn[23]).strip())
    tela.mct_vendedor.setText(str(arq_forn[22]).strip())
    tela.mobs.setText(str(arq_forn[26]).strip())
    tela.mobs1.setText(str(arq_forn[27]).strip())
    tela.mobs2.setText(str(arq_forn[28]).strip())
    tela.mobs3.setText(str(arq_forn[29]).strip())
    tela.mobs4.setText(str(arq_forn[30]).strip())
    tela.mobs5.setText(str(arq_forn[31]).strip())
    for widget in tela.findChildren((QLineEdit, QComboBox, QRadioButton)):
        widget.setEnabled(False)

    tab_widget.setTabOrder(tela.bt_conta_apagar, tela.bt_movimento_produto)
    tab_widget.setTabOrder(tela.bt_movimento_produto, tela.bt_sair)

    tela.bt_conta_apagar.setFocus()

    tela.bt_salvar.setEnabled(False)
    # tela.bt_salvar.clicked.connect(salvar_fornecedor)
    tela.bt_sair.clicked.connect(fecha_tela)
    tela.bt_sair.setIcon(icon_sair)
    tela.bt_salvar.setIcon(icon_salvar)

    tela.show()


def fecha_tela():
    tela.close()
    tela.closeEvent = on_close_event
    return


if __name__ == '__main__':
    consulta_fornecedor('0001')
    app.exec()
    hg.conexao_bd.close()
