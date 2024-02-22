# CARTOES

from PyQt6 import uic, QtWidgets
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QButtonGroup, QMessageBox, QAbstractItemView, QTableWidgetItem
import os
import hti_global as hg

app = QtWidgets.QApplication([])
app.setStyleSheet(hg.style_sheet)
tela = uic.loadUi(f"{hg.c_ui}\\lista_cartao.ui")
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

# PEGA O NOME DO ARQUIVO EM EXECUCAO
nome_file_com = os.path.basename(__file__)
nome_file, ext = os.path.splitext(nome_file_com)

tela.statusBar.showMessage(f"<< {nome_file} >>")
tabela = tela.tableWidget

hg.conexao_cursor.execute(f"SELECT cod_forn, razao FROM sacforn WHERE not forn_desp = 'F'")
arq_forn = hg.conexao_cursor.fetchall()
hg.conexao_bd.commit()

item = f'0000 - DEFAULT'.strip('(),')
tela.comboBox_2.addItem(item)
for ret_forn in arq_forn:
    item = f'{ret_forn[0]} - {ret_forn[1]}'.strip('(),')
    tela.comboBox_2.addItem(item)
tela.comboBox_2.setCurrentIndex(0)

hg.conexao_cursor.execute(f"SELECT codigo,desc1 FROM sacdesp")
arq_desp = hg.conexao_cursor.fetchall()
hg.conexao_bd.commit()

item = f'0000 - DEFAULT'.strip('(),')
tela.comboBox.addItem(item)
for ret_desp in arq_desp:
    item = f'{ret_desp[0]} - {ret_desp[1]}'.strip('(),')
    tela.comboBox.addItem(item)
tela.comboBox.setCurrentIndex(0)

tela.comboBox_3.addItems(["Avista", "Prazo"])
tela.comboBox_3.setCurrentIndex(0)  # coloca o focus no index

tela.comboBox_4.addItems(["Sim", "Nao"])
tela.comboBox_4.setCurrentIndex(0)  # coloca o focus no index


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


def f_incl_cartao():
    m_codigo = tela.mcodigo.text().upper()
    m_cartao = tela.mcartao.text().upper()
    m_sigla = tela.msigla.text().upper()
    m_prazo = tela.doubleSpinBox_2.value()
    m_desconto = tela.doubleSpinBox.value()
    index = tela.comboBox_2.currentIndex()
    mop = tela.comboBox_2.itemText(index)
    m_cod_forn = mop[0]

    index = tela.comboBox.currentIndex()
    mop = tela.comboBox.itemText(index)
    m_tipo_conta = mop[0]

    index = tela.comboBox_3.currentIndex()
    mop = tela.comboBox_3.itemText(index)
    m_tipo_venda = mop[0][0]

    index = tela.comboBox_4.currentIndex()
    mop = tela.comboBox_4.itemText(index)
    m_tef = mop[0][0]

    sql = "INSERT INTO saccarta (codigo, cartao, sigla, prazo, desconto, cod_forn, tipo_conta, tipo_venda, tef, " \
          "sr_deleted) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) "
    hg.conexao_cursor.execute(sql, (m_codigo, m_cartao, m_sigla, m_prazo, m_desconto, m_cod_forn, m_tipo_conta,
                                            m_tipo_venda, m_tef, ' '))

    hg.conexao_bd.commit()
    QMessageBox.information(tela, "Inclusao de TIPO DE DOCUMENTO", "Cadastro feito com SUCESSO!")

    tela.mcodigo.setEnabled(False)
    tela.mcartao.setEnabled(False)
    tela.msigla.setEnabled(False)
    tela.doubleSpinBox_2.setEnabled(False)
    tela.doubleSpinBox.setEnabled(False)
    tela.comboBox_2.setEnabled(False)
    tela.comboBox.setEnabled(False)
    tela.comboBox_3.setEnabled(False)
    tela.comboBox_4.setEnabled(False)
    tela.bt_salvar.setEnabled(False)
    tela.mcodigo.setText('')
    tela.mcartao.setText('')
    tela.msigla.setText('')
    tela.doubleSpinBox.setValue(0)
    tela.doubleSpinBox_2.setValue(0)
    tela.doubleSpinBox_3.setValue(0)
    tela.doubleSpinBox_4.setValue(0)
    listar_cartao()
    return


def chama_alteracao(mcod_cli):
    m_codigo = tela.mcodigo.text().upper()
    m_cartao = tela.mcartao.text().upper()
    m_sigla = tela.msigla.text().upper()
    m_prazo = tela.doubleSpinBox_2.value()
    m_desconto = tela.doubleSpinBox.value()

    index = tela.comboBox_2.currentIndex()
    mop = tela.comboBox_2.itemText(index)
    m_cod_forn = mop[0]

    index = tela.comboBox.currentIndex()
    mop = tela.comboBox.itemText(index)
    m_tipo_conta = mop[0]

    index = tela.comboBox_3.currentIndex()
    mop = tela.comboBox_3.itemText(index)
    m_tipo_venda = mop[0][0]

    index = tela.comboBox_4.currentIndex()
    mop = tela.comboBox_4.itemText(index)
    m_tef = mop[0][0]
    sql = "UPDATE saccarta SET (cartao = ?, sigla = ?, prazo = ?, desconto = ?, cod_forn = ?" \
          ", tipo_conta = ?, tipo_venda = ?, tef = ? WHERE tipo_doc = ?"

    hg.conexao_cursor.execute(sql, (m_cartao, m_sigla, m_prazo, m_desconto, m_cod_forn, m_tipo_conta,
                                            m_tipo_venda, m_tef, m_codigo))

    hg.conexao_bd.commit()
    QMessageBox.information(tela, "ALTERACAO de CARTAO", "ALTERACAO feita com SUCESSO!")

    tela.mcodigo.setEnabled(False)
    tela.mcartao.setEnabled(False)
    tela.msigla.setEnabled(False)
    tela.doubleSpinBox_2.setEnabled(False)
    tela.doubleSpinBox.setEnabled(False)
    tela.comboBox_2.setEnabled(False)
    tela.comboBox.setEnabled(False)
    tela.comboBox_3.setEnabled(False)
    tela.comboBox_4.setEnabled(False)
    tela.bt_salvar.setEnabled(False)
    tela.mcodigo.setText('')
    tela.mcartao.setText('')
    tela.msigla.setText('')
    tela.doubleSpinBox.setValue(0)
    tela.doubleSpinBox_2.setValue(0)
    tela.doubleSpinBox_3.setValue(0)
    tela.doubleSpinBox_4.setValue(0)
    listar_cartao()
    return


def editar_item(row):
    codigo = tabela.item(row, 0).text()
    cartao = tabela.item(row, 1).text()
    sigla = tabela.item(row, 2).text()
    prazo = tabela.item(row, 3).text()
    desconto = tabela.item(row, 4).text()
    cod_forn = tabela.item(row, 5).text()
    tipo_conta = tabela.item(row, 6).text()
    tipo_venda = tabela.item(row, 7).text()
    tipo_venda = tipo_venda[1]
    tef = tabela.item(row, 8).text()
    tabela.itemDoubleClicked.disconnect()

    if tela.rb_alteracao.isChecked():
        tela.mcodigo.setText(codigo)
        tela.mcartao.setText(str(cartao))
        tela.msigla.setText(str(sigla))
        tela.doubleSpinBox_2.setValue(float(prazo))
        tela.doubleSpinBox.setValue(float(desconto))

        for i in range(tela.comboBox_2.count()):
            item_text = tela.comboBox_2.itemText(i)
            if str(cod_forn).strip() in item_text:
                tela.comboBox_2.setCurrentIndex(i)
                break

        for i in range(tela.comboBox.count()):
            item_text = tela.comboBox.itemText(i)
            if str(tipo_conta).strip() in item_text:
                tela.comboBox.setCurrentIndex(i)
                break

        for i in range(tela.comboBox_3.count()):
            item_text = tela.comboBox_3.itemText(i)
            if str(tipo_venda).strip() in item_text:
                tela.comboBox_3.setCurrentIndex(i)
                break

        for i in range(tela.comboBox_4.count()):
            item_text = tela.comboBox_4.itemText(i)
            if str(tef).strip() in item_text:
                tela.comboBox_4.setCurrentIndex(i)
                break

        tela.bt_salvar.clicked.connect(chama_alteracao)
        tela.bt_retornar.clicked.connect(listar_cartao)
        tela.mcartao.setEnabled(True)
        tela.msigla.setEnabled(True)
        tela.doubleSpinBox_2.setEnabled(True)
        tela.doubleSpinBox.setEnabled(True)
        tela.comboBox_2.setEnabled(True)
        tela.comboBox.setEnabled(True)
        tela.comboBox_3.setEnabled(True)
        tela.comboBox_4.setEnabled(True)
        tela.bt_salvar.setEnabled(True)
        tela.bt_retornar.setEnabled(True)
        tela.mcartao.setFocus()
    else:
        # chama_consulta(item.text())
        pass

    tabela.itemDoubleClicked.connect(lambda items: editar_item(items.row()))
    return


# def pesquisa():
def habilitar_objeto():
    tela.mcodigo.setEnabled(True)
    hg.conexao_cursor.execute(f"SELECT max(codigo) FROM saccarta")
    arq_cartao = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()
    codigo = int(arq_cartao[0]) + 1
    tela.mcodigo.setText(str(codigo).zfill(3))
    tela.msigla.setText('CT')
    tela.bt_salvar.clicked.connect(f_incl_cartao)
    tela.bt_cancelar.clicked.connect(listar_cartao)

    tela.mcartao.setEnabled(True)
    tela.msigla.setEnabled(True)
    tela.doubleSpinBox_2.setEnabled(True)
    tela.doubleSpinBox.setEnabled(True)
    tela.comboBox_2.setEnabled(True)
    tela.comboBox.setEnabled(True)
    tela.comboBox_3.setEnabled(True)
    tela.comboBox_4.setEnabled(True)
    tela.bt_salvar.setEnabled(True)
    tela.bt_cancelar.setEnabled(True)
    tela.mcartao.setFocus()


def listar_cartao():
    hg.conexao_cursor.execute(f"SELECT CAST(codigo as char(3)), "
                                      f"CAST(cartao as char(20)), "
                                      f"CAST(sigla as char(2)), "
                                      f"prazo, "
                                      f"desconto, "
                                      f"CAST(cod_forn as char(4)), "
                                      f"CAST(tipo_conta as char(4)), "
                                      f"iif(tipo_venda = 'A','AVISTA','APRAZO'), "
                                      f"iif(tef = 'S','Sim','Nao') "
                                      f" FROM saccarta ORDER BY codigo")

    dados_lidos = hg.conexao_cursor.fetchall()
    hg.conexao_bd.commit()
    tabela.setRowCount(len(dados_lidos))
    tabela.setColumnCount(9)
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
    tela.mcartao.setEnabled(False)
    tela.msigla.setEnabled(False)
    tela.doubleSpinBox_2.setEnabled(False)
    tela.doubleSpinBox.setEnabled(False)
    tela.comboBox_2.setEnabled(False)
    tela.comboBox.setEnabled(False)
    tela.comboBox_3.setEnabled(False)
    tela.comboBox_4.setEnabled(False)
    tela.bt_salvar.setEnabled(False)
    tela.bt_cancelar.setEnabled(False)

    tabela.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
    tabela.itemDoubleClicked.connect(lambda items: editar_item(items.row()))
    tela.bt_inclusao.clicked.connect(habilitar_objeto)
    tela.bt_sair.clicked.connect(fecha_tela)
    tela.bt_sair.setIcon(icon_sair)
    tela.bt_salvar.setIcon(icon_salvar)
    tela.bt_inclusao.setIcon(icon_incluir)
    tela.bt_cancelar.setIcon(icon_cancelar)

    tela.show()


tela.tableWidget.itemDoubleClicked.connect(lambda items: editar_item(items.row()))


if __name__ == '__main__':
    from hti_funcoes import conexao_banco
    conexao_banco()
    listar_cartao()
    app.exec()
    hg.conexao_bd.close()
