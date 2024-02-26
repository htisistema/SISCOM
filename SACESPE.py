# ESPECIE

from PyQt6 import uic, QtWidgets
from PyQt6.QtGui import QIcon, QGuiApplication
from PyQt6.QtWidgets import QButtonGroup, QMessageBox, QAbstractItemView, QTableWidgetItem
import os
import hti_global as hg

titulo = 'ESPECIE DO PRODUTO'
app = QtWidgets.QApplication([])
app.setStyleSheet(hg.style_sheet)
tela = uic.loadUi(f"{hg.c_ui}\\lista_especie.ui")
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
# PEGA O NOME DO ARQUIVO EM EXECUCAO
nome_file_com = os.path.basename(__file__)
nome_file, ext = os.path.splitext(nome_file_com)

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
def ajustar_colunas_tabela(tabela1):
    header = tabela1.horizontalHeader()
    header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
    header.setStretchLastSection(False)


def chama_alteracao():
    m_cod_espe = tela.mcod_espe.text().upper()
    m_descri = tela.mdescri.text().upper()

    sql = "UPDATE sacespe SET descri = ? WHERE cod_espe = ?"
    hg.conexao_cursor.execute(sql, (m_descri, m_cod_espe))

    hg.conexao_bd.commit()
    QMessageBox.information(tela, "ALTERACAO DA ESPECIE DE PRODUTO ", "Alteracao feita com SUCESSO!")
    listar_especie()


def editar_item(row):
    vcodigo = str(tabela.item(row, 0).text())
    vdescri = tabela.item(row, 1).text()
    tabela.itemDoubleClicked.disconnect()
    if tela.rb_alteracao.isChecked():
        tela.mdescri.setEnabled(True)
        tela.bt_salvar.clicked.connect(chama_alteracao)
        tela.bt_cancelar.clicked.connect(listar_especie)
        tela.bt_salvar.setEnabled(True)
        tela.bt_cancelar.setEnabled(True)
        tela.mcod_espe.setText(vcodigo)
        tela.mdescri.setText(str(vdescri))
        tela.mdescri.setFocus()
    else:
        # chama_consulta(item.text())
        pass

    tabela.itemDoubleClicked.connect(lambda items: editar_item(items.row()))
    return


def f_incl_especie():
    tela.bt_salvar.clicked.disconnect()
    m_cod_espe = tela.mcod_espe.text().upper()
    m_descri = tela.mdescri.text().upper()
    sql = "INSERT INTO sacespe (cod_espe, descri, sr_deleted) VALUES (?, ?, ?)"
    hg.conexao_cursor.execute(sql, (m_cod_espe, m_descri, ' '))
    hg.conexao_bd.commit()
    QMessageBox.information(tela, "Inclusao de ESPECIE DE PRODUTO", "Cadastro feito com SUCESSO!")
    listar_especie()


def habilitar_objeto():
    tela.mcod_espe.clear()
    tela.mdescri.clear()
    hg.conexao_cursor.execute(f"SELECT max(cod_espe) FROM sacespe")
    arq_especie = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()
    if arq_especie is None:
        codigo = 1
        tela.mcod_espe.setText(str(codigo).zfill(4))
    else:
        codigo = int(arq_especie[0]) + 1
        tela.mcod_espe.setText(str(codigo).zfill(4))

    tela.bt_salvar.clicked.connect(f_incl_especie)
    tela.bt_cancelar.clicked.connect(listar_especie)
    tela.mdescri.setEnabled(True)
    tela.bt_salvar.setEnabled(True)
    tela.bt_cancelar.setEnabled(True)
    tela.mdescri.setFocus()


def listar_especie():
    hg.conexao_cursor.execute(f"SELECT CAST(cod_espe as char(4)), descri FROM sacespe order BY cod_espe")
    dados_lidos = hg.conexao_cursor.fetchall()
    hg.conexao_bd.commit()
    tabela.setRowCount(len(dados_lidos))
    tabela.setColumnCount(2)
    tabela.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
    for i, linha in enumerate(dados_lidos):
        for j, valor in enumerate(linha):
            valor = str(valor) if valor is not None else ""
            cart = QTableWidgetItem(valor)
            tabela.setItem(i, j, cart)
    ajustar_colunas_tabela(tabela)

    rb_tipo_group = QButtonGroup()
    rb_tipo_group.addButton(tela.rb_alteracao, id=1)
    rb_tipo_group.addButton(tela.rb_exclusao, id=2)
    tela.rb_alteracao.setChecked(True)
    tela.mcod_espe.setText('')
    tela.mdescri.setText('')
    tela.mcod_espe.setEnabled(False)
    tela.mdescri.setEnabled(False)
    tela.bt_salvar.setEnabled(False)
    tela.bt_cancelar.setEnabled(False)

    tela.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
    tela.tableWidget.itemDoubleClicked.connect(lambda item: editar_item(item.row()))
    tela.bt_sair.clicked.connect(fecha_tela)
    tela.bt_inclusao.clicked.connect(habilitar_objeto)

    tela.bt_sair.setIcon(icon_sair)
    tela.bt_salvar.setIcon(icon_salvar)
    tela.bt_inclusao.setIcon(icon_incluir)
    tela.bt_cancelar.setIcon(icon_cancelar)

    tela.show()


tela.tableWidget.itemDoubleClicked.connect(lambda item: editar_item(item.row()))

if __name__ == '__main__':
    from hti_funcoes import conexao_banco
    conexao_banco()
    listar_especie()
    app.exec()
    hg.conexao_bd.close()
