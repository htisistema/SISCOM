# CIDADES

from PyQt6 import uic, QtWidgets
from PyQt6.QtGui import QIcon, QGuiApplication
from PyQt6.QtWidgets import QButtonGroup, QMessageBox, QAbstractItemView, QTableWidgetItem
import os
import hti_global as hg

titulo = 'CIDADES CADASTRADAS'
app = QtWidgets.QApplication([])
app.setStyleSheet(hg.style_sheet)
tela = uic.loadUi(f"{hg.c_ui}\\lista_cidade.ui")
icon = QIcon(f"{hg.c_imagem}\\htiico.jpg")
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


def editar_item(row):
    vcidade = tabela.item(row, 0).text().strip()
    vuf = tabela.item(row, 1).text().strip()
    vcep = tabela.item(row, 2).text().strip()
    vcod_cid = tabela.item(row, 3).text().strip()
    tabela.itemDoubleClicked.disconnect()
    if tela.rb_alteracao.isChecked():
        tela.mcidade.setEnabled(True)
        tela.muf.setEnabled(True)
        tela.mcep.setEnabled(True)
        tela.mcod_cid.setEnabled(True)
        tela.bt_salvar.clicked.connect(chama_alteracao)
        tela.bt_cancelar.clicked.connect(listar_cidade)
        tela.bt_salvar.setEnabled(True)
        tela.bt_cancelar.setEnabled(True)
        tela.muf.setText(vuf)
        tela.mcidade.setText(vcidade)
        tela.mcep.setText(vcep)
        tela.mcod_cid.setText(vcod_cid)
        tela.mcidade.setFocus()
    else:
        # chama_consulta(item.text())
        pass

    tabela.itemDoubleClicked.connect(lambda items: editar_item(items.row()))
    return


def f_incl_cidade():
    tela.bt_salvar.clicked.disconnect()
    m_cidade = tela.mcidade.text().upper()
    m_uf = tela.muf.text().upper().strip()
    m_cep = tela.mcep.text().upper()
    m_cep = ''.join(filter(str.isdigit, m_cep))
    m_cod_cid = tela.mcod_cid.text().upper()
    hg.conexao_cursor.execute(f"SELECT cod_cid FROM saccid WHERE cod_cid = '{m_cod_cid}'")
    arq_uf = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()
    if arq_uf is not None:
        QMessageBox.information(tela, "INCLUSAO ESTADOS ", "codigo de CIDADE ja CADASTRADO !")
        tela.muf.setFocus()
        return

    sql = "INSERT INTO saccid (cidade, uf, cep, cod_cid, sr_deleted) VALUES (?, ?, ?, ?, ?)"
    hg.conexao_cursor.execute(sql, (m_cidade, m_uf, m_cep, m_cod_cid, ' '))
    hg.conexao_bd.commit()
    QMessageBox.information(tela, "Inclusao de ESTADO", "Cadastro feito com SUCESSO!")
    listar_cidade()


def habilitar_objeto():
    tela.mcidade.clear()
    tela.muf.clear()
    tela.mcep.clear()
    tela.mcod_cid.clear()
    tela.bt_salvar.clicked.connect(f_incl_cidade)
    tela.bt_cancelar.clicked.connect(listar_cidade)
    # print('ok')
    tela.mcidade.setEnabled(True)
    tela.muf.setEnabled(True)
    tela.mcep.setEnabled(True)
    tela.mcod_cid.setEnabled(True)
    tela.bt_salvar.setEnabled(True)
    tela.bt_cancelar.setEnabled(True)
    tela.mcidade.setFocus()


def chama_alteracao():
    m_uf = tela.muf.text().upper().strip()
    m_cidade = tela.mcidade.text().upper()
    m_cep = tela.mcep.text().upper()
    m_cep = ''.join(filter(str.isdigit, m_cep))
    m_cod_cid = tela.mcod_cid.text().upper()
    hg.conexao_cursor.execute(f"SELECT cod_cid FROM saccid WHERE cod_cid = '{m_cod_cid}'")
    arq_uf = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()
    if arq_uf is None:
        QMessageBox.information(tela, "ALTERACAO DE CIDADES ", "Cidade nao CADASTRADO !")
        tela.mcidade.setFocus()
        return

    sql = "UPDATE saccid SET cidade = ?, uf = ?, cep = ? WHERE cod_cid = ?"
    hg.conexao_cursor.execute(sql, (m_cidade, m_uf, m_cep, m_cod_cid))
    hg.conexao_bd.commit()
    QMessageBox.information(tela, "ALTERACAO DE CIDADES", "Alteracao feita com SUCESSO!")
    listar_cidade()


def listar_cidade():
    tabela.clearContents()
    tabela.setRowCount(0)
    hg.conexao_cursor.execute(f"SELECT cidade, uf, cep, cod_cid FROM saccid order BY cidade")
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
    tela.mcidade.setText('')
    tela.muf.setText('')
    tela.mcep.setText('')
    tela.mcod_cid.setText('')

    tela.mcidade.setEnabled(False)
    tela.muf.setEnabled(False)
    tela.mcep.setEnabled(False)
    tela.mcod_cid.setEnabled(False)
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
    app.exec()


if __name__ == '__main__':
    from hti_funcoes import conexao_banco
    conexao_banco()
    listar_cidade()
    hg.conexao_bd.close()
