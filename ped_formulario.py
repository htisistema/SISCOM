# RELATORIO DE RESERVAS
import sys
from PyQt6.QtWidgets import QMessageBox, QApplication
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import hti_global as hg
from hti_funcoes import conexao_banco
from ver_pdf import main

titulo = "PEDIDO"
app = QApplication([])


def on_close_event(event):
    event.accept()


def fecha_tela():
    return


def mm2p(milimitros):
    return milimitros / 0.352777


def ped_formulario(mnumero_pedido):
    hg.conexao_cursor.execute(
        f"SELECT pcod_merc, pmerc, plocal, punidade, pquantd, pvlr_fat FROM sacped_s "
        f"WHERE pnum_ped = {mnumero_pedido}"
    )
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
            mqtd_p = f"{cons_ped[i][4]:,.2f}".replace(",", " ").replace(".", ",")
            mvalor = (
                "{:12,.2f}".format(cons_ped[i][5]).replace(".", ",").replace(",", ".")
            )
            mvalor_total = (
                "{:12,.2f}".format(cons_ped[i][4] * cons_ped[i][5])
                .replace(".", ",")
                .replace(",", ".")
            )
            total_valor += cons_ped[i][4] * cons_ped[i][5]
            cnv.drawString(
                mm2p(5),
                mm2p(eixo),
                f"{cons_ped[i][0]}  {cons_ped[i][1]}  {cons_ped[i][2]}  {cons_ped[i][3]}  {mqtd_p} X {mvalor} = {mvalor_total}",
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
        # from IMPRESSAO_RELATORIO import ImpressaoApp
        cam_pdf = f"{hg.c_pdf}\\{mnumero_pedido}.pdf"
        # cam_pdf = "C:\\HTI\\PYTHON\\SISCOM\\pdf\\REL_RESERVA.PDF"
        # print("formulario")
        main(cam_pdf)
        app.exec()


if __name__ == "__main__":
    conexao_banco()
    mnum_ped = "411560"
    ped_formulario(mnum_ped)
    hg.conexao_bd.close()
