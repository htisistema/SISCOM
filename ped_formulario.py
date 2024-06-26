# RELATORIO DE RESERVAS
import sys
import os
from icecream import ic
from PyQt6 import uic, QtWidgets
from PyQt6.QtGui import QIcon, QGuiApplication, QPixmap, QFont
from PyQt6.QtPdfWidgets import QPdfView
from PyQt6.QtWidgets import (
    QButtonGroup,
    QMessageBox,
    QMainWindow,
)
from PyQt6.QtCore import QDateTime
from datetime import datetime, date
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import hti_global as hg
from hti_funcoes import conexao_banco

# Carregando a fonte Arial
# configureOutput(prefix="DEBUG ->", contextAbsPath=True)
conexao_banco()

titulo = "PEDIDO"
# app = QtWidgets.QApplication([])
# app.setStyleSheet(hg.style_sheet)
# tela = uic.loadUi(f"{hg.c_ui}\\rel_reserva.ui")
# icon = QIcon(f"{hg.c_imagem}\\htiico.jpg")
# icon_sair = QIcon(f"{hg.c_imagem}\\sair.png")
# icon_imprimir = QIcon(f"{hg.c_imagem}\\impressora.jpg")
# tela.setWindowIcon(icon)
# # Centraliza a janela na tela
# qt_rectangle = tela.frameGeometry()
# center_point = app.primaryScreen().availableGeometry().center()
# qt_rectangle.moveCenter(center_point)
# tela.move(qt_rectangle.topLeft())
#
# if hg.mtp_tela == "G":
#     primary_screen = QGuiApplication.primaryScreen()
#     if primary_screen is not None:
#         screen_geometry = primary_screen.geometry()
#         tela.setGeometry(screen_geometry)
#
#
# tela.setWindowTitle(titulo)
# # Suponhamos que você queira um tamanho de fonte de 12 pontos
# tamanho_da_fonte = 35
#
# # Criar um objeto QFont com o tamanho desejado
# fonte = QFont()
# fonte.setPointSize(tamanho_da_fonte)
#
# # Configurar a fonte no QLabel
# lbl_titulo_cliente = tela.findChild(QtWidgets.QLabel, "tit_rel_reserva")
# lbl_titulo_cliente.setFont(fonte)
# lbl_titulo_cliente.setText(titulo)
# # PEGA O NOME DO ARQUIVO EM EXECUCAO
# nome_file_com = os.path.basename(__file__)
# nome_file, ext = os.path.splitext(nome_file_com)
#
# tela.statusBar.showMessage(f"<< {nome_file} >>")
#
# if os.path.exists(f"{hg.c_imagem}\\htifirma.jpg"):
#     imagem = QPixmap(f"{hg.c_imagem}\\htifirma.jpg")
# else:
#     imagem = QPixmap(f"{hg.c_imagem}\\htifirma1.jpg")
#
# pixmap_redimensionado = imagem.scaled(350, 50)  # redimensiona a imagem para 100x100
# tela.empresa.setPixmap(pixmap_redimensionado)
#
# data_vazia = date(1900, 1, 1)
# data_atual = QDateTime.currentDateTime()
# tela.qdata_inicial.setDateTime(data_atual)
# tela.qdata_final.setDateTime(data_atual)
#
#
# class BDadosApp(QMainWindow):
#     def __init__(self):
#         global m_set
#         super().__init__()
#         from hti_funcoes import conexao_banco
#
#         conexao_banco()
#         tela.comboBox.clear()
#         tela.comboBox_2.clear()
#         hg.conexao_cursor.execute(f"SELECT * FROM sacsetup")
#         # Recupere o resultado
#         m_set = hg.conexao_cursor.fetchone()
#         hg.conexao_bd.commit()
#
#         hg.conexao_cursor.execute(
#             f"SELECT scod_op, snome FROM insopera ORDER BY snome"
#         )
#         arq_usuario = hg.conexao_cursor.fetchall()
#         hg.conexao_bd.commit()
#
#         hg.conexao_cursor.execute(
#             f"SELECT cod_cli, razao FROM saccli ORDER BY razao"
#         )
#         arq_cli = hg.conexao_cursor.fetchall()
#         hg.conexao_bd.commit()
#         # COMBOX
#
#         tela.comboBox.addItem("      -                ")
#         for ret_cli in arq_cli:
#             mcod_c = str(ret_cli[0]).zfill(5)
#             item = f"{mcod_c} - {ret_cli[1]}".strip("(),")
#             tela.comboBox.addItem(item)
#
#         tela.comboBox.setCurrentIndex(0)
#
#         tela.comboBox_2.addItem("    -                ")
#         for ret_usuario in arq_usuario:
#             item = f"{ret_usuario[0]} - {ret_usuario[1]}".strip("(),")
#             tela.comboBox_2.addItem(item)
#
#         tela.comboBox_2.setCurrentIndex(0)
#         rel_reserva()
#


def on_close_event(event):
    event.accept()


def fecha_tela():
    return


def mm2p(milimitros):
    return milimitros / 0.352777


def ped_formulario(mnumero_pedido):
    # tela.data_inicial.setDateTime(QtCore.QDateTime.currentDateTime())
    # tela.mdata_nas.setDateTime(QtCore.QDateTime.currentDateTime())
    hg.conexao_cursor.execute(f"SELECT pcod_merc, pmerc, plocal, punidade, pquantd, pvlr_fat FROM sacped_s "
                              f"WHERE pnum_ped = {mnumero_pedido}")
    cons_ped = hg.conexao_cursor.fetchall()
    hg.conexao_bd.commit()
    if len(cons_ped) == 0:
        QMessageBox.information(
            tela,
            titulo,
            f"Pedido nao encontrado No.: {mnumero_pedido}",
        )
    else:
        mpag = 1
        # CABECALHO DO RELATORIO
        cnv = canvas.Canvas(f"{hg.c_pdf}\\{mnumero_pedido}.pdf", pagesize=A4)
        cnv.setFont("Courier", 16)
        cnv.drawString(mm2p(5), mm2p(280), str(hg.m_set[128].strip()))  # string EMPRESA
        cnv.setFont("Courier", 8)
        cnv.drawString(mm2p(5), mm2p(276), f"PEDIDO No.: {mnumero_pedido}")
        cnv.drawString(mm2p(170), mm2p(276), f"Pagina: {mpag}")
        # cnv.drawString(
        #     mm2p(5), mm2p(273), f"Periodo: {m_data_inicial} a {m_data_final}"
        # )
        # data_formatada = data_atual.toString("dd/MM/yyyy")
        # cnv.drawString(mm2p(170), mm2p(273), f"Data: {data_formatada}")
        cnv.rect(13, 770, 557, 0)  # linha
        cnv.drawString(
            mm2p(5),
            mm2p(268),
            "Codigo Descricao                                   Local UN    Quantd.   Vlr. Venda  Vlr.Total",
        )
        cnv.rect(13, 755, 557, 0)  # linha
        cnv.setFont("Courier", 8)
        eixo = 263
        i = 0
        total_valor = 0
        for i in range(len(cons_ped)):
            # # mdt_incl = cons_ped[i][1].strftime("%d/%m/%Y")
            # mdt_reserva = cons_ped[i][2].strftime("%d/%m/%Y")
            # mdt_incial = cons_ped[i][5].strftime("%d/%m/%Y")
            # mdt_final = cons_ped[i][6].strftime("%d/%m/%Y")
            mqtd_p = f"{cons_ped[i][4]:,.2f}".replace(",", " ").replace(".", ",")
            mvalor = (
                "{:12,.2f}".format(cons_ped[i][5]).replace(".", ",").replace(",", ".")
            )
            mvalor_total = (
                "{:12,.2f}".format(cons_ped[i][4] * cons_ped[i][5]).replace(".", ",").replace(",", ".")
            )
            total_valor += cons_ped[i][4] * cons_ped[i][5]
            cnv.drawString(
                mm2p(5),
                mm2p(eixo),
                f"{cons_ped[i][0]}  {cons_ped[i][1]}  {cons_ped[i][2]}  {cons_ped[i][3]}  {mqtd_p} X {mvalor} = {mvalor_total}"
            )
            eixo -= 4

        total_valor = (
            "{:12,.2f}".format(total_valor).replace(".", ",").replace(",", ".")
        )
        cnv.setFont("Courier", 12)
        cnv.rect(13, 100, 250, 0)  # linha
        cnv.drawString(mm2p(5), mm2p(26), f"Total Geral R$...: {total_valor}")
        cnv.save()
        # ic()
        hg.arquivo_impressao = f"{mnumero_pedido}.PDF"
        from IMPRESSAO_RELATORIO import ImpressaoApp

        ImpressaoApp()


if __name__ == "__main__":
    mnum_ped = "411560"
    ped_formulario(mnum_ped)
    hg.conexao_bd.close()

