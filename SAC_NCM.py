# LISTA DE NCM

from PyQt6 import uic, QtWidgets
from PyQt6.QtGui import QIcon, QGuiApplication
from PyQt6.QtWidgets import QButtonGroup, QMessageBox, QTableWidgetItem, QAbstractItemView
import os
import hti_global as hg

titulo = 'NCM CADASTRADO'
app = QtWidgets.QApplication([])
app.setStyleSheet(hg.style_sheet)
tela = uic.loadUi(f"{hg.c_ui}\\lista_ncm.ui")
tela.setWindowTitle(titulo)
icon = QIcon(f"{hg.c_imagem}\\htiico.ico")
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


def on_close_event(event):
    # Esta função será chamada quando o usuário clicar no botão de fechar a janela
    # print("Fechando a janela...")
    tela.close()
    event.accept()
    tela.closeEvent = on_close_event


def fecha_tela():
    tela.close()


# Define a função para ajustar as colunas da tabela
def ajustar_colunas_tabela(tabela1):
    header = tabela1.horizontalHeader()
    header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
    header.setStretchLastSection(False)


def f_incl_ncm():
    tela.bt_salvar.clicked.disconnect()
    m_codigo = tela.mcodigo.text().upper()
    hg.conexao_cursor.execute(f"SELECT codigo FROM sacncm WHERE codigo = '{m_codigo}'")
    arq_profi = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()
    if arq_profi is not None:
        QMessageBox.information(tela, "Inclusao de NCM", "NCM ja CADASTRADO!")
        return

    m_cest = tela.mcest.text().upper()
    m_descri = tela.mdescri.text().upper()
    m_aliqnac = tela.doubleSpinBox.value()
    m_aliqimp = tela.doubleSpinBox_2.value()

    sql = "INSERT INTO sacncm (codigo, cest, descri, aliqnac, aliqimp) VALUES (?, ?, ?, ?, ?) "
    print(sql, (m_codigo, m_cest, m_descri, m_aliqnac, m_aliqimp))
    hg.conexao_cursor.execute(sql, (m_codigo, m_cest, m_descri, m_aliqnac, m_aliqimp))
    hg.conexao_bd.commit()
    QMessageBox.information(tela, "Inclusao de NCM", "Cadastro feito com SUCESSO!")

    # tela.mcodigo.setText('')
    # tela.mcest.setText('')
    # tela.mdescri.setText('')
    listar_ncm()


def chama_alteracao():
    tela.bt_salvar.clicked.disconnect()
    m_codigo = tela.mcodigo.text().upper()
    hg.conexao_cursor.execute(f"SELECT codigo FROM sacncm WHERE codigo = '{m_codigo}'")
    arq_profi = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()
    if arq_profi is None:
        QMessageBox.information(tela, "Alteracao de NCM", "NCM nao CADASTRADO!")
        return

    m_cest = tela.mcest.text().upper()
    m_descri = tela.mdescri.text().upper()
    m_aliqnac = tela.doubleSpinBox.value()
    m_aliqimp = tela.doubleSpinBox_2.value()

    sql = "UPDATE sacncm SET cest = ?, descri = ?, aliqnac = ?, aliqimp = ? WHERE codigo = ?"
    print(sql, (m_cest, m_descri, m_aliqnac, m_aliqimp, m_codigo))
    hg.conexao_cursor.execute(sql, (m_cest, m_descri, m_aliqnac, m_aliqimp, m_codigo))
    hg.conexao_bd.commit()
    QMessageBox.information(tela, "ALTERACAO DE NCM", "Alteracao feita com SUCESSO!")
    listar_ncm()


def editar_item(row):
    tela.groupBox.setTitle("ALTERACAO")
    vcodigo = str(tabela.item(row, 0).text())
    vcest = tabela.item(row, 1).text().strip()
    vdescri = tabela.item(row, 2).text().strip()
    valiqnac = tabela.item(row, 3).text().strip()
    valiqimp = tabela.item(row, 4).text().strip()
    tabela.itemDoubleClicked.disconnect()
    if tela.rb_alteracao.isChecked():
        tela.mcodigo.setEnabled(False)
        tela.mcest.setEnabled(True)
        tela.mdescri.setEnabled(True)
        tela.doubleSpinBox.setEnabled(True)
        tela.doubleSpinBox_2.setEnabled(True)
        tela.bt_salvar.setEnabled(True)
        tela.bt_cancelar.setEnabled(True)
        tela.mcodigo.setText(vcodigo)
        tela.mcest.setText(vcest)
        tela.mdescri.setText(vdescri)
        tela.doubleSpinBox.setValue(float(valiqnac))
        tela.doubleSpinBox_2.setValue(float(valiqimp))
        tela.bt_salvar.clicked.connect(chama_alteracao)
        tela.bt_cancelar.clicked.connect(listar_ncm)
        tela.mcest.setFocus()

    else:
        # chama_consulta(item.text())
        pass

    tabela.itemDoubleClicked.connect(lambda items: editar_item(items.row()))
    return


def habilitar_objeto():
    tela.groupBox.setTitle("INCLUSAO")
    tela.mcodigo.clear()
    tela.mcest.clear()
    tela.mdescri.clear()
    tela.bt_salvar.clicked.connect(f_incl_ncm)
    tela.bt_cancelar.clicked.connect(listar_ncm)
    tela.mcodigo.setEnabled(True)
    tela.mcest.setEnabled(True)
    tela.mdescri.setEnabled(True)
    tela.doubleSpinBox.setEnabled(True)
    tela.doubleSpinBox_2.setEnabled(True)
    tela.bt_salvar.setEnabled(True)
    tela.bt_cancelar.setEnabled(True)
    tela.mcodigo.setFocus()


def listar_ncm():
    hg.conexao_cursor.execute("SELECT codigo, cest, descri, REPLACE(CAST(aliqnac AS DECIMAL(12, 2)), '.', ',')"
                                      ", REPLACE(CAST(aliqimp AS DECIMAL(12, 2)), '.', ',') FROM sacncm")
    dados_lidos = hg.conexao_cursor.fetchall()
    hg.conexao_bd.commit()
    tabela.setRowCount(len(dados_lidos))
    tabela.setColumnCount(5)
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

    tela.mcodigo.setEnabled(False)
    tela.mcest.setEnabled(False)
    tela.mdescri.setEnabled(False)
    tela.doubleSpinBox.setEnabled(False)
    tela.doubleSpinBox_2.setEnabled(False)
    tela.mcodigo.setText('')
    tela.mcest.setText('')
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


if __name__ == '__main__':
    from hti_funcoes import conexao_banco
    conexao_banco()
    listar_ncm()
    app.exec()
    hg.conexao_bd.close()
