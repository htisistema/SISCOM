from PyQt6 import uic, QtWidgets
from PyQt6.QtGui import QIcon, QGuiApplication
from PyQt6.QtWidgets import QButtonGroup
import os
import hti_global as hg

# PEGA O NOME DO ARQUIVO EM EXECUCAO
nome_file_com = os.path.basename(__file__)
nome_file, ext = os.path.splitext(nome_file_com)

titulo = 'USUARIO CADASTRADO'
app = QtWidgets.QApplication([])
app.setStyleSheet(hg.style_sheet)
tela = uic.loadUi(f"{hg.c_ui}\\lista_usuario.ui")
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
    tela.closeEvent = on_close_event
    return


# Define a função para ajustar as colunas da tabela

def ajustar_colunas_tabela(tabela):
    header = tabela.horizontalHeader()
    header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
    header.setStretchLastSection(False)


def f_incl_usuario():
    from SACSENHA1 import inclusao_usuario
    inclusao_usuario()
    return


def chama_alteracao(mcod_usu):
    from SACSENHA2 import alteracao_usuario
    alteracao_usuario(mcod_usu[0:3])
    return


def chama_consulta(mcod_cli):
    # from cons_usuario import consulta_usuario
    # consulta_usuario(mcod_cli[0:4])
    # print(mcod_cli)
    return


def botao_item():
    selected_item = tela.tableWidget.currentItem()
    if selected_item is not None:
        codigo_usuario = selected_item.text()
        chama_alteracao(codigo_usuario)
        return
    else:
        return


def editar_item(row):
    rb_tipo_consulta = None
    item = tela.tableWidget.item(row, 0)
    if item.isSelected():
        tela.tableWidget.itemDoubleClicked.disconnect()
    else:
        tela.tableWidget.itemDoubleClicked.disconnect()

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
    hg.conexao_cursor.execute(f"SELECT CAST(scod_op as char(5)) as cod_op,COALESCE(snome, ' ') as nome,"
                                      f"COALESCE(stipo, ' ') as tipo,COALESCE(stipo_sis, ' ') as tiposis,"
                                      f"COALESCE(snivel, ' ') as nivel, "
                                      f"COALESCE(fone, ' ') as fone, cidade, uf, "
                                      f"REPLACE(CAST(scota AS DECIMAL(18,2)), '.', ',') as cota, "
                                      f"ver_pocket "
                                      f"FROM insopera WHERE snome LIKE UPPER('{nome_buscar}%') ORDER BY snome")


def listar_usuario():
    pesquisa()
    dados_lidos = hg.conexao_cursor.fetchall()
    hg.conexao_bd.commit()
    tela.tableWidget.setRowCount(len(dados_lidos))
    # tela.tableWidget.setColumnWidth(0, 100)
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
    tela.bt_inclusao.clicked.connect(f_incl_usuario)
    tela.bt_sair.clicked.connect(fecha_tela)

    tela.bt_sair.setIcon(icon_sair)
    tela.bt_inclusao.setIcon(icon_incluir)

    tela.show()
    app.exec()


# tela.consulta_usuario.clicked.connect(botao_item)
# tela.pesquisa.textChanged.connect(listar_usuario)
# tela.tableWidget.itemDoubleClicked.connect(lambda item: editar_item(item.row()))
# tela.pesquisa.returnPressed.connect(listar_usuario)
# tela.bt_sair.clicked.connect(fecha_tela)

if __name__ == '__main__':
    from hti_funcoes import conexao_banco
    conexao_banco()
    listar_usuario()
    hg.conexao_bd.close()
