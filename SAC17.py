# DESPESA

from PyQt6 import uic, QtWidgets
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QButtonGroup, QMessageBox, QAbstractItemView, QTableWidgetItem
import os
import hti_global as hg


app = QtWidgets.QApplication([])
app.setStyleSheet(hg.style_sheet)
tela = uic.loadUi(f"{hg.c_ui}\\lista_despesa.ui")
tela.setWindowTitle('DESPESAS CADASTRADAS')
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
if hg.mtp_tela == 'G':
    primary_screen = QGuiApplication.primaryScreen()
    if primary_screen is not None:
        screen_geometry = primary_screen.geometry()
        tela.setGeometry(screen_geometry)


tabela = tela.tableWidget

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


def chama_alteracao(mcod_cli):
    tela.bt_salvar.clicked.disconnect()
    m_codigo = tela.mcodigo.text().upper()
    m_desc1 = tela.mdesc1.text().upper()
    m_desc2 = tela.mdesc2.text().upper()

    sql = "UPDATE saccadde SET desc1 = ?, desc2 = ? WHERE codigo = ?"
    hg.conexao_cursor.execute(sql, (m_desc1, m_desc2, m_codigo))

    hg.conexao_bd.commit()
    QMessageBox.information(tela, "ALTERACAO DE DESPESA", "Alteracao feita com SUCESSO!")
    listar_despesa()


def editar_item(row):
    vcodigo = str(tabela.item(row, 0).text())
    vdesc1 = tabela.item(row, 1).text()
    vdesc2 = tabela.item(row, 2).text()
    tabela.itemDoubleClicked.disconnect()
    if tela.rb_alteracao.isChecked():
        tela.mdesc1.setEnabled(True)
        tela.mdesc2.setEnabled(True)
        tela.bt_salvar.clicked.connect(chama_alteracao)
        tela.bt_retorno.clicked.connect(listar_despesa)
        tela.bt_salvar.setEnabled(True)
        tela.bt_retorno.setEnabled(True)
        tela.mcodigo.setText(vcodigo)
        tela.mdesc1.setText(str(vdesc1))
        tela.mdesc2.setText(str(vdesc2))
        tela.mdesc1.setFocus()
    else:
        # chama_consulta(item.text())
        pass

    tabela.itemDoubleClicked.connect(lambda items: editar_item(items.row()))
    return


def f_incl_despesa():
    # tela.bt_salvar.clicked.disconnect(f_incl_despesa)
    tela.bt_salvar.clicked.disconnect()
    m_codigo = tela.mcodigo.text().upper()
    m_desc1 = tela.mdesc1.text().upper()
    m_desc2 = tela.mdesc2.text().upper()
    sql = "INSERT INTO saccadde (codigo, desc1, desc2, sr_deleted) VALUES (?, ?, ?, ?)"
    hg.conexao_cursor.execute(sql, (m_codigo, m_desc1, m_desc2, ' '))
    hg.conexao_bd.commit()
    QMessageBox.information(tela, "Inclusao de CONDICOES DE PAGAMENTOS", "Cadastro feito com SUCESSO!")
    listar_despesa()


def habilitar_objeto():
    tela.mcodigo.clear()
    tela.mdesc1.clear()
    tela.mdesc2.clear()
    hg.conexao_cursor.execute(f"SELECT max(codigo) FROM saccadde")
    arq_despesa = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()
    if arq_despesa is None:
        codigo = 1
        tela.mcodigo.setText(str(codigo).zfill(3))
    else:
        codigo = int(arq_despesa[0]) + 1
        tela.mcodigo.setText(str(codigo).zfill(3))

    tela.bt_salvar.clicked.connect(f_incl_despesa)
    tela.bt_retorno.clicked.connect(listar_despesa)
    tela.mdesc1.setEnabled(True)
    tela.mdesc2.setEnabled(True)
    tela.bt_salvar.setEnabled(True)
    tela.bt_retorno.setEnabled(True)
    tela.mdesc1.setFocus()


def listar_despesa():
    hg.conexao_cursor.execute(f"SELECT CAST(codigo as char(3)), desc1, desc2  FROM saccadde order BY codigo")
    dados_lidos = hg.conexao_cursor.fetchall()
    hg.conexao_bd.commit()
    tabela.setRowCount(len(dados_lidos))
    tabela.setColumnCount(3)
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
    tela.mcodigo.setText('')
    tela.mdesc1.setText('')
    tela.mdesc2.setText('')
    tela.mcodigo.setEnabled(False)
    tela.mdesc1.setEnabled(False)
    tela.mdesc2.setEnabled(False)
    tela.rb_alteracao.setChecked(True)
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
    listar_despesa()
    app.exec()
    hg.conexao_bd.close()
