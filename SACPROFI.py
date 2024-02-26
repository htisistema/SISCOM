# PROFISSAO

from PyQt6 import uic, QtWidgets
from PyQt6.QtGui import QIcon, QGuiApplication
from PyQt6.QtWidgets import QButtonGroup, QMessageBox, QTableWidgetItem, QTableWidget, QStatusBar, QAbstractItemView
import os
import hti_global as hg

titulo = 'PROFISSAO'
app = QtWidgets.QApplication([])
app.setStyleSheet(hg.style_sheet)
tela = uic.loadUi(f"{hg.c_ui}\\lista_profissao.ui")
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


def f_incl_profissao():
    tela.bt_salvar.clicked.disconnect()
    m_cod_profi = tela.mcod_profi.text().upper()
    m_profi = tela.mprofi.text().upper()
    sql = "INSERT INTO sacprofi (cod_profi, profi, sr_deleted) VALUES (?, ?, ?) "
    hg.conexao_cursor.execute(sql, (m_cod_profi, m_profi, ' '))
    hg.conexao_bd.commit()
    QMessageBox.information(tela, "Inclusao de OBSERVACAO", "Cadastro feito com SUCESSO!")

    tela.mcod_profi.setEnabled(False)
    tela.mprofi.setEnabled(False)
    tela.bt_salvar.setEnabled(False)
    tela.mcod_profi.setText('')
    tela.mprofi.setText('')
    listar_profissao()


def chama_alteracao():
    tela.bt_salvar.clicked.disconnect()
    m_cod_profi = tela.mcod_profi.text().upper()
    m_profi = tela.mprofi.text().upper()

    sql = "UPDATE sacprofi SET profi = ? WHERE cod_profi = ?"
    hg.conexao_cursor.execute(sql, (m_profi, m_cod_profi))

    hg.conexao_bd.commit()
    QMessageBox.information(tela, "ALTERACAO DE PROFISSAO", "Alteracao feita com SUCESSO!")
    listar_profissao()


def editar_item(row):
    tela.groupBox.setTitle("ALTERACAO")
    vcodigo = str(tabela.item(row, 0).text())
    vprofi = tabela.item(row, 1).text().strip()
    tabela.itemDoubleClicked.disconnect()
    if tela.rb_alteracao.isChecked():
        tela.mprofi.setEnabled(True)
        tela.bt_salvar.clicked.connect(chama_alteracao)
        tela.bt_cancelar.clicked.connect(listar_profissao)
        tela.bt_salvar.setEnabled(True)
        tela.bt_cancelar.setEnabled(True)
        tela.mcod_profi.setText(vcodigo)
        tela.mprofi.setText(vprofi)
        tela.mprofi.setFocus()
    else:
        # chama_consulta(item.text())
        pass

    tabela.itemDoubleClicked.connect(lambda items: editar_item(items.row()))
    return


def habilitar_objeto():
    tela.groupBox.setTitle("INCLUSAO")
    tela.mcod_profi.clear()
    tela.mprofi.clear()
    hg.conexao_cursor.execute(f"SELECT max(cod_profi) FROM sacprofi")
    arq_profi = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()
    if arq_profi is None:
        codigo = 1
        tela.mcod_profi.setText(str(codigo).zfill(5))
    else:
        codigo = int(arq_profi[0]) + 1
        tela.mcod_profi.setText(str(codigo).zfill(5))

    tela.bt_salvar.clicked.connect(f_incl_profissao)
    tela.bt_cancelar.clicked.connect(listar_profissao)
    tela.mprofi.setEnabled(True)
    tela.bt_salvar.setEnabled(True)
    tela.bt_cancelar.setEnabled(True)
    tela.mprofi.setFocus()


def listar_profissao():
    tela.groupBox.setTitle("INCLUSAO/ALTERACAO")
    hg.conexao_cursor.execute(f"SELECT cod_profi, profi FROM sacprofi order BY cod_profi")
    dados_lidos = hg.conexao_cursor.fetchall()
    hg.conexao_bd.commit()
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

    tela.mcod_profi.setEnabled(False)
    tela.mprofi.setEnabled(False)

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


if __name__ == '__main__':
    from hti_funcoes import conexao_banco
    conexao_banco()
    listar_profissao()
    app.exec()
    hg.conexao_bd.close()
