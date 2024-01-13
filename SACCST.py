# CST

from PyQt6 import uic, QtWidgets
from PyQt6.QtGui import QIcon, QGuiApplication
from PyQt6.QtWidgets import QButtonGroup, QMessageBox, QTableWidgetItem, QTableWidget, QStatusBar, QAbstractItemView
# from PyQt6.QtWidgets import QGroupBox
import os
import hti_global as hg

titulo = 'CST/CSOSN CADASTRADO'
app = QtWidgets.QApplication([])
app.setStyleSheet(hg.style_sheet)
tela = uic.loadUi(f"{hg.c_ui}\\lista_cst.ui")
tela.setWindowTitle(titulo)
icon = QIcon(f"{hg.c_imagem}\\htiico.jpg")
icon_cancelar = QIcon(f"{hg.c_imagem}\\cancelar.png")
icon_sair = QIcon(f"{hg.c_imagem}\\sair.png")
icon_salvar = QIcon(f"{hg.c_imagem}\\salvar.png")
icon_incluir = QIcon(f"{hg.c_imagem}\\incluir.png")
tela.setWindowIcon(icon)
tabela = tela.tableWidget
# Centraliza a janela na tela
qt_rectangle = tela.frameGeometry()
center_point = app.primaryScreen().availableGeometry().center()
qt_rectangle.moveCenter(center_point)
tela.move(qt_rectangle.topLeft())
# tela.setGeometry(0, 0, 400, 200)  # Defina um tamanho inicial para a janela
if hg.mtp_tela == 'G':
    primary_screen = QGuiApplication.primaryScreen()
    if primary_screen is not None:
        screen_geometry = primary_screen.geometry()
        tela.setGeometry(screen_geometry)

# PEGA O NOME DO ARQUIVO EM EXECUCAO
nome_file_com = os.path.basename(__file__)
nome_file, ext = os.path.splitext(nome_file_com)

tela.statusBar.showMessage(f"<< {nome_file} >>")

deb_cred = ['Isento', 'Tributado', 'Nao tributado', 'F->Substituicao', "Servico"]
tela.comboBox.addItems(deb_cred)
tela.comboBox.setCurrentIndex(0)  # coloca o focus no index
ent_sai = ['Sim', 'Nao']
tela.comboBox_2.addItems(ent_sai)
tela.comboBox_2.setCurrentIndex(0)  # coloca o focus no index


# Define a função para ajustar as colunas da tabela
def ajustar_colunas_tabela(tabela1):
    header = tabela1.horizontalHeader()
    header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
    header.setStretchLastSection(False)


def on_close_event(event):
    # Esta função será chamada quando o usuário clicar no botão de fechar a janela
    # print("Fechando a janela...")
    tela.close()
    event.accept()
    tela.closeEvent = on_close_event


def fecha_tela():
    tela.close()


def f_incl_cst():
    tela.bt_salvar.clicked.disconnect()
    m_cst = tela.mcst.text().upper()
    hg.conexao_cursor.execute(f"SELECT cst FROM saccst WHERE cst = {m_cst}")
    arq_profi = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()
    if arq_profi is not None:
        QMessageBox.information(tela, "Inclusao de CST", "CST ja CADASTRADO!")
        return

    m_descri = tela.mdescri.text().upper()

    index = tela.comboBox.currentIndex()
    mop = tela.comboBox.itemText(index)
    m_sittrib = mop[0:1]

    index = tela.comboBox_2.currentIndex()
    mop = tela.comboBox_2.itemText(index)
    m_simples = mop[0:1]

    sql = "INSERT INTO saccst (cst, descri, sittrib, simples, sr_deleted) VALUES (?, ?, ?, ?, ?) "
    hg.conexao_cursor.execute(sql, (m_cst, m_descri, m_sittrib, m_simples, ' '))
    hg.conexao_bd.commit()
    QMessageBox.information(tela, "Inclusao de CST", "Cadastro feito com SUCESSO!")

    listar_cst()


def chama_alteracao(mcod_cli):
    tela.bt_salvar.clicked.disconnect()
    m_cst = tela.mcst.text().upper()
    hg.conexao_cursor.execute(f"SELECT cst FROM saccst WHERE cst = {m_cst}")
    arq_profi = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()
    if arq_profi is None:
        QMessageBox.information(tela, "Inclusao de CST", "CST nao CADASTRADO!")
        return

    m_descri = tela.mdescri.text().upper()

    index = tela.comboBox.currentIndex()
    mop = tela.comboBox.itemText(index)
    m_sittrib = mop[0:1]

    index = tela.comboBox_2.currentIndex()
    mop = tela.comboBox_2.itemText(index)
    m_simples = mop[0:1]

    sql = "UPDATE saccst SET descri = ?, sittrib = ?, simples = ? WHERE cst = ?"
    hg.conexao_cursor.execute(sql, (m_descri, m_sittrib, m_simples, m_cst))
    hg.conexao_bd.commit()
    QMessageBox.information(tela, "ALTERACAO de CST", "Alteracao feita com SUCESSO!")

    listar_cst()


def editar_item(row):
    tela.groupBox.setTitle("ALTERACAO")
    vcst = str(tabela.item(row, 0).text())
    vdescri = tabela.item(row, 1).text().strip()
    vsittrib = tabela.item(row, 2).text().strip()
    vsittrib = vsittrib[0]
    vsimples = tabela.item(row, 3).text().strip()
    vsimples = vsimples[0]
    tabela.itemDoubleClicked.disconnect()
    if tela.rb_alteracao.isChecked():
        tela.mcst.setEnabled(False)
        tela.mdescri.setEnabled(True)
        tela.comboBox.setEnabled(True)
        tela.comboBox_2.setEnabled(True)
        tela.bt_salvar.clicked.connect(chama_alteracao)
        tela.bt_cancelar.clicked.connect(listar_cst)
        tela.bt_salvar.setEnabled(True)
        tela.bt_cancelar.setEnabled(True)
        tela.mcst.setText(vcst)
        tela.mdescri.setText(vdescri)

        for i in range(tela.comboBox.count()):
            item_text = tela.comboBox.itemText(i)
            if str(vsittrib).strip() in item_text:
                tela.comboBox.setCurrentIndex(i)
                break

        for i in range(tela.comboBox_2.count()):
            item_text = tela.comboBox_2.itemText(i)
            if str(vsimples).strip() in item_text:
                tela.comboBox_2.setCurrentIndex(i)
                break

        tela.mdescri.setFocus()
    else:
        # chama_consulta(item.text())
        pass

    tabela.itemDoubleClicked.connect(lambda items: editar_item(items.row()))
    return


def habilitar_objeto():
    tela.groupBox.setTitle("INCLUSAO")
    tela.mcst.clear()
    tela.mdescri.clear()
    tela.bt_salvar.clicked.connect(f_incl_cst)
    tela.bt_cancelar.clicked.connect(listar_cst)
    tela.mcst.setEnabled(True)
    tela.mdescri.setEnabled(True)
    tela.comboBox.setEnabled(True)
    tela.comboBox_2.setEnabled(True)
    tela.bt_salvar.setEnabled(True)
    tela.bt_cancelar.setEnabled(True)
    tela.mcst.setFocus()


def listar_cst():
    hg.conexao_cursor.execute(f"SELECT CAST(cst as char(4)), descri, "
                                      f"iif(sittrib = 'I','Isento',iif(sittrib = 'T','Tributado', "
                                      f"iif(sittrib = 'N','Nao Tributado', "
                                      f"iif(sittrib = 'F','Substituicao','Servico')))), "
                                      f"iif(simples = 'S','Sim','Nao') FROM saccst ORDER BY cst")

    dados_lidos = hg.conexao_cursor.fetchall()
    hg.conexao_bd.commit()
    tabela.setRowCount(len(dados_lidos))
    tabela.setColumnCount(4)
    tabela.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
    for i, linha in enumerate(dados_lidos):
        for j, valor in enumerate(linha):
            valor = str(valor) if valor is not None else ""
            item = QTableWidgetItem(valor)
            tabela.setItem(i, j, item)
    ajustar_colunas_tabela(tabela)

    rb_tipo_group = QButtonGroup()
    rb_tipo_group.addButton(tela.rb_alteracao, id=1)
    rb_tipo_group.addButton(tela.rb_exclusao, id=2)
    tela.rb_alteracao.setChecked(True)

    tela.mcst.setEnabled(False)
    tela.mdescri.setEnabled(False)
    tela.comboBox.setEnabled(False)
    tela.comboBox_2.setEnabled(False)
    tela.mcst.setText('')
    tela.mdescri.setText('')

    tabela.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
    tabela.itemDoubleClicked.connect(lambda item1: editar_item(item1.row()))
    tela.bt_salvar.setEnabled(False)
    tela.bt_cancelar.setEnabled(False)
    tela.bt_inclusao.clicked.connect(habilitar_objeto)
    tela.bt_sair.clicked.connect(fecha_tela)
    tela.bt_sair.setIcon(icon_sair)
    tela.bt_salvar.setIcon(icon_salvar)
    tela.bt_inclusao.setIcon(icon_incluir)
    tela.bt_cancelar.setIcon(icon_cancelar)

    tela.show()
    app.exec()


if __name__ == '__main__':
    from hti_funcoes import conexao_banco
    conexao_banco()
    listar_cst()
    hg.conexao_bd.close()
