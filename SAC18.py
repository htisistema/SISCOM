# ESTADOS

from PyQt6 import uic, QtWidgets
from PyQt6.QtGui import QIcon, QGuiApplication
from PyQt6.QtWidgets import QButtonGroup, QMessageBox, QAbstractItemView, QTableWidgetItem
import os
import hti_global as hg

app = QtWidgets.QApplication([])
app.setStyleSheet(hg.style_sheet)
tela = uic.loadUi(f"{hg.c_ui}\\lista_estados.ui")
tela.setWindowTitle('ESTADOS CADASTRADO')
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


def f_incl_estados():
    tela.bt_salvar.clicked.disconnect()
    m_uf = tela.muf.text().upper().strip()
    m_estado = tela.mestado.text().upper()
    m_percent = tela.doubleSpinBox.value()
    hg.conexao_cursor.execute(f"SELECT uf FROM sacuf WHERE uf = '{m_uf}'")
    arq_uf = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()
    if arq_uf is not None:
        QMessageBox.information(tela, "INCLUSAO ESTADOS ", "Estado ja CADASTRADO !")
        tela.muf.setFocus()
        return

    sql = "INSERT INTO sacuf (uf, estado, percent) VALUES (?, ?, ?)"
    hg.conexao_cursor.execute(sql, (m_uf, m_estado, m_percent))
    hg.conexao_bd.commit()
    QMessageBox.information(tela, "Inclusao de ESTADO", "Cadastro feito com SUCESSO!")
    listar_estados()


def chama_alteracao(mcod_cli):
    m_uf = tela.muf.text().upper().strip()
    m_estado = tela.mestado.text().upper()
    m_percent = tela.doubleSpinBox.value()
    hg.conexao_cursor.execute(f"SELECT uf FROM sacuf WHERE uf = '{m_uf}'")
    arq_uf = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()
    if arq_uf is None:
        QMessageBox.information(tela, "INCLUSAO ESTADOS ", "Estado nao CADASTRADO !")
        tela.muf.setFocus()

    sql = "UPDATE sacuf SET estado = ?, percent = ? WHERE uf = ?"
    hg.conexao_cursor.execute(sql, (m_estado, m_percent, m_uf))

    hg.conexao_bd.commit()
    QMessageBox.information(tela, "ALTERACAO DE ESTADOS", "Alteracao feita com SUCESSO!")
    listar_estados()


def editar_item(row):
    vuf = str(tabela.item(row, 0).text())
    vestado = tabela.item(row, 1).text().strip()
    vpercent = tabela.item(row, 2).text()
    vpercent = vpercent.replace(",", ".")
    tabela.itemDoubleClicked.disconnect()
    if tela.rb_alteracao.isChecked():
        tela.mestado.setEnabled(True)
        tela.doubleSpinBox.setEnabled(True)
        tela.bt_salvar.clicked.connect(chama_alteracao)
        tela.bt_retorno.clicked.connect(listar_estados)
        tela.bt_salvar.setEnabled(True)
        tela.bt_retorno.setEnabled(True)
        tela.muf.setText(vuf)
        tela.mestado.setText(vestado)
        tela.doubleSpinBox.setValue(float(vpercent))
        tela.mestado.setFocus()
    else:
        # chama_consulta(item.text())
        pass

    tabela.itemDoubleClicked.connect(lambda items: editar_item(items.row()))
    return


def habilitar_objeto():
    tela.muf.clear()
    tela.mestado.clear()
    tela.doubleSpinBox.setValue(0)
    tela.bt_salvar.clicked.connect(f_incl_estados)
    tela.bt_retorno.clicked.connect(listar_estados)
    tela.muf.setEnabled(True)
    tela.mestado.setEnabled(True)
    tela.doubleSpinBox.setEnabled(True)
    tela.bt_salvar.setEnabled(True)
    tela.bt_retorno.setEnabled(True)
    tela.muf.setFocus()


def listar_estados():
    hg.conexao_cursor.execute(f"SELECT CAST(uf as char(2)), "
                                      f"CAST(estado as char(20)), "
                                      f"REPLACE(CAST(percent AS DECIMAL(18,2)), '.', ',') FROM sacuf ORDER BY estado")

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
    tela.rb_alteracao.setChecked(True)
    tela.mestado.setText('')
    tela.muf.setText('')
    tela.doubleSpinBox.setValue(0)
    tela.mestado.setEnabled(False)
    tela.muf.setEnabled(False)
    tela.doubleSpinBox.setEnabled(False)
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


if __name__ == '__main__':
    from hti_funcoes import conexao_banco
    conexao_banco()
    listar_estados()
    app.exec()
    hg.conexao_bd.close()
