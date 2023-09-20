# LISTA DE FORNECEDORES

from PyQt6 import uic, QtWidgets
from PyQt6.QtGui import QIcon
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtWidgets import QButtonGroup
import hti_global
import os

app = QtWidgets.QApplication([])
app.setStyleSheet(hti_global.style_sheet)
tela = uic.loadUi(f"{hti_global.c_ui}\\lista_fornecedor.ui")
tela.setWindowTitle('FORNECEDOR CADASTRADO')
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

# PEGA O NOME DO ARQUIVO EM EXECUCAO
nome_file_com = os.path.basename(__file__)
nome_file, ext = os.path.splitext(nome_file_com)

tela.statusBar.showMessage(f"<< {nome_file} >>")
nome_arquivo = os.path.basename(__file__)


def fecha_tela():
    tela.close()
    tela.closeEvent = on_close_event
    return


def on_close_event(event):
    tela.close()
    event.accept()


tela.closeEvent = on_close_event


# Define a função para ajustar as colunas da tabela
def ajustar_colunas_tabela(tabela):
    header = tabela.horizontalHeader()
    header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
    header.setStretchLastSection(False)


def f_incl_fornecedor():
    from SAC140 import sac140
    sac140()
    # inclusao_fornecedor()
    return


def chama_alteracao(mcod_forn):
    from SAC141 import alteracao_fornecedor
    alteracao_fornecedor(mcod_forn[0:4])
    return


def chama_consulta(mcod_forn):
    from SAC43 import consulta_fornecedor
    consulta_fornecedor(mcod_forn[0:4])
    # print(mcod_forn)
    return


def botao_item():
    selected_item = tela.tableWidget.currentItem()
    if selected_item is not None:
        codigo_fornecedor = selected_item.text()
        chama_alteracao(codigo_fornecedor)
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
        chama_alteracao(item.text())
    else:
        chama_consulta(item.text())

    tela.tableWidget.itemDoubleClicked.connect(lambda item: editar_item(item.row()))
    return


def pesquisa():
    nome_buscar = tela.pesquisa.text()
    hti_global.conexao_cursor.execute(f"SELECT CAST(cod_forn as char(5)) as cod_forn,"
                                      f"COALESCE(razao, ' ') as razao,"
                                      f"COALESCE(fantasia, ' ') as fantasia,"
                                      f"COALESCE(forn_desp, ' '), "
                                      f"COALESCE(cgc, ' ') as cgc,"
                                      f"COALESCE(cpf, ' ') as cpf, "
                                      f"tel1, "
                                      f"cidade,"
                                      f"uf, REPLACE(CAST(limite AS DECIMAL(18,2)), '.', ',') as limite_formatado, "
                                      f"obs "
                                      f"FROM sacforn WHERE (fantasia LIKE UPPER('%{nome_buscar}%') OR "
                                      f"razao LIKE UPPER('%{nome_buscar}%') OR cod_forn LIKE UPPER('%{nome_buscar}%') "
                                      f"OR tel1 LIKE UPPER('%{nome_buscar}%')) ORDER BY razao")


def listar_fornecedor():
    pesquisa()
    dados_lidos = hti_global.conexao_cursor.fetchall()
    # hti_global.conexao_bd.commit()
    tela.tableWidget.setRowCount(len(dados_lidos))
    tela.tableWidget.setColumnCount(10)
    for i, linha in enumerate(dados_lidos):
        for j, valor in enumerate(linha):
            valor = str(valor) if valor is not None else ""
            item = QtWidgets.QTableWidgetItem(valor)
            tela.tableWidget.setItem(i, j, item)
            # print(item.text())
    ajustar_colunas_tabela(tela.tableWidget)

    rb_tipo_group = QButtonGroup()
    rb_tipo_group.addButton(tela.rb_alteracao, id=1)
    rb_tipo_group.addButton(tela.rb_consulta, id=2)
    tela.rb_alteracao.setChecked(True)

    tela.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
    tela.tableWidget.itemDoubleClicked.connect(lambda item: editar_item(item.row()))
    tela.bt_sair.clicked.connect(fecha_tela)
    tela.bt_sair.setIcon(icon_sair)
    tela.bt_inclusao.setIcon(icon_incluir)

    tela.show()
    app.exec()


tela.bt_inclusao.clicked.connect(f_incl_fornecedor)
# tela.consulta_fornecedor.clicked.connect(botao_item)
tela.pesquisa.textChanged.connect(listar_fornecedor)
tela.tableWidget.itemDoubleClicked.connect(lambda item: editar_item(item.row()))

if __name__ == '__main__':
    from hti_funcoes import conexao_banco
    conexao_banco()
    listar_fornecedor()
    hti_global.conexao_bd.close()
