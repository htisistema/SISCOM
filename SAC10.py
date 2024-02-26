# GRUPOS

from PyQt6 import uic, QtWidgets
from PyQt6.QtGui import QIcon, QGuiApplication
from PyQt6.QtWidgets import QButtonGroup, QMessageBox, QTableWidgetItem, QTableWidget, QStatusBar, QAbstractItemView
from PyQt6.QtWidgets import QGroupBox
import os
import hti_global as hg

app = QtWidgets.QApplication([])
app.setStyleSheet(hg.style_sheet)
tela = uic.loadUi(f"{hg.c_ui}\\lista_grupo.ui")
tela.setWindowTitle('GRUPOS E SUB-GRUPOS')
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

# PEGA O NOME DO ARQUIVO EM EXECUCAO
nome_file_com = os.path.basename(__file__)
nome_file, ext = os.path.splitext(nome_file_com)

tela.statusBar.showMessage(f"<< {nome_file} >>")


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


def f_incl_grupo():
    tela.bt_salvar.clicked.disconnect()
    m_grupo = tela.mgrupo.text().upper()
    m_merc = tela.mmerc.text().upper()
    m_subgrupo = tela.msubgrupo.text().upper()
    m_gru_sub = f"{m_grupo}{m_subgrupo}"
    hg.conexao_cursor.execute(f"SELECT gru_sub FROM sacgrupo WHERE gru_sub = {m_gru_sub}")
    arq_profi = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()
    if arq_profi is not None:
        QMessageBox.information(tela, "Inclusao de GRUPO", "GRUPO ja CADASTRADO!")
        return

    sql = "INSERT INTO sacgrupo (gru_sub, merc, sr_deleted) VALUES (?, ?, ?) "
    hg.conexao_cursor.execute(sql, (m_gru_sub, m_merc, ' '))
    hg.conexao_bd.commit()
    QMessageBox.information(tela, "Inclusao de TIPO DE DOCUMENTO", "Cadastro feito com SUCESSO!")

    listar_grupo()


def chama_alteracao(mcod_cli):
    tela.bt_salvar.clicked.disconnect()
    m_grupo = tela.mgrupo.text().upper()
    m_subgrupo = tela.msubgrupo.text().upper()
    m_gru_sub = f"{m_grupo}{m_subgrupo}"
    m_merc = tela.mmerc.text().upper()
    hg.conexao_cursor.execute(f"SELECT gru_sub FROM sacgrupo WHERE gru_sub = {m_grupo}")
    arq_profi = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()
    if arq_profi is None:
        QMessageBox.information(tela, "Inclusao de GRUPO/SUB GRUPO", "GRUPO/SUB GRUPO nao CADASTRADO!")
        return

    sql = "UPDATE sacgrupo SET merc = ? WHERE gru_sub = ?"
    hg.conexao_cursor.execute(sql, (m_merc, m_gru_sub))
    hg.conexao_bd.commit()
    QMessageBox.information(tela, "Inclusao de GRUPPO", "Alteracao feita com SUCESSO!")

    listar_grupo()


def editar_item(row):
    tela.groupBox.setTitle("ALTERACAO")
    vgrupo = str(tabela.item(row, 0).text())
    vsubgrupo = tabela.item(row, 1).text().strip()
    vmerc = tabela.item(row, 2).text().strip()
    tabela.itemDoubleClicked.disconnect()
    if tela.rb_alteracao.isChecked():
        tela.mgrupo.setEnabled(False)
        if len(vsubgrupo) > 0:
            tela.msubgrupo.setEnabled(True)
        tela.mmerc.setEnabled(True)
        tela.mgrupo.setText(vgrupo)
        tela.msubgrupo.setText(vsubgrupo)
        tela.mmerc.setText(vmerc)
        tela.bt_salvar.clicked.connect(chama_alteracao)
        tela.bt_cancelar.clicked.connect(listar_grupo)
        tela.bt_salvar.setEnabled(True)
        tela.bt_cancelar.setEnabled(True)
        tela.mmerc.setFocus()
    elif tela.rb_subgrupo.isChecked():
        tela.mgrupo.setEnabled(False)
        tela.msubgrupo.setEnabled(True)
        tela.mmerc.setEnabled(True)
        tela.mgrupo.setText(vgrupo)
        tela.msubgrupo.setText(vsubgrupo)
        tela.mmerc.setText(vmerc)
        tela.bt_salvar.clicked.connect(f_incl_grupo)
        tela.bt_cancelar.clicked.connect(listar_grupo)
        tela.bt_salvar.setEnabled(True)
        tela.bt_cancelar.setEnabled(True)
        tela.msubgrupo.setFocus()
    else:
        # chama_consulta(item.text())
        pass

    tabela.itemDoubleClicked.connect(lambda items: editar_item(items.row()))
    return


def habilitar_objeto():
    tela.groupBox.setTitle("INCLUSAO")
    tela.mgrupo.clear()
    tela.msubgrupo.clear()
    tela.mmerc.clear()
    tela.mgrupo.setEnabled(True)
    tela.msubgrupo.setEnabled(False)
    tela.mmerc.setEnabled(True)
    tela.bt_salvar.clicked.connect(f_incl_grupo)
    tela.bt_cancelar.clicked.connect(listar_grupo)
    tela.bt_salvar.setEnabled(True)
    tela.bt_cancelar.setEnabled(True)
    tela.mgrupo.setFocus()


def listar_grupo():
    # pesquisa()
    hg.conexao_cursor.execute(f"SELECT CAST(substring(gru_sub from 1 for 3) as char(3)) as grupo, "
                                      f"CAST(substring(gru_sub from 4 for 2) as char(3)) as subgrupo, "
                                      f"COALESCE(merc, ' ') as merc FROM sacgrupo ORDER BY gru_sub")

    dados_lidos = hg.conexao_cursor.fetchall()
    hg.conexao_bd.commit()

    tabela.setRowCount(len(dados_lidos))
    tabela.setColumnCount(3)
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
    rb_tipo_group.addButton(tela.rb_subgrupo, id=2)
    tela.rb_alteracao.setChecked(True)

    tela.mgrupo.setEnabled(False)
    tela.msubgrupo.setEnabled(False)
    tela.mmerc.setEnabled(False)
    tela.mgrupo.setText('')
    tela.msubgrupo.setText('')
    tela.mmerc.setText('')

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
    listar_grupo()
    app.exec()
    hg.conexao_bd.close()
