from PyQt6 import uic, QtWidgets, QtCore
from PyQt6.QtGui import QIcon, QGuiApplication, QPixmap
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QDateTime, Qt, QDate
from datetime import datetime
from icecream import ic
from hti_funcoes import conexao_banco
# from ATENCAO import atencao
# from ver_pagamento import ver_pagamento
import hti_global as hg
import os

# ic()

app = QApplication([])
app.setStyleSheet(hg.style_sheet)
tela = uic.loadUi(f"{hg.c_ui}\\caixa_pdv.ui")
icon = QIcon(f"{hg.c_imagem}\\htiico.ico")
tela.setWindowIcon(icon)
tela.setWindowTitle(
    f"FECHAMENTO DO PEDIDO DE VENDA         {hg.SISTEMA}  Versao: {hg.VERSAO}"
)
# Centraliza a janela na tela
qt_rectangle = tela.frameGeometry()
center_point = app.primaryScreen().availableGeometry().center()
qt_rectangle.moveCenter(center_point)
tela.move(qt_rectangle.topLeft())
icon_salvar = QIcon(f"{hg.c_imagem}\\confirma.png")
icon_sair = QIcon(f"{hg.c_imagem}\\sair.png")
# Centraliza a janela na tela
# AJUSTAR A TELA EM RELACAO AO MONITOR
if hg.mtp_tela == "G":
    primary_screen = QGuiApplication.primaryScreen()
    if primary_screen is not None:
        screen_geometry = primary_screen.geometry()
        tela.setGeometry(screen_geometry)

# PEGA O NOME DO ARQUIVO EM EXECUCAO
nome_file_com = os.path.basename(__file__)
nome_file, ext = os.path.splitext(nome_file_com)
tela.statusbar.showMessage(f"<< {nome_file} >>")

if os.path.exists(f"{hg.c_imagem}\\htifirma.jpg"):
    imagem = QPixmap(f"{hg.c_imagem}\\htifirma.jpg")
else:
    imagem = QPixmap(f"{hg.c_imagem}\\htifirma1.jpg")

pixmap_redimensionado = imagem.scaled(350, 50)  # redimensiona a imagem para 100x100
tela.empresa.setPixmap(pixmap_redimensionado)

# logohti = QPixmap(f"{hg.c_imagem}\\LOGOhti.png")
# pixmap_redimensionado = logohti.scaled(85, 85)  # redimensiona a imagem para 100x100
# tela.logohti.setStyleSheet(
#     "background-color: rgb(190, 216, 255);border-width: 0px;border-radius: 0px;"
# )
# tela.logohti.setPixmap(pixmap_redimensionado)

# if os.path.exists(f"{hg.c_imagem}\\htifirma.jpg"):
#     imagem = QPixmap(f"{hg.c_imagem}\\htifirma.jpg")
# else:
#     imagem = QPixmap(f"{hg.c_imagem}\\htifirma1.jpg")
#
# pixmap_redimensionado = imagem.scaled(450, 350)  # redimensiona a imagem para 100x100
# tela.foto_produto.setPixmap(pixmap_redimensionado)
# print(f"{hg.c_usuario}\\{hg.geral_cod_usuario}.jpg")

# lbl_operador = tela.findChild(QtWidgets.QLabel, "operador")
# if os.path.exists(f"{hg.c_usuario}\\{hg.geral_cod_usuario}.jpg"):
#     usuario = QPixmap(f"{hg.c_usuario}\\{hg.geral_cod_usuario}.jpg")
#
# else:
#     usuario = QPixmap(f"{hg.c_usuario}\\htiusu.jpg")
# pixmap_redimensionado = usuario.scaled(125, 130)  # redimensiona a imagem para 100x100
# tela.usuario.setPixmap(pixmap_redimensionado)
# lbl_operador.setText(f" Operador: {hg.geral_cod_usuario}")
lbl_numero_pedido = tela.findChild(QtWidgets.QLabel, "numero_pedido")

lbl_dinheiro = tela.findChild(QtWidgets.QLabel, "lb_dinheiro")
lbl_pix = tela.findChild(QtWidgets.QLabel, "lb_pix")
lbl_cartao = tela.findChild(QtWidgets.QLabel, "lb_cartao")
lbl_duplicata = tela.findChild(QtWidgets.QLabel, "lb_duplicata")
lbl_cheque = tela.findChild(QtWidgets.QLabel, "lb_cheque")
lbl_recebido = tela.findChild(QtWidgets.QLabel, "lb_recebido")
lbl_areceber = tela.findChild(QtWidgets.QLabel, "lb_areceber")

lbl_dinheiro.setText("0.00")
lbl_pix.setText("0.00")
lbl_cartao.setText("0.00")
lbl_duplicata.setText("0.00")
lbl_cheque.setText("0.00")
lbl_recebido.setText("0.00")
lbl_areceber.setText("0.00")


lbl_produto = tela.findChild(QtWidgets.QLabel, "produto")
lbl_produto.setText("F E C H A M E N T O   D O   C A I X A")
lbl_cabecalho = tela.findChild(QtWidgets.QLabel, "cabecalho")

tela_pg = uic.loadUi(f"{hg.c_ui}\\tipo_pagamento.ui")
# icon = QIcon(f"{hg.c_imagem}\\htiico.ico")
tela_pg.setWindowIcon(icon)
# icon_salvar = QIcon(f"{hg.c_imagem}\\confirma.png")
# icon_sair = QIcon(f"{hg.c_imagem}\\sair.png")
tela_pg.setWindowIcon(icon)
tela_pg.setWindowTitle(f"DADOS DO PAGAMENTO        {hg.SISTEMA}  Versao: {hg.VERSAO}")
lbl_valor = tela_pg.findChild(QtWidgets.QLabel, "lb_valor")
tela_pg.empresa.setPixmap(pixmap_redimensionado)
tela_pg.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, False)


conexao_banco()
# hg.conexao_cursor.execute("SELECT * FROM sacsetup")
# # # 145082Recupere o resultado
# m_set = hg.conexao_cursor.fetchone()
# hg.conexao_bd.commit()

hg.conexao_cursor.execute(f"SELECT razao, cod_cli FROM saccli ORDER BY razao")
arq_cli = hg.conexao_cursor.fetchall()
hg.conexao_bd.commit()
for ret_cli in arq_cli:
    item = f"{ret_cli[0]} - {str(ret_cli[1]).zfill(5)}".strip("(),")
    tela.cb_cliente.addItem(item)
tela.cb_cliente.setCurrentIndex(0)

data_atual = QDateTime.currentDateTime()
mnumero_pedido = ""
mcli_aux = 0

mtotal_pedido = 0
m_recebe = []
# tela.cb_forma_pg.addItems(
#     [
#         "1->Dinheiro",
#         "2->PIX",
#         "3->Cartao",
#         "4->Cartao Debito",
#         "5->Duplicata",
#         "6->Cheque",
#         "7->Financiamento",
#     ]
# )
# tela.cb_forma_pg.setCurrentIndex(0)  # coloca o focus no index

# rb_tipo_desconto_group = QButtonGroup()
# rb_tipo_desconto_group.addButton(tela.rb_percentual, id=1)
# rb_tipo_desconto_group.addButton(tela.rb_valor, id=2)
# tela.rb_valor.setChecked(True)


def fecha_tela():
    tela.close()
    # tela.closeEvent = on_close_event
    return


# def on_close_event(event):
#     print("esc")
#     tela.close()
#     event.accept()


def criar_tela():
    global mtotal_pedido
    tela.textBrowser.clear()
    lbl_numero_pedido.setText(f" Numero Pedido: {mnumero_pedido}")
    lbl_cabecalho.setText(f"Itens  Codigo   Descricao                  ")
    try:
        hg.conexao_cursor.execute(
            f"SELECT pcod_merc, pmerc, pquantd, pvlr_fat, COALESCE(pos, ' ') as app FROM sacped_s "
            f"WHERE pnum_ped = {mnumero_pedido}"
        )
        # # 145082Recupere o resultado
        resultados = hg.conexao_cursor.fetchall()
        hg.conexao_bd.commit()
        # print(resultados)

        lbl_sub_total = tela.findChild(QtWidgets.QLabel, "sub_total")
        # fonte = QtGui.QFont()
        # fonte.setFamily("Courier")
        # fonte.setPointSize(9)
        # tela.textBrowser.setFont(fonte)
        mtotal_geral = 0
        i = 0
        # Exibir os resultados no QTextEdit
        if len(resultados) > 0:
            for resultado in resultados:
                i += 1
                # ic(resultado[2], resultado[0])
                pcod_merc, pmerc, pquantd, pvlr_fat, pos = resultado
                # pcod_merc
                mquantd = "{:9,.3f}".format(pquantd)
                mvalor = "{:10,.2f}".format(pvlr_fat)
                soma = pquantd * pvlr_fat
                msoma = "{:12,.2f}".format(soma)
                linha = f"  {i}   {pcod_merc}  {pmerc}"
                linha1 = f"              {mquantd} x {mvalor} = {msoma}"
                mtotal_geral += soma
                # linha = " ".join(map(str, resultado))
                tela.textBrowser.append(linha)
                tela.textBrowser.append(linha1)
                # print(f"{hg.c_produto}\\{mcodigo}.jpg")
            mtotal_pedido = "{:12,.2f}".format(mtotal_geral)
            # VariavelP.mtotal_g = "{:12,.2f}".format(mtotal_geral)
            linha1 = f"SUB-TOTAL: {mtotal_pedido}"
            lbl_sub_total.setText(linha1)

    except Exception as e:
        print(f"Erro ao executar a consulta: {e}")


def salva_pedido():
    # ic("salva_pedido")
    index = tela.cb_cliente.currentIndex()
    mop = tela.cb_cliente.itemText(index)
    mcod_cli = mop[43:48]
    # ic(f"SELECT * FROM saccli WHERE cod_cli = {mcod_cli}")
    hg.conexao_cursor.execute(f"SELECT cod_cli, razao, nome, cgc, cpf, tipo FROM saccli WHERE cod_cli = {mcod_cli}")
    cons_cli = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()
    codigo_cli = int(mcod_cli)
    hg.conexao_cursor.execute(
        f"SELECT * FROM insopera WHERE scod_op = {hg.geral_cod_usuario}"
    )
    cons_oper = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()

    sql = (
        f"UPDATE sacped_s SET "
        f"pcgc = ?, "
        f"pcpf = ?, "
        f"pcod_cli = ?, "
        f"pcomi_oper = ?, "
        f"pcod_fin = ?, "
        f"pcod_tab = ?, "
        f"pvlr_pres = ?, "
        f"pcond_veze = ?, "
        f"pcond_inte = ?, "
        f"ptp_vend = ?, "
        f"pvlr_ent = ?, "
        f"pstat_item = ?, "
        f"pcod_vend = ?, "
        f"pvendedor = ?, "
        f"pcomissao = ?, "
        f"pdesc = ?, "
        f"pdesc_merc = ?, "
        f"pfecha = ? "
        f" WHERE pnum_ped = {mnumero_pedido}"
    )
    mcomissao = float(cons_oper[8])
    values = (
        cons_cli[3],
        cons_cli[4],
        codigo_cli,  # cod_cli
        mcomissao,  # comissao ooperador
        "",  # codigo finan
        "",  # cod tabela
        0,  # vlr presta
        "",  # cond vezes
        "",  # cond intenv
        "",  # tp_venda
        0,  # vlr_enta
        "",  # stat_itam
        "",  # cod_vend
        "",  # vendedor
        0,  # comissao
        0,  # desc
        0,  # desc_merc
        "F",  # fecha
    )
    hg.conexao_cursor.execute(sql, values)
    hg.conexao_bd.commit()

    hg.conexao_cursor.execute(f"SELECT * FROM sacped_s WHERE pnum_ped = {mnumero_pedido}")
    cons_ped = hg.conexao_cursor.fetchall()
    hg.conexao_bd.commit()
    mcontador = len(cons_ped)
    print(mcontador)
    for i in range(mcontador):
        sql = (
            "INSERT INTO sacmov ("
            "empresa,"
            "num_ped           ,"
            "data_ped          ,"
            "documento         ,"
            "codigo            ,"
            "gru_sub           ,"
            "produto           ,"
            "especie           ,"
            "cod_fab           ,"
            "fabrica           ,"
            "data_s_e          ,"
            "ent_sai           ,"
            "quantd            ,"
            "pr_venda1         ,"
            "pr_venda          ,"
            "vl_vend           ,"
            "vl_fatura         ,"
            "peso              ,"
            "cod_vend          ,"
            "cod_oper          ,"
            "cod_cli           ,"
            "cliente           ,"
            "tipo              ,"
            "pr_unit           ,"
            "cust_mer          ,"
            "isento            ,"
            "com_oper          ,"
            "tp_venda          ,"
            "cond_vezes        ,"
            "cond_intev        ,"
            "producao          ,"
            "comissao          ,"
            "montador          ,"
            "montador1         ,"
            "com_monta         ,"
            "com_monta1        ,"
            "convidado         ,"
            "cod_presente      ,"
            "sr_deleted)       "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
            "?, ?, ?, ?, ?, ?, ?) "
        )
        mdocumento = 'PD'+mnumero_pedido
        hg.conexao_cursor.execute(
            sql,
            (
                hg.mcodempresa,
                mnumero_pedido,
                cons_ped[i][3], # DATA DO PEDIDO
                mdocumento,
                cons_ped[i][5], # COD -PRODUTO
                cons_ped[i][4], # GRUPO
                cons_ped[i][6], # PRODUTO
                cons_ped[i][8], # ESPECIE
                cons_ped[i][29], # FABRICANTE
                cons_ped[i][30], # RAZAO
                hg.mdata_sis,
                'S',
                cons_ped[i][13], # QUANTD
                cons_ped[i][18], # PR_VENDA1
                cons_ped[i][19], # PR_VENDA
                cons_ped[i][18], # VL_VENDA
                cons_ped[i][18],
                cons_ped[i][10], # PESO
                hg.geral_cod_usuario,
                hg.geral_cod_usuario,
                codigo_cli, # cod_cli
                cons_cli[1], # razao
                '02',
                cons_ped[i][17], # pr_unit
                cons_ped[i][21], # cus_merc
                cons_ped[i][50], # isento
                0,
                ' ',
                '   ',
                '  ',
                ' ',
                0,
                ' ',
                ' ',
                0,
                0,
                cons_ped[i][104],
                cons_ped[i][98],
                ' '
            ),
        )
        hg.conexao_bd.commit()

    mvezes = len(m_recebe)
    mnum_dup = " "
    mdup_num = " "
    ic(mvezes)
    for i in range(mvezes):
        mhora = datetime.now().strftime("%H:%M:%S")
        venc_formatada = m_recebe[i][5]
        if m_recebe[i][0] == "DN":
            mnum_dup = mnumero_pedido
            mdup_num = "99999999"
        elif m_recebe[i][0] == "DU" or m_recebe[i][0] == "TR" or m_recebe[i][0] == "CR":
            mnum_dup = m_recebe[i][4]
            mdup_num = m_recebe[i][8]
        elif m_recebe[i][0] == "CH":
            mnum_dup = m_recebe[i][4]
            mdup_num = m_recebe[i][3]
        elif m_recebe[i][0] == "CT":
            mnum_dup = m_recebe[i][4]
            mdup_num = m_recebe[i][8]
        elif m_recebe[i][0] == "PX":
            mnum_dup = m_recebe[i][4]
            mdup_num = m_recebe[i][4]
        elif m_recebe[i][0] == "FI":
            mnum_dup = m_recebe[i][10]
            mdup_num = m_recebe[i][10]

        # CAIXA

        sql = (
            "INSERT INTO saccaixa ("
            "empresa, "
            "data, "
            "tipo, "
            "tipo_comp, "
            "nota, "
            "cod_cli, "
            "cod_vend, "
            "cod_opera, "
            "hora, "
            "valor_com, "
            "comissao, "
            "venci, "
            "valor, "
            "num_ban, "
            "cod_ct, "
            "c_s, "
            "num_dup, "
            "documento, "
            "descri2, "
            "obs, "
            "SR_DELETED) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) "
        )

        hg.conexao_cursor.execute(
            sql,
            (
                hg.mcodempresa,
                hg.mdata_sis,
                m_recebe[i][0],
                m_recebe[i][1],
                "PD" + mnumero_pedido,
                codigo_cli,
                hg.geral_cod_usuario,
                hg.geral_cod_usuario,
                mhora,
                m_recebe[i][9],
                0,
                venc_formatada,
                m_recebe[i][9],
                m_recebe[i][2],
                m_recebe[i][7],
                "",
                mnum_dup,
                mdup_num,
                m_recebe[i][11],
                m_recebe[i][18],
                " ",
            ),
        )
        hg.conexao_bd.commit()

        # CONTAS A RECEBER

        # if m_recebe[i][0] == "DN":
        #     mnum_dup = STRZERO(mnum_ped,6)
        # elif m_recebe[i][0] == "CH":
        #    mnum_dup = m_recebe[i,4]
        # elif m_recebe[i][0] == "DU" or m_recebe[i][0] == "TR" or m_recebe[i][0] == "CR":
        #     mnum_dup = m_recebe[i,5]
        # elif m_recebe[i][0] == "FI":
        #     mnum_dup = m_recebe[i,11]
        # elif m_recebe[i][0] == "CT":
        #     mnum_dup = m_recebe[i,9]
        mbaixar = "N"
        sql = (
            "INSERT INTO sacdupr ("
            "empresa         ,"
            "emissao         ,"
            "tipo            ,"
            "tip_cli         ,"
            "fornec          ,"
            "cliente         ,"
            "venc            ,"
            "venc1           ,"
            "comissao        ,"
            "comissao1       ,"
            "vlr_tab         ,"
            "operador        ,"
            "vendedor        ,"
            "num_ped         ,"
            "banco           ,"
            "ope_venda       ,"
            "ope_comi        ,"
            "mov_cx          ,"
            "c_cpfcnpj       ,"
            "numero          ,"
            "duplicata       ,"
            "valor_dup       ,"
            "valor           ,"
            "agencia         ,"
            "c_c             ,"
            "datpag          ,"
            "vlpago          ,"
            "pago            ,"
            "corrente        ,"
            "cpfcnpj         ,"
            "vl_ipi          ,"
            "com_sem         ,"
            "obs           ,"
            "SR_DELETED) "
            "VALUES (?,?,?,?,?,?,?,?,?,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,? ,' ') "
        )
        if len(cons_cli[3]) > 0:
            mcgccpf = cons_cli[3]
        else:
            mcgccpf = cons_cli[4]

        if m_recebe[i][0] == "FI" or m_recebe[i][0] == "CT":
            mtip = m_recebe[i][7]
        else:
            mtip = m_recebe[i][2]

        if m_recebe[i][0] == "CT":
            mvlr = m_recebe[i][9] - (m_recebe[i][9] * (m_recebe[i][15] / 100))
        else:
            mvlr = m_recebe[i][9]

        if (m_recebe[i][0] == "DN" or m_recebe[i][0] == "CR" or m_recebe[i][0] == "PX" or
                ((m_recebe[i][0] == "CT" or m_recebe[i][0] == "CH") and m_recebe[i][5] <= hg.mdata_sis
                 and mbaixar == "S")):
            mdata_pg = m_recebe[i][5]
        else:
            mdata_pg = None

        if (m_recebe[i][0] == "DN" or m_recebe[i][0] == "CR" or m_recebe[i][0] == "PX" or
                ((m_recebe[i][0] == "CT" or m_recebe[i][0] == "CH") and m_recebe[i][5] <= hg.mdata_sis
                 and mbaixar == "S")):
            mvlr_pago = m_recebe[i][9]
        else:
            mvlr_pago = 0

        if (m_recebe[i][0] == "DN" or m_recebe[i][0] == "CR" or m_recebe[i][0] == "PX" or
                ((m_recebe[i][0] == "CT" or m_recebe[i][0] == "CH") and m_recebe[i][5] <= hg.mdata_sis
                 and mbaixar == "S")):
            mpago = "B"
        else:
            mpago = " "

        if m_recebe[i][0] == "CH":
            mcnpjcfp = m_recebe[i][15]
        else:
            mcnpjcfp = " "

        mperc_comissao = 0
        mperc_com1 = 0
        mvlr_tab = 0
        print(sql,(
                hg.mcodempresa,
                hg.mdata_sis,
                m_recebe[i][0],
                cons_cli[5],
                codigo_cli,
                cons_cli[1],
                m_recebe[i][5],
                m_recebe[i][5],
                mperc_comissao,
                mperc_com1,
                mvlr_tab,
                hg.geral_cod_usuario,
                hg.geral_cod_usuario,
                mnumero_pedido,
                m_recebe[i][6],
                hg.geral_cod_usuario,
                0,
                "C",
                mcgccpf,
                mtip,
                mnum_dup,
                m_recebe[i][9],
                mvlr,
                m_recebe[i][12],
                m_recebe[i][13],
                mdata_pg,
                mvlr_pago,
                mpago,
                m_recebe[i][14],
                mcnpjcfp,
                0,
                '',
                m_recebe[i][18]))

        hg.conexao_cursor.execute(
            sql,
            (
                hg.mcodempresa,
                hg.mdata_sis,
                m_recebe[i][0],
                cons_cli[5],
                codigo_cli,
                cons_cli[1],
                m_recebe[i][5],
                m_recebe[i][5],
                mperc_comissao,
                mperc_com1,
                mvlr_tab,
                hg.geral_cod_usuario,
                hg.geral_cod_usuario,
                mnumero_pedido,
                m_recebe[i][6],
                hg.geral_cod_usuario,
                0,
                "C",
                mcgccpf,
                mtip,
                mnum_dup,
                m_recebe[i][9],
                mvlr,
                m_recebe[i][12],
                m_recebe[i][13],
                mdata_pg,
                mvlr_pago,
                mpago,
                m_recebe[i][14],
                mcnpjcfp,
                0,
                "",
                m_recebe[i][18]
            ),
        )
        hg.conexao_bd.commit()


    # ic(m_recebe)
    # print(sql, values)
    m_recebe.clear()
    return
    # fecha_tela()


def verifica_condicao():
    # ic("verifica_condicao")
    global m_recebe
    mdin = 0
    mpx = 0
    mct = 0
    mdu = 0
    mch = 0

    tela.ds_dinheiro.editingFinished.disconnect()
    tela.ds_pix.editingFinished.disconnect()
    tela.ds_cartao.editingFinished.disconnect()
    tela.ds_duplicata.editingFinished.disconnect()
    tela.ds_cheque.editingFinished.disconnect()

    mvalor_dinheiro = tela.ds_dinheiro.value()
    mvalor_pix = tela.ds_pix.value()
    mvalor_cartao = tela.ds_cartao.value()
    mvalor_duplicata = tela.ds_duplicata.value()
    mvalor_cheque = tela.ds_cheque.value()
    # if mvalor_dinheiro == 0 and mvalor_pix == 0 and mvalor_cartao == 0 and mvalor_duplicata == 0 and mcheque == 0:
    #     ic()
    #     return
    # tela.ds_entrada.setValue(float(0))
    # tela.ds_qtd_dias.setValue(float(0))

    index = tela.cb_cliente.currentIndex()
    mop = tela.cb_cliente.itemText(index)
    # mcod_cli = mop[0:5]
    # index = tela.cb_forma_pg.currentIndex()
    # mop = tela.cb_forma_pg.itemText(index)
    # m_tipo_pag = mop[0:1]
    # # ic(m_tipo_pag)
    # if m_tipo_pag == "2":
    #     tela.ds_dia1.setValue(float(1))
    #     tela.ds_qtd_dias.setValue(float(1))
    # elif m_tipo_pag == "3":
    #     tela.ds_qtd_dias.setEnabled(True)
    #     tela.ds_qtd_dias.setFocus()
    #     tela.ds_qtd_dias.selectAll()
    # elif m_tipo_pag == "4" or m_tipo_pag == "5":
    #     tela.ds_entrada.setEnabled(True)
    #     tela.ds_qtd_dias.setEnabled(True)
    #     tela.ds_entrada.setFocus()
    #     tela.ds_entrada.selectAll()
    #
    # hg.conexao_cursor.execute(f"SELECT * FROM saccli WHERE cod_cli = {mcod_cli}")
    # cons_cli = hg.conexao_cursor.fetchone()
    # hg.conexao_bd.commit()
    # if len(cons_cli) > 0 and cons_cli[58] > 0 and m_tipo_pag != "3":
    #     mdesc = cons_cli[58] / 100
    #     atencao(
    #         f"ESTE CLIENTE: {cons_cli[1]} - {cons_cli[2]} TERA UM DESCONTO DE: {cons_cli[58]}"
    #     )
    #
    # elif (
    #     (m_tipo_pag == "1" or m_tipo_pag == "2" or hg.m_set[34] == "S")
    #     and hg.m_set[104] == "S"
    #     or (m_tipo_pag == "6" and ver_serie() == "141416")
    # ) and m_tipo_pag != "3":
    #     tela.rb_percentual.setEnabled(True)
    #     tela.rb_valor.setEnabled(True)
    #     tela.ds_desconto.setEnabled(True)
    # print(f"SELECT pcod_merc, pmerc, pquantd, pvlr_fat, COALESCE(pos, " ") as app FROM sacped_s "
    #      f"WHERE pnum_ped = "{mnumero_pedido}"")
    hg.conexao_cursor.execute(f"SELECT pcod_merc, pmerc, pquantd, pvlr_fat, COALESCE(pos, ' ') as app FROM sacped_s "
                              f"WHERE pnum_ped = {mnumero_pedido}")
    # # 145082Recupere o resultado
    resultados = hg.conexao_cursor.fetchall()
    hg.conexao_bd.commit()
    # print(resultados)
    # print(resultados[0][1])
    mos = str(resultados[0][4])
    if mvalor_dinheiro != 0:
        m_recebe.append(
            [
                "DN",
                "AV",
                "   ",
                "      ",
                "99999999",
                hg.mdata_sis,
                "C",
                "   ",
                "",
                mvalor_dinheiro,
                "",
                "",
                "        ",
                "             ",
                "",
                "",
                "",
                "",
                " OS:",
            ]
        )

        tela.ds_dinheiro.setValue(float(0))
    if mvalor_pix != 0:
        m_recebe.append(
            [
                "PX",
                "AV",
                "   ",
                "      ",
                "99999999",
                hg.mdata_sis,
                "C",
                "   ",
                "",
                mvalor_pix,
                "",
                "",
                "        ",
                "             ",
                "",
                "",
                "",
                "",
                " OS:",
            ]
        )

        tela.ds_pix.setValue(float(0))

    if mvalor_cartao > 0:
        index = tela_pg.cb_tipo_pg.currentIndex()
        mop = tela_pg.cb_tipo_pg.itemText(index)
        mcod_pag = mop[0:3]
        mnumero = tela_pg.n_documento.text()
        ic(mcod_pag)
        hg.conexao_cursor.execute(
            f"SELECT codigo, descri, percent, cond, COALESCE(dia1, 0), COALESCE(dia2, 0) , "
            f"COALESCE(dia3, 0), COALESCE(dia4, 0), COALESCE(dia5, 0), COALESCE(dia6, 0), "
            f"COALESCE(dia7, 0), COALESCE(dia8, 0), COALESCE(dia9, 0), COALESCE(dia10, 0), "
            f"COALESCE(dia11, 0), COALESCE(dia12, 0), COALESCE(dia13, 0), COALESCE(dia14, 0), "
            f"COALESCE(dia15, 0), cod_forn, tipo_conta, percent FROM sactabpg WHERE codigo = {mcod_pag}"
        )
        # Recupere o resultado
        arq_sactabpg = hg.conexao_cursor.fetchone()
        hg.conexao_bd.commit()
        mvezes = tela_pg.sb_qtd_parcelas.value()
        # mvezes = int(arq_sactabpg[3][1:3])
        # ndia = arq_sactabpg[4]
        mdia = 30
        mpercentual = float(arq_sactabpg[21])
        mcod_forn = arq_sactabpg[19]
        mtipo_conta = arq_sactabpg[20]
        ic(
            f"vezes {mvezes} dias {mdia} fornecedor {mcod_forn} tipo_conta {mtipo_conta}"
        )

        if mdia > 0:
            #     //               1    2       3      4         5       6          7           8                 9            10          11      12       13       14        15         16            17            18
            #     AADD(m_recebe,{"CT","AP",SPACE(3),SPACE(6),mn_dup,m_parcela[i,2],"B",STRZERO(mcod_cart,3),m_parcela[i,1],m_parcela[i,3],mn_fin,mcartao,SPACE(8),SPACE(13),mcorrente,mdesc_cart,m_parcela[i,4],m_parcela[i,5],IF(EMPTY(VAL(ALLTRIM(cons_ped[1,94]))),""," OS:"+ALLTRIM(cons_ped[1,94]))})
            # nova_data = data_atual.addDays(mdia)
            mvalor_parcela = mvalor_cartao / mvezes
            mvalor = round(mvalor_parcela, 2)
            mvalor_parcela = mvalor
            mdiferenca = round(mvalor_cartao - (mvalor_parcela * mvezes), 2)
            ic(
                f"valor cartao {mvalor_cartao} vezes {mvezes} diferenca {mdiferenca} parcela {mvalor_parcela}"
            )
            # if mdiferenca > 0:
            for i in range(mvezes):
                mdia = mdia * (i + 1)
                mdata_sis = QDate.fromString(hg.mdata_sis, "yyyy-MM-dd")
                # Verifique se a conversão foi bem-sucedida
                if not mdata_sis.isValid():
                    print(f"Data inválida: {hg.mdata_sis}")

                mdata_f = mdata_sis.addDays(mdia)
                mdata_venc = mdata_f.toString("yyyy-MM-dd")
                mvalor_p = mvalor_parcela + mdiferenca
                mdiferenca = 0
                m_recebe.append(
                    [
                        "CT",
                        "AP",
                        "   ",
                        "      ",
                        mnumero,
                        mdata_venc,
                        "B",
                        mcod_pag,
                        f"{mnumero}-{i+1}/{mvezes}",
                        mvalor_p,
                        "",
                        mnumero,
                        "        ",
                        "             ",
                        "",
                        mpercentual,
                        mcod_forn,
                        mtipo_conta,
                        " OS:",
                    ]
                )
                mdia = mdia + 30
        else:
            mdata_sis = QDate.fromString(hg.mdata_sis, "yyyy-MM-dd")
            m_recebe.append(
                [
                    "CT",
                    "AV",
                    "   ",
                    "      ",
                    mnumero,
                    mdata_sis,
                    "B",
                    mcod_pag,
                    f"{mnumero}-{mvezes}/1",
                    mvalor_cartao,
                    "",
                    "",
                    "        ",
                    "             ",
                    "",
                    mpercentual,
                    mcod_forn,
                    mtipo_conta,
                    " OS:",
                ]
            )

        tela.ds_cartao.setValue(float(0))

    if mvalor_duplicata > 0:
        index = tela_pg.cb_tipo_pg.currentIndex()
        mop = tela_pg.cb_tipo_pg.itemText(index)
        mcod_pag = mop[0:3]
        mnumero = tela_pg.n_documento.text()
        ic(mcod_pag)
        hg.conexao_cursor.execute(
            f"SELECT codigo, descri, percent, cond, COALESCE(dia1, 0), COALESCE(dia2, 0) , "
            f"COALESCE(dia3, 0), COALESCE(dia4, 0), COALESCE(dia5, 0), COALESCE(dia6, 0), "
            f"COALESCE(dia7, 0), COALESCE(dia8, 0), COALESCE(dia9, 0), COALESCE(dia10, 0), "
            f"COALESCE(dia11, 0), COALESCE(dia12, 0), COALESCE(dia13, 0), COALESCE(dia14, 0), "
            f"COALESCE(dia15, 0), cod_forn, tipo_conta, percent FROM sactabpg WHERE codigo = {mcod_pag}"
        )
        arq_sactabpg = hg.conexao_cursor.fetchone()
        hg.conexao_bd.commit()
        mvezes = tela_pg.sb_qtd_parcelas.value()
        mdia = int(arq_sactabpg[4])
        mpercentual = float(arq_sactabpg[21])
        mcod_forn = arq_sactabpg[19]
        mtipo_conta = arq_sactabpg[20]
        ic(
            f"vezes {mvezes} dias {mdia} fornecedor {mcod_forn} tipo_conta {mtipo_conta}"
        )

        if mdia > 0:
            #     //               1    2       3      4         5       6          7           8                 9            10          11      12       13       14        15         16            17            18
            #     AADD(m_recebe,{"CT","AP",SPACE(3),SPACE(6),mn_dup,m_parcela[i,2],"B",STRZERO(mcod_cart,3),m_parcela[i,1],m_parcela[i,3],mn_fin,mcartao,SPACE(8),SPACE(13),mcorrente,mdesc_cart,m_parcela[i,4],m_parcela[i,5],IF(EMPTY(VAL(ALLTRIM(cons_ped[1,94]))),""," OS:"+ALLTRIM(cons_ped[1,94]))})
            # nova_data = data_atual.addDays(mdia)
            mvalor_parcela = mvalor_duplicata / mvezes
            mvalor = round(mvalor_parcela, 2)
            mvalor_parcela = mvalor
            mdiferenca = round(mvalor_duplicata - (mvalor_parcela * mvezes), 2)
            ic(
                f"valor cartao {mvalor_duplicata} vezes {mvezes} diferenca {mdiferenca} parcela {mvalor_parcela}"
            )
            # if mdiferenca > 0:
            for i in range(mvezes):
                mdia = int(arq_sactabpg[4 * (i + 1)])
                mdata_sis = QDate.fromString(hg.mdata_sis, "yyyy-MM-dd")
                if not mdata_sis.isValid():
                    print(f"Data inválida: {hg.mdata_sis}")

                mdata_f = mdata_sis.addDays(mdia)
                mdata_venc = mdata_f.toString("yyyy-MM-dd")
                mvalor_p = mvalor_parcela + mdiferenca
                mdiferenca = 0
                m_recebe.append(
                    [
                        "DU",
                        "AP",
                        "   ",
                        "      ",
                        mnumero,
                        mdata_venc,
                        "B",
                        mcod_pag,
                        f"{mnumero}-{i+1}/{mvezes}",
                        mvalor_p,
                        "",
                        mnumero,
                        "        ",
                        "             ",
                        "",
                        mpercentual,
                        mcod_forn,
                        mtipo_conta,
                        " OS:",
                    ]
                )
        else:
            mdata_sis = QDate.fromString(hg.mdata_sis, "yyyy-MM-dd")
            m_recebe.append(
                [
                    "DU",
                    "AV",
                    "   ",
                    "      ",
                    mnumero,
                    mdata_sis,
                    "B",
                    mcod_pag,
                    f"{mnumero}-{mvezes}/1",
                    mvalor_duplicata,
                    "",
                    "",
                    "        ",
                    "             ",
                    "",
                    mpercentual,
                    mcod_forn,
                    mtipo_conta,
                    " OS:",
                ]
            )
        tela.ds_duplicata.setValue(float(0))

    if mvalor_cheque > 0:
        m_recebe.append(
            [
                "CH",
                "AV",
                "   ",
                "      ",
                "99999999",
                hg.mdata_sis,
                "C",
                "   ",
                "",
                mvalor_cheque,
                "",
                "",
                "        ",
                "             ",
                "",
                "",
                "",
                "",
                " OS:",
            ]
        )

        tela.ds_cheque.setValue(float(0))

        # print(m_recebe[0])
    # i = 0
    total_recebido = 0
    total_areceber = 0
    for i in range(len(m_recebe)):
        # for recebe in m_recebe:
        mtipo = m_recebe[i][0]
        mvlr = m_recebe[i][9]
        mvlr_tx = float(mvlr)
        # print(mtipo)
        if mtipo == "DN":
            mdin += mvlr_tx
        if mtipo == "PX":
            mpx += mvlr_tx
        if mtipo == "CT":
            mct += mvlr_tx
        if mtipo == "DU":
            mdu += mvlr_tx
        if mtipo == "CH":
            mch += mvlr_tx
        total_recebido = total_recebido + mvlr_tx
        ic(total_recebido)
        mtot_total = float(mtotal_pedido)
        total_areceber = mtot_total - total_recebido

    total_f = "{:12,.2f}".format(total_recebido)
    mtotal_tx = f"{total_f}"

    total_ar = "{:12,.2f}".format(total_areceber)
    mareceber_tx = f"{total_ar}"

    mdin_f = "{:12,.2f}".format(mdin)
    mdin_tx = f"{mdin_f}"

    mpix_f = "{:12,.2f}".format(mpx)
    mpix_tx = f"{mpix_f}"

    mct_f = "{:12,.2f}".format(mct)
    mct_tx = f"{mct_f}"

    mdu_f = "{:12,.2f}".format(mdu)
    mdu_tx = f"{mdu_f}"

    mch_f = "{:12,.2f}".format(mch)
    mch_tx = f"{mch_f}"

    lbl_dinheiro.setText(mdin_tx)
    lbl_pix.setText(mpix_tx)
    lbl_cartao.setText(mct_tx)
    lbl_duplicata.setText(mdu_tx)
    lbl_cheque.setText(mch_tx)
    lbl_recebido.setText(mtotal_tx)
    lbl_areceber.setText(mareceber_tx)
    tela.ds_dinheiro.editingFinished.connect(verifica_condicao)
    tela.ds_pix.editingFinished.connect(verifica_condicao)
    tela.ds_cartao.editingFinished.connect(condicao_pagamento)
    tela.ds_duplicata.editingFinished.connect(condicao_pagamento)
    tela.ds_cheque.editingFinished.connect(verifica_condicao)
    mt_pedido = float(mtotal_pedido)
    mt_recebido = float(total_recebido)
    ic(f"pedido {float(mtotal_pedido)} - recebido {float(total_recebido)}")
    if mt_recebido >= mt_pedido:
        salva_pedido()
        m_recebe.clear()
        fecha_tela()
        # return

    # ic(m_recebe)
    # if mvalor_dinheiro == mtotal_pedido:
    #     mvalor = mvalor_dinheiro
    #
    #     m_recebe.append("DN")   # ,"AV","   ","      ","99999999",data_atual,"C","   ",mn_cupom,mvalor,mn_fin,mcartao,SPACE(8),SPACE(13),mcorrente," "," "," ",IF(EMPTY(VAL(ALLTRIM(cons_ped[1,94]))),""," OS:"+ALLTRIM(cons_ped[1,94])))}
    #     m_recebe.append("AV")   # ,"   ","      ","99999999",data_atual,"C","   ",mn_cupom,mvalor,mn_fin,mcartao,SPACE(8),SPACE(13),mcorrente," "," "," ",IF(EMPTY(VAL(ALLTRIM(cons_ped[1,94]))),""," OS:"+ALLTRIM(cons_ped[1,94])))}
    # elif mvalor_dinheiro == 0 and mn_banco ==  .AND. EMPTY(mn_cred) .AND. EMPTY(mn_pix) .AND. ;
    #       EMPTY(mn_dup) .AND. EMPTY(mcod_cart) .AND. EMPTY(mn_fin) .AND. EMPTY(mn_trans) .AND. LEN(m_parcela) = 0);
    #       .OR. mvalor_dinheiro = mtot_nota:
    #   IF ! EMPTY(mvalor_dinheiro)   //.OR. mvalor_dinheiro = mtot_nota
    #       IF mvalor_dinheiro + mtot_verif > mtot_nota
    #           mvalor = mtot_nota - mtot_verif
    #           mtroco = mvalor_dinheiro+mtot_verif - mtot_nota
    #           SUB_BANNER(30,01,"Troco:"+TRANSFORM(mtroco,"999,999.99"))
    #           INKEY(,10)
    #           INKEY(30)
    #       ELSE
    #           mvalor = mvalor_dinheiro
    #       ENDIF
    #       AADD(m_alt,"DINHEIRO...: Valor: "+TRANSFORM(mvalor_dinheiro,"999,999.99"))
    #       AADD(m_recebe,{"DN","AV",SPACE(3),SPACE(6),"99999999",mdata_sis,"C",STRZERO(mcod_cart,3),mn_cupom,mvalor,mn_fin,mcartao,SPACE(8),SPACE(13),mcorrente," "," "," ",IF(EMPTY(VAL(ALLTRIM(cons_ped[1,94]))),""," OS:"+ALLTRIM(cons_ped[1,94]))})
    #   ELSE
    #       IF ! EMPTY(mn_cheque)
    #           IF (mvalor + mtot_verif) - mtot_nota > .01
    #               mcred_cheq = op_simnao("S","O Valor de R$:"+TRANSFORM(mvalor+mtot_verif - mtot_nota,"999,999.99")+"  vai ser gerado um CREDITO para o cliente:")
    #               IF  mcred_cheq = "N"
    #                   LOOP
    #               ENDIF
    #               mvlr_credcheq = mvalor+mtot_verif - mtot_nota
    #               IF mvencimento > mdata_sis
    # *       	                                                         1    2      3         4       5        6       7         8                 9      10     11     12       13     14      15        16   17  18       19
    #                   AADD(m_recebe,{"CH","AP",mn_banco,mn_cheque,mn_dup,mvencimento,"B",STRZERO(mcod_cart,3),mn_cupom,mvalor,mn_fin,mcartao,magencia,mc_c,mcorrente,mcpfcnpj," "," ","CREDITO P/ CLIENTE DE R$:"+TRANSFORM(mvalor+mtot_verif - mtot_nota,"999,999.99")+IF(EMPTY(VAL(ALLTRIM(cons_ped[1,94]))),""," OS:"+ALLTRIM(cons_ped[1,94]))})
    #                   mqtd_doc ++
    #                   mqtd_dias = mqtd_dias + (mvencimento - mdata_sis)
    #               ELSE
    #                   AADD(m_recebe,{"CH","AV",mn_banco,mn_cheque,mn_dup,mvencimento,"B",STRZERO(mcod_cart,3),mn_cupom,mvalor,mn_fin,mcartao,magencia,mc_c,mcorrente,mcpfcnpj," "," ","CREDITO P/ CLIENTE DE R$:"+TRANSFORM(mvalor+mtot_verif - mtot_nota,"999,999.99")+IF(EMPTY(VAL(ALLTRIM(cons_ped[1,94]))),""," OS:"+ALLTRIM(cons_ped[1,94]))})
    #               ENDIF
    #           ELSE
    #               IF mvencimento > mdata_sis
    # *       	                                                         1    2      3         4       5        6       7         8                 9      10     11     12       13     14      15        16   17  18   19
    #                   AADD(m_recebe,{"CH","AP",mn_banco,mn_cheque,mn_dup,mvencimento,"B",STRZERO(mcod_cart,3),mn_cupom,mvalor,mn_fin,mcartao,magencia,mc_c,mcorrente,mcpfcnpj," "," ",IF(EMPTY(VAL(ALLTRIM(cons_ped[1,94]))),""," OS:"+ALLTRIM(cons_ped[1,94]))})
    #                   mqtd_doc ++
    #                   mqtd_dias = mqtd_dias + (mvencimento - mdata_sis)
    #               ELSE
    #                   AADD(m_recebe,{"CH","AV",mn_banco,mn_cheque,mn_dup,mvencimento,"B",STRZERO(mcod_cart,3),mn_cupom,mvalor,mn_fin,mcartao,magencia,mc_c,mcorrente,mcpfcnpj," "," ",IF(EMPTY(VAL(ALLTRIM(cons_ped[1,94]))),""," OS:"+ALLTRIM(cons_ped[1,94]))})
    #               ENDIF
    #           ENDIF
    #           AADD(m_alt,"CHEQUE.....: Bco.: "+mn_banco+" No: "+mn_cheque+" Venc: "+DTOC(mvencimento)+" Vlr:"+TRANSFORM(mvalor,"999,999.99"))
    #       ELSEIF ! EMPTY(mn_dup)
    #           i = 0
    #           FOR i = 1 TO LEN(m_parcela)
    #               IF EMPTY(m_parcela[i,1])
    #                   LOOP
    #               ENDIF
    #               AADD(m_alt,"DUPLICATA..: No.:"+m_parcela[i,1]+" Venc:"+DTOC(m_parcela[i,2])+" Vlr:"+TRANSFORM(m_parcela[i,3],"999,999.99"))
    #               IF m_parcela[i,2] > mdata_sis
    #                   AADD(m_recebe,{"DU","AP",mn_banco,SPACE(6),m_parcela[i,1],m_parcela[i,2],mt_pag,STRZERO(mcod_cart,3),m_parcela[i,1],m_parcela[i,3],mn_fin,mcartao,SPACE(8),SPACE(13),mcorrente," "," "," ",IF(EMPTY(VAL(ALLTRIM(cons_ped[1,94]))),""," OS:"+ALLTRIM(cons_ped[1,94]))})
    #                   mqtd_doc ++
    #                   mqtd_dias = mqtd_dias + (m_parcela[i,2] - mdata_sis)
    #               ELSE
    #                   AADD(m_recebe,{"DU","AV",mn_banco,SPACE(6),m_parcela[i,1],m_parcela[i,2],mt_pag,STRZERO(mcod_cart,3),m_parcela[i,1],m_parcela[i,3],mn_fin,mcartao,SPACE(8),SPACE(13),mcorrente," "," "," ",IF(EMPTY(VAL(ALLTRIM(cons_ped[1,94]))),""," OS:"+ALLTRIM(cons_ped[1,94]))})
    #               ENDIF
    #           NEXT
    #       ELSEIF ! EMPTY(mn_cupom)
    #           i = 0
    #           FOR i = 1 TO LEN(m_parcela)
    #               IF EMPTY(m_parcela[i,1])
    #                   LOOP
    #               ENDIF
    #               AADD(m_alt,"CARTAO.....: "+STRZERO(mcod_cart,3)+" Cupom No.: "+m_parcela[i,1]+" Valor: "+TRANSFORM(m_parcela[i,3],"999,999.99"))
    #               IF m_parcela[i,2] > mdata_sis
    # //               1    2       3      4         5       6          7           8                 9            10          11      12       13       14        15         16            17            18
    #                   AADD(m_recebe,{"CT","AP",SPACE(3),SPACE(6),mn_dup,m_parcela[i,2],"B",STRZERO(mcod_cart,3),m_parcela[i,1],m_parcela[i,3],mn_fin,mcartao,SPACE(8),SPACE(13),mcorrente,mdesc_cart,m_parcela[i,4],m_parcela[i,5],IF(EMPTY(VAL(ALLTRIM(cons_ped[1,94]))),""," OS:"+ALLTRIM(cons_ped[1,94]))})
    #                   mqtd_doc ++
    #                   mqtd_dias = mqtd_dias + (m_parcela[i,2] - mdata_sis)
    #               ELSE
    #
    #                   AADD(m_recebe,{"CT","AV",SPACE(3),SPACE(6),mn_dup,m_parcela[i,2],"B",STRZERO(mcod_cart,3),m_parcela[i,1],m_parcela[i,3],mn_fin,mcartao,SPACE(8),SPACE(13),mcorrente,mdesc_cart,m_parcela[i,4],m_parcela[i,5],IF(EMPTY(VAL(ALLTRIM(cons_ped[1,94]))),""," OS:"+ALLTRIM(cons_ped[1,94]))})
    #               ENDIF
    #           NEXT
    #       ELSEIF ! EMPTY(mn_fin)  // .OR. LEN(m_parcela) > 0
    #           i = 0
    #           FOR i = 1 TO LEN(m_parcela)
    #               IF EMPTY(m_parcela[i,1])
    #                   LOOP
    #               ENDIF
    #               AADD(m_alt,"FINANCIAMEN: "+m_parcela[i,1]+" Venc.: "+DTOC(m_parcela[i,2])+" Vlr: "+TRANSFORM(m_parcela[i,3],"999,999.99"))
    #               IF m_parcela[i,2] > mdata_sis
    #                   AADD(m_recebe,{"FI","AP",SPACE(3),SPACE(6),mn_dup,m_parcela[i,2],"B",STRZERO(mcod_cart,3),mn_cupom,m_parcela[i,3],m_parcela[i,1],mcartao,SPACE(8),SPACE(13),mcorrente," "," "," ",IF(EMPTY(VAL(ALLTRIM(cons_ped[1,94]))),""," OS:"+ALLTRIM(cons_ped[1,94]))})
    #                   mqtd_doc ++
    #                   mqtd_dias = mqtd_dias + (m_parcela[i,2] - mdata_sis)
    #               ELSE
    #                   AADD(m_recebe,{"FI","AV",SPACE(3),SPACE(6),mn_dup,m_parcela[i,2],"B",STRZERO(mcod_cart,3),mn_cupom,m_parcela[i,3],m_parcela[i,1],mcartao,SPACE(8),SPACE(13),mcorrente," "," "," ",IF(EMPTY(VAL(ALLTRIM(cons_ped[1,94]))),""," OS:"+ALLTRIM(cons_ped[1,94]))})
    #               ENDIF
    #           NEXT
    #       ELSEIF ! EMPTY(mn_trans)
    #           AADD(m_alt,"TRANSFERENC: "+mn_trans+" Venc.: "+DTOC(mvencimento)+" Valor: "+TRANSFORM(mvalor,"999,999.99"))
    #           AADD(m_recebe,{"TR","AP",SPACE(3),SPACE(6),mn_trans,mvencimento,mt_pag,STRZERO(mcod_cart,3),mn_cupom,mvalor,mn_fin,mcartao,SPACE(8),SPACE(13),mcorrente," "," "," ",IF(EMPTY(VAL(ALLTRIM(cons_ped[1,94]))),""," OS:"+ALLTRIM(cons_ped[1,94]))})
    #       ELSEIF ! EMPTY(mn_cred)
    #           mtipo_pg = 1
    #           mcredito = mcredito - mvalor
    #           AADD(m_alt,"CREDITO....: "+mn_cred+" Venc.: "+DTOC(mvencimento)+" Valor: "+TRANSFORM(mvalor,"999,999.99"))
    #           AADD(m_recebe,{"CR","AV",SPACE(3),SPACE(6),mn_cred,mvencimento,mt_pag,STRZERO(mcod_cart,3),mn_cupom,mvalor,mn_fin,mcartao,SPACE(8),SPACE(13),mcorrente," "," "," ",IF(EMPTY(VAL(ALLTRIM(cons_ped[1,94]))),""," OS:"+ALLTRIM(cons_ped[1,94]))})
    #       ELSEIF ! EMPTY(mn_pix)
    #           AADD(m_alt,"No.PIX.....: "+mn_pix+" Venc.: "+DTOC(mvencimento)+" Valor: "+TRANSFORM(mvalor,"999,999.99"))
    #           AADD(m_recebe,{"PX","AV",SPACE(3),SPACE(6),mn_pix,mvencimento,mt_pag,STRZERO(mcod_cart,3),mn_cupom,mvalor,mn_fin,mcartao,SPACE(8),SPACE(13),mcorrente," "," "," ",IF(EMPTY(VAL(ALLTRIM(cons_ped[1,94]))),""," OS:"+ALLTRIM(cons_ped[1,94]))})
    #       ENDIF
    # ENDIF
    # ENDIF
    # tela.ds_dinheiro.setFocus()
    # tela.ds_dinheiro.selectAll()
    # tela.ds_dinheiro.editingFinished.connect(verifica_condicao)
    # tela.ds_pix.editingFinished.connect(verifica_condicao)
    # tela.ds_cartao.editingFinished.connect(condicao_pagamento)
    # tela.ds_duplicata.editingFinished.connect(verifica_condicao)
    # tela.ds_cheque.editingFinished.connect(verifica_condicao)


def limpa_valores():
    tela.ds_dinheiro.setFocus()
    tela.ds_dinheiro.setValue(float(0))
    tela.ds_pix.setValue(float(0))
    tela.ds_cartao.setValue(float(0))
    tela.ds_duplicata.setValue(float(0))
    tela.ds_cheque.setValue(float(0))


def condicao_pagamento():
    tela_pg.sb_qtd_parcelas.setEnabled(False)
    tela_pg.cb_tipo_pg.clear()
    mcart = tela.ds_cartao.value()
    mdupli = tela.ds_duplicata.value()
    mcheq = tela.ds_cheque.value()
    tela_pg.sb_qtd_parcelas.setValue(0)
    if mcart > 0:
        tela_pg.sb_qtd_parcelas.setEnabled(True)
        mct_f = "{:12,.2f}".format(mcart)
        mct_tx = f"{mct_f}"
        lbl_valor.setText(mct_tx)
        tela_pg.n_documento.setText(mnumero_pedido)
        mtipo_pg = "CT"
    elif mdupli > 0:
        mct_f = "{:12,.2f}".format(mdupli)
        mct_tx = f"{mct_f}"
        lbl_valor.setText(mct_tx)
        tela_pg.n_documento.setText(mnumero_pedido)
        mtipo_pg = "DU"
    elif mcheq > 0:
        mct_f = "{:12,.2f}".format(mcheq)
        mct_tx = f"{mct_f}"
        lbl_valor.setText(mct_tx)
        mtipo_pg = "CH"
    else:
        return

    hg.conexao_cursor.execute(
        f"SELECT codigo, descri, percent, cond, COALESCE(dia1, 0), COALESCE(dia2, 0) , "
        f"COALESCE(dia3, 0), COALESCE(dia4, 0), COALESCE(dia5, 0), COALESCE(dia6, 0), "
        f"COALESCE(dia7, 0), COALESCE(dia8, 0), COALESCE(dia9, 0), COALESCE(dia10, 0), "
        f"COALESCE(dia11, 0), COALESCE(dia12, 0), COALESCE(dia13, 0), COALESCE(dia14, 0), "
        f"COALESCE(dia15, 0) FROM sactabpg WHERE sigla = {mtipo_pg} ORDER BY codigo"
    )
    # Recupere o resultado
    arq_sactabpg = hg.conexao_cursor.fetchall()
    hg.conexao_bd.commit()

    # tela_pg.cb_tipo_pg.addItem("000-DEFAULT                                     ")
    for ret_sactabpg in arq_sactabpg:
        # print(f"{ret_sactabpg[2]:,.2f}".replace(",", " ").replace(".", ","))
        # formatar numero com tamanho de 8
        valor = "{:,.2f}".format(ret_sactabpg[2]).rjust(7)

        mdia1 = "{:,.0f}".format(ret_sactabpg[4]).rjust(3)
        mdia2 = "{:,.0f}".format(ret_sactabpg[5]).rjust(3)
        mdia3 = "{:,.0f}".format(ret_sactabpg[6]).rjust(3)
        mdia4 = "{:,.0f}".format(ret_sactabpg[7]).rjust(3)
        mdia5 = "{:,.0f}".format(ret_sactabpg[8]).rjust(3)
        mdia6 = "{:,.0f}".format(ret_sactabpg[9]).rjust(3)
        mdia7 = "{:,.0f}".format(ret_sactabpg[10]).rjust(3)
        mdia8 = "{:,.0f}".format(ret_sactabpg[11]).rjust(3)
        mdia9 = "{:,.0f}".format(ret_sactabpg[12]).rjust(3)
        mdia10 = "{:,.0f}".format(ret_sactabpg[13]).rjust(3)
        mdia11 = "{:,.0f}".format(ret_sactabpg[14]).rjust(3)
        mdia12 = "{:,.0f}".format(ret_sactabpg[15]).rjust(3)
        mdia13 = "{:,.0f}".format(ret_sactabpg[16]).rjust(3)
        mdia14 = "{:,.0f}".format(ret_sactabpg[17]).rjust(3)
        mdia15 = "{:,.0f}".format(ret_sactabpg[18]).rjust(3)
        # valor = f"{ret_sactabpg[0][2]:,.2f}".replace(",", " ").replace(".", ",")
        item_pg = (
            f"{ret_sactabpg[0]}-{ret_sactabpg[1]}-(%):{valor}-Cond: {ret_sactabpg[3][0]}+{ret_sactabpg[3][1:3]} "
            f"dias: {mdia1} {mdia2} {mdia3} {mdia4} {mdia5} {mdia6} {mdia7} {mdia8} {mdia9} {mdia10} "
            f"{mdia11} {mdia12} {mdia13} {mdia14} {mdia15}"
        )
        # tela.doubleSpinBox_18.value()
        tela_pg.cb_tipo_pg.addItem(item_pg)
    index = tela_pg.cb_tipo_pg.currentIndex()
    ic(index)
    mop = tela_pg.cb_tipo_pg.itemText(index)
    # ic(mop)
    # ic(mop[0])
    # ic(mop[45:47])
    nvezes = int(mop[45:47])
    tela_pg.sb_qtd_parcelas.setValue(nvezes)

    def confirma():
        tela_pg.close()
        tela.ds_dinheiro.setFocus()
        verifica_condicao()
        return

    def sair():
        tela_pg.close()
        limpa_valores()
        return

    tela_pg.keyPressEvent = keyPressEvent
    tela_pg.cb_tipo_pg.setCurrentIndex(0)
    tela_pg.bt_confirma.clicked.connect(confirma)
    tela_pg.bt_confirma.setIcon(icon_salvar)
    tela_pg.bt_sair.clicked.connect(sair)
    tela_pg.bt_sair.setIcon(icon_sair)
    tela_pg.show()


def keyPressEvent(event):
    if event.key() == QtCore.Qt.Key.Key_Escape:
        tela_pg.close()
        limpa_valores()
        # event.ignore()  # Ignora o evento, impedindo que a tecla ESC feche a janela


def fechar_pedido(mnum_pedido):
    global mcli_aux, mnumero_pedido
    mnumero_pedido = mnum_pedido
    # tela.cb_cliente.setEnabled(False)
    mcod_cli = str(hg.m_set[83]).zfill(5)
    mcli_aux = str(hg.m_set[83]).zfill(5)
    for i in range(tela.cb_cliente.count()):
        item_text = tela.cb_cliente.itemText(i)
        if str(mcod_cli).strip() == item_text[43:48]:
            tela.cb_cliente.setCurrentIndex(i)
            break

    tela.ds_dinheiro.editingFinished.connect(verifica_condicao)
    tela.ds_pix.editingFinished.connect(verifica_condicao)
    tela.ds_cartao.editingFinished.connect(condicao_pagamento)

    tela.ds_duplicata.editingFinished.connect(condicao_pagamento)
    tela.ds_cheque.editingFinished.connect(verifica_condicao)
    # tela.ds_pix.setEnabled(False)

    # tela.bt_fecha.clicked.connect(salva_pedido)
    # tela.bt_fecha.setIcon(icon_salvar)
    tela.bt_sair.clicked.connect(fecha_tela)
    tela.bt_sair.setIcon(icon_sair)

    # tela.mcodigo.returnPressed.connect(verificar_produto)
    # tela.mcodigo.setFocus()
    # tela.textBrowser.itemDoubleClicked.connect(lambda item: editar_item(item.row()))
    criar_tela()
    tela.show()


if __name__ == "__main__":
    mnum_ped = "411561"
    fechar_pedido(mnum_ped)
    app.exec()
    hg.conexao_bd.close()
    tela.close()
