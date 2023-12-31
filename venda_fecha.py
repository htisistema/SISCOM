from PyQt6 import uic, QtWidgets, QtGui
from PyQt6.QtGui import QIcon, QGuiApplication, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QButtonGroup
from PyQt6.QtCore import QDateTime
from datetime import datetime
from hti_funcoes import conexao_banco
import hti_global
import os
from icecream import ic

app = QApplication([])
app.setStyleSheet(hti_global.style_sheet)
tela = uic.loadUi(f"{hti_global.c_ui}\\venda_fecha.ui")
icon = QIcon(f"{hti_global.c_imagem}\\htiico.jpg")
tela.setWindowIcon(icon)
tela.setWindowTitle(
    f"FECHAMENTO DO PEDIDO DE VENDA         {hti_global.SISTEMA}  Versao: {hti_global.VERSAO}"
)
# Centraliza a janela na tela
qt_rectangle = tela.frameGeometry()
center_point = app.primaryScreen().availableGeometry().center()
qt_rectangle.moveCenter(center_point)
tela.move(qt_rectangle.topLeft())
icon_sair = QIcon(f"{hti_global.c_imagem}\\sair.png")
tela.setWindowIcon(icon)
# Centraliza a janela na tela
# AJUSTAR A TELA EM RELACAO AO MONITOR
qt_rectangle = tela.frameGeometry()
center_point = app.primaryScreen().availableGeometry().center()
qt_rectangle.moveCenter(center_point)
tela.move(qt_rectangle.topLeft())

if hti_global.mtp_tela == "G":
    primary_screen = QGuiApplication.primaryScreen()
    if primary_screen is not None:
        screen_geometry = primary_screen.geometry()
        tela.setGeometry(screen_geometry)

# PEGA O NOME DO ARQUIVO EM EXECUCAO
nome_file_com = os.path.basename(__file__)
nome_file, ext = os.path.splitext(nome_file_com)
tela.statusbar.showMessage(f"<< {nome_file} >>")

if os.path.exists(f"{hti_global.c_imagem}\\htifirma.jpg"):
    imagem = QPixmap(f"{hti_global.c_imagem}\\htifirma.jpg")
else:
    imagem = QPixmap(f"{hti_global.c_imagem}\\htifirma1.jpg")

pixmap_redimensionado = imagem.scaled(350, 50)  # redimensiona a imagem para 100x100
tela.empresa.setPixmap(pixmap_redimensionado)

# logohti = QPixmap(f"{hti_global.c_imagem}\\LOGOhti.png")
# pixmap_redimensionado = logohti.scaled(85, 85)  # redimensiona a imagem para 100x100
# tela.logohti.setStyleSheet(
#     "background-color: rgb(190, 216, 255);border-width: 0px;border-radius: 0px;"
# )
# tela.logohti.setPixmap(pixmap_redimensionado)

# if os.path.exists(f"{hti_global.c_imagem}\\htifirma.jpg"):
#     imagem = QPixmap(f"{hti_global.c_imagem}\\htifirma.jpg")
# else:
#     imagem = QPixmap(f"{hti_global.c_imagem}\\htifirma1.jpg")
#
# pixmap_redimensionado = imagem.scaled(450, 350)  # redimensiona a imagem para 100x100
# tela.foto_produto.setPixmap(pixmap_redimensionado)
# print(f"{hti_global.c_usuario}\\{hti_global.geral_cod_usuario}.jpg")

# lbl_operador = tela.findChild(QtWidgets.QLabel, "operador")
# if os.path.exists(f"{hti_global.c_usuario}\\{hti_global.geral_cod_usuario}.jpg"):
#     usuario = QPixmap(f"{hti_global.c_usuario}\\{hti_global.geral_cod_usuario}.jpg")
#
# else:
#     usuario = QPixmap(f"{hti_global.c_usuario}\\htiusu.jpg")
# pixmap_redimensionado = usuario.scaled(125, 130)  # redimensiona a imagem para 100x100
# tela.usuario.setPixmap(pixmap_redimensionado)
# lbl_operador.setText(f" Operador: {hti_global.geral_cod_usuario}")
lbl_numero_pedido = tela.findChild(QtWidgets.QLabel, "numero_pedido")

mnum_ped = ""
lbl_produto = tela.findChild(QtWidgets.QLabel, "produto")
lbl_produto.setText("F E C H A M E N T O   D O   P E D I D O")
lbl_cabecalho = tela.findChild(QtWidgets.QLabel, "cabecalho")
data_atual = QDateTime.currentDateTime()

conexao_banco()
hti_global.conexao_cursor.execute("SELECT * FROM sacsetup")
# # 145082Recupere o resultado
m_set = hti_global.conexao_cursor.fetchone()
hti_global.conexao_bd.commit()

tela.cb_forma_pg.addItems(["1->Dinheiro", "2->PIX", "3->Cartao", "4->Duplicata", "5->Cheque", "6->Cheque Pre"])
tela.cb_forma_pg.setCurrentIndex(0)  # coloca o focus no index

rb_tipo_desconto_group = QButtonGroup()
rb_tipo_desconto_group.addButton(tela.rb_percentual, id=1)
rb_tipo_desconto_group.addButton(tela.rb_valor, id=2)
tela.rb_valor.setChecked(True)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        conexao_banco()
        fechar_pedido(mnum_ped)


def criar_tela(mnum_pedido):
    tela.textBrowser.clear()
    lbl_numero_pedido.setText(f" Numero Pedido: {mnum_pedido}")
    lbl_cabecalho.setText(f"Itens  Codigo   Descricao                  ")
    try:
        hti_global.conexao_cursor.execute(
            f"SELECT pcod_merc, pmerc, pquantd, pvlr_fat FROM sacped_s WHERE pnum_ped = '{mnum_pedido}'"
        )
        # # 145082Recupere o resultado
        resultados = hti_global.conexao_cursor.fetchall()
        hti_global.conexao_bd.commit()

        lbl_sub_total = tela.findChild(QtWidgets.QLabel, "sub_total")
        fonte = QtGui.QFont()
        fonte.setFamily("Courier")
        fonte.setPointSize(9)
        tela.textBrowser.setFont(fonte)

        # tela.textBrowser.append("Itens Codigo   Descricao                  ")
        # tela.textBrowser.append('Quant.   Valor R$   Total R$')
        # tela.textBrowser.append(
        #     "--------------------------------------------------------"
        # )
        mtotal_geral = 0
        i = 0
        # ic(resultados)
        # Exibir os resultados no QTextEdit
        if len(resultados) > 0:
            for resultado in resultados:
                i += 1
                pcod_merc, pmerc, pquantd, pvlr_fat = resultado
                # pcod_merc
                mquantd = "{:9,.3f}".format(pquantd)
                mvalor = "{:10,.2f}".format(pvlr_fat)
                soma = pquantd * pvlr_fat
                # ic(soma)
                msoma = "{:12,.2f}".format(soma)
                linha = f"  {i}   {pcod_merc}  {pmerc}"  # Formatar o campo valor como float com 2 casas decimais
                linha1 = f"                   {mquantd} x {mvalor} = {msoma}"  # Formatar o campo valor como float com 2 casas decimais
                mtotal_geral += soma
                # linha = ' '.join(map(str, resultado))
                tela.textBrowser.append(linha)
                tela.textBrowser.append(linha1)
                # print(f"{hti_global.c_produto}\\{mcodigo}.jpg")
            mtotal_g = "{:12,.2f}".format(mtotal_geral)
            linha1 = f"SUB-TOTAL: {mtotal_g}"
            lbl_sub_total.setText(linha1)

    except Exception as e:
        print(f"Erro ao executar a consulta: {e}")


def fechar_pedido(mnum_pedido):
    # tela.mcodigo.returnPressed.connect(verificar_produto)
    # tela.mcodigo.setFocus()
    # tela.textBrowser.itemDoubleClicked.connect(lambda item: editar_item(item.row()))
    criar_tela(mnum_pedido)
    tela.show()
    app.exec()


if __name__ == "__main__":
    # from hti_funcoes import conexao_banco
    # conexao_banco()
    mnum_ped = "145082"
    fechar_pedido(mnum_ped)
    # tela.show()
    # app.exec()
    hti_global.conexao_bd.close()
