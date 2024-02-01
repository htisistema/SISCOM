# REGIAO

from PyQt6 import uic, QtWidgets
from PyQt6.QtGui import QIcon, QGuiApplication
from PyQt6.QtWidgets import QButtonGroup, QMessageBox, QTableWidgetItem, QTableWidget, QStatusBar, QAbstractItemView
from PyQt6.QtWidgets import QGroupBox
import os
import hti_global as hg

titulo = 'REGIAO CADASTRADO'
app = QtWidgets.QApplication([])
app.setStyleSheet(hg.style_sheet)
tela = uic.loadUi(f"{hg.c_ui}\\lista_regiao.ui")
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


def f_incl_regiao():
    tela.groupBox.setTitle("INCLUSAO")
    tela.bt_salvar.clicked.disconnect()
    m_codigo = tela.mcodigo.text().upper()
    hg.conexao_cursor.execute(f"SELECT codigo FROM regiao WHERE codigo = {m_codigo}")
    arq_regiao = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()
    if arq_regiao is not None:
        QMessageBox.information(tela, "Inclusao de REGIAO", "REGIAO ja CADASTRADO!")
        return

    m_regiao = tela.mregiao.text().upper()

    index = tela.comboBox.currentIndex()
    mop = tela.comboBox.itemText(index)
    m_codvend = mop[0:3]

    sql = "INSERT INTO regiao (codigo, regiao, codvend, sr_deleted) VALUES (?, ?, ?, ?) "
    hg.conexao_cursor.execute(sql, (m_codigo, m_regiao, m_codvend, ' '))
    hg.conexao_bd.commit()
    QMessageBox.information(tela, "Inclusao de REGIAO", "Cadastro feito com SUCESSO!")

    listar_regiao()


def chama_alteracao(mcod_cli):
    tela.bt_salvar.clicked.disconnect()
    m_codigo = tela.mcodigo.text().upper()
    hg.conexao_cursor.execute(f"SELECT codigo FROM regiao WHERE codigo = {m_codigo}")
    arq_profi = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()
    print('ok')
    if arq_profi is None:
        QMessageBox.information(tela, "Inclusao de REGIAO", "REGIAO nao CADASTRADO!")
        return

    m_regiao = tela.mregiao.text().upper()

    index = tela.comboBox.currentIndex()
    mop = tela.comboBox.itemText(index)
    m_codvend = mop[0:3]
    sql = "UPDATE regiao SET regiao = ?, codvend = ? WHERE codigo = ?"
    hg.conexao_cursor.execute(sql, (m_regiao, m_codvend, m_codigo))
    hg.conexao_bd.commit()
    QMessageBox.information(tela, "ALTERACAO de REGIAO", "Alteracao feita com SUCESSO!")

    listar_regiao()


def editar_item(row):
    tela.groupBox.setTitle("ALTERACAO")
    vcodigo = str(tabela.item(row, 0).text())
    vregiao = tabela.item(row, 1).text().strip()
    vcodvend = tabela.item(row, 2).text().strip()
    vcodvend = vcodvend[0:3]
    tabela.itemDoubleClicked.disconnect()
    if tela.rb_alteracao.isChecked():
        tela.mcodigo.setEnabled(False)
        tela.mregiao.setEnabled(True)
        tela.comboBox.setEnabled(True)
        tela.mcodigo.setText(vcodigo)
        tela.mregiao.setText(vregiao)
        tela.bt_salvar.clicked.connect(chama_alteracao)
        tela.bt_cancelar.clicked.connect(listar_regiao)
        tela.bt_salvar.setEnabled(True)
        tela.bt_cancelar.setEnabled(True)

        for i in range(tela.comboBox.count()):
            item_text = tela.comboBox.itemText(i)
            if str(vcodvend).strip() in item_text:
                tela.comboBox.setCurrentIndex(i)
                break

        tela.mregiao.setFocus()
    else:
        # chama_consulta(item.text())
        pass

    tabela.itemDoubleClicked.connect(lambda items: editar_item(items.row()))
    return


def habilitar_objeto():
    tela.mcodigo.clear()
    tela.mregiao.clear()
    tela.mcodigo.setEnabled(False)
    hg.conexao_cursor.execute(f"SELECT max(codigo) FROM regiao")
    max_regiao = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()
    if max_regiao is None:
        codigo = 1
        tela.mcodigo.setText(str(codigo).zfill(2))
    else:
        codigo = int(max_regiao[0]) + 1
        tela.mcodigo.setText(str(codigo).zfill(2))

    tela.groupBox.setTitle("INCLUSAO")
    tela.mregiao.setEnabled(True)
    tela.bt_salvar.clicked.connect(f_incl_regiao)
    tela.bt_cancelar.clicked.connect(listar_regiao)
    tela.comboBox.setEnabled(True)
    tela.bt_salvar.setEnabled(True)
    tela.bt_cancelar.setEnabled(True)
    tela.mregiao.setFocus()


def listar_regiao():
    tela.groupBox.setTitle("INCLUSAO/ALTERACAO")
    hg.conexao_cursor.execute(f"SELECT scod_op, snome FROM insopera order BY snome")
    ver_vendedor = hg.conexao_cursor.fetchall()
    hg.conexao_bd.commit()
    for ret_vendedor in ver_vendedor:
        item = f'{ret_vendedor[0]} - {ret_vendedor[1]}'.strip('(),')
        tela.comboBox.addItem(item)
    tela.comboBox.setCurrentIndex(0)

    hg.conexao_cursor.execute(f"SELECT codigo, regiao, codvend FROM regiao order BY regiao")
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
    tela.rb_alteracao.setChecked(True)

    tela.mcodigo.setEnabled(False)
    tela.mregiao.setEnabled(False)
    tela.comboBox.setEnabled(False)
    tela.mcodigo.setText('')
    tela.mregiao.setText('')

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
    listar_regiao()
    app.exec()
    hg.conexao_bd.close()
