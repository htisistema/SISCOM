# TIPO DE DOCUMENTOS

from PyQt6 import uic, QtWidgets
from PyQt6.QtGui import QIcon, QGuiApplication
from PyQt6.QtWidgets import QButtonGroup, QMessageBox, QTableWidgetItem, QTableWidget, QStatusBar, QAbstractItemView
import os
import hti_global

app = QtWidgets.QApplication([])
app.setStyleSheet(hti_global.style_sheet)
tela = uic.loadUi(f"{hti_global.c_ui}\\lista_documento.ui")
icon = QIcon(f"{hti_global.c_imagem}\\htiico.jpg")
icon_cancelar = QIcon(f"{hti_global.c_imagem}\\cancelar.png")
icon_sair = QIcon(f"{hti_global.c_imagem}\\sair.png")
icon_salvar = QIcon(f"{hti_global.c_imagem}\\salvar.png")
icon_incluir = QIcon(f"{hti_global.c_imagem}\\incluir.png")
tela.setWindowIcon(icon)
# Centraliza a janela na tela
qt_rectangle = tela.frameGeometry()
center_point = app.primaryScreen().availableGeometry().center()
qt_rectangle.moveCenter(center_point)
tela.move(qt_rectangle.topLeft())

if hti_global.mtp_tela == 'G':
    primary_screen = QGuiApplication.primaryScreen()
    if primary_screen is not None:
        screen_geometry = primary_screen.geometry()
        tela.setGeometry(screen_geometry)

tela.setWindowTitle('TIPO DE DOCUMENTO CADASTRADO')
# PEGA O NOME DO ARQUIVO EM EXECUCAO
nome_file_com = os.path.basename(__file__)
nome_file, ext = os.path.splitext(nome_file_com)

status_bar = QStatusBar()
tela.setStatusBar(status_bar)
tela.statusBar.showMessage(f"<< {nome_file} >>")
tabela = tela.tableWidget


def on_close_event(event):
    # Esta função será chamada quando o usuário clicar no botão de fechar a janela
    # print("Fechando a janela...")
    tela.close()
    event.accept()


tela.closeEvent = on_close_event


def fecha_tela():
    tela.close()


# Define a função para ajustar as colunas da tabela
def ajustar_colunas_tabela(tabela):
    header = tabela.horizontalHeader()
    header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
    header.setStretchLastSection(False)


def f_incl_documento():
    tela.bt_salvar.clicked.disconnect()
    m_sigla = tela.msigla.text().upper()
    m_descricao = tela.mdescricao.text().upper()

    sql = "INSERT INTO sactipdc (tipo_doc, descri, sr_deleted) VALUES (?, ?, ?) "
    hti_global.conexao_cursor.execute(sql, (m_sigla, m_descricao, ' '))

    hti_global.conexao_bd.commit()
    QMessageBox.information(tela, "Inclusao de TIPO DE DOCUMENTO", "Cadastro feito com SUCESSO!")

    tela.msigla.setEnabled(False)
    tela.mdescricao.setEnabled(False)
    tela.bt_salvar.setEnabled(False)
    tela.msigla.setText('')
    tela.mdescricao.setText('')
    return


def chama_alteracao():
    tela.bt_salvar.clicked.disconnect()
    m_sigla = tela.msigla.text().upper()
    m_descricao = tela.mdescricao.text().upper()

    sql = "UPDATE sactipdc SET descri = ? WHERE tipo_doc = ?"
    # print(sql, (m_descricao, m_sigla))

    hti_global.conexao_cursor.execute(sql, (m_descricao, m_sigla))
    hti_global.conexao_bd.commit()
    QMessageBox.information(tela, "ALTERACAO DE TIPO DE DOCUMENTO", "Alteraco feita com SUCESSO!")

    tela.msigla.setEnabled(False)
    tela.mdescricao.setEnabled(False)
    tela.msigla.setText('')
    tela.mdescricao.setText('')
    tela.bt_salvar.setEnabled(False)
    listar_documento()


def editar_item(row):
    item = tabela.item(row, 0)
    descricao = tabela.item(row, 1)
    tabela.itemDoubleClicked.disconnect()
    if tela.rb_alteracao.isChecked():
        tela.bt_salvar.clicked.connect(chama_alteracao)
        tela.bt_cancelar.clicked.connect(listar_documento)
        tela.bt_salvar.setEnabled(True)
        tela.bt_cancelar.setEnabled(True)
        tela.mdescricao.setEnabled(True)
        print('ok')
        tela.msigla.setText(str(item.text()))
        tela.mdescricao.setText(str(descricao.text().strip()))
        tela.mdescricao.setFocus()
    else:
        # chama_consulta(item.text())
        pass

    tabela.itemDoubleClicked.connect(lambda item: editar_item(item.row()))
    return


def habilitar_objeto():
    tela.bt_salvar.clicked.connect(f_incl_documento)
    tela.bt_cancelar.clicked.connect(listar_documento)
    tela.bt_salvar.setEnabled(True)
    tela.bt_cancelar.setEnabled(True)
    tela.msigla.setEnabled(True)
    tela.mdescricao.setEnabled(True)
    tela.msigla.setFocus()


def listar_documento():
    # tabela = tela.tableWidget
    hti_global.conexao_cursor.execute(f"SELECT tipo_doc, descri FROM sactipdc order BY tipo_doc")
    dados_lidos = hti_global.conexao_cursor.fetchall()
    hti_global.conexao_bd.commit()

    tabela.setRowCount(len(dados_lidos))
    tabela.setColumnCount(2)
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

    tela.msigla.setEnabled(False)
    tela.mdescricao.setEnabled(False)

    tabela.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
    tabela.itemDoubleClicked.connect(lambda item: editar_item(item.row()))
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
    listar_documento()
    hti_global.conexao_bd.close()
