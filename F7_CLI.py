# LISTA DE CLIENTES

from PyQt6 import uic, QtWidgets
from PyQt6.QtGui import QIcon, QGuiApplication, QPixmap
from PyQt6.QtWidgets import QButtonGroup
import os
import hti_global as hg

app = QtWidgets.QApplication([])
app.setStyleSheet(hg.style_sheet)
tela = uic.loadUi(f"{hg.c_ui}\\f7_cli.ui")
tela.setWindowTitle('CLIENTES CADASTRADO')
icon = QIcon(f"{hg.c_imagem}\\htiico.ico")
icon_cancelar = QIcon(f"{hg.c_imagem}\\cancelar.png")
icon_sair = QIcon(f"{hg.c_imagem}\\sair.png")
icon_salvar = QIcon(f"{hg.c_imagem}\\salvar.png")
icon_incluir = QIcon(f"{hg.c_imagem}\\incluir.png")
tela.setWindowIcon(icon)
# Centraliza a janela na tela
# AJUSTAR A TELA EM RELACAO AO MONITOR
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
if os.path.exists(f"{hg.c_imagem}\\htifirma.jpg"):
    imagem = QPixmap(f"{hg.c_imagem}\\htifirma.jpg")
else:
    imagem = QPixmap(f"{hg.c_imagem}\\htifirma1.jpg")

pixmap_redimensionado = imagem.scaled(350, 50)  # redimensiona a imagem para 100x100
tela.empresa.setPixmap(pixmap_redimensionado)

# tela.comboBox.addItems(["Geral", "Razao", "Fantasia", "Cidade"])
# tela.comboBox.setCurrentIndex(0)  # coloca o focus no index


def on_close_event(event):
    tela.close()
    event.accept()


tela.closeEvent = on_close_event


def fecha_tela():
    tela.close()
    tela.closeEvent = on_close_event
    return


# Define a função para ajustar as colunas da tabela
def ajustar_colunas_tabela(tabela):
    header = tabela.horizontalHeader()
    header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
    header.setStretchLastSection(False)


def f_incl_cliente():
    from SAC130 import inclusao_cliente
    inclusao_cliente()
    return


def chama_alteracao(mcod_cli):
    from SAC131 import alteracao_cliente
    alteracao_cliente(mcod_cli[0:5])
    return


def chama_consulta(mcod_cli):
    from SAC42 import consulta_cliente
    consulta_cliente(mcod_cli[0:5])
    # print(mcod_cli)
    return


def botao_item():
    selected_item = tela.tableWidget.currentItem()
    if selected_item is not None:
        codigo_cliente = selected_item.text()
        chama_alteracao(codigo_cliente)
        return
    else:
        return


def editar_item(row):
    item = tela.tableWidget.item(row, 0)
    tela.tableWidget.itemDoubleClicked.disconnect()
    # print(item.text())
    if tela.rb_alteracao.isChecked():
        chama_alteracao(item.text())
    else:
        chama_consulta(item.text())

    tela.tableWidget.itemDoubleClicked.connect(lambda item: editar_item(item.row()))
    return


# def editar_item(row):
#     item = tela.tableWidget.item(row, 0)
#     # print(item.text())
#     chama_alteracao(item.text())
#     return

# hg.conexao_cursor.execute(f"SELECT CAST(cod_cli as char(5)) as cod_cli,COALESCE(razao, ' ') as razao,"
#                f"COALESCE(nome, ' ') as nome,COALESCE(cgc, ' ') as cgc,COALESCE(cpf, ' ') as cpf "
#                f"FROM saccli ORDER BY razao")


def pesquisa():
    nome_buscar = tela.pesquisa.text()
    hg.conexao_cursor.execute(f"SELECT CAST(cod_cli as char(5)) as cod_cli,COALESCE(razao, ' ') as razao, "
                                      f"COALESCE(nome, ' ') as nome,COALESCE(cgc, ' ') as cgc, "
                                      f"COALESCE(cpf, ' ') as cpf, tel1, cidade, "
                                      f"uf, REPLACE(CAST(limite AS DECIMAL(18,2)), '.', ',') as limite_formatado, "
                                      f"obs "
                                      f"FROM saccli WHERE (nome LIKE UPPER('%{nome_buscar}%') OR "
                                      f"razao LIKE UPPER('%{nome_buscar}%') "
                                      f"OR cod_cli LIKE UPPER('%{nome_buscar}%') "
                                      f"or cgc LIKE UPPER('%{nome_buscar}%') "
                                      f"OR cpf LIKE UPPER('%{nome_buscar}%') "
                                      f"OR tel1 LIKE UPPER('%{nome_buscar}%')) ORDER BY razao")


def listar_cliente():
    pesquisa()
    dados_lidos = hg.conexao_cursor.fetchall()
    hg.conexao_bd.commit()
    tela.tableWidget.setRowCount(len(dados_lidos))
    tela.tableWidget.setColumnCount(10)
    for i, linha in enumerate(dados_lidos):
        for j, valor in enumerate(linha):
            valor = str(valor) if valor is not None else ""
            item = QtWidgets.QTableWidgetItem(valor)
            tela.tableWidget.setItem(i, j, item)
            # print(item.text())
            # item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
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


tela.bt_inclusao.clicked.connect(f_incl_cliente)
tela.pesquisa.textChanged.connect(listar_cliente)
# tela.tableWidget.cellChanged.connect(lambda row, col: editar_item(row))
# tela.tableWidget.cellChanged.connect(lambda item: editar_item(item.row()))
tela.tableWidget.cellActivated.connect(lambda row, col: editar_item(row))
tela.tableWidget.itemDoubleClicked.connect(lambda item: editar_item(item.row()))

# tela.pesquisa.returnPressed.connect(listar_cliente)


if __name__ == '__main__':
    from hti_funcoes import conexao_banco
    conexao_banco()
    listar_cliente()
    app.exec()
    hg.conexao_bd.close()
