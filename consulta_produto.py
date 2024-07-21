from PyQt6 import uic, QtWidgets
from PyQt6.QtGui import QIcon, QGuiApplication, QPixmap
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QApplication
import hti_global as hg
from hti_funcoes import conexao_banco
import os


class TelaProduto(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dados_lidos = []
        self.mcod_produto = ""
        self.init_ui()

    def init_ui(self):
        self.tela = uic.loadUi(f"{hg.c_ui}\\f4_merc.ui", self)
        self.tela.setWindowTitle("PRODUTOS CADASTRADO")
        icon = QIcon(f"{hg.c_imagem}\\htiico.ico")
        self.tela.setWindowIcon(icon)
        self.tabela1 = self.tela.tableWidget

        if hg.mtp_tela == "G":
            primary_screen = QGuiApplication.primaryScreen()
            if primary_screen is not None:
                screen_geometry = primary_screen.geometry()
                self.tela.setGeometry(screen_geometry)

        if os.path.exists(f"{hg.c_imagem}\\htifirma.jpg"):
            imagem = QPixmap(f"{hg.c_imagem}\\htifirma.jpg")
        else:
            imagem = QPixmap(f"{hg.c_imagem}\\htifirma1.jpg")

        pixmap_redimensionado = imagem.scaled(350, 50)
        self.tela.empresa.setPixmap(pixmap_redimensionado)

        self.tela.pesquisa.textChanged.connect(self.pesquisa_prod)
        self.tela.bt_sair.clicked.connect(self.close)
        self.tabela1.cellActivated.connect(lambda row, col: self.editar_prod(row))
        self.tabela1.itemDoubleClicked.connect(
            lambda item: self.editar_prod(item.row())
        )

    def carregar_dados(self):
        valor_aprazo_calculado = (
            "pr_venda * ((varejo / 100) + 1)"
            if hg.mtipo_temrinal == "L"
            else "iif(pr_venda1 > 0, pr_venda1, pr_venda * ((varejo / 100) + 1))"
        )

        hg.conexao_cursor.execute(
            f"SELECT CAST(cod_merc as char(5)) as cod_merc, COALESCE(merc, ' ') as merc, "
            f"REPLACE(CAST(saldo_mer AS DECIMAL(12, 2)), '.', ',') as saldomer, "
            f"REPLACE(CAST(pr_venda AS DECIMAL(12, 2)), '.', ',') as prvenda, "
            f"REPLACE(CAST({valor_aprazo_calculado} AS DECIMAL(12, 2)), '.', ','), "
            f"COALESCE(unidade, ' '), "
            f"COALESCE(cod_barr, ' '), COALESCE(ref, ' ') FROM sacmerc "
            f"ORDER BY merc"
        )
        self.dados_lidos = hg.conexao_cursor.fetchall()
        hg.conexao_bd.commit()

    def editar_prod(self, row):
        item = self.tabela1.item(row, 0)
        self.mcod_produto = item.text()
        print(f"editar {self.mcod_produto}")
        self.close()

    def pesquisa_prod(self):
        nome_buscar = self.tela.pesquisa.text().strip().upper()
        resultados = (
            [dado for dado in self.dados_lidos if nome_buscar in dado[1]]
            if nome_buscar.startswith("*") and len(nome_buscar) > 1
            else [dado for dado in self.dados_lidos if dado[1].startswith(nome_buscar)]
        )
        self.listar_produto(resultados)

    def listar_produto(self, resultados):
        self.tela.pesquisa.setFocus()
        self.tabela1.setRowCount(len(resultados))
        self.tabela1.setColumnCount(8)
        for i, linha in enumerate(resultados):
            for j, valor in enumerate(linha):
                valor = str(valor) if valor is not None else ""
                item = QTableWidgetItem(valor)
                self.tabela1.setItem(i, j, item)
        header = self.tabela1.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setStretchLastSection(False)

        self.tabela1.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers
        )

    def consulta_produto(self):
        self.carregar_dados()
        self.listar_produto(self.dados_lidos)
        self.show()
        # Bloquear o loop de eventos principal até a janela ser fechada
        QApplication.processEvents()  # Processa os eventos pendentes
        QApplication.instance().exec()  # Executa o loop de eventos
        print(f"consulta {self.mcod_produto}")
        return self.mcod_produto


def consulta_produto(mcod):
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    tela_produto = TelaProduto()
    print(f"hti {tela_produto.consulta_produto()}")
    return tela_produto.consulta_produto()


if __name__ == "__main__":
    app = QApplication([])
    conexao_banco()
    resultado = consulta_produto("")
    print(f"Produto selecionado: {resultado}")
    hg.conexao_bd.close()


# from PyQt6 import uic, QtWidgets, QtGui
# from PyQt6.QtGui import QIcon, QGuiApplication, QPixmap
# from PyQt6.QtWidgets import QApplication, QButtonGroup, QMessageBox
# import hti_global as hg
# from hti_funcoes import conexao_banco
# import os
#
# app = QApplication([])
# app.setStyleSheet(hg.style_sheet)
# tela = uic.loadUi(f"{hg.c_ui}\\f4_merc.ui")
# tela.setWindowTitle("PRODUTOS CADASTRADO")
# icon = QIcon(f"{hg.c_imagem}\\htiico.ico")
# # icon_sair = QIcon(f"{hg.c_imagem}\\sair.png")
# # icon_incluir = QIcon(f"{hg.c_imagem}\\incluir.png")
# tela.setWindowIcon(icon)
# tabela1 = tela.tableWidget
# if hg.mtp_tela == "G":
#     primary_screen = QGuiApplication.primaryScreen()
#     if primary_screen is not None:
#         screen_geometry = primary_screen.geometry()
#         tela.setGeometry(screen_geometry)
#
# # tela.statusBar.showMessage(f"<< {nome_file} >>")
# if os.path.exists(f"{hg.c_imagem}\\htifirma.jpg"):
#     imagem = QPixmap(f"{hg.c_imagem}\\htifirma.jpg")
# else:
#     imagem = QPixmap(f"{hg.c_imagem}\\htifirma1.jpg")
#
# pixmap_redimensionado = imagem.scaled(350, 50)  # redimensiona a imagem para 100x100
# tela.empresa.setPixmap(pixmap_redimensionado)
# dados_lidos = []
# mcod_produto = ''
#
#
# def fecha_tela():
#     tela.close()
#     return ""
#
#
# def carregar_dados():
#     global dados_lidos
#     if hg.mtipo_temrinal == "L":
#         valor_aprazo_calculado = "pr_venda * ((varejo / 100) + 1)"
#     else:
#         valor_aprazo_calculado = (
#             "iif(pr_venda1 > 0, pr_venda1, pr_venda * ((varejo / 100) + 1))"
#         )
#
#     hg.conexao_cursor.execute(
#         f"SELECT CAST(cod_merc as char(5)) as cod_merc, COALESCE(merc, ' ') as merc, "
#         f"REPLACE(CAST(saldo_mer AS DECIMAL(12, 2)), '.', ',') as saldomer, "
#         f"REPLACE(CAST(pr_venda AS DECIMAL(12, 2)), '.', ',') as prvenda, "
#         f"REPLACE(CAST({valor_aprazo_calculado} AS DECIMAL(12, 2)), '.', ','), "
#         f"COALESCE(unidade, ' '), "
#         f"COALESCE(cod_barr, ' '), COALESCE(ref, ' ') FROM sacmerc "
#         f"ORDER BY merc"
#     )
#     dados_lidos = hg.conexao_cursor.fetchall()
#     hg.conexao_bd.commit()
#
#
# def editar_prod(row):
#     global mcod_produto
#     tela.tableWidget.itemDoubleClicked.disconnect()
#     tela.tableWidget.cellActivated.disconnect()
#     item = tela.tableWidget.item(row, 0)
#     # tela.tableWidget.cellActivated.connect(lambda row1, col: editar_prod(item.row()))
#     # tela.tableWidget.itemDoubleClicked.connect(lambda item1: editar_prod(item.row()))
#     mcod_produto = item.text()
#     print(mcod_produto)
#     tela.close()
#     return mcod_produto
#
#
# def pesquisa_prod():
#     global dados_lidos
#     nome_buscar = tela.pesquisa.text().strip().upper()
#     # print(nome_buscar[0:1], nome_buscar[1:])
#
#     resultados = []
#
#     if nome_buscar.startswith("*") and len(nome_buscar) > 1:
#         nome_buscar = nome_buscar[1:]
#         resultados = [dado for dado in dados_lidos if nome_buscar in dado[1]]
#     else:
#         resultados = [dado for dado in dados_lidos if dado[1].startswith(nome_buscar)]
#
#     # Atualize a interface do usuário com os dados filtrados
#     listar_produto(resultados)
#
#
# # Função para listar os produtos na interface do usuário
# def listar_produto(resultados):
#     tela.pesquisa.setFocus()
#     # tela.listView.clear()  # Limpa a listView (ou outro widget que você esteja usando)
#     tela.tableWidget.setRowCount(len(resultados))
#     tela.tableWidget.setColumnCount(8)
#     for i, linha in enumerate(resultados):
#         for j, valor in enumerate(linha):
#             valor = str(valor) if valor is not None else ""
#             item = QtWidgets.QTableWidgetItem(valor)
#             tela.tableWidget.setItem(i, j, item)
#     header = tabela1.horizontalHeader()
#     header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
#     header.setStretchLastSection(False)
#
#     tela.tableWidget.setEditTriggers(
#         QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers
#     )
#     tela.tableWidget.cellActivated.connect(lambda row, col: editar_prod(item.row()))
#     tela.tableWidget.itemDoubleClicked.connect(lambda item: editar_prod(item.row()))
#     # print(mcod_produto)
#
#     tela.show()
#
#
# def consulta_produto(mcod):
#     global dados_lidos
#     carregar_dados()
#     listar_produto(dados_lidos)
#     # tela.bt_sair.clicked.connect(fecha_tela)
#     # tela.bt_sair.setIcon(icon_sair)
#     tela.pesquisa.textChanged.connect(pesquisa_prod)
#     # tela.tableWidget.cellActivated.connect(lambda row, col: editar_prod(item.row()))
#     # tela.tableWidget.itemDoubleClicked.connect(lambda item: editar_prod(item.row()))
#     tela.rb_alteracao.setEnabled(False)
#     tela.rb_consulta.setEnabled(False)
#     tela.bt_inclusao.setEnabled(False)
#     tela.bt_sair.clicked.connect(fecha_tela)
#     tela.show()
#     print(f"codigo: {mcod_produto}")
#     return mcod_produto
#
#
# if __name__ == "__main__":
#     conexao_banco()
#     consulta_produto('')
#     app.exec()
#     hg.conexao_bd.close()
