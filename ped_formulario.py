# RELATORIO DE RESERVAS
# import sys
from PyQt6.QtWidgets import QMessageBox, QApplication
# from PyQt6.QtCore import QDate, QDateTime, QTime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, A0
from datetime import datetime, timedelta
import hti_global as hg
from hti_funcoes import conexao_banco, ver_serie
from ver_pdf import ver_relatorio

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

    if ali == "orcam":
        arquivo_db = "sacorcam"
    else:
        arquivo_db = "sacped_s"
    # data = QDate.fromString(str(hg.mdata_sis), "yyyy-MM-dd")
    # mdatasis = QDateTime(data, QTime(0, 0))
    #                0         1      2        3         4        5         6       7       8       9       10
    #        11          12          13      14     15       16       17      18    19     20      21        22
    #        23         24           25         26          27         28        29
    hg.conexao_cursor.execute(
        f"SELECT pcod_merc, pmerc, plocal, punidade, pquantd, pvlr_fat, pcod_cli, ppag, pmotivo, pdat_ped, phora, "
        f"PCOD_OPER, PCOD_VEND, PVENDEDOR, POS, DATA_APP, PTERMINA, POBS1, POBS2, POBS3, POBS4, PQUANTD, PDESC_MERC, "
        f"PPROMOCAO, PPRE_VENDA, PD_ENTREGA, PCOND_VEZE, PCOND_INTE, PVLR_ENT, PPRAZO "
        f"FROM {arquivo_db} "
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
        cnv.drawImage(
            f"{hg.c_imagem}\\001.jpg",
            mm2p(5),
            mm2p(eixo),
            width=mm2p(15),
            height=mm2p(15),
        )

        cnv.setFont("Helvetica", 12)
        cnv.drawString(
            mm2p(25), mm2p(eixo + 12), str(hg.m_set[129].strip())
        )  # string EMPRESA

        cnv.setFont("Courier", 10)
        cnv.drawString(
            mm2p(25), mm2p(eixo + 9), str(hg.m_set[128].strip())
        )  # string EMPRESA
        cnv.drawString(
            mm2p(25),
            mm2p(eixo + 6),
            f"End.: {str(hg.m_set[131].strip())} "
            f"No.: {str(hg.m_set[159].strip())} "
            f"Complemento: {str(hg.m_set[160].strip())}",
        )  # string EMPRESA
        cnv.drawString(
            mm2p(25),
            mm2p(eixo + 3),
            f"Bairro: {str(hg.m_set[132].strip())} "
            f"Cidade: {str(hg.m_set[133].strip())} "
            f"UF: {str(hg.m_set[18].strip())} CEP: {str(hg.m_set[134].strip())} ",
        )  # string EMPRESA
        cnv.setFont("Helvetica", 11)
        cnv.drawString(
            mm2p(25),
            mm2p(eixo - 1),
            f"FONE: {str(hg.m_set[135].strip())}",
        )  # string EMPRESA

        eixo -= linhas
        cnv.line(mm2p(5), mm2p(eixo), mm2p(201), mm2p(eixo))
        # cnv.rect(13, 776, 557, 0)  # linha
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
        eixo -= linhas
        cnv.line(mm2p(5), mm2p(eixo), mm2p(201), mm2p(eixo))
        # cnv.rect(13, 710, 557, 0)  # linha
        eixo -= 5
        cnv.drawString(
            mm2p(5),
            mm2p(eixo),
            "Codigo Descricao                              Local UN     Quantd.     Vlr. Venda      Vlr.Total",
        )
        eixo -= linhas
        cnv.line(mm2p(5), mm2p(eixo), mm2p(201), mm2p(eixo))

        # cnv.rect(13, 695, 557, 0)  # linha
        # cnv.setFont("Courier", 10)
        eixo -= 5
        i = 0
        total_valor = 0
        mtot_volume = 0
        mtot_desc = 0
        mdesconto = 0
        mt_pedido = 0
        mtot_quant = 0
        mtot_prazo = 0
        mprazo_aux = 0

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
            mtot_volume += cons_ped[i][22]
            # print(f"hti {hg.m_set[35]}")
            if hg.m_set[35] == "S":
                if cons_ped[i][24] > 0:
                    mdesconto = mperc = 0
                elif cons_ped[i][25] > cons_ped[i][6]:
                    mdesconto = (cons_ped[i][6] * cons_ped[i][6]) - (
                        cons_ped[i][6] * cons_ped[i][25]
                    )
                    mperc = (
                        (
                            (cons_ped[i][6] * cons_ped[i][25])
                            - (cons_ped[i][6] * cons_ped[i][6])
                        )
                        / (cons_ped[i][6] * cons_ped[i][25])
                    ) * 100
                # else:
                #    mperc = imppedido[cont,39]
            else:
                mdesconto = 0

            mtot_desc = mtot_desc + mdesconto
            mt_pedido += (cons_ped[i][4] * cons_ped[i][5]) - mdesconto
            mtot_quant += cons_ped[i][4]
            if cons_ped[i][29] > 0:
                mtot_prazo += mt_pedido
                mprazo_aux = cons_ped[i][29]

            eixo -= 4

        cnv.setFont("Courier", 10)
        eixo = 170
        cnv.drawString(
            mm2p(5),
            mm2p(eixo),
            f"OBS.: {cons_ped[i][17].rstrip()} {cons_ped[i][18].rstrip()}",
        )

        eixo -= linhas
        cnv.drawString(
            mm2p(5),
            mm2p(eixo),
            f"     {cons_ped[i][19].rstrip()} {cons_ped[i][20].rstrip()}",
        )
        # cnv.rect(13, 470, 557, 0)  # linha
        eixo -= linhas
        cnv.line(mm2p(5), mm2p(eixo), mm2p(201), mm2p(eixo))

        # if hg.m_set[1][109] == 'S':
        #    eixo -= linhas
        #    cnv.drawString(
        #        mm2p(5),
        #        mm2p(eixo),
        #        f"Doc.Vencidos R$: {mlim_venc} Doc.A vencer R$: {mlim_avenc} Sld.Devedor R$: {mtot_limite}")
        if hg.m_set[108] == "S":
            mtot_desc = cons_ped[i][23] * -1

        eixo -= 5
        mtotal_pedido = mt_pedido + mtot_desc
        mtotal_ped = mt_pedido + mtot_desc
        mt_pedido = "{:10,.2f}".format(mt_pedido).replace(".", ",").replace(",", ".")
        mtot_desc = "{:10,.2f}".format(mtot_desc).replace(".", ",").replace(",", ".")
        mtotal_pedido = (
            "{:10,.2f}".format(mtotal_pedido).replace(".", ",").replace(",", ".")
        )

        cnv.drawString(
            mm2p(5),
            mm2p(eixo),
            f"Volumes: {mtot_volume} Qtd.Itens: {len(cons_ped)} Sub-total: {mt_pedido} Desconto: {mtot_desc}",
        )
        cnv.setFont("Helvetica", 11)
        cnv.drawString(mm2p(158), mm2p(eixo), f"Total Nota R$: {mtotal_pedido}")

        cnv.setFont("Courier", 9)

        if cons_ped[0][25] is not None:
            eixo -= linhas
            cnv.drawString(
                mm2p(5), mm2p(eixo), f"PREVISAO DE ENTREGA: {cons_ped[0][25]}"
            )  # - {ver_dia(imppedido[1,101])}",)

            # if len(mtipo_pag) > 0
        if cons_ped[0][26] is not None:
            # if float(cons_ped[0][26][1:3]) == 0:
            # print(cons_ped[0][26][1:3], cons_ped[0][27][0:2])
            eixo -= linhas
            if cons_ped[0][27][0:2] == "CH":
                # eixo -= linhas
                cnv.drawString(
                    mm2p(5),
                    mm2p(eixo),
                    f"Pagamento AVISTA - Modo de Pagamento: CHEQUE",
                )

            elif cons_ped[0][27][0:2] == "DN":
                # eixo -= linhas
                cnv.drawString(
                    mm2p(5),
                    mm2p(eixo),
                    f"Pagamento AVISTA - Modo de Pagamento: DINHEIRO",
                )
            elif cons_ped[0][27][0:2] == "PX":
                # eixo -= linhas
                cnv.drawString(
                    mm2p(5),
                    mm2p(eixo),
                    f"Pagamento AVISTA - Modo de Pagamento: PIX",
                )

            if cons_ped[0][28] > 0:
                # eixo -= linhas
                cnv.drawString(
                    mm2p(120),
                    mm2p(eixo),
                    f"Valor da Entrada R$: {cons_ped[0][27]}",
                )
        else:
            if (
                cons_ped[0][27][0:2] == "CH"
                or cons_ped[0][27][0:2] == "DU"
                or cons_ped[0][27][0:2] == "CT"
            ):
                if cons_ped[0][27][0:2] == "CH":
                    eixo -= linhas
                    cnv.drawString(
                        mm2p(5),
                        mm2p(eixo),
                        f"CHEQUES",
                    )
                elif cons_ped[0][27][0:2] == "DU":
                    eixo -= linhas
                    cnv.drawString(
                        mm2p(5),
                        mm2p(eixo),
                        f"DUPLICATAS",
                    )
                else:
                    eixo -= linhas
                    cnv.drawString(
                        mm2p(5),
                        mm2p(eixo),
                        f"CARTAO",
                    )

                mtexto = f"APRAZO: {cons_ped[0][26][0:1]} + {cons_ped[0][26][1:3]} p/ {cons_ped[0][27][2:5]}"
                # print(cons_ped[0][27][5:8])
                if float(cons_ped[0][27][5:8]) > 0:
                    mtexto += f" + {cons_ped[0][27][5:8]}"
                if float(cons_ped[0][27][8:11]) > 0:
                    mtexto += f" + {cons_ped[0][27][8:11]}"
                if float(cons_ped[0][27][11:14]) > 0:
                    mtexto += f" + {cons_ped[0][27][11:14]}"
                if float(cons_ped[0][27][14:17]) > 0:
                    mtexto += f" + {cons_ped[0][27][14:17]}"
                if float(cons_ped[0][27][17:20]) > 0:
                    mtexto += f" + {cons_ped[0][27][17:20]}"
                if float(cons_ped[0][27][20:23]) > 0:
                    mtexto += f" + {cons_ped[0][27][20:23]}"
                if float(cons_ped[0][27][23:26]) > 0:
                    mtexto += f" + {cons_ped[0][27][23:26]}"
                if float(cons_ped[0][27][26:29]) > 0:
                    mtexto += f" + {cons_ped[0][27][26:29]}"
                if float(cons_ped[0][27][29:32]) > 0:
                    mtexto += f" + {cons_ped[0][27][29:32]}"
                if float(cons_ped[0][27][32:35]) > 0:
                    mtexto += f" + {cons_ped[0][27][32:35]}"
                if float(cons_ped[0][27][35:38]) > 0:
                    mtexto += f" + {cons_ped[0][27][35:38]}"
                if float(cons_ped[0][27][38:41]) > 0:
                    mtexto += f" + {cons_ped[0][27][38:41]}"
                if float(cons_ped[0][27][41:44]) > 0:
                    mtexto += f" + {cons_ped[0][27][41:44]}"
                if float(cons_ped[0][27][44:47]) > 0:
                    mtexto += f" + {cons_ped[0][27][44:47]}"

                eixo -= linhas
                cnv.drawString(mm2p(5), mm2p(eixo), f"{mtexto}")

                if cons_ped[0][28] > 0:
                    eixo -= linhas
                    cnv.drawString(
                        mm2p(5),
                        mm2p(eixo),
                        f"Valor da Entrada R$: {cons_ped[0][27]}",
                    )
                if mtot_prazo > 0:
                    mprazo = int(mprazo_aux)
                    mdataemi1 = datetime.strptime(mdataemi, "%d/%m/%Y")
                    mdata_emissao = mdataemi1 + timedelta(days=mprazo)
                    mdata_emissao = mdata_emissao.strftime("%d/%m/%Y")
                    eixo -= linhas
                    cnv.drawString(
                        mm2p(5),
                        mm2p(eixo),
                        f"Venc. : {mdata_emissao} - R$: {mtot_prazo}",
                    )
                # print(f"hti {cons_ped[0][26][1:3]}")

                if int(cons_ped[0][26][1:3]) >= 2:
                    mc_dup = 0
                    h = 5
                    f = 0
                    x = 2
                    y = 5
                    mtotal = (mtotal_ped - cons_ped[0][28] - mtot_prazo) / int(
                        cons_ped[0][26][1:3]
                    )
                    mtotal = (
                        "{:8,.2f}".format(mtotal).replace(".", ",").replace(",", ".")
                    )

                    mcontador = int(cons_ped[0][26][1:3])
                    for mc_dup in range(mcontador):
                        if f == 0:
                            eixo -= linhas
                            cnv.drawString(
                                mm2p(5),
                                mm2p(eixo),
                                "",
                            )
                        mprazo = int(cons_ped[0][27][x:y])
                        mdatavenc = datetime.strptime(mdataemi, "%d/%m/%Y")
                        mdata_venc = mdatavenc + timedelta(days=mprazo)
                        mdata_venc = mdata_venc.strftime("%d/%m/%Y")
                        # eixo -= linhas
                        mentrada = cons_ped[0][28]

                        cnv.drawString(
                            mm2p(h),
                            mm2p(eixo),
                            f"Venc.{mc_dup+1}:{mdata_venc} - " f"R$: {mtotal}",
                        )
                        # print(f"Venc.{mc_dup+1}:{mdata_venc} - " f"R$: {mtotal}")
                        # print(mcontador, mc_dup)

                        h += 65
                        x += 3
                        y += 3
                        f += 1
                        if f == 3:
                            h = 5
                            f = 0
            else:
                pass
            #     if mcust_real-mvlr_ent-mtot_prazo > 0:
            #         eixo -= linhas
            #         cnv.drawString(
            #             mm2p(5),
            #             mm2p(eixo),
            #             f"'Venc.1: '{mdata+m_dia[1]} - R$: {(mcust_real+mtot_ipi)-mvlr_ent-mtot_prazo)}"
            #
            #     elif cons_ped[0][27][0:2 == 'FI':
            #         hg.conexao_cursor.execute(f"SELECT * FROM sacfin WHERE cod_fin = {mcod_fin}")
            #         cons_finan = hg.conexao_cursor.fetchall()
            #         hg.conexao_bd.commit()
            #         eixo -= linhas
            #         cnv.drawString(mm2p(5), mm2p(eixo), "Pag. APRAZO",)
            #         if len(cons_finan) == 0:
            #             mtexto = f"Modo: FINANCIAMENTO - {mcod_fin} -     - Condicao: "
            #         else:
            #             mtexto = f"Modo: FINANCIAMENTO - {mcod_fin}-{cons_finan[1,2]} - Condicao: "
            #
            #         mtexto += mtipo_fin
            #
            #         if mvlr_ent > 0:
            #             mtexto += f" - Entrada R$: {mvlr_ent}"
            #
            #         mtexto += f" - Prestacao R$: {mvalor_pres}"
            #         eixo -= linhas
            #         cnv.drawString(
            #             mm2p(5),
            #             mm2p(eixo),
            #             mtexto,
            #         )
            #     else:
            #         hg.conexao_cursor.execute(f"SELECT * FROM saccaixa WHERE nota = {mnumero_pedido}")
            #         cons_caixa = hg.conexao_cursor.fetchall()
            #         hg.conexao_bd.commit()
            #         i = 0
            #         for i in len(cons_caixa)
            #             if cons_caixa[i,2] == 'DN':
            #                 DEVPOS(PROW()+1,00);DEVOUT('Dinheiro R$..: '+TRANSFORM(cons_caixa[i,10],'9,999,999.99'))
            #             elif cons_caixa[i,2] == 'CR':
            #                 DEVPOS(PROW()+1,00);DEVOUT('Credito R$...: '+TRANSFORM(cons_caixa[i,10],'9,999,999.99'))
            #             elif cons_caixa[i,2] == 'CH':
            #                 DEVPOS(PROW()+1,00);DEVOUT('Cheque R$....: '+TRANSFORM(cons_caixa[i,10],'9,999,999.99')+' Bco: '+cons_caixa[i,6]+' No.: '+cons_caixa[i,8]+' Venc.: '+DTOC(cons_caixa[i,9]))
            #             elif cons_caixa[i,2] == 'DU':
            #                 DEVPOS(PROW()+1,00);DEVOUT('Duplicata R$.: '+TRANSFORM(cons_caixa[i,10],'9,999,999.99')+' No.: '+cons_caixa[i,8]+IF(cons_caixa[i,20] = '*',' Pag..: ',' Venc.: ')+DTOC(cons_caixa[i,9]))
            #             elif cons_caixa[i,2] == 'FI':
            #                 DEVPOS(PROW()+1,00);DEVOUT('Financeira R$: '+TRANSFORM(cons_caixa[i,10],'9,999,999.99')+' No.: '+cons_caixa[i,8]+' Venc.: '+DTOC(cons_caixa[i,9]))
            #             elif cons_caixa[i,2] == 'CT':
            #                 DEVPOS(PROW()+1,00);DEVOUT('Cartao R$....: '+TRANSFORM(cons_caixa[i,10],'9,999,999.99')+' Cod.: '+cons_caixa[i,7]+' Doc.: '+cons_caixa[i,8]+' Venc.: '+DTOC(cons_caixa[i,9]))
            #             elif cons_caixa[i,2] == 'CA':
            #                 DEVPOS(PROW()+1,00);DEVOUT('PEDIDO CANCELADO PELO OPERADOR COD.: '+cons_caixa[i,17])
            #             elif cons_caixa[i,2] == 'ES':
            #                 DEVPOS(PROW()+1,00);DEVOUT(cons_caixa[i,13]+'-'+cons_caixa[i,14])

        eixo -= linhas
        cnv.line(mm2p(5), mm2p(eixo), mm2p(201), mm2p(eixo))

        if len(hg.m_set[24].rstrip()) > 0:
            eixo -= 3
            cnv.drawString(mm2p(5), mm2p(eixo), f"{hg.m_set[24].rstrip()}")

        if len(hg.m_set[25].rstrip()) > 0:
            eixo -= linhas
            cnv.drawString(
                mm2p(5),
                mm2p(eixo),
                f"{hg.m_set[25].rstrip()}",
            )
        if len(hg.m_set[26].rstrip()) > 0:
            eixo -= linhas
            cnv.drawString(
                mm2p(5),
                mm2p(eixo),
                f"{hg.m_set[26].rstrip()}",
            )
        if len(hg.m_set[27].rstrip()) > 0:
            eixo -= linhas
            cnv.drawString(
                mm2p(5),
                mm2p(eixo),
                f"{hg.m_set[27].rstrip()}",
            )

        eixo -= linhas
        cnv.line(mm2p(5), mm2p(eixo), mm2p(201), mm2p(eixo))

        # cnv.rect(13, 430, 557, 0)  # linha
        if hg.m_set[21] == "S":
            eixo -= 3
            cnv.drawString(
                mm2p(140),
                mm2p(eixo),
                f"HTI Sistemas - f.:(81) {hg.FONE_HTI}",
            )

        # cnv.line(mm2p(5), mm2p(eixo), mm2p(201), mm2p(eixo))
        # cnv.line(150, 0, 160, 180)
        cnv.showPage()
        eixo = 275
        cnv.drawString(
            mm2p(5),
            mm2p(eixo),
            f"HTI Sistemas - f.:(81) {hg.FONE_HTI}",
        )

        cnv.save()
        # ic()
        hg.arquivo_impressao = f"{mnumero_pedido}.PDF"
        # from IMPRESSAO_RELATORIO import ImpressaoApp
        cam_pdf = f"{hg.c_pdf}\\{mnumero_pedido}.pdf"
        # cam_pdf = "C:\\HTI\\PYTHON\\SISCOM\\pdf\\REL_RESERVA.PDF"
        # print("formulario")
        ver_relatorio(cam_pdf)
        app.exec()


if __name__ == "__main__":
    conexao_banco()
    mnum_ped = "397749"  # "411550"
    ped_formulario(mnum_ped, "PED_S", "")
    hg.conexao_bd.close()
