from PyQt6 import uic, QtWidgets, QtGui
from PyQt6.QtGui import QIcon, QGuiApplication, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QButtonGroup
from PyQt6.QtCore import QDateTime, Qt
# import keyboard
# from datetime import datetime
from hti_funcoes import conexao_banco, ver_serie
import hti_global as hg
import os
from icecream import ic

app = QApplication([])
app.setStyleSheet(hg.style_sheet)
tela = uic.loadUi(f"{hg.c_ui}\\venda_fecha.ui")
icon = QIcon(f"{hg.c_imagem}\\htiico.jpg")
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
qt_rectangle = tela.frameGeometry()
center_point = app.primaryScreen().availableGeometry().center()
qt_rectangle.moveCenter(center_point)
tela.move(qt_rectangle.topLeft())

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

mnum_ped = ""
lbl_produto = tela.findChild(QtWidgets.QLabel, "produto")
lbl_produto.setText("F E C H A M E N T O   D O   P E D I D O")
lbl_cabecalho = tela.findChild(QtWidgets.QLabel, "cabecalho")
data_atual = QDateTime.currentDateTime()

conexao_banco()
# hg.conexao_cursor.execute("SELECT * FROM sacsetup")
# # # 145082Recupere o resultado
# m_set = hg.conexao_cursor.fetchone()
# hg.conexao_bd.commit()

hg.conexao_cursor.execute(f"SELECT cod_cli, razao FROM saccli")
arq_cli = hg.conexao_cursor.fetchall()
hg.conexao_bd.commit()
for ret_cli in arq_cli:
    item = f'{str(ret_cli[0]).zfill(5)} - {ret_cli[1]}'.strip('(),')
    tela.cb_cliente.addItem(item)
tela.cb_cliente.setCurrentIndex(0)

mcli_aux = 0

tela.cb_forma_pg.addItems(["1->Dinheiro", "2->PIX", "3->Cartao", "4->Duplicata", "5->Cheque", "6->Financiamento"])
tela.cb_forma_pg.setCurrentIndex(0)  # coloca o focus no index

rb_tipo_desconto_group = QButtonGroup()
rb_tipo_desconto_group.addButton(tela.rb_percentual, id=1)
rb_tipo_desconto_group.addButton(tela.rb_valor, id=2)
tela.rb_valor.setChecked(True)


def fecha_tela():
    tela.close()
    # tela.closeEvent = on_close_event
    return


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        conexao_banco()
        fechar_pedido(mnum_ped)


class VariavelP(QMainWindow):
    def __init__(self):
        super().__init__()
        self.numero_pedido = ''
        self.mtotal_g = 0
        conexao_banco()
        fechar_pedido(mnum_ped)


def criar_tela(mnum_pedido):
    tela.textBrowser.clear()
    lbl_numero_pedido.setText(f" Numero Pedido: {VariavelP.numero_pedido}")
    lbl_cabecalho.setText(f"Itens  Codigo   Descricao                  ")
    try:
        hg.conexao_cursor.execute(
            f"SELECT pcod_merc, pmerc, pquantd, pvlr_fat FROM sacped_s WHERE pnum_ped = '{VariavelP.numero_pedido}'"
        )
        # # 145082Recupere o resultado
        resultados = hg.conexao_cursor.fetchall()
        hg.conexao_bd.commit()

        lbl_sub_total = tela.findChild(QtWidgets.QLabel, "sub_total")
        fonte = QtGui.QFont()
        fonte.setFamily("Courier")
        fonte.setPointSize(9)
        tela.textBrowser.setFont(fonte)
        mtotal_geral = 0
        i = 0
        # ic(resultados)
        # Exibir os resultados no QTextEdit
        if len(resultados) > 0:
            for resultado in resultados:
                i += 1
                # ic(resultado[2], resultado[0])
                pcod_merc, pmerc, pquantd, pvlr_fat = resultado
                # pcod_merc
                mquantd = "{:9,.3f}".format(pquantd)
                mvalor = "{:10,.2f}".format(pvlr_fat)
                soma = pquantd * pvlr_fat
                # ic(soma)
                msoma = "{:12,.2f}".format(soma)
                linha = f"  {i}   {pcod_merc}  {pmerc}"
                linha1 = f"              {mquantd} x {mvalor} = {msoma}"
                mtotal_geral += soma
                # linha = ' '.join(map(str, resultado))
                tela.textBrowser.append(linha)
                tela.textBrowser.append(linha1)
                # print(f"{hg.c_produto}\\{mcodigo}.jpg")
            VariavelP.mtotal_g = "{:12,.2f}".format(mtotal_geral)
            linha1 = f"SUB-TOTAL: {VariavelP.mtotal_g}"
            lbl_sub_total.setText(linha1)

    except Exception as e:
        print(f"Erro ao executar a consulta: {e}")


def salva_pedido():
    app1 = QApplication([])
    app1.setStyleSheet(hg.style_sheet)
    tela1 = uic.loadUi(f"{hg.c_ui}\\venda_ini.ui")
    icon1 = QIcon(f"{hg.c_imagem}\\htiico.jpg")
    tela1.setWindowIcon(icon)
    tela1.setWindowTitle(
        f"FECHAMENTO DO PEDIDO DE VENDA         {hg.SISTEMA}  Versao: {hg.VERSAO}"
    )
    # Centraliza a janela na tela
    qt_rectangle1 = tela1.frameGeometry()
    center_point1 = app1.primaryScreen().availableGeometry().center()
    qt_rectangle.moveCenter(center_point)
    tela1.move(qt_rectangle.topLeft())
    tela1.show()
    app1.exec()
    ic()


def atualizar_pedido():
    mjuros = 0
    mdesc_aux = tela.ds_desconto.value()
    mcod_cli = tela.ds_desconto.value()
    mdesc = 0
    # ic(tela.rb_valor.isChecked())
    if tela.rb_percentual.isChecked():
        mdesc = mdesc_aux / 100
    elif tela.rb_valor.isChecked():
        mvalor_pedido_str = VariavelP.mtotal_g
        mvalor_pedido_str = mvalor_pedido_str.replace(",", "").replace(",", ".")
        mvalor_pedido = float(mvalor_pedido_str)
        mdesc = mdesc_aux / mvalor_pedido

    mcomissao = 0

    if mjuros > 1 or mdesc > 0:
        ic('Atualizando e Recalculando o PEDIDO....')
        if hg.m_set[112] > 0 and mdesc >= hg.m_set[113]:
            if hg.m_set[112] > 1:
                comissao = mcomissao * (hg.m_set[113]/100)

        # ic(VariavelP.numero_pedido)
        index = tela.cb_cliente.currentIndex()
        mop = tela.cb_cliente.itemText(index)
        mcod_cli = mop[0:5]

        hg.conexao_cursor.execute(
            f"SELECT * FROM saccli WHERE cod_cli = {mcod_cli}"
        )
        cons_cli = hg.conexao_cursor.fetchone()
        hg.conexao_bd.commit()

        hg.conexao_cursor.execute(
            f"SELECT * FROM insopera WHERE cod_cli = {hg.geral_cod_usuario}"
        )
        cons_oper = hg.conexao_cursor.fetchone()
        hg.conexao_bd.commit()

        hg.conexao_cursor.execute(
            # f"SELECT pcod_merc, pmerc, pquantd, pvlr_fat FROM sacped_s WHERE pnum_ped = '{VariavelP.numero_pedido}'"
            f"SELECT * FROM sacped_s WHERE pnum_ped = {VariavelP.numero_pedido} AND SR_DELETED =' '"
        )
        cons_ped = hg.conexao_cursor.fetchall()
        hg.conexao_bd.commit()
        if len(cons_ped) > 0:
            # ic(cons_ped)
            for tupla in cons_ped:
                promocao = float(tupla[51])
                # ic(promocao)
                if promocao > 0:
                    pass
                else:
                    if tupla[16] < tupla[19]:
                        valor_teste = float(tupla[19]) * (mdesc + (float(tupla[38]/100)))
                        if valor_teste > 0.01:
                            # ic(valor_teste)
                            valor = valor_teste - (valor_teste * (mdesc + (float(tupla[38])/100)))
                            # ic(valor)
                    else:
                        valor_teste = float(tupla[17]) * mdesc
                        if valor_teste > 0.01:
                            # ic(mdesc)
                            # ic(valor_teste)
                            valor = valor_teste - (valor_teste * mdesc)
                            # ic(valor)

                    sql = (f"UPDATE sacped_s SET "
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
                           f"pobs1 = ?, "
                           f"pobs2 = ?, "
                           f"pobs3 = ?, "
                           f"pobs4 = ?, "
                           f"pobs5 = ?, "
                           f"pobs6 = ?, "
                           f"pobs7 = ?, "
                           f"pobs8 = ?, "
                           f"pproducao = ?, "
                           f"pcod_tran = ?, "
                           f"pd_entrega = ?, "
                           f"pfecha = ? "
                           f"WHERE  WHERE SR_RECNO = {cons_ped[110]}")

                    values = (cons_cli[31],
                              cons_cli[33],
                              mplaca,
                              m_carro,
                              m_modelo,
                              m_km,
                              cons_cli[1],
                              cons_oper[8])

                    print(sql, values)

                    hg.conexao_cursor.execute(sql, values)
                    hg.conexao_bd.commit()

# SR_BEGINTRANSACTION()
# ccomm := "UPDATE sacped_s SET pcgc = "+sr_cdbvalue(mcgc)
# ccomm := ccomm + ",pcpf ="+sr_cdbvalue(mcpf)
# ccomm := ccomm + ",pplaca = "+sr_cdbvalue(mplaca)
# ccomm := ccomm + ",pcarro = "+sr_cdbvalue(mcarro)
# ccomm := ccomm + ",pmodelo = "+sr_cdbvalue(mmodelo)
# ccomm := ccomm + ",pkm = "+sr_cdbvalue(mkm)
# ccomm := ccomm + ",pcod_cli = "+sr_cdbvalue(mcod_cli)
# ccomm := ccomm + ",pcomi_oper ="+sr_cdbvalue(mcom_oper)
# ccomm := ccomm + ",pcod_fin = "+sr_cdbvalue(STRZERO(mcod_fin,3))
# ccomm := ccomm + ",pcod_tab = "+sr_cdbvalue(STRZERO(mcod_cond,3))
# ccomm := ccomm + ",pvlr_pres = "+sr_cdbvalue(mvalor_pres)
# ccomm := ccomm + ",pcond_veze = "+sr_cdbvalue(mcond_veze)
# ccomm := ccomm + ",pcond_inte = "+sr_cdbvalue(IF(! EMPTY(mcond_int),mtipo_pg+STRZERO(VAL(mcond_int),3),mtipo_pg+STRZERO(m_dia[1],3)+STRZERO(m_dia[2],3)+STRZERO(m_dia[3],3)+STRZERO(m_dia[4],3)+STRZERO(m_dia[5],3)+STRZERO(m_dia[6],3)+STRZERO(m_dia[7],3)+STRZERO(m_dia[8],3)+STRZERO(m_dia[9],3)+STRZERO(m_dia[10],3)+STRZERO(m_dia[11],3)+STRZERO(m_dia[12],3)+STRZERO(m_dia[13],3)+STRZERO(m_dia[14],3)+STRZERO(m_dia[15],3)))
# ccomm := ccomm + ",ptp_vend = "+sr_cdbvalue(mtp_venda)
# ccomm := ccomm + ",pvlr_ent = "+sr_cdbvalue(mvlr_ent)
# ccomm := ccomm + ",pstat_item = "+sr_cdbvalue(mtelemark)
# ccomm := ccomm + ",pcod_vend = "+sr_cdbvalue(mcod_ven)
# ccomm := ccomm + ",pvendedor = "+sr_cdbvalue(mnome_ven)
# ccomm := ccomm + ",pcomissao = "+sr_cdbvalue(mcomissao)
# ccomm := ccomm + ",pdesc = "+sr_cdbvalue(mdesc_aux * 100)
# ccomm := ccomm + ",pdesc_merc = "+sr_cdbvalue(mvlr_desc)
# ccomm := ccomm + ",pvlr_fat = "+sr_cdbvalue(cons_ped[i,18]*mjuros)
# ccomm := ccomm + ",pobs1 = "+sr_cdbvalue(mobs1)
# ccomm := ccomm + ",pobs2 = "+sr_cdbvalue(mobs2)
# ccomm := ccomm + ",pobs3 = "+sr_cdbvalue(mobs3)
# ccomm := ccomm + ",pobs4 = "+sr_cdbvalue(mobs4)
# ccomm := ccomm + ",pobs5 = "+sr_cdbvalue(mobs5)
# ccomm := ccomm + ",pobs6 = "+sr_cdbvalue(mobs6)
# ccomm := ccomm + ",pobs7 = "+sr_cdbvalue(mobs7)
# ccomm := ccomm + ",pobs8 = "+sr_cdbvalue(mobs8)
# ccomm := ccomm + ",pproducao = "+sr_cdbvalue(mproducao)
# ccomm := ccomm + ",pcod_tran = "+sr_cdbvalue(mcod_tran)
# ccomm := ccomm + ",pd_entrega = "+IF(! EMPTY(mpd_entrega),sr_cdbvalue(mpd_entrega),'NULL')
# ccomm := ccomm + ",pfecha = 'F' WHERE SR_RECNO = "+sr_cdbvalue(cons_ped[i,111])
# //ccomm := ccomm + ",pfecha = 'F' WHERE pnum_ped = "+sr_cdbvalue(STRZERO(mnum_ped,6))+" AND pcod_merc = "+sr_cdbvalue(cons_ped[i,6])
# sr_getconnection():exec(ccomm,,.f.)
# sr_committransaction()
# SR_ENDTRANSACTION()
# NEXT


def verifica_condicao():
    tela.groupBox.setEnabled(False)
    tela.ds_desconto.setEnabled(False)
    tela.ds_vlr_entrada.setValue(float(0))
    tela.ds_entrada.setValue(float(0))
    tela.ds_qtd_dias.setValue(float(0))

    index = tela.cb_cliente.currentIndex()
    mop = tela.cb_cliente.itemText(index)
    mcod_cli = mop[0:5]
    index = tela.cb_forma_pg.currentIndex()
    mop = tela.cb_forma_pg.itemText(index)
    m_tipo_pag = mop[0:1]
    # ic(m_tipo_pag)
    if m_tipo_pag == '2':
        tela.ds_dia1.setValue(float(1))
        tela.ds_qtd_dias.setValue(float(1))
    elif m_tipo_pag == "3":
        tela.ds_qtd_dias.setEnabled(True)
        tela.ds_qtd_dias.setFocus()
        tela.ds_qtd_dias.selectAll()
    elif m_tipo_pag == '4' or m_tipo_pag == '5':
        tela.ds_entrada.setEnabled(True)
        tela.ds_qtd_dias.setEnabled(True)
        tela.ds_entrada.setFocus()
        tela.ds_entrada.selectAll()

    # if not mcli_aux == mcod_cli and not m_tipo_pag == '3':
    # ic(m_tipo_pag)
    # if m_tipo_pag != '3':
    hg.conexao_cursor.execute(
        f"SELECT * FROM saccli WHERE cod_cli = {mcod_cli}"
    )
    # # 145082Recupere o resultado
    # ic(mcod_cli, mcli_aux)
    cons_cli = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()
    if len(cons_cli) > 0 and cons_cli[58] > 0 and m_tipo_pag != '3':
        mdesc = cons_cli[58]/100
        print(f"ESTE CLIENTE: {cons_cli[1]} - {cons_cli[2]} TERA UM DESCONTO DE: {cons_cli[58]}")

    elif ((m_tipo_pag == '1' or m_tipo_pag == '2' or hg.m_set[34] == 'S') and hg.m_set[104] == 'S'
          or (m_tipo_pag == '6' and ver_serie() == '141416')) and m_tipo_pag != '3':
        tela.groupBox.setEnabled(True)
        tela.ds_desconto.setEnabled(True)

    return


def liberar_campos():
    tela.groupBox.setEnabled(False)
    tela.ds_desconto.setEnabled(False)
    tela.data_previsao.setEnabled(False)
    tela.ds_vlr_entrada.setEnabled(False)
    tela.ds_entrada.setEnabled(False)
    tela.ds_qtd_dias.setEnabled(False)
    tela.ds_dia1.setEnabled(False)
    tela.ds_dia2.setEnabled(False)
    tela.ds_dia3.setEnabled(False)
    tela.ds_dia4.setEnabled(False)
    tela.ds_dia5.setEnabled(False)
    tela.ds_dia6.setEnabled(False)
    tela.ds_dia7.setEnabled(False)
    tela.ds_dia8.setEnabled(False)
    tela.ds_dia9.setEnabled(False)
    tela.ds_dia10.setEnabled(False)
    tela.ds_dia11.setEnabled(False)
    tela.ds_dia12.setEnabled(False)
    tela.ds_dia13.setEnabled(False)
    tela.ds_dia14.setEnabled(False)
    tela.ds_dia15.setEnabled(False)

    tela.ds_dia1.setValue(float(0))
    tela.ds_dia2.setValue(float(0))
    tela.ds_dia3.setValue(float(0))
    tela.ds_dia4.setValue(float(0))
    tela.ds_dia5.setValue(float(0))
    tela.ds_dia6.setValue(float(0))
    tela.ds_dia7.setValue(float(0))
    tela.ds_dia8.setValue(float(0))
    tela.ds_dia9.setValue(float(0))
    tela.ds_dia10.setValue(float(0))
    tela.ds_dia11.setValue(float(0))
    tela.ds_dia12.setValue(float(0))
    tela.ds_dia13.setValue(float(0))
    tela.ds_dia14.setValue(float(0))
    tela.ds_dia15.setValue(float(0))

    index = tela.cb_forma_pg.currentIndex()
    mop = tela.cb_forma_pg.itemText(index)
    m_tipo_pag = mop[0:1]
    mentrada = tela.ds_entrada.value()
    mqtd_dias = tela.ds_qtd_dias.value()
    if mentrada > 0:
        tela.ds_vlr_entrada.setEnabled(True)
    if m_tipo_pag == '2':
        tela.ds_dia1.setValue(float(1))
    else:
        if mqtd_dias >= 1:
            if m_tipo_pag == '3':
                tela.ds_dia1.setValue(float(30))
            else:
                tela.ds_dia1.setEnabled(True)
                tela.ds_dia1.setFocus()
                tela.ds_dia1.selectAll()

        if mqtd_dias >= 2:
            if m_tipo_pag == '3':
                tela.ds_dia2.setValue(float(60))
            else:
                tela.ds_dia2.setEnabled(True)
        if mqtd_dias >= 3:
            if m_tipo_pag == '3':
                tela.ds_dia3.setValue(float(90))
            else:
                tela.ds_dia3.setEnabled(True)
        if mqtd_dias >= 4:
            if m_tipo_pag == '3':
                tela.ds_dia4.setValue(float(120))
            else:
                tela.ds_dia4.setEnabled(True)
        if mqtd_dias >= 5:
            if m_tipo_pag == '3':
                tela.ds_dia5.setValue(float(150))
            else:
                tela.ds_dia5.setEnabled(True)
        if mqtd_dias >= 6:
            if m_tipo_pag == '3':
                tela.ds_dia6.setValue(float(180))
            else:
                tela.ds_dia6.setEnabled(True)
        if mqtd_dias >= 7:
            if m_tipo_pag == '3':
                tela.ds_dia7.setValue(float(210))
            else:
                tela.ds_dia7.setEnabled(True)
        if mqtd_dias >= 8:
            if m_tipo_pag == '3':
                tela.ds_dia8.setValue(float(240))
            else:
                tela.ds_dia8.setEnabled(True)
        if mqtd_dias >= 9:
            if m_tipo_pag == '3':
                tela.ds_dia9.setValue(float(270))
            else:
                tela.ds_dia9.setEnabled(True)
        if mqtd_dias >= 10:
            if m_tipo_pag == '3':
                tela.ds_dia10.setValue(float(300))
            else:
                tela.ds_dia10.setEnabled(True)
        if mqtd_dias >= 11:
            if m_tipo_pag == '3':
                tela.ds_dia11.setValue(float(330))
            else:
                tela.ds_dia11.setEnabled(True)
        if mqtd_dias >= 12:
            if m_tipo_pag == '3':
                tela.ds_dia12.setValue(float(360))
            else:
                tela.ds_dia12.setEnabled(True)

        if mqtd_dias >= 13:
            if m_tipo_pag == '3':
                tela.ds_dia13.setValue(float(390))
            else:
                tela.ds_dia13.setEnabled(True)
        if mqtd_dias >= 14:
            if m_tipo_pag == '3':
                tela.ds_dia14.setValue(float(420))
            else:
                tela.ds_dia14.setEnabled(True)
        if mqtd_dias >= 15:
            if m_tipo_pag == '3':
                tela.ds_dia15.setValue(float(450))
            else:
                tela.ds_dia15.setEnabled(True)


def fechar_pedido(mnum_pedido):
    global mcli_aux
    VariavelP.numero_pedido = mnum_pedido
    # ic(VariavelP.numero_pedido)
    hg.conexao_cursor.execute(f"SELECT pcod_cli FROM sacped_s WHERE pnum_ped = '{mnum_pedido}'")
    res_pedido = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()
    # ic(res_pedido[0])
    if res_pedido[0] == 0:
        mcod_cli = hg.m_set[83]
        mcli_aux = hg.m_set[83]
    else:
        mcod_cli = res_pedido[0]
        mcli_aux = res_pedido[0]

    for i in range(tela.cb_cliente.count()):
        item_text = tela.cb_cliente.itemText(i)
        if str(mcod_cli).strip() in item_text:
            tela.cb_cliente.setCurrentIndex(i)
            break

    liberar_campos()
    tela.cb_forma_pg.currentIndexChanged.connect(verifica_condicao)
    tela.ds_qtd_dias.valueChanged.connect(liberar_campos)
    tela.ds_desconto.valueChanged.connect(atualizar_pedido)

    tela.bt_fecha.clicked.connect(salva_pedido)
    tela.bt_fecha.setIcon(icon_salvar)
    tela.bt_sair.clicked.connect(fecha_tela)
    tela.bt_sair.setIcon(icon_sair)

    # tela.mcodigo.returnPressed.connect(verificar_produto)
    # tela.mcodigo.setFocus()
    # tela.textBrowser.itemDoubleClicked.connect(lambda item: editar_item(item.row()))
    criar_tela(mnum_pedido)
    liberar_campos()
    verifica_condicao()
    tela.show()
    app.exec()


if __name__ == "__main__":
    mnum_ped = "145082"
    fechar_pedido(mnum_ped)
    hg.conexao_bd.close()

                # IF hg.m_set[1,37] = 'S'
                #         op_tela(10,35,13,75,' Dados do Carro ')
                #         DEVPOS(00,00);DEVOUT('Placa No..:')
                #         DEVPOS(01,00);DEVOUT('Marca.....:')
                #         DEVPOS(02,00);DEVOUT('Modelo....:')
                #         DEVPOS(03,00);DEVOUT('KM........:')
                #         mensagem('Preencha os campos')
                #         @ 00,12 GET mplaca PICT '@!'
                #         READ
                #         IF ! EMPTY(mplaca)
                #                 m_envelope:={}
                #                 sr_getconnection():exec("SELECT * FROM sacped_s WHERE sr_deleted = ' ' AND penvelope = "+sr_cdbvalue(mplaca),,.t.,@m_envelope)
                #                 sr_getconnection():exec('COMMIT',,.f.)
                #                 IF LEN(m_envelope) > 0
                #                         mcarro  := m_envelope[1,27]
                #                         mmodelo := m_envelope[1,28]
                #                         mkm     := m_envelope[1,29]
                #                 ENDIF
                #         ENDIF
                #         @ 01,12 GET mcarro PICT '@!'
                #         @ 02,12 GET mmodelo PICT '@!'
                #         @ 03,12 GET mkm PICT '@!'
                #         READ
                #         opcao := op_simnao('S','Confirma os dados digitados:')
        		# fecha_tela()
                #         IF LASTKEY() = 27 .OR. opcao = 'N'
                #                 LOOP
                #         ENDIF
                # ENDIF
