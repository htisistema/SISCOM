# CFOP

from PyQt6 import uic, QtWidgets
from PyQt6.QtGui import QIcon, QGuiApplication
from PyQt6.QtWidgets import QButtonGroup, QMessageBox, QTableWidgetItem, QTableWidget, QStatusBar, QAbstractItemView
from PyQt6.QtWidgets import QGroupBox
import os
import hti_global

app = QtWidgets.QApplication([])
app.setStyleSheet(hti_global.style_sheet)
tela = uic.loadUi(f"{hti_global.c_ui}\\lista_cfop.ui")
tela.setWindowTitle('CFOP CADASTRADO')
icon = QIcon(f"{hti_global.c_imagem}\\htiico.jpg")
icon_cancelar = QIcon(f"{hti_global.c_imagem}\\cancelar.png")
icon_sair = QIcon(f"{hti_global.c_imagem}\\sair.png")
icon_salvar = QIcon(f"{hti_global.c_imagem}\\salvar.png")
icon_incluir = QIcon(f"{hti_global.c_imagem}\\incluir.png")
tela.setWindowIcon(icon)
tabela = tela.tableWidget
# Centraliza a janela na tela
qt_rectangle = tela.frameGeometry()
center_point = app.primaryScreen().availableGeometry().center()
qt_rectangle.moveCenter(center_point)
tela.move(qt_rectangle.topLeft())
# tela.setGeometry(0, 0, 400, 200)  # Defina um tamanho inicial para a janela
if hti_global.mtp_tela == 'G':
    primary_screen = QGuiApplication.primaryScreen()
    if primary_screen is not None:
        screen_geometry = primary_screen.geometry()
        tela.setGeometry(screen_geometry)

# PEGA O NOME DO ARQUIVO EM EXECUCAO
nome_file_com = os.path.basename(__file__)
nome_file, ext = os.path.splitext(nome_file_com)

tela.statusBar.showMessage(f"<< {nome_file} >>")

deb_cred = ['Debito', 'Credito']
tela.comboBox.addItems(deb_cred)
tela.comboBox.setCurrentIndex(0)  # coloca o focus no index
ent_sai = ['Saida', 'Entrada']
tela.comboBox_2.addItems(ent_sai)
tela.comboBox_2.setCurrentIndex(0)  # coloca o focus no index
tipo_nota = ['1-Normal', '2-Complementar', '3-Ajuste', '4-Devolucao/Retorno']
tela.comboBox_3.addItems(tipo_nota)
tela.comboBox_3.setCurrentIndex(0)  # coloca o focus no index


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


def f_incl_cfop():
    tela.bt_salvar.clicked.disconnect()
    m_operacao = tela.moperacao.text().upper()
    hti_global.conexao_cursor.execute(f"SELECT operacao FROM sacop WHERE operacao = {m_operacao}")
    arq_profi = hti_global.conexao_cursor.fetchone()
    hti_global.conexao_bd.commit()
    if arq_profi is None:
        QMessageBox.information(tela, "Inclusao de CFOP", "CFOP ja CADASTRADO!")
        return

    m_descr_op = tela.mdescr_op.text().upper()

    index = tela.comboBox.currentIndex()
    mop = tela.comboBox.itemText(index)
    m_credito = mop[0:1]

    index = tela.comboBox_2.currentIndex()
    mop = tela.comboBox_2.itemText(index)
    m_sai_ent = mop[0:1]

    index = tela.comboBox_3.currentIndex()
    mop = tela.comboBox_3.itemText(index)
    m_tipo = mop[0:1]

    sql = "INSERT INTO sacop (operacao, descr_op, credito, sai_ent, tipo, sr_deleted) VALUES (?, ?, ?, ?, ?, ?) "
    hti_global.conexao_cursor.execute(sql, (m_operacao, m_descr_op, m_credito, m_sai_ent, m_tipo, ' '))
    hti_global.conexao_bd.commit()
    QMessageBox.information(tela, "Inclusao de OBSERVACAO", "Cadastro feito com SUCESSO!")

    tela.moperacao.setEnabled(False)
    tela.mdescr_op.setEnabled(False)
    tela.comboBox.setEnabled(False)
    tela.comboBox_2.setEnabled(False)
    tela.comboBox_3.setEnabled(False)
    tela.bt_salvar.setEnabled(False)
    tela.moperacao.setText('')
    tela.mdescr_op.setText('')
    listar_cfop()


def chama_alteracao(mcod_cli):
    # from alt_grupo import alteracao_grupo
    # alteracao_grupo(mcod_cli[0:5])
    pass
    return


def editar_item(row):
    tela.groupBox.setTitle("ALTERACAO")
    vcodigo = str(tabela.item(row, 0).text())
    vdescri = tabela.item(row, 1).text().strip()
    vdeb_cred = tabela.item(row, 2).text().strip()
    vdeb_cred = vdeb_cred[0]
    vent_sai = tabela.item(row, 3).text().strip()
    vent_sai = vent_sai[0]
    vtipo = tabela.item(row, 4).text().strip()
    vtipo = vtipo[0]
    # print('1')
    tabela.itemDoubleClicked.disconnect()
    if tela.rb_alteracao.isChecked():
        tela.moperacao.setEnabled(True)
        tela.mdescr_op.setEnabled(True)
        tela.comboBox.setEnabled(True)
        tela.comboBox_2.setEnabled(True)
        tela.comboBox_3.setEnabled(True)
        tela.bt_salvar.clicked.connect(chama_alteracao)
        tela.bt_cancelar.clicked.connect(listar_cfop)
        tela.bt_salvar.setEnabled(True)
        tela.bt_cancelar.setEnabled(True)
        tela.moperacao.setText(vcodigo)
        tela.mdescr_op.setText(vdescri)

        for i in range(tela.comboBox.count()):
            item_text = tela.comboBox.itemText(i)
            if str(vdeb_cred).strip() in item_text:
                tela.comboBox.setCurrentIndex(i)
                break

        for i in range(tela.comboBox_2.count()):
            item_text = tela.comboBox_2.itemText(i)
            if str(vent_sai).strip() in item_text:
                tela.comboBox_2.setCurrentIndex(i)
                break

        for i in range(tela.comboBox_3.count()):
            item_text = tela.comboBox_3.itemText(i)
            if str(vtipo).strip() in item_text:
                tela.comboBox_3.setCurrentIndex(i)
                break

        tela.moperacao.setFocus()
    else:
        # chama_consulta(item.text())
        pass

    tabela.itemDoubleClicked.connect(lambda items: editar_item(items.row()))
    return


def habilitar_objeto():
    tela.groupBox.setTitle("INCLUSAO")
    tela.moperacao.clear()
    tela.mdescr_op.clear()
    tela.bt_salvar.clicked.connect(f_incl_cfop)
    tela.bt_cancelar.clicked.connect(listar_cfop)
    tela.moperacao.setEnabled(True)
    tela.mdescr_op.setEnabled(True)
    tela.comboBox.setEnabled(True)
    tela.comboBox_2.setEnabled(True)
    tela.comboBox_3.setEnabled(True)
    tela.bt_salvar.setEnabled(True)
    tela.bt_cancelar.setEnabled(True)
    tela.moperacao.setFocus()


def listar_cfop():
    hti_global.conexao_cursor.execute(f"SELECT CAST(operacao as char(5)), "
                                      f"CAST(descr_op as char(40)), "
                                      f"iif(credito = 'S','S-Debito ou Credito','N-Sem Movimentacao'), "
                                      f"iif(sai_ent = 'S', 'S-Nota de SAIDA', 'E-Nota de ENTRADA'), "
                                      f"iif(tipo = '1', '1 - NFe NORMAL', iif(tipo = '2', '2 - NFe COMPLEMENTAR', "
                                      f"iif(tipo = '3', '3 - NFe AJUSTE', '4 - DEVOLUCAO/RETORNO')))  "
                                      f" FROM sacop ORDER BY operacao")

    dados_lidos = hti_global.conexao_cursor.fetchall()
    hti_global.conexao_bd.commit()
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

    tela.moperacao.setEnabled(False)
    tela.mdescr_op.setEnabled(False)
    tela.comboBox.setEnabled(False)
    tela.comboBox_2.setEnabled(False)
    tela.comboBox_3.setEnabled(False)
    tela.moperacao.setText('')
    tela.mdescr_op.setText('')

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
    listar_cfop()
    hti_global.conexao_bd.close()
