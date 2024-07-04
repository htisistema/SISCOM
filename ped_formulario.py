# RELATORIO DE RESERVAS
import sys
from PyQt6.QtWidgets import QMessageBox, QApplication
from PyQt6.QtCore import QDate, QDateTime, QTime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, A0
from datetime import datetime
import hti_global as hg
from hti_funcoes import conexao_banco, ver_serie
from ver_pdf import main

titulo = "PEDIDO"
app = QApplication([])


def on_close_event(event):
    event.accept()


def fecha_tela():
    return


def mm2p(milimitros):
    return milimitros / 0.352777


def ped_formulario(mnumero_pedido, ali, mvia):
    data_obj = datetime.strptime(hg.mdata_sis, "%Y-%m-%d")
    mdatasis = data_obj.strftime("%d/%m/%Y")

    # data = QDate.fromString(str(hg.mdata_sis), "yyyy-MM-dd")
    # mdatasis = QDateTime(data, QTime(0, 0))

    hg.conexao_cursor.execute(
        f"SELECT pcod_merc, pmerc, plocal, punidade, pquantd, pvlr_fat, pcod_cli, ppag, pmotivo, pdat_ped, phora, "
        f"PCOD_OPER, PCOD_VEND, PVENDEDOR, POS, DATA_APP, PTERMINA FROM sacped_s "
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
        hg.conexao_cursor.execute(
            f"SELECT cod_cli,razao,cgc,insc,cpf,nome,comprado,endereco,bairro,cidade,uf,tel1,cep,rota,tel2,numero,"
            f"complemento,rota1 FROM saccli WHERE cod_cli = {cons_ped[0][6]} "
        )
        cons_cli = hg.conexao_cursor.fetchone()
        hg.conexao_bd.commit()
        if len(cons_cli) == 0:
            print(f"cliente nao encontrado {cons_ped[0][6]}")
        mpag = 1
        # CABECALHO DO RELATORIO
        data_obj = cons_ped[0][9]
        mdataemi = data_obj.strftime("%d/%m/%Y")

        eixo = 275
        linhas = 3
        cnv = canvas.Canvas(f"{hg.c_pdf}\\{mnumero_pedido}.pdf", pagesize=A4)
        cnv.setFont("Courier", 12)
        cnv.drawImage("c:\\hti\\python\\siscom\\imagem\\001.jpg", mm2p(5), mm2p(eixo), width=mm2p(15), height=mm2p(15))

        cnv.setFont("Helvetica", 12)
        cnv.drawString(mm2p(25), mm2p(eixo+12), str(hg.m_set[129].strip()))  # string EMPRESA
        cnv.setFont("Courier", 10)
        cnv.drawString(mm2p(25), mm2p(eixo+9), str(hg.m_set[128].strip()))  # string EMPRESA
        cnv.drawString(mm2p(25), mm2p(eixo+6), f"End.: {str(hg.m_set[131].strip())} "
                                               f"No.: {str(hg.m_set[159].strip())} "
                                               f"Complemento: {str(hg.m_set[160].strip())}")  # string EMPRESA
        cnv.drawString(mm2p(25), mm2p(eixo+3), f"Bairro: {str(hg.m_set[132].strip())} "
                                               f"Cidade: {str(hg.m_set[133].strip())} "
                                               f"UF: {str(hg.m_set[18].strip())} CEP: {str(hg.m_set[134].strip())} "
                                               f"FONE: {str(hg.m_set[135].strip())}")  # string EMPRESA

        cnv.setFont("Helvetica", 11)
        cnv.rect(13, 776, 557, 0)  # linha
        eixo -= 5
        if ali == "orcam":
            cnv.drawString(mm2p(5), mm2p(eixo), f"{hg.m_set[23]}: {mnumero_pedido}")
        else:
            cnv.drawString(mm2p(5), mm2p(eixo), f"{hg.m_set[22]}: {mnumero_pedido}")
        # cnv.drawString(mm2p(170), mm2p(276), f"Pagina: {mpag}")
        cnv.setFont("Courier", 9)
        cnv.drawString(mm2p(130), mm2p(eixo), f"Emissao: {mdataemi} - ")
        cnv.drawString(mm2p(172), mm2p(eixo), f"Horas: {cons_ped[0][10]}")
        cnv.setFont("Courier", 11)

        if not ver_serie() == "141237" and not ver_serie() == "141473":
            eixo -= linhas
            cnv.drawString(mm2p(5), mm2p(eixo), "SEM VALOR FISCAL")

        cnv.setFont("Courier", 9)
        cnv.drawString(mm2p(130), mm2p(eixo), f"{mvia}  T:{cons_ped[0][16]}")
        cnv.drawString(mm2p(160), mm2p(eixo), f"Ope: {cons_ped[0][11]}")
        cnv.drawString(mm2p(180), mm2p(eixo), f"Cod.: {cons_ped[0][12]}")

        cnv.setFont("Courier", 9)

        if hg.m_set[80] == "S":
            cnv.drawString(mm2p(100), mm2p(eixo), f" {cons_ped[0][13]}")

        if cons_ped[0][14] == "LOJA":
            cnv.drawString(mm2p(120), mm2p(eixo), f"Filial: {cons_ped[0][14]}")
        elif len(cons_ped[0][14].replace(" ", "")) > 0:
            cnv.drawString(mm2p(120), mm2p(eixo), f"No.OS: {cons_ped[0][14]}")

        if cons_ped[0][15] == "":
            cnv.drawString(mm2p(130), mm2p(eixo), f"Data APP: {cons_ped[0][15]}")

        # @ PROW(),00 SAY PADL(mvia+'  T:'+ALLTRIM(imppedido[1,3])+IF(mquantd > 1,' C-'+STRZERO(i,2),''),132)

        cnv.setFont("Courier", 11)
        eixo -= linhas
        mcod_cli = str(cons_cli[0])
        cnv.drawString(mm2p(5), mm2p(eixo), f"{mcod_cli} {cons_cli[1]}")
        cnv.setFont("Courier", 9)
        if hg.m_set[38] == "S":
            if len(cons_cli[2]) > 0:
                cnv.drawString(
                    mm2p(100), mm2p(eixo), f"CNPJ: {cons_cli[2]} -IE: {cons_cli[3]}"
                )
            elif len(cons_cli[4]) > 0:
                cnv.drawString(mm2p(100), mm2p(eixo), f"CPF: {cons_cli[4]}")

        if hg.m_set[39] == "S":
            eixo -= linhas
            cnv.drawString(mm2p(5), mm2p(eixo), f"Nome Fantasia: {cons_cli[5]}")
            cnv.drawString(mm2p(80), mm2p(eixo), f"Nome Responsavel: {cons_cli[6]}")
            cnv.drawString(mm2p(120), mm2p(eixo), f"   - Fone: {cons_cli[14]}")
            eixo -= linhas
            cnv.drawString(
                mm2p(5),
                mm2p(eixo),
                f"End.: {cons_cli[7].rstrip()}, {cons_cli[15].rstrip()} - {cons_cli[16].rstrip()} "
                f"- {cons_cli[8].rstrip()} - {cons_cli[9].rstrip()} - {cons_cli[10].rstrip()} "
                f"- Fone: {cons_cli[11].rstrip()} - CEP: {cons_cli[12]}",
            )
        if len(cons_cli[13]) > 0:
            eixo -= linhas
            cnv.drawString(mm2p(5), mm2p(eixo), f"Rota: {cons_cli[13]}")

        if len(cons_cli[17]) > 0:
            eixo -= linhas
            cnv.drawString(mm2p(5), mm2p(eixo), f"      {cons_cli[17]}")

        cnv.setFont("Helvetica", 9)

        if cons_ped[0][7] == "*" and not ver_serie() == "141599":
            eixo -= linhas
            cnv.drawString(mm2p(5), mm2p(eixo), "PAGO")

        if mvia == "2":
            if cons_ped[0][7] == "C":
                eixo -= linhas
                cnv.drawString(
                    mm2p(5), mm2p(eixo), f"CANCELADO - MOTIVO: {cons_ped[0][8]}"
                )
                eixo -= linhas
                cnv.setFont("Courier", 9)
                cnv.drawString(mm2p(5), mm2p(eixo), f"Emissao da 2a.via: {mdatasis}")
                mhora = datetime.now().strftime("%H:%M:%S")
                cnv.drawString(mm2p(70), mm2p(eixo), f"Horas: {mhora}")
                cnv.drawString(
                    mm2p(80), mm2p(eixo), f"Operador: {hg.geral_cod_usuario}"
                )
            elif cons_ped[0][7] == " " or cons_ped[0][7] == "":
                eixo -= linhas
                cnv.drawString(mm2p(5), mm2p(eixo), "ABERTO")
                cnv.setFont("Courier", 9)

                cnv.drawString(mm2p(25), mm2p(eixo), f"Emissao da 2a.via: {mdatasis}")
                mhora = datetime.now().strftime("%H:%M:%S")
                cnv.drawString(mm2p(70), mm2p(eixo), f"Horas: {mhora}")
                cnv.drawString(
                    mm2p(80), mm2p(eixo), f"Operador: {hg.geral_cod_usuario}"
                )
        cnv.setFont("Courier", 9)
        cnv.rect(13, 725, 557, 0)  # linha
        cnv.drawString(
            mm2p(5),
            mm2p(252),
            "Codigo Descricao                              Local UN     Quantd.     Vlr. Venda      Vlr.Total",
        )
        cnv.rect(13, 710, 557, 0)  # linha
        # cnv.setFont("Courier", 10)
        eixo = 247
        i = 0
        total_valor = 0
        for i in range(len(cons_ped)):
            # mqtd_p = f"{cons_ped[i][4]:,.2f}".replace(",", " ").replace(".", ",")
            mqtd_p = (
                "{:10,.3f}".format(cons_ped[i][4]).replace(".", ",").replace(",", ".")
            )
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
                f"{cons_ped[i][0]} {cons_ped[i][1]} {cons_ped[i][2]} {cons_ped[i][3]} {mqtd_p} X {mvalor} = "
                f"{mvalor_total}",
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
    ped_formulario(mnum_ped, "PED_S", "")
    hg.conexao_bd.close()
