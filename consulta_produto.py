from PyQt6 import uic, QtWidgets, QtGui
from PyQt6.QtGui import QIcon, QGuiApplication, QPixmap
from PyQt6.QtWidgets import QApplication, QButtonGroup, QMessageBox
import hti_global as hg
from hti_funcoes import conexao_banco
import os

app = QApplication([])
app.setStyleSheet(hg.style_sheet)
tela = uic.loadUi(f"{hg.c_ui}\\f4_merc.ui")
tela.setWindowTitle("PRODUTOS CADASTRADO")
icon = QIcon(f"{hg.c_imagem}\\htiico.ico")
# icon_sair = QIcon(f"{hg.c_imagem}\\sair.png")
# icon_incluir = QIcon(f"{hg.c_imagem}\\incluir.png")
tela.setWindowIcon(icon)
tabela1 = tela.tableWidget
if hg.mtp_tela == "G":
    primary_screen = QGuiApplication.primaryScreen()
    if primary_screen is not None:
        screen_geometry = primary_screen.geometry()
        tela.setGeometry(screen_geometry)

# tela.statusBar.showMessage(f"<< {nome_file} >>")
if os.path.exists(f"{hg.c_imagem}\\htifirma.jpg"):
    imagem = QPixmap(f"{hg.c_imagem}\\htifirma.jpg")
else:
    imagem = QPixmap(f"{hg.c_imagem}\\htifirma1.jpg")

pixmap_redimensionado = imagem.scaled(350, 50)  # redimensiona a imagem para 100x100
tela.empresa.setPixmap(pixmap_redimensionado)
dados_lidos = []


def fecha_tela():
    tela.close()
    return ''


def pesquisa_prod():
    global dados_lidos
    tela.pesquisa.textChanged.disconnect()
    if hg.mtipo_temrinal == "L":
        valor_aprazo_calculado = "pr_venda * ((varejo / 100) + 1)"
    else:
        valor_aprazo_calculado = (
            "iif(pr_venda1 > 0, pr_venda1, pr_venda * ((varejo / 100) + 1))"
        )

    nome_buscar = tela.pesquisa.text().strip()
    # print(f"pesquisa_produto {nome_buscar}")
    # or cod_merc LIKE UPPER('%{nome_buscar}%') or cod_barr LIKE UPPER('%{nome_buscar}%')
    # or ref LIKE UPPER('%{nome_buscar}%'))
    hg.conexao_cursor.execute(
        f"SELECT CAST(cod_merc as char(5)) as cod_merc, COALESCE(merc, ' ') as merc, "
        f"REPLACE(CAST(saldo_mer AS DECIMAL(12, 2)), '.', ',') as saldomer, "
        f"REPLACE(CAST(pr_venda AS DECIMAL(12, 2)), '.', ',') as prvenda, "
        f"REPLACE(CAST({valor_aprazo_calculado} AS DECIMAL(12, 2)), '.', ','), "
        f"COALESCE(unidade, ' '), "
        f"COALESCE(cod_barr, ' '), COALESCE(ref, ' ') FROM sacmerc "
        f"WHERE merc LIKE UPPER('%{nome_buscar}%') ORDER BY merc"
    )
    dados_lidos = hg.conexao_cursor.fetchall()
    hg.conexao_bd.commit()
    tela.pesquisa.textChanged.connect(pesquisa_prod)
    listar_produto()


def editar_prod(row):
    # rb_tipo_consulta = None
    tela.tableWidget.itemDoubleClicked.disconnect()
    tela.tableWidget.cellActivated.disconnect()
    # item = tela.tableWidget.item(row, 0)
    item = tela.tableWidget.item(row, 0)
    # print(f"item {item.text()}")
    # tela.tableWidget.cellActivated.connect(lambda row1, col: editar_prod(item.row()))
    # tela.tableWidget.itemDoubleClicked.connect(lambda item: editar_prod(item.row()))
    # verificar_produto()
    # criar_tela()
    tela.close()
    return item


def listar_produto():
    tela.pesquisa.setFocus()
    tela.tableWidget.setRowCount(len(dados_lidos))
    tela.tableWidget.setColumnCount(8)
    for i, linha in enumerate(dados_lidos):
        for j, valor in enumerate(linha):
            valor = str(valor) if valor is not None else ""
            item = QtWidgets.QTableWidgetItem(valor)
            tela.tableWidget.setItem(i, j, item)
    header = tabela1.horizontalHeader()
    header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
    header.setStretchLastSection(False)

    tela.tableWidget.setEditTriggers(
        QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers
    )
    # tela.bt_sair.clicked.connect(fecha_tela)
    # tela.bt_sair.setIcon(icon_sair)
    tela.pesquisa.textChanged.connect(pesquisa_prod)
    tela.tableWidget.cellActivated.connect(lambda row, col: editar_prod(item.row()))
    tela.tableWidget.itemDoubleClicked.connect(lambda item: editar_prod(item.row()))
    # tela.mcodigo.returnPressed.connect(verificar_produto)
    tela.rb_alteracao.setEnabled(False)
    tela.rb_consulta.setEnabled(False)
    tela.bt_inclusao.setEnabled(False)
    tela.bt_sair.clicked.connect(fecha_tela)

    tela.show()


if __name__ == "__main__":
    conexao_banco()
    mcod = listar_produto()
    # print(mcod)
    app.exec()
    hg.conexao_bd.close()
