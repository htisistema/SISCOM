# CONDICAO DE PAGAMENTO

import os
from PyQt6 import uic, QtWidgets
from PyQt6.QtGui import QIcon, QGuiApplication
from PyQt6.QtWidgets import QButtonGroup, QMessageBox, QAbstractItemView, QTableWidgetItem
import hti_global

app = QtWidgets.QApplication([])
app.setStyleSheet(hti_global.style_sheet)
tela = uic.loadUi(f"{hti_global.c_ui}\\lista_cond_pag.ui")
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

tela.setWindowTitle('CONDICOES DE PAGAMENTOS CADASTRADAS')
tabela = tela.tableWidget

tela.statusBar = QtWidgets.QStatusBar()
tela.setStatusBar(tela.statusBar)

# PEGA O NOME DO ARQUIVO EM EXECUCAO
nome_file_com = os.path.basename(__file__)
nome_file, ext = os.path.splitext(nome_file_com)

tela.statusBar.showMessage(f"<< {nome_file} >>")

tela.comboBox_2.addItems([" ", "1", "2", "C", "A"])
tela.comboBox_2.setCurrentIndex(0)  # coloca o focus no index

tela.comboBox.addItems(["Sim", "Nao"])
tela.comboBox.setCurrentIndex(0)  # coloca o focus no index


def on_close_event(event):
    # Esta função será chamada quando o usuário clicar no botão de fechar a janela
    # print("Fechando a janela...")
    tela.close()
    event.accept()


tela.closeEvent = on_close_event


def fecha_tela():
    tela.close()


# Define a função para ajustar as colunas da tela
def ajustar_colunas_tabela(tabela):
    header = tabela.horizontalHeader()
    header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
    header.setStretchLastSection(False)


def f_incl_cond_pag():
    m_codigo = tela.mcodigo.text().upper()
    m_descri = tela.mdescri.text().upper()
    m_cond = tela.mcond.text().upper()
    m_cond = ''.join(filter(str.isdigit, m_cond))
    m_percent = tela.doubleSpinBox.value()
    m_comi_tab = tela.doubleSpinBox_3.value()
    m_dia1 = tela.doubleSpinBox_4.value()
    m_dia2 = tela.doubleSpinBox_5.value()
    m_dia3 = tela.doubleSpinBox_6.value()
    m_dia4 = tela.doubleSpinBox_7.value()
    m_dia5 = tela.doubleSpinBox_8.value()
    m_dia6 = tela.doubleSpinBox_9.value()
    m_dia7 = tela.doubleSpinBox_10.value()
    m_dia8 = tela.doubleSpinBox_11.value()
    m_dia9 = tela.doubleSpinBox_12.value()
    m_dia10 = tela.doubleSpinBox_13.value()
    m_dia11 = tela.doubleSpinBox_14.value()
    m_dia12 = tela.doubleSpinBox_15.value()
    m_dia13 = tela.doubleSpinBox_16.value()
    m_dia14 = tela.doubleSpinBox_17.value()
    m_dia15 = tela.doubleSpinBox_18.value()
    m_dia1 = int(m_dia1)
    m_dia2 = int(m_dia2)
    m_dia3 = int(m_dia3)
    m_dia4 = int(m_dia4)
    m_dia5 = int(m_dia5)
    m_dia6 = int(m_dia6)
    m_dia7 = int(m_dia7)
    m_dia8 = int(m_dia8)
    m_dia9 = int(m_dia9)
    m_dia10 = int(m_dia10)
    m_dia11 = int(m_dia11)
    m_dia12 = int(m_dia12)
    m_dia13 = int(m_dia13)
    m_dia14 = int(m_dia14)
    m_dia15 = int(m_dia15)

    index = tela.comboBox_2.currentIndex()
    mop = tela.comboBox_2.itemText(index)
    m_preco = mop[0]

    index = tela.comboBox.currentIndex()
    mop = tela.comboBox.itemText(index)
    m_pocket = mop[0][0]

    sql = "INSERT INTO sactabpg (codigo, descri, percent, cond, dia1, dia2, dia3, dia4, dia5, dia6, dia7, dia8, " \
          "dia9, dia10, dia11, dia12, dia13, dia14, dia15, comi_tab, pocket, preco, " \
          "sr_deleted) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

    hti_global.conexao_cursor.execute(sql, (m_codigo, m_descri, m_percent, m_cond, m_dia1, m_dia2, m_dia3, m_dia4,
                                            m_dia5, m_dia6, m_dia7, m_dia8, m_dia9, m_dia10, m_dia11, m_dia12, m_dia13,
                                            m_dia14, m_dia15, m_comi_tab, m_pocket, m_preco, ' '))

    hti_global.conexao_bd.commit()
    QMessageBox.information(tela, "Inclusao de CONDICOES DE PAGAMENTOS", "Cadastro feito com SUCESSO!")

    tela.mcodigo.setEnabled(False)
    tela.mdescri.setEnabled(False)
    tela.mcond.setEnabled(False)
    tela.comboBox_2.setEnabled(False)
    tela.comboBox.setEnabled(False)
    tela.doubleSpinBox.setEnabled(False)
    tela.doubleSpinBox_3.setEnabled(False)
    tela.doubleSpinBox_4.setEnabled(False)
    tela.doubleSpinBox_5.setEnabled(False)
    tela.doubleSpinBox_6.setEnabled(False)
    tela.doubleSpinBox_7.setEnabled(False)
    tela.doubleSpinBox_8.setEnabled(False)
    tela.doubleSpinBox_9.setEnabled(False)
    tela.doubleSpinBox_10.setEnabled(False)
    tela.doubleSpinBox_11.setEnabled(False)
    tela.doubleSpinBox_12.setEnabled(False)
    tela.doubleSpinBox_13.setEnabled(False)
    tela.doubleSpinBox_14.setEnabled(False)
    tela.doubleSpinBox_15.setEnabled(False)
    tela.doubleSpinBox_16.setEnabled(False)
    tela.doubleSpinBox_17.setEnabled(False)
    tela.doubleSpinBox_18.setEnabled(False)
    tela.bt_salvar.setEnabled(False)
    tela.bt_retornar.setEnabled(False)
    tela.mcodigo.setText('')
    tela.mdescri.setText('')
    tela.mcond.setText('')
    tela.doubleSpinBox.setValue(0)
    tela.doubleSpinBox_3.setValue(0)
    tela.doubleSpinBox_4.setValue(0)
    tela.doubleSpinBox_5.setValue(0)
    tela.doubleSpinBox_6.setValue(0)
    tela.doubleSpinBox_7.setValue(0)
    tela.doubleSpinBox_8.setValue(0)
    tela.doubleSpinBox_9.setValue(0)
    tela.doubleSpinBox_10.setValue(0)
    tela.doubleSpinBox_11.setValue(0)
    tela.doubleSpinBox_12.setValue(0)
    tela.doubleSpinBox_13.setValue(0)
    tela.doubleSpinBox_14.setValue(0)
    tela.doubleSpinBox_15.setValue(0)
    tela.doubleSpinBox_16.setValue(0)
    tela.doubleSpinBox_17.setValue(0)
    tela.doubleSpinBox_18.setValue(0)
    listar_cond_pag()
    return


def chama_alteracao(mcod_cli):
    m_codigo = tela.mcodigo.text().upper()
    m_descri = tela.mdescri.text().upper()
    m_cond = tela.mcond.text().upper()
    m_cond = ''.join(filter(str.isdigit, m_cond))
    m_percent = tela.doubleSpinBox.value()
    m_comi_tab = tela.doubleSpinBox_3.value()
    m_dia1 = tela.doubleSpinBox_4.value()
    m_dia2 = tela.doubleSpinBox_5.value()
    m_dia3 = tela.doubleSpinBox_6.value()
    m_dia4 = tela.doubleSpinBox_7.value()
    m_dia5 = tela.doubleSpinBox_8.value()
    m_dia6 = tela.doubleSpinBox_9.value()
    m_dia7 = tela.doubleSpinBox_10.value()
    m_dia8 = tela.doubleSpinBox_11.value()
    m_dia9 = tela.doubleSpinBox_12.value()
    m_dia10 = tela.doubleSpinBox_13.value()
    m_dia11 = tela.doubleSpinBox_14.value()
    m_dia12 = tela.doubleSpinBox_15.value()
    m_dia13 = tela.doubleSpinBox_16.value()
    m_dia14 = tela.doubleSpinBox_17.value()
    m_dia15 = tela.doubleSpinBox_18.value()
    m_dia1 = int(m_dia1)
    m_dia2 = int(m_dia2)
    m_dia3 = int(m_dia3)
    m_dia4 = int(m_dia4)
    m_dia5 = int(m_dia5)
    m_dia6 = int(m_dia6)
    m_dia7 = int(m_dia7)
    m_dia8 = int(m_dia8)
    m_dia9 = int(m_dia9)
    m_dia10 = int(m_dia10)
    m_dia11 = int(m_dia11)
    m_dia12 = int(m_dia12)
    m_dia13 = int(m_dia13)
    m_dia14 = int(m_dia14)
    m_dia15 = int(m_dia15)

    index = tela.comboBox_2.currentIndex()
    mop = tela.comboBox_2.itemText(index)
    m_preco = mop[0]

    index = tela.comboBox.currentIndex()
    mop = tela.comboBox.itemText(index)
    m_pocket = mop[0][0]
    print('ok')

    sql = f"UPDATE sactabpg SET descri = ?, percent = ?, cond = ?, dia1 = ?, dia2 = ?, dia3 = ?, dia4 = ?, " \
          f"dia5 = ?, dia6 = ?, dia7 = ?, dia8 = ?, dia9 = ?, dia10 = ?, dia11 = ?, dia12 = ?, dia13 = ?, dia14 = ?, " \
          f"dia15 = ?, comi_tab = ?, pocket = ?, preco = ? WHERE codigo = ?"

    hti_global.conexao_cursor.execute(sql, (m_descri, m_percent, m_cond, m_dia1, m_dia2, m_dia3, m_dia4,
                                            m_dia5, m_dia6, m_dia7, m_dia8, m_dia9, m_dia10, m_dia11, m_dia12, m_dia13,
                                            m_dia14, m_dia15, m_comi_tab, m_pocket, m_preco, m_codigo))

    hti_global.conexao_bd.commit()
    QMessageBox.information(tela, "ALTERACAO de CONDICOES DE PAGAMENTOS", "Alteracao feito com SUCESSO!")

    tela.mcodigo.setEnabled(False)
    tela.mdescri.setEnabled(False)
    tela.mcond.setEnabled(False)
    tela.comboBox_2.setEnabled(False)
    tela.comboBox.setEnabled(False)
    tela.doubleSpinBox.setEnabled(False)
    tela.doubleSpinBox_3.setEnabled(False)
    tela.doubleSpinBox_4.setEnabled(False)
    tela.doubleSpinBox_5.setEnabled(False)
    tela.doubleSpinBox_6.setEnabled(False)
    tela.doubleSpinBox_7.setEnabled(False)
    tela.doubleSpinBox_8.setEnabled(False)
    tela.doubleSpinBox_9.setEnabled(False)
    tela.doubleSpinBox_10.setEnabled(False)
    tela.doubleSpinBox_11.setEnabled(False)
    tela.doubleSpinBox_12.setEnabled(False)
    tela.doubleSpinBox_13.setEnabled(False)
    tela.doubleSpinBox_14.setEnabled(False)
    tela.doubleSpinBox_15.setEnabled(False)
    tela.doubleSpinBox_16.setEnabled(False)
    tela.doubleSpinBox_17.setEnabled(False)
    tela.doubleSpinBox_18.setEnabled(False)
    tela.bt_salvar.setEnabled(False)
    tela.bt_retornar.setEnabled(False)
    tela.mcodigo.setText('')
    tela.mdescri.setText('')
    tela.mcond.setText('')
    tela.doubleSpinBox.setValue(0)
    tela.doubleSpinBox_3.setValue(0)
    tela.doubleSpinBox_4.setValue(0)
    tela.doubleSpinBox_5.setValue(0)
    tela.doubleSpinBox_6.setValue(0)
    tela.doubleSpinBox_7.setValue(0)
    tela.doubleSpinBox_8.setValue(0)
    tela.doubleSpinBox_9.setValue(0)
    tela.doubleSpinBox_10.setValue(0)
    tela.doubleSpinBox_11.setValue(0)
    tela.doubleSpinBox_12.setValue(0)
    tela.doubleSpinBox_13.setValue(0)
    tela.doubleSpinBox_14.setValue(0)
    tela.doubleSpinBox_15.setValue(0)
    tela.doubleSpinBox_16.setValue(0)
    tela.doubleSpinBox_17.setValue(0)
    tela.doubleSpinBox_18.setValue(0)
    listar_cond_pag()
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
    codigo = str(tabela.item(row, 0).text())
    hti_global.conexao_cursor.execute(f"SELECT dia1, dia2, dia3, dia4, dia5, dia6, dia7, dia8, dia9, dia10, dia11, "
                                      f"dia12, dia13, dia14, dia15 "
                                      f"FROM sactabpg WHERE codigo = {codigo}")
    # hti_global.conexao_cursor.execute(f"SELECT * FROM sactabpg WHERE codigo = {codigo}")
    ver_dias = hti_global.conexao_cursor.fetchone()
    hti_global.conexao_bd.commit()
    descri = tabela.item(row, 1).text()
    cond = tabela.item(row, 3).text()
    percent = tabela.item(row, 2).text()
    comi_tab = tabela.item(row, 4).text()
    preco = tabela.item(row, 5).text()
    pocket = tabela.item(row, 7).text()
    tela.doubleSpinBox_4.setValue(float(ver_dias[0]))
    tela.doubleSpinBox_5.setValue(float(ver_dias[1]))
    tela.doubleSpinBox_6.setValue(float(ver_dias[2]))
    tela.doubleSpinBox_7.setValue(float(ver_dias[3]))
    tela.doubleSpinBox_8.setValue(float(ver_dias[4]))
    tela.doubleSpinBox_9.setValue(float(ver_dias[5]))
    tela.doubleSpinBox_10.setValue(float(ver_dias[6]))
    tela.doubleSpinBox_11.setValue(float(ver_dias[7]))
    tela.doubleSpinBox_12.setValue(float(ver_dias[8]))
    tela.doubleSpinBox_13.setValue(float(ver_dias[9]))
    tela.doubleSpinBox_14.setValue(float(ver_dias[10]))
    tela.doubleSpinBox_15.setValue(float(ver_dias[11]))
    tela.doubleSpinBox_16.setValue(float(ver_dias[12]))
    tela.doubleSpinBox_17.setValue(float(ver_dias[13]))
    tela.doubleSpinBox_18.setValue(float(ver_dias[14]))
    tabela.itemDoubleClicked.disconnect()
    if tela.rb_alteracao.isChecked():
        tela.mcodigo.setText(codigo)
        tela.mdescri.setText(str(descri))
        tela.mcond.setText(str(cond))
        tela.doubleSpinBox.setValue(float(percent))
        tela.doubleSpinBox_3.setValue(float(comi_tab))

        for i in range(tela.comboBox_2.count()):
            item_text = tela.comboBox_2.itemText(i)
            if str(preco).strip() in item_text:
                tela.comboBox_2.setCurrentIndex(i)
                break

        for i in range(tela.comboBox.count()):
            item_text = tela.comboBox.itemText(i)
            if str(pocket).strip() in item_text:
                tela.comboBox.setCurrentIndex(i)
                break

        tela.bt_salvar.clicked.connect(chama_alteracao)
        tela.bt_retornar.clicked.connect(listar_cond_pag)
        tela.mdescri.setEnabled(True)
        tela.doubleSpinBox.setEnabled(True)
        tela.mcond.setEnabled(True)
        tela.doubleSpinBox_3.setEnabled(True)
        tela.comboBox_2.setEnabled(True)
        tela.doubleSpinBox_4.setEnabled(True)
        tela.doubleSpinBox_5.setEnabled(True)
        tela.doubleSpinBox_6.setEnabled(True)
        tela.doubleSpinBox_7.setEnabled(True)
        tela.doubleSpinBox_8.setEnabled(True)
        tela.doubleSpinBox_9.setEnabled(True)
        tela.doubleSpinBox_10.setEnabled(True)
        tela.doubleSpinBox_11.setEnabled(True)
        tela.doubleSpinBox_12.setEnabled(True)
        tela.doubleSpinBox_13.setEnabled(True)
        tela.doubleSpinBox_14.setEnabled(True)
        tela.doubleSpinBox_15.setEnabled(True)
        tela.doubleSpinBox_16.setEnabled(True)
        tela.doubleSpinBox_17.setEnabled(True)
        tela.doubleSpinBox_18.setEnabled(True)
        tela.comboBox.setEnabled(True)
        tela.bt_salvar.setEnabled(True)
        tela.bt_retornar.setEnabled(True)
        tela.mdescri.setFocus()
    else:
        # chama_consulta(item.text())
        pass

    tabela.itemDoubleClicked.connect(lambda items: editar_item(items.row()))
    return


def habilitar_objeto():
    hti_global.conexao_cursor.execute(f"SELECT max(codigo) FROM sactabpg")
    arq_cond_pag = hti_global.conexao_cursor.fetchone()
    if arq_cond_pag is None:
        codigo = 1
        tela.mcodigo.setText(str(codigo).zfill(3))
    else:
        codigo = int(arq_cond_pag[0]) + 1
        tela.mcodigo.setText(str(codigo).zfill(3))

    # hti_global.conexao_bd.commit()

    tela.bt_salvar.clicked.connect(f_incl_cond_pag)
    tela.bt_retornar.clicked.connect(listar_cond_pag)
    tela.mdescri.setEnabled(True)
    tela.doubleSpinBox.setEnabled(True)
    tela.mcond.setEnabled(True)
    tela.doubleSpinBox_3.setEnabled(True)
    tela.comboBox_2.setEnabled(True)
    tela.doubleSpinBox_4.setEnabled(True)
    tela.doubleSpinBox_5.setEnabled(True)
    tela.doubleSpinBox_6.setEnabled(True)
    tela.doubleSpinBox_7.setEnabled(True)
    tela.doubleSpinBox_8.setEnabled(True)
    tela.doubleSpinBox_9.setEnabled(True)
    tela.doubleSpinBox_10.setEnabled(True)
    tela.doubleSpinBox_11.setEnabled(True)
    tela.doubleSpinBox_12.setEnabled(True)
    tela.doubleSpinBox_13.setEnabled(True)
    tela.doubleSpinBox_14.setEnabled(True)
    tela.doubleSpinBox_15.setEnabled(True)
    tela.doubleSpinBox_16.setEnabled(True)
    tela.doubleSpinBox_17.setEnabled(True)
    tela.doubleSpinBox_18.setEnabled(True)
    tela.comboBox.setEnabled(True)
    tela.bt_salvar.setEnabled(True)
    tela.bt_retornar.setEnabled(True)
    tela.mdescri.setFocus()


def listar_cond_pag():
    hti_global.conexao_cursor.execute(f"SELECT codigo, descri, percent, cond, comi_tab, preco, dia1 || ' - ' || "
                                      f"dia2 || ' - ' || dia3 || ' - ' || dia4 || ' - ' || dia5 || ' - ' || "
                                      f"dia6 || ' - ' || dia7 || ' - ' || dia8 || ' - ' || dia9 || ' - ' || "
                                      f"dia10 || ' - ' || dia11 || ' - ' || dia12 || ' - ' || dia13 || ' - ' || "
                                      f"dia14 || ' - ' || dia15, iif(pocket = 'S', 'Sim', 'Nao')  "
                                      f"FROM sactabpg order BY codigo")

    dados_lidos = hti_global.conexao_cursor.fetchall()
    hti_global.conexao_bd.commit()
    tabela.setRowCount(len(dados_lidos))
    tabela.setColumnCount(8)
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

    tela.mcodigo.setEnabled(False)
    tela.mdescri.setEnabled(False)
    tela.doubleSpinBox.setEnabled(False)
    tela.mcond.setEnabled(False)
    tela.doubleSpinBox_3.setEnabled(False)
    tela.comboBox_2.setEnabled(False)
    tela.doubleSpinBox_4.setEnabled(False)
    tela.doubleSpinBox_5.setEnabled(False)
    tela.doubleSpinBox_6.setEnabled(False)
    tela.doubleSpinBox_7.setEnabled(False)
    tela.doubleSpinBox_8.setEnabled(False)
    tela.doubleSpinBox_9.setEnabled(False)
    tela.doubleSpinBox_10.setEnabled(False)
    tela.doubleSpinBox_11.setEnabled(False)
    tela.doubleSpinBox_12.setEnabled(False)
    tela.doubleSpinBox_13.setEnabled(False)
    tela.doubleSpinBox_14.setEnabled(False)
    tela.doubleSpinBox_15.setEnabled(False)
    tela.doubleSpinBox_16.setEnabled(False)
    tela.doubleSpinBox_17.setEnabled(False)
    tela.doubleSpinBox_18.setEnabled(False)
    tela.comboBox.setEnabled(False)
    tela.bt_salvar.setEnabled(False)
    tela.bt_cancelar.setEnabled(False)

    tela.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
    tela.tableWidget.itemDoubleClicked.connect(lambda items: editar_item(items.row()))

    tela.bt_inclusao.clicked.connect(habilitar_objeto)
    tela.bt_sair.clicked.connect(fecha_tela)
    tela.bt_sair.setIcon(icon_sair)
    tela.bt_salvar.setIcon(icon_salvar)
    tela.bt_inclusao.setIcon(icon_incluir)
    tela.bt_cancelar.setIcon(icon_cancelar)

    tela.show()
    app.exec()


tela.tableWidget.itemDoubleClicked.connect(lambda items: editar_item(items.row()))

if __name__ == '__main__':
    from hti_funcoes import conexao_banco
    conexao_banco()
    listar_cond_pag()
    hti_global.conexao_bd.close()
