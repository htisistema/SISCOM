# LISTA CLIENTES PRODUTOS

import sys
import os
from PyQt6 import uic, QtWidgets, QtCore
from PyQt6.QtGui import QIcon, QGuiApplication, QPixmap
from PyQt6.QtWidgets import QButtonGroup, QApplication, QMainWindow
from hti_funcoes import conexao_banco
import hti_global as hg


app = QtWidgets.QApplication([])
app.setStyleSheet(hg.style_sheet)
tela = uic.loadUi(f"{hg.c_ui}\\f4_merc.ui")
tela.setWindowTitle("PRODUTOS CADASTRADO")
icon = QIcon(f"{hg.c_imagem}\\htiico.jpg")
icon_sair = QIcon(f"{hg.c_imagem}\\sair.png")
icon_incluir = QIcon(f"{hg.c_imagem}\\incluir.png")
tela.setWindowIcon(icon)

# PEGA O NOME DO ARQUIVO EM EXECUCAO
nome_file_com = os.path.basename(__file__)
nome_file, ext = os.path.splitext(nome_file_com)
# AJUSTAR A TELA EM RELACAO AO MONITOR
qt_rectangle = tela.frameGeometry()
center_point = app.primaryScreen().availableGeometry().center()
qt_rectangle.moveCenter(center_point)
# tela.move(15, 10)

if hg.mtp_tela == "G":
    primary_screen = QGuiApplication.primaryScreen()
    if primary_screen is not None:
        screen_geometry = primary_screen.geometry()
        tela.setGeometry(screen_geometry)

tela.statusBar.showMessage(f"<< {nome_file} >>")
if os.path.exists(f"{hg.c_imagem}\\htifirma.jpg"):
    imagem = QPixmap(f"{hg.c_imagem}\\htifirma.jpg")
else:
    imagem = QPixmap(f"{hg.c_imagem}\\htifirma1.jpg")

pixmap_redimensionado = imagem.scaled(350, 50)  # redimensiona a imagem para 100x100
tela.empresa.setPixmap(pixmap_redimensionado)
mconsulta_imclusao = ""


def on_close_event(event):
    # Esta função será chamada quando o usuário clicar no botão de fechar a janela
    # print("Fechando a janela...")
    tela.close()
    event.accept()


tela.closeEvent = on_close_event


def fecha_tela():
    tela.close()
    return


# Define a função para ajustar as colunas da tabela
def ajustar_colunas_tabela(tabela):
    header = tabela.horizontalHeader()
    header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
    header.setStretchLastSection(False)


def f_incl_produto():
    from SAC110 import inclusao_produto

    inclusao_produto()
    return


def chama_alteracao(mcod_prod):
    from SAC111 import alteracao_produto

    alteracao_produto(mcod_prod[0:5])
    return


def chama_consulta(mcod_prod):
    # from SAC111 import alteracao_produto
    # alteracao_produto(mcod_prod[0:5])
    return


def botao_item():
    selected_item = tela.tableWidget.currentItem()
    if selected_item is not None:
        codigo_produto = selected_item.text()
        chama_alteracao(codigo_produto)
        return
    else:
        return


def editar_item(row):
    # rb_tipo_consulta = None
    item = tela.tableWidget.item(row, 0)

    if mconsulta_imclusao == "C":
        tela.close()
        print(f"f4: {item.text()}")
        return item.text()
    else:
        # if item.isSelected():
        #     tela.tableWidget.itemDoubleClicked.disconnect()
        # else:
        tela.tableWidget.itemDoubleClicked.disconnect()

    if tela.rb_alteracao.isChecked():
        chama_alteracao(item.text())
        # rb_tipo_consulta = "A"
    elif tela.rb_consulta.isChecked():
        chama_consulta(item.text())
        # rb_tipo_consulta = "C"

    # if rb_tipo_consulta == 'A':
    #     chama_alteracao(item.text())
    # else:
    #     chama_consulta(item.text())

    tela.tableWidget.itemDoubleClicked.connect(lambda item: editar_item(item.row()))
    return


def pesquisa():
    if hg.mtipo_temrinal == "L":
        valor_aprazo_calculado = "pr_venda * ((varejo / 100) + 1)"
    else:
        valor_aprazo_calculado = (
            "iif(pr_venda1 > 0, pr_venda1, pr_venda * ((varejo / 100) + 1))"
        )

    nome_buscar = tela.pesquisa.text()
    hg.conexao_cursor.execute(
        f"SELECT CAST(cod_merc as char(5)) as cod_merc, COALESCE(merc, ' ') as merc, "
        f"REPLACE(CAST(saldo_mer AS DECIMAL(12, 2)), '.', ',') as saldomer, "
        f"REPLACE(CAST(pr_venda AS DECIMAL(12, 2)), '.', ',') as prvenda, "
        f"REPLACE(CAST({valor_aprazo_calculado} AS DECIMAL(12, 2)), '.', ','), "
        f"COALESCE(unidade, ' '), "
        f"COALESCE(cod_barr, ' '), COALESCE(ref, ' ') FROM sacmerc "
        f"WHERE (cod_merc LIKE UPPER('%{nome_buscar}%') OR "
        f"merc LIKE UPPER('%{nome_buscar}%') OR cod_barr LIKE UPPER('%{nome_buscar}%') "
        f"OR ref LIKE UPPER('%{nome_buscar}%')) ORDER BY cod_merc"
    )


def incluir_produto():
    from SAC110 import inclusao_produto

    inclusao_produto()


def listar_produto(mtipo):
    global mconsulta_imclusao
    pesquisa()
    mconsulta_imclusao = mtipo
    dados_lidos = hg.conexao_cursor.fetchall()
    hg.conexao_bd.commit()
    tela.tableWidget.setRowCount(len(dados_lidos))
    tela.tableWidget.setColumnCount(8)
    for i, linha in enumerate(dados_lidos):
        for j, valor in enumerate(linha):
            valor = str(valor) if valor is not None else ""
            item = QtWidgets.QTableWidgetItem(valor)
            tela.tableWidget.setItem(i, j, item)
            # item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter | QtCore.Qt.AlignmentFlag.AlignVCenter)
            # print(item.text())
    ajustar_colunas_tabela(tela.tableWidget)

    rb_tipo_group = QButtonGroup()
    rb_tipo_group.addButton(tela.rb_alteracao, id=1)
    rb_tipo_group.addButton(tela.rb_consulta, id=2)
    tela.rb_alteracao.setChecked(True)

    tela.tableWidget.setEditTriggers(
        QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers
    )
    tela.tableWidget.itemDoubleClicked.connect(lambda item: editar_item(item.row()))
    tela.bt_inclusao.clicked.connect(incluir_produto)
    tela.bt_sair.clicked.connect(fecha_tela)
    tela.bt_sair.setIcon(icon_sair)
    tela.bt_inclusao.setIcon(icon_incluir)

    tela.show()
    app.exec()


# tela.incl_produto.clicked.connect(f_incl_produto)
# tela.consulta_produto.clicked.connect(botao_item)
tela.pesquisa.textChanged.connect(listar_produto)
tela.tableWidget.cellActivated.connect(lambda row, col: editar_item(row))
tela.tableWidget.itemDoubleClicked.connect(lambda item: editar_item(item.row()))

# tela.pesquisa.returnPressed.connect(listar_produto)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # locale.setlocale(locale.LC_NUMERIC, '')
        # Executar a consulta
        conexao_banco()
        listar_produto("I")


if __name__ == "__main__":
    # from hti_funcoes import conexao_banco
    # conexao_banco()
    # listar_produto()
    MainWindow()
    hg.conexao_bd.close()
    hg.conexao_cursor.close()
    tela.close()
