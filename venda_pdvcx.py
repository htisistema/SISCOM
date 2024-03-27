from PyQt6 import uic, QtWidgets
from PyQt6.QtGui import QIcon, QGuiApplication, QPixmap
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QDateTime
from datetime import date, datetime
from icecream import ic
from hti_funcoes import conexao_banco, ver_serie
from autorizacao_senha import aut_sen
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
tela.setWindowIcon(icon)
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

lbl_produto = tela.findChild(QtWidgets.QLabel, "produto")
lbl_produto.setText("F E C H A M E N T O   D O   P E D I D O")
lbl_cabecalho = tela.findChild(QtWidgets.QLabel, "cabecalho")

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
data_vazia = date(1900, 1, 1)
mtotal_pedido = 0
m_recebe = []
resultados = []
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


# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         conexao_banco()
#         fechar_pedido(mnum_ped)
#
#
# class VariavelP(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.numero_pedido = ""
#         self.mtotal_g = 0
#         conexao_banco()
#         fechar_pedido(mnum_ped)


def criar_tela():
    global mtotal_pedido, resultados
    tela.textBrowser.clear()
    lbl_numero_pedido.setText(f" Numero Pedido: {mnumero_pedido}")
    lbl_cabecalho.setText(f"Itens  Codigo   Descricao                  ")
    try:
        hg.conexao_cursor.execute(
            f"SELECT pcod_merc, pmerc, pquantd, pvlr_fat, COALESCE(pos, ' ') as app FROM sacped_s "
            f"WHERE pnum_ped = '{mnumero_pedido}'"
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
        # ic(resultados)
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
                # linha = ' '.join(map(str, resultado))
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
    index = tela.cb_cliente.currentIndex()
    mop = tela.cb_cliente.itemText(index)
    mcod_cli = mop[0:5]

    hg.conexao_cursor.execute(f"SELECT * FROM saccli WHERE cod_cli = {mcod_cli}")
    cons_cli = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()
    hg.conexao_cursor.execute(
        f"SELECT * FROM insopera WHERE scod_op = {hg.geral_cod_usuario}"
    )
    cons_oper = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()

    sql = (
        f"UPDATE sacped_s SET "
        f"pcgc = ?, "
        f"pcpf = ?, "
        f"pplaca = ?, "
        f"pcarro = ?, "
        f"pmodelo = ?, "
        f"pkm = ?, "
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
        f"pvlr_fat = ?, "
        f"pfecha = ? "
        f"WHERE  WHERE SR_RECNO = {mnumero_pedido}"
    )

    values = (
        cons_cli[31],
        cons_cli[33],
        "",  # mplaca
        "",  # m_carro
        "",  # m_modelo,
        "",  # m_km,
        cons_cli[1],  # cod_cli
        cons_oper[8],  # comissao ooperador
        "",  # codigo finan
        "",  # cod tabela
        "",  # vlr presta
        "",  # cond vezes
        "",  # cond intenv
        "",  # tp_venda
        "",  # vlr_enta
        "",  # stat_itam
        "",  # cod_vend
        "",  # vendedor
        "",  # comissao
        "",  # desc
        "",  # desc_merc
        "",  # vlr_fat
        "F",  # fecha
    )

    print(sql, values)

    hg.conexao_cursor.execute(sql, values)
    hg.conexao_bd.commit()


def verifica_condicao():
    global m_recebe
    mdin = 0
    mpx = 0
    tela.ds_dinheiro.editingFinished.disconnect()
    tela.ds_pix.editingFinished.disconnect()
    tela.ds_cartao.editingFinished.disconnect()
    tela.ds_duplicata.editingFinished.disconnect()
    tela.ds_cheque.editingFinished.disconnect()

    mdinheiro = tela.ds_dinheiro.value()
    mpix = tela.ds_pix.value()
    mcartao = tela.ds_cartao.value()
    mduplicata = tela.ds_duplicata.value()
    mcheque = tela.ds_cheque.value()

    # tela.ds_entrada.setValue(float(0))
    # tela.ds_qtd_dias.setValue(float(0))

    index = tela.cb_cliente.currentIndex()
    mop = tela.cb_cliente.itemText(index)
    mcod_cli = mop[0:5]
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

    if mdinheiro > 0:
        m_recebe.append("DN")
        m_recebe.append("AV")
        m_recebe.append("   ")
        m_recebe.append("      ")
        m_recebe.append("99999999")
        m_recebe.append(data_atual)
        m_recebe.append("C")
        m_recebe.append("   ")
        m_recebe.append("")  # cupom
        m_recebe.append(mdinheiro)  # valor
        m_recebe.append("")  # finan
        m_recebe.append("")  # cartao
        m_recebe.append("        ")
        m_recebe.append("             ")
        m_recebe.append("")  # corrente
        m_recebe.append(" ")
        m_recebe.append(" ")
        m_recebe.append(" ")
        mos = str(resultados[5])
        m_recebe.append(" OS:" + mos)

        tela.ds_dinheiro.setValue(float(0))
        print(m_recebe)
    if mpix > 0:
        m_recebe.append("PX")
        m_recebe.append("AV")
        m_recebe.append("   ")
        m_recebe.append("      ")
        m_recebe.append("99999999")
        m_recebe.append(data_atual)
        m_recebe.append("C")
        m_recebe.append("   ")
        m_recebe.append("")  # cupom
        m_recebe.append(mpix)  # valor
        m_recebe.append("")  # finan
        m_recebe.append("")  # cartao
        m_recebe.append("        ")
        m_recebe.append("             ")
        m_recebe.append("")  # corrente
        m_recebe.append(" ")
        m_recebe.append(" ")
        m_recebe.append(" ")
        mos = str(resultados[4])
        m_recebe.append(" OS:" + mos)

        tela.ds_pix.setValue(float(0))
        # print(m_recebe[0])
    for recebe in m_recebe:
        mtipo = m_recebe[0]
        # print(mtipo)
        if mtipo == "DN":
            mdin += float(m_recebe[9])
            print(mdin)
        if mtipo == "PX":
            mpx += float(m_recebe[9])
            print(mpx)
    mdin_f = "{:12,.2f}".format(mdin)
    mdin_tx = f"{mdin_f}"
    mpix_f = "{:12,.2f}".format(mpx)
    mpix_tx = f"{mpix_f}"
    lbl_dinheiro.setText(mdin_tx)
    lbl_pix.setText(mpix_tx)
    print(m_recebe)
    # if mdinheiro == mtotal_pedido:
    #     mvalor = mdinheiro
    #
    #     m_recebe.append('DN')   # ,'AV','   ','      ','99999999',data_atual,'C','   ',mn_cupom,mvalor,mn_fin,mcartao,SPACE(8),SPACE(13),mcorrente,' ',' ',' ',IF(EMPTY(VAL(ALLTRIM(cons_ped[1,94]))),'',' OS:'+ALLTRIM(cons_ped[1,94])))}
    #     m_recebe.append('AV')   # ,'   ','      ','99999999',data_atual,'C','   ',mn_cupom,mvalor,mn_fin,mcartao,SPACE(8),SPACE(13),mcorrente,' ',' ',' ',IF(EMPTY(VAL(ALLTRIM(cons_ped[1,94]))),'',' OS:'+ALLTRIM(cons_ped[1,94])))}
    # elif mdinheiro == 0 and mn_banco ==  .AND. EMPTY(mn_cred) .AND. EMPTY(mn_pix) .AND. ;
    #       EMPTY(mn_dup) .AND. EMPTY(mcod_cart) .AND. EMPTY(mn_fin) .AND. EMPTY(mn_trans) .AND. LEN(m_parcela) = 0);
    #       .OR. mdinheiro = mtot_nota:
    #   IF ! EMPTY(mdinheiro)   //.OR. mdinheiro = mtot_nota
    #       IF mdinheiro + mtot_verif > mtot_nota
    #           mvalor := mtot_nota - mtot_verif
    #           mtroco := mdinheiro+mtot_verif - mtot_nota
    #           SUB_BANNER(30,01,'Troco:'+TRANSFORM(mtroco,'999,999.99'))
    #           INKEY(,10)
    #           INKEY(30)
    #       ELSE
    #           mvalor := mdinheiro
    #       ENDIF
    #       AADD(m_alt,'DINHEIRO...: Valor: '+TRANSFORM(mdinheiro,'999,999.99'))
    #       AADD(m_recebe,{'DN','AV',SPACE(3),SPACE(6),'99999999',mdata_sis,'C',STRZERO(mcod_cart,3),mn_cupom,mvalor,mn_fin,mcartao,SPACE(8),SPACE(13),mcorrente,' ',' ',' ',IF(EMPTY(VAL(ALLTRIM(cons_ped[1,94]))),'',' OS:'+ALLTRIM(cons_ped[1,94]))})
    #   ELSE
    #       IF ! EMPTY(mn_cheque)
    #           IF (mvalor + mtot_verif) - mtot_nota > .01
    #               mcred_cheq := op_simnao('S','O Valor de R$:'+TRANSFORM(mvalor+mtot_verif - mtot_nota,'999,999.99')+'  vai ser gerado um CREDITO para o cliente:')
    #               IF  mcred_cheq = 'N'
    #                   LOOP
    #               ENDIF
    #               mvlr_credcheq := mvalor+mtot_verif - mtot_nota
    #               IF mvencimento > mdata_sis
    # *       	                                                         1    2      3         4       5        6       7         8                 9      10     11     12       13     14      15        16   17  18       19
    #                   AADD(m_recebe,{'CH','AP',mn_banco,mn_cheque,mn_dup,mvencimento,'B',STRZERO(mcod_cart,3),mn_cupom,mvalor,mn_fin,mcartao,magencia,mc_c,mcorrente,mcpfcnpj,' ',' ','CREDITO P/ CLIENTE DE R$:'+TRANSFORM(mvalor+mtot_verif - mtot_nota,'999,999.99')+IF(EMPTY(VAL(ALLTRIM(cons_ped[1,94]))),'',' OS:'+ALLTRIM(cons_ped[1,94]))})
    #                   mqtd_doc ++
    #                   mqtd_dias := mqtd_dias + (mvencimento - mdata_sis)
    #               ELSE
    #                   AADD(m_recebe,{'CH','AV',mn_banco,mn_cheque,mn_dup,mvencimento,'B',STRZERO(mcod_cart,3),mn_cupom,mvalor,mn_fin,mcartao,magencia,mc_c,mcorrente,mcpfcnpj,' ',' ','CREDITO P/ CLIENTE DE R$:'+TRANSFORM(mvalor+mtot_verif - mtot_nota,'999,999.99')+IF(EMPTY(VAL(ALLTRIM(cons_ped[1,94]))),'',' OS:'+ALLTRIM(cons_ped[1,94]))})
    #               ENDIF
    #           ELSE
    #               IF mvencimento > mdata_sis
    # *       	                                                         1    2      3         4       5        6       7         8                 9      10     11     12       13     14      15        16   17  18   19
    #                   AADD(m_recebe,{'CH','AP',mn_banco,mn_cheque,mn_dup,mvencimento,'B',STRZERO(mcod_cart,3),mn_cupom,mvalor,mn_fin,mcartao,magencia,mc_c,mcorrente,mcpfcnpj,' ',' ',IF(EMPTY(VAL(ALLTRIM(cons_ped[1,94]))),'',' OS:'+ALLTRIM(cons_ped[1,94]))})
    #                   mqtd_doc ++
    #                   mqtd_dias := mqtd_dias + (mvencimento - mdata_sis)
    #               ELSE
    #                   AADD(m_recebe,{'CH','AV',mn_banco,mn_cheque,mn_dup,mvencimento,'B',STRZERO(mcod_cart,3),mn_cupom,mvalor,mn_fin,mcartao,magencia,mc_c,mcorrente,mcpfcnpj,' ',' ',IF(EMPTY(VAL(ALLTRIM(cons_ped[1,94]))),'',' OS:'+ALLTRIM(cons_ped[1,94]))})
    #               ENDIF
    #           ENDIF
    #           AADD(m_alt,'CHEQUE.....: Bco.: '+mn_banco+' No: '+mn_cheque+' Venc: '+DTOC(mvencimento)+' Vlr:'+TRANSFORM(mvalor,'999,999.99'))
    #       ELSEIF ! EMPTY(mn_dup)
    #           i := 0
    #           FOR i = 1 TO LEN(m_parcela)
    #               IF EMPTY(m_parcela[i,1])
    #                   LOOP
    #               ENDIF
    #               AADD(m_alt,'DUPLICATA..: No.:'+m_parcela[i,1]+' Venc:'+DTOC(m_parcela[i,2])+' Vlr:'+TRANSFORM(m_parcela[i,3],'999,999.99'))
    #               IF m_parcela[i,2] > mdata_sis
    #                   AADD(m_recebe,{'DU','AP',mn_banco,SPACE(6),m_parcela[i,1],m_parcela[i,2],mt_pag,STRZERO(mcod_cart,3),m_parcela[i,1],m_parcela[i,3],mn_fin,mcartao,SPACE(8),SPACE(13),mcorrente,' ',' ',' ',IF(EMPTY(VAL(ALLTRIM(cons_ped[1,94]))),'',' OS:'+ALLTRIM(cons_ped[1,94]))})
    #                   mqtd_doc ++
    #                   mqtd_dias := mqtd_dias + (m_parcela[i,2] - mdata_sis)
    #               ELSE
    #                   AADD(m_recebe,{'DU','AV',mn_banco,SPACE(6),m_parcela[i,1],m_parcela[i,2],mt_pag,STRZERO(mcod_cart,3),m_parcela[i,1],m_parcela[i,3],mn_fin,mcartao,SPACE(8),SPACE(13),mcorrente,' ',' ',' ',IF(EMPTY(VAL(ALLTRIM(cons_ped[1,94]))),'',' OS:'+ALLTRIM(cons_ped[1,94]))})
    #               ENDIF
    #           NEXT
    #       ELSEIF ! EMPTY(mn_cupom)
    #           i := 0
    #           FOR i = 1 TO LEN(m_parcela)
    #               IF EMPTY(m_parcela[i,1])
    #                   LOOP
    #               ENDIF
    #               AADD(m_alt,'CARTAO.....: '+STRZERO(mcod_cart,3)+' Cupom No.: '+m_parcela[i,1]+' Valor: '+TRANSFORM(m_parcela[i,3],'999,999.99'))
    #               IF m_parcela[i,2] > mdata_sis
    # //               1    2       3      4         5       6          7           8                 9            10          11      12       13       14        15         16            17            18
    #                   AADD(m_recebe,{'CT','AP',SPACE(3),SPACE(6),mn_dup,m_parcela[i,2],'B',STRZERO(mcod_cart,3),m_parcela[i,1],m_parcela[i,3],mn_fin,mcartao,SPACE(8),SPACE(13),mcorrente,mdesc_cart,m_parcela[i,4],m_parcela[i,5],IF(EMPTY(VAL(ALLTRIM(cons_ped[1,94]))),'',' OS:'+ALLTRIM(cons_ped[1,94]))})
    #                   mqtd_doc ++
    #                   mqtd_dias := mqtd_dias + (m_parcela[i,2] - mdata_sis)
    #               ELSE
    #
    #                   AADD(m_recebe,{'CT','AV',SPACE(3),SPACE(6),mn_dup,m_parcela[i,2],'B',STRZERO(mcod_cart,3),m_parcela[i,1],m_parcela[i,3],mn_fin,mcartao,SPACE(8),SPACE(13),mcorrente,mdesc_cart,m_parcela[i,4],m_parcela[i,5],IF(EMPTY(VAL(ALLTRIM(cons_ped[1,94]))),'',' OS:'+ALLTRIM(cons_ped[1,94]))})
    #               ENDIF
    #           NEXT
    #       ELSEIF ! EMPTY(mn_fin)  // .OR. LEN(m_parcela) > 0
    #           i := 0
    #           FOR i = 1 TO LEN(m_parcela)
    #               IF EMPTY(m_parcela[i,1])
    #                   LOOP
    #               ENDIF
    #               AADD(m_alt,'FINANCIAMEN: '+m_parcela[i,1]+' Venc.: '+DTOC(m_parcela[i,2])+' Vlr: '+TRANSFORM(m_parcela[i,3],'999,999.99'))
    #               IF m_parcela[i,2] > mdata_sis
    #                   AADD(m_recebe,{'FI','AP',SPACE(3),SPACE(6),mn_dup,m_parcela[i,2],'B',STRZERO(mcod_cart,3),mn_cupom,m_parcela[i,3],m_parcela[i,1],mcartao,SPACE(8),SPACE(13),mcorrente,' ',' ',' ',IF(EMPTY(VAL(ALLTRIM(cons_ped[1,94]))),'',' OS:'+ALLTRIM(cons_ped[1,94]))})
    #                   mqtd_doc ++
    #                   mqtd_dias := mqtd_dias + (m_parcela[i,2] - mdata_sis)
    #               ELSE
    #                   AADD(m_recebe,{'FI','AV',SPACE(3),SPACE(6),mn_dup,m_parcela[i,2],'B',STRZERO(mcod_cart,3),mn_cupom,m_parcela[i,3],m_parcela[i,1],mcartao,SPACE(8),SPACE(13),mcorrente,' ',' ',' ',IF(EMPTY(VAL(ALLTRIM(cons_ped[1,94]))),'',' OS:'+ALLTRIM(cons_ped[1,94]))})
    #               ENDIF
    #           NEXT
    #       ELSEIF ! EMPTY(mn_trans)
    #           AADD(m_alt,'TRANSFERENC: '+mn_trans+' Venc.: '+DTOC(mvencimento)+' Valor: '+TRANSFORM(mvalor,'999,999.99'))
    #           AADD(m_recebe,{'TR','AP',SPACE(3),SPACE(6),mn_trans,mvencimento,mt_pag,STRZERO(mcod_cart,3),mn_cupom,mvalor,mn_fin,mcartao,SPACE(8),SPACE(13),mcorrente,' ',' ',' ',IF(EMPTY(VAL(ALLTRIM(cons_ped[1,94]))),'',' OS:'+ALLTRIM(cons_ped[1,94]))})
    #       ELSEIF ! EMPTY(mn_cred)
    #           mtipo_pg := 1
    #           mcredito := mcredito - mvalor
    #           AADD(m_alt,'CREDITO....: '+mn_cred+' Venc.: '+DTOC(mvencimento)+' Valor: '+TRANSFORM(mvalor,'999,999.99'))
    #           AADD(m_recebe,{'CR','AV',SPACE(3),SPACE(6),mn_cred,mvencimento,mt_pag,STRZERO(mcod_cart,3),mn_cupom,mvalor,mn_fin,mcartao,SPACE(8),SPACE(13),mcorrente,' ',' ',' ',IF(EMPTY(VAL(ALLTRIM(cons_ped[1,94]))),'',' OS:'+ALLTRIM(cons_ped[1,94]))})
    #       ELSEIF ! EMPTY(mn_pix)
    #           AADD(m_alt,'No.PIX.....: '+mn_pix+' Venc.: '+DTOC(mvencimento)+' Valor: '+TRANSFORM(mvalor,'999,999.99'))
    #           AADD(m_recebe,{'PX','AV',SPACE(3),SPACE(6),mn_pix,mvencimento,mt_pag,STRZERO(mcod_cart,3),mn_cupom,mvalor,mn_fin,mcartao,SPACE(8),SPACE(13),mcorrente,' ',' ',' ',IF(EMPTY(VAL(ALLTRIM(cons_ped[1,94]))),'',' OS:'+ALLTRIM(cons_ped[1,94]))})
    #       ENDIF
    # ENDIF
    # ENDIF
    # tela.ds_dinheiro.setFocus()
    # tela.ds_dinheiro.selectAll()
    tela.ds_dinheiro.editingFinished.connect(verifica_condicao)
    tela.ds_pix.editingFinished.connect(verifica_condicao)
    tela.ds_cartao.editingFinished.connect(verifica_condicao)
    tela.ds_duplicata.editingFinished.connect(verifica_condicao)
    tela.ds_cheque.editingFinished.connect(verifica_condicao)


def fechar_pedido(mnum_pedido):
    global mcli_aux, mnumero_pedido
    mnumero_pedido = mnum_pedido
    # tela.cb_cliente.setEnabled(False)
    mcod_cli = str(hg.m_set[83]).zfill(5)
    mcli_aux = str(hg.m_set[83]).zfill(5)
    # print(mcli_aux)
    for i in range(tela.cb_cliente.count()):
        item_text = tela.cb_cliente.itemText(i)
        # print(item_text)
        # print(f"{mcod_cli} {item_text[43:48]}")
        if str(mcod_cli).strip() == item_text[43:48]:
            tela.cb_cliente.setCurrentIndex(i)
            break

    tela.ds_dinheiro.editingFinished.connect(verifica_condicao)
    tela.ds_pix.editingFinished.connect(verifica_condicao)
    tela.ds_cartao.editingFinished.connect(verifica_condicao)
    tela.ds_duplicata.editingFinished.connect(verifica_condicao)
    tela.ds_cheque.editingFinished.connect(verifica_condicao)
    # tela.ds_pix.setEnabled(False)

    tela.bt_fecha.clicked.connect(salva_pedido)
    tela.bt_fecha.setIcon(icon_salvar)
    tela.bt_sair.clicked.connect(fecha_tela)
    tela.bt_sair.setIcon(icon_sair)

    # tela.mcodigo.returnPressed.connect(verificar_produto)
    # tela.mcodigo.setFocus()
    # tela.textBrowser.itemDoubleClicked.connect(lambda item: editar_item(item.row()))
    criar_tela()
    tela.show()


if __name__ == "__main__":
    mnum_ped = "145082"
    fechar_pedido(mnum_ped)
    app.exec()
    hg.conexao_bd.close()
