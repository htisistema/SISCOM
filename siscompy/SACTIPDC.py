# OBSERVACOES

from PyQt6 import uic, QtWidgets
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QButtonGroup, QMessageBox
import os
import hti_global as hg

app = QtWidgets.QApplication([])
tela = uic.loadUi("C:\BACKUP_HTI\TELASREMOTA(PYTHON)\lista_documento.ui")
tela.setWindowTitle('TIPOS DE DOCUMENTOS CADASTRADAS')
icon = QIcon('C:\HTI\PYTHON\SISCOM\imagem\htiico.jpg')
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
def ajustar_colunas_tabela(tabela):
    header = tabela.horizontalHeader()
    header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
    header.setStretchLastSection(False)


def f_incl_documento():
    # from incl_grupo import inclusao_grupo
    # inclusao_grupo()
    m_sigla = tela.msigla.text().upper()
    m_descricao = tela.mdescricao.text().upper()

    sql = "INSERT INTO sactipdc (tipo_doc, descri, sr_deleted) VALUES (?, ?, ?) "
    hg.conexao_cursor.execute(sql, (m_sigla, m_descricao, ' '))

    hg.conexao_bd.commit()
    QMessageBox.information(tela, "Inclusao de TIPO DE DOCUMENTO", "Cadastro feito com SUCESSO!")

    tela.msigla.setEnabled(False)
    tela.mdescricao.setEnabled(False)
    tela.msigla.setText('')
    tela.mdescricao.setText('')

    return


def chama_alteracao(mcod_cli):
    # from alt_grupo import alteracao_grupo
    # alteracao_grupo(mcod_cli[0:5])
    pass
    return


def chama_consulta(mcod_cli):
    # from cons_grupo import consulta_grupo
    # consulta_grupo(mcod_cli[0:5])
    # print(mcod_cli)
    pass
    return


def botao_item():
    selected_item = tela.tableWidget.currentItem()
    if selected_item is not None:
        codigo_grupo = selected_item.text()
        chama_alteracao(codigo_grupo)
        return
    else:
        return


def editar_item(row):
    rb_tipo_consulta = None
    item = tela.tableWidget.item(row, 0)
    if item.isSelected():
        tela.tableWidget.itemDoubleClicked.disconnect()
        # print("Duplo clique!")
    else:
        tela.tableWidget.itemDoubleClicked.disconnect()
        # print("Clique simples.")

    # print(item.text())
    if tela.rb_alteracao.isChecked():
        rb_tipo_consulta = 'A'
    elif tela.rb_consulta.isChecked():
        rb_tipo_consulta = 'C'

    if rb_tipo_consulta == 'A':
        # chama_alteracao(item.text())
        pass
    else:
        # chama_consulta(item.text())
        pass

    tela.tableWidget.itemDoubleClicked.connect(lambda item: editar_item(item.row()))
    return


def habilitar_objeto():
    tela.msigla.setEnabled(True)
    tela.mdescricao.setEnabled(True)
    tela.msigla.setFocus()


def desabilitar_objeto():
    tela.doubleSpinBox_18.setEnabled(False)


def listar_documento():
    hg.conexao_cursor.execute(f"SELECT tipo_doc, descri FROM sactipdc order BY tipo_doc")

    dados_lidos = hg.conexao_cursor.fetchall()
    hg.conexao_bd.commit()
    tela.tableWidget.setRowCount(len(dados_lidos))
    tela.tableWidget.setColumnCount(2)
    for i, linha in enumerate(dados_lidos):
        for j, valor in enumerate(linha):
            valor = str(valor) if valor is not None else ""
            item = QtWidgets.QTableWidgetItem(valor)
            tela.tableWidget.setItem(i, j, item)
            # print(item.text())
    ajustar_colunas_tabela(tela.tableWidget)

    rb_tipo_group = QButtonGroup()
    rb_tipo_group.addButton(tela.rb_alteracao, id=1)
    rb_tipo_group.addButton(tela.rb_exclusao, id=2)
    tela.rb_alteracao.setChecked(True)

    tela.msigla.setEnabled(False)
    tela.mdescricao.setEnabled(False)

    tela.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
    tela.tableWidget.itemDoubleClicked.connect(lambda item: editar_item(item.row()))
    tela.bt_salvar.clicked.connect(f_incl_documento)
    tela.incl_fornecedor.clicked.connect(habilitar_objeto)
    tela.bt_sair.clicked.connect(fecha_tela)

    tela.show()
    app.exec()


# tela.incl_grupo.clicked.connect(f_incl_grupo)
# tela.consulta_grupo.clicked.connect(botao_item)
# tela.pesquisa.textChanged.connect(listar_grupo)
tela.tableWidget.itemDoubleClicked.connect(lambda item: editar_item(item.row()))

# tela.pesquisa.returnPressed.connect(listar_grupo)


if __name__ == '__main__':
    listar_documento()
    hg.conexao_bd.close()
