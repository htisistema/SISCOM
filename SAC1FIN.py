# FINANCIAMENTO

from PyQt6 import uic, QtWidgets, QtCore
from PyQt6.QtGui import QIcon, QGuiApplication
from PyQt6.QtWidgets import QButtonGroup, QMessageBox, QTableWidgetItem, QTableWidget, QStatusBar, QAbstractItemView
import os
import hti_global

app = QtWidgets.QApplication([])
app.setStyleSheet(hti_global.style_sheet)
tela = uic.loadUi(f"{hti_global.c_ui}\\lista_financiamento.ui")
tela.setWindowTitle('FINANCIAMENTO CADASTRADO')
icon = QIcon(f"{hti_global.c_imagem}\\htiico.jpg")
icon_cancelar = QIcon(f"{hti_global.c_imagem}\\cancelar.png")
icon_sair = QIcon(f"{hti_global.c_imagem}\\sair.png")
icon_incluir = QIcon(f"{hti_global.c_imagem}\\incluir.png")
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


def on_close_event(event):
    # Esta função será chamada quando o usuário clicar no botão de fechar a janela
    # print("Fechando a janela...")
    tela.close()
    event.accept()


tela.closeEvent = on_close_event


def fecha_tela():
    tela.close()


# Define a função para ajustar as colunas da tabela
def ajustar_colunas_tabela(tabela):
    header = tabela.horizontalHeader()
    header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
    header.setStretchLastSection(False)


def f_incl_financiamento():
    from SAC1FIN1 import inclusao_financiamento
    inclusao_financiamento()
    tela.close()
    return


def f_incl_aliquota():
    from SAC2FIN import listar_aliquota
    listar_aliquota()
    return


def chama_alteracao(mcod_cli):
    # from alt_grupo import alteracao_grupo
    # alteracao_grupo(mcod_cli[0:5])
    pass
    return


def chama_consulta(mcod_cli):
    # from cons_grupo import consulta_grupo
    # consulta_grupo(mcod_cli[0:5])
    # print(mcod_cli)
    pass
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
    rb_tipo_consulta = None
    item = tela.tableWidget.item(row, 0)
    if item.isSelected():
        tela.tableWidget.itemDoubleClicked.disconnect()
        # print("Duplo clique!")
    else:
        tela.tableWidget.itemDoubleClicked.disconnect()
        # print("Clique simples.")

    # print(item.text())
    if tela.rb_alteracao.isChecked():
        rb_tipo_consulta = 'A'
    elif tela.rb_consulta.isChecked():
        rb_tipo_consulta = 'C'

    if rb_tipo_consulta == 'A':
        # chama_alteracao(item.text())
        pass
    else:
        # chama_consulta(item.text())
        pass

    tela.tableWidget.itemDoubleClicked.connect(lambda item: editar_item(item.row()))
    return


def chama_arquivo():
    hti_global.conexao_cursor.execute(f"SELECT CAST(cod_fin as char(5)), CAST(desc_fin as char(25)), "
                                      f"REPLACE(CAST(taxa_fin AS DECIMAL(18,2)), '.', ','), "
                                      f"REPLACE(CAST(taxa_adm AS DECIMAL(18,2)), '.', ','), "
                                      f"iif(cobra_fin = 'S','Sim','Nao')  "
                                      f"FROM sacfin GROUP BY cod_fin, desc_fin,taxa_fin, taxa_adm, cobra_fin "
                                      f"ORDER BY cod_fin ")


def listar_financiamento():
    chama_arquivo()
    dados_lidos = hti_global.conexao_cursor.fetchall()
    hti_global.conexao_bd.commit()
    tela.tableWidget.setRowCount(len(dados_lidos))
    tela.tableWidget.setColumnCount(5)
    for i, linha in enumerate(dados_lidos):
        for j, valor in enumerate(linha):
            valor = str(valor) if valor is not None else ""
            item = QtWidgets.QTableWidgetItem(valor)
            tela.tableWidget.setItem(i, j, item)
            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
            # print(item.text())
    ajustar_colunas_tabela(tela.tableWidget)

    QtWidgets.QApplication.processEvents()

    rb_tipo_group = QButtonGroup()
    rb_tipo_group.addButton(tela.rb_alteracao, id=1)
    tela.rb_alteracao.setChecked(True)

    tela.incl_aliquota.clicked.connect(f_incl_aliquota)
    tela.bt_inclusao.clicked.connect(f_incl_financiamento)

    tela.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
    tela.tableWidget.itemDoubleClicked.connect(lambda items: editar_item(items.row()))
    tela.bt_sair.clicked.connect(fecha_tela)
    tela.bt_sair.setIcon(icon_sair)
    tela.bt_inclusao.setIcon(icon_incluir)
    tela.incl_aliquota.setIcon(icon_incluir)

    tela.show()
    app.exec()


if __name__ == '__main__':
    from hti_funcoes import conexao_banco
    conexao_banco()
    listar_financiamento()
    hti_global.conexao_bd.close()
