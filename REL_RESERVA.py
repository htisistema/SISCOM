# RELATORIO DE RESERVAS
import sys
import os
from icecream import ic
from PyQt6 import uic, QtWidgets
from PyQt6.QtGui import QIcon, QGuiApplication, QPixmap, QFont
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

# Carregando a fonte Arial
# configureOutput(prefix="DEBUG ->", contextAbsPath=True)

titulo = "RELATORIO DE RESERVAS"
app = QtWidgets.QApplication([])
app.setStyleSheet(hg.style_sheet)
tela = uic.loadUi(f"{hg.c_ui}\\rel_reserva.ui")
icon = QIcon(f"{hg.c_imagem}\\htiico.jpg")
icon_sair = QIcon(f"{hg.c_imagem}\\sair.png")
icon_imprimir = QIcon(f"{hg.c_imagem}\\impressora.jpg")
tela.setWindowIcon(icon)
# Centraliza a janela na tela
qt_rectangle = tela.frameGeometry()
center_point = app.primaryScreen().availableGeometry().center()
qt_rectangle.moveCenter(center_point)
tela.move(qt_rectangle.topLeft())

if hg.mtp_tela == "G":
    primary_screen = QGuiApplication.primaryScreen()
    if primary_screen is not None:
        screen_geometry = primary_screen.geometry()
        tela.setGeometry(screen_geometry)


tela.setWindowTitle(titulo)
# Suponhamos que você queira um tamanho de fonte de 12 pontos
tamanho_da_fonte = 35

# Criar um objeto QFont com o tamanho desejado
fonte = QFont()
fonte.setPointSize(tamanho_da_fonte)

# Configurar a fonte no QLabel
lbl_titulo_cliente = tela.findChild(QtWidgets.QLabel, "tit_rel_reserva")
lbl_titulo_cliente.setFont(fonte)
lbl_titulo_cliente.setText(titulo)
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

data_vazia = date(1900, 1, 1)
m_set = []
data_atual = QDateTime.currentDateTime()
tela.qdata_inicial.setDateTime(data_atual)
tela.qdata_final.setDateTime(data_atual)


class BDadosApp(QMainWindow):
    def __init__(self):
        global m_set
        super().__init__()
        from hti_funcoes import conexao_banco

        conexao_banco()
        tela.comboBox.clear()
        tela.comboBox_2.clear()
        hg.conexao_cursor.execute(f"SELECT * FROM sacsetup")
        # Recupere o resultado
        m_set = hg.conexao_cursor.fetchone()
        hg.conexao_bd.commit()

        hg.conexao_cursor.execute(
            f"SELECT scod_op, snome FROM insopera ORDER BY snome"
        )
        arq_usuario = hg.conexao_cursor.fetchall()
        hg.conexao_bd.commit()

        hg.conexao_cursor.execute(
            f"SELECT cod_cli, razao FROM saccli ORDER BY razao"
        )
        arq_cli = hg.conexao_cursor.fetchall()
        hg.conexao_bd.commit()
        # COMBOX

        tela.comboBox.addItem("      -                ")
        for ret_cli in arq_cli:
            mcod_c = str(ret_cli[0]).zfill(5)
            item = f"{mcod_c} - {ret_cli[1]}".strip("(),")
            tela.comboBox.addItem(item)

        tela.comboBox.setCurrentIndex(0)

        tela.comboBox_2.addItem("    -                ")
        for ret_usuario in arq_usuario:
            item = f"{ret_usuario[0]} - {ret_usuario[1]}".strip("(),")
            tela.comboBox_2.addItem(item)

        tela.comboBox_2.setCurrentIndex(0)
        rel_reserva()


def on_close_event(event):
    tela.close()
    event.accept()
    tela.closeEvent = on_close_event


def fecha_tela():
    # ic()
    tela.close()
    tela.closeEvent = on_close_event
    tela.bt_sair.clicked.disconnect()
    return


def mm2p(milimitros):
    return milimitros / 0.352777


def imprimir():
    tela.bt_imprimir.clicked.disconnect()
    if tela.rb_inclusao.isChecked():
        rb_tipo_data = "I"
    elif tela.rb_inireserva.isChecked():
        rb_tipo_data = "R"

    m_data_inicial_f = datetime.strptime(tela.qdata_inicial.text(), "%d/%m/%Y").date()
    m_data_inicial = m_data_inicial_f.strftime("%Y/%m/%d")
    if m_data_inicial_f == data_vazia:
        m_data_inicial = None

    m_data_final_f = datetime.strptime(tela.qdata_final.text(), "%d/%m/%Y").date()
    m_data_final = m_data_final_f.strftime("%Y/%m/%d")
    if m_data_final_f == data_vazia:
        m_data_final = None

    index1 = tela.comboBox.currentIndex()
    mop = tela.comboBox.itemText(index1)
    m_cod_cli = mop[0:5].strip()
    index1 = tela.comboBox_2.currentIndex()
    mop = tela.comboBox_2.itemText(index1)
    m_operador = mop[0:3].strip()
    comando = "SELECT r.reserva, MAX(r.data_inclusao) AS data_inclusao, MAX(r.data_reserva) AS data_reserva, "
    comando += "MAX(r.cliente) AS cliente, "
    comando += "MAX((SELECT razao FROM saccli c WHERE c.cod_cli = cast(r.cliente as int))) AS razao_cliente, "
    comando += "MIN(r.data_inicial) AS data_inicial, MAX(r.data_final) AS data_final, "
    comando += "MAX(r.qtd_pessoas) AS qtd_pessoas, "
    comando += "MAX(r.qtd_dias) AS qtd_dias, MAX(r.valor) AS valor, SUM(r.qtd_dias * r.valor) AS total_valor, "
    comando += "MAX(r.oper_inclusao) AS oper_inclusao FROM mastreserva r WHERE r.reserva IS NOT NULL"

    if rb_tipo_data == "I":
        comando += (
            f" AND r.data_inclusao BETWEEN '{m_data_inicial}' AND '{m_data_final}'"
        )

    else:
        comando += (
            f" AND r.data_inicial BETWEEN '{m_data_inicial}' AND '{m_data_final}'"
        )

    if len(m_cod_cli) > 0:
        comando += f" AND cliente = {m_cod_cli}"

    if len(m_operador) > 0:
        comando += f" AND oper_inclusao = {m_operador}"

    comando += " GROUP BY reserva"
    hg.conexao_cursor.execute(comando)
    m_reserva = hg.conexao_cursor.fetchall()
    hg.conexao_bd.commit()
    # QMessageBox.information(tela, "Inclusao de CLIENTE", "Cadastro feito com SUCESSO!")

    if len(m_reserva) == 0:
        QMessageBox.information(
            tela,
            titulo,
            f"Nenhuma reserva nesse periodo de '{m_data_inicial} a '{m_data_final}'",
        )
        BDadosApp()
    else:
        mpag = 1
        global m_set
        # CABECALHO DO RELATORIO
        cnv = canvas.Canvas(f"{hg.c_pdf}\\REL_RESERVA.pdf", pagesize=A4)
        cnv.setFont("Courier", 16)
        cnv.drawString(mm2p(5), mm2p(280), str(m_set[128].strip()))  # string EMPRESA
        cnv.setFont("Courier", 8)
        cnv.drawString(mm2p(5), mm2p(276), "Titulo: RELATORIO DE RESERVAS")
        cnv.drawString(mm2p(170), mm2p(276), f"Pagina: {mpag}")
        cnv.drawString(
            mm2p(5), mm2p(273), f"Periodo: {m_data_inicial} a {m_data_final}"
        )
        data_formatada = data_atual.toString("dd/MM/yyyy")
        cnv.drawString(mm2p(170), mm2p(273), f"Data: {data_formatada}")
        cnv.rect(13, 770, 557, 0)  # linha
        cnv.drawString(
            mm2p(5),
            mm2p(268),
            "No.Reserva   Reserva    Cliente                     "
            "   Dt.Inicial   Dt.Final Qtd.P Qtd.D    Vlr/Dia    Vlr.Total Ope",
        )
        cnv.rect(13, 755, 557, 0)  # linha
        cnv.setFont("Courier", 8)
        eixo = 263
        i = 0
        total_valor = 0
        total_dias = 0
        total_pessoas = 0
        for i in range(len(m_reserva)):
            # mdt_incl = m_reserva[i][1].strftime("%d/%m/%Y")
            mdt_reserva = m_reserva[i][2].strftime("%d/%m/%Y")
            mdt_incial = m_reserva[i][5].strftime("%d/%m/%Y")
            mdt_final = m_reserva[i][6].strftime("%d/%m/%Y")
            mqtd_p = f"{m_reserva[i][7]:,.0f}".replace(",", " ").replace(".", ",")
            mqtd_d = (
                "{:2,.0f}".format(m_reserva[i][8]).replace(".", ",").replace(",", " ")
            )
            mvalor = (
                "{:12,.2f}".format(m_reserva[i][9]).replace(".", ",").replace(",", ".")
            )
            mvalor_total = (
                "{:12,.2f}".format(m_reserva[i][10]).replace(".", ",").replace(",", ".")
            )
            total_valor += m_reserva[i][10]
            total_dias += m_reserva[i][8]
            total_pessoas += m_reserva[i][7]
            cnv.drawString(
                mm2p(5),
                mm2p(eixo),
                f"{m_reserva[i][0]} {mdt_reserva} "
                f"{m_reserva[i][3].strip()}-{m_reserva[i][4][0:30]} {mdt_incial} "
                f"{mdt_final}    {mqtd_p}   {mqtd_d} "
                f"{mvalor} {mvalor_total} {m_reserva[i][11]}",
            )
            eixo -= 4

        total_valor = (
            "{:12,.2f}".format(total_valor).replace(".", ",").replace(",", ".")
        )
        cnv.setFont("Courier", 12)
        cnv.rect(13, 100, 250, 0)  # linha
        cnv.drawString(mm2p(5), mm2p(30), "         RESUMO GERAL")
        cnv.drawString(mm2p(5), mm2p(26), f"Total Geral R$...: {total_valor}")
        cnv.drawString(mm2p(5), mm2p(22), f"Total de Dias....: {total_dias}")
        cnv.drawString(mm2p(5), mm2p(18), f"Total de Pessoas.: {total_pessoas}")
        cnv.drawString(mm2p(5), mm2p(14), f"Total de Reservas: {len(m_reserva)}")

        cnv.save()
        # ic()
        hg.arquivo_impressao = "REL_RESERVA.PDF"
        from IMPRESSAO_RELATORIO import ImpressaoApp

        ImpressaoApp()
        BDadosApp()


def rel_reserva():
    # tela.data_inicial.setDateTime(QtCore.QDateTime.currentDateTime())
    # tela.mdata_nas.setDateTime(QtCore.QDateTime.currentDateTime())

    # RADIO BUTTON
    tipo_data = QButtonGroup()
    tipo_data.addButton(tela.rb_inclusao, id=1)
    tipo_data.addButton(tela.rb_inireserva, id=2)
    tela.rb_inclusao.setChecked(True)

    tela.bt_imprimir.clicked.connect(imprimir)
    tela.bt_sair.clicked.connect(fecha_tela)
    tela.bt_sair.setIcon(icon_sair)
    tela.bt_imprimir.setIcon(icon_imprimir)

    tela.show()
    app.exec()


if __name__ == "__main__":
    # app = QApplication(sys.argv)
    BDadosApp()
    # window.setGeometry(10, 10, 800, 600)
    # window.show()
    sys.exit(app.exec())

    # from hti_funcoes import conexao_banco
    #
    # conexao_banco()
    # banco_dados()
    # rel_reserva()
    # hg.conexao_bd.close()
