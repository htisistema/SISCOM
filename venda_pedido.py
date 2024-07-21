from PyQt6 import uic, QtWidgets, QtGui, QtCore
from PyQt6.QtGui import QIcon, QGuiApplication, QPixmap
from PyQt6.QtWidgets import QApplication, QListView
from PyQt6.QtCore import QDateTime, Qt
from datetime import datetime
import keyboard
from hti_funcoes import conexao_banco, gerar_numero_pedido

# from autorizacao_senha import aut_sen
import hti_global as hg
import os
from ATENCAO import atencao
from consulta_produto import consulta_produto
from venda_pdvcx import fechar_pedido

# import time

app = QApplication([])
app.setStyleSheet(hg.style_sheet)
tela_venda = uic.loadUi(f"{hg.c_ui}\\venda_pdv.ui")
icon = QIcon(f"{hg.c_imagem}\\htiico.ico")
tela_venda.setWindowIcon(icon)
tela_venda.setWindowTitle(f"PEDIDO DE VENDA         {hg.SISTEMA}  Versao: {hg.VERSAO}")
# Centraliza a janela na tela_venda
qt_rectangle = tela_venda.frameGeometry()
center_point = app.primaryScreen().availableGeometry().center()
qt_rectangle.moveCenter(center_point)
tela_venda.move(qt_rectangle.topLeft())
icon_sair = QIcon(f"{hg.c_imagem}\\sair.png")
icon_salvar = QIcon(f"{hg.c_imagem}\\confirma.png")
icon_consulta = QIcon(f"{hg.c_imagem}\\consulta.png")
tela_venda.setWindowIcon(icon)
# Centraliza a janela na tela_venda
# AJUSTAR A tela_venda EM RELACAO AO MONITOR
qt_rectangle = tela_venda.frameGeometry()
center_point = app.primaryScreen().availableGeometry().center()
qt_rectangle.moveCenter(center_point)
tela_venda.move(qt_rectangle.topLeft())

if hg.mtp_tela == "G":
    primary_screen = QGuiApplication.primaryScreen()
    if primary_screen is not None:
        screen_geometry = primary_screen.geometry()
        tela_venda.setGeometry(screen_geometry)

# PEGA O NOME DO ARQUIVO EM EXECUCAO
nome_file_com = os.path.basename(__file__)
nome_file, ext = os.path.splitext(nome_file_com)
tela_venda.statusbar.showMessage(f"<< {nome_file} >>")

if os.path.exists(f"{hg.c_imagem}\\htifirma.jpg"):
    imagem = QPixmap(f"{hg.c_imagem}\\htifirma.jpg")
else:
    imagem = QPixmap(f"{hg.c_imagem}\\htifirma1.jpg")

pixmap_redimensionado = imagem.scaled(350, 50)  # redimensiona a imagem para 100x100
tela_venda.empresa.setPixmap(pixmap_redimensionado)

logohti = QPixmap(f"{hg.c_imagem}\\LOGOhti.png")
pixmap_redimensionado = logohti.scaled(85, 85)  # redimensiona a imagem para 100x100
tela_venda.logohti.setStyleSheet(
    "background-color: rgb(190, 216, 255);border-width: 0px;border-radius: 0px;"
)
tela_venda.logohti.setPixmap(pixmap_redimensionado)

if os.path.exists(f"{hg.c_imagem}\\htifirma.jpg"):
    imagem = QPixmap(f"{hg.c_imagem}\\htifirma.jpg")
else:
    imagem = QPixmap(f"{hg.c_imagem}\\htifirma1.jpg")

pixmap_redimensionado = imagem.scaled(280, 240)  # redimensiona a imagem para 100x100
tela_venda.foto_produto.setPixmap(pixmap_redimensionado)
# print(f"{hg.c_usuario}\\{hg.geral_cod_usuario}.jpg")

lbl_operador = tela_venda.findChild(QtWidgets.QLabel, "operador")
if os.path.exists(f"{hg.c_usuario}\\{hg.geral_cod_usuario}.jpg"):
    usuario = QPixmap(f"{hg.c_usuario}\\{hg.geral_cod_usuario}.jpg")

else:
    usuario = QPixmap(f"{hg.c_usuario}\\htiusu.jpg")
pixmap_redimensionado = usuario.scaled(125, 130)  # redimensiona a imagem para 100x100
tela_venda.usuario.setPixmap(pixmap_redimensionado)
lbl_operador.setText(f" Operador: {hg.geral_cod_usuario}")
lbl_numero_pedido = tela_venda.findChild(QtWidgets.QLabel, "numero_pedido")
lbl_cliente = tela_venda.findChild(QtWidgets.QLabel, "lb_cliente")
lbl_produto = tela_venda.findChild(QtWidgets.QLabel, "produto")
lbl_cabecalho = tela_venda.findChild(QtWidgets.QLabel, "cabecalho")
lbl_preco = tela_venda.findChild(QtWidgets.QLabel, "preco")
lbl_preco.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
lbl_quantidade = tela_venda.findChild(QtWidgets.QLabel, "quantidade")
lbl_quantidade.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
lbl_total_itens = tela_venda.findChild(QtWidgets.QLabel, "total_itens")
lbl_total_itens.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
data_atual = QDateTime.currentDateTime()
lbl_sub_total = tela_venda.findChild(QtWidgets.QLabel, "sub_total")
lbl_cabecalho.setText(f"Itens  Codigo   Descricao                  ")
m_informacao_pedido = []
mnum_ped = ""
infor_pedido = []
key_f5 = 0
key_f10 = 0
# # tela_venda do montador
# tela_venda_mont = uic.loadUi(f"{hg.c_ui}\\montador.ui")
# tela_venda_mont.setWindowTitle("Inclusao de Montadores")
# # icon = QIcon(f"{hg.c_imagem}\\htiico.ico")
# # icon_sair = QIcon(f"{hg.c_imagem}\\sair.png")
# # icon_incluir = QIcon(f"{hg.c_imagem}\\incluir.png")
# tela_venda_mont.setWindowIcon(icon)
# if hg.mtp_tela_venda == "G":
#     primary_screen = QGuiApplication.primaryScreen()
#     if primary_screen is not None:
#         screen_geometry = primary_screen.geometry()
#         tela_venda_mont.setGeometry(screen_geometry)
#
# if os.path.exists(f"{hg.c_imagem}\\htifirma.jpg"):
#     imagem = QPixmap(f"{hg.c_imagem}\\htifirma.jpg")
# else:
#     imagem = QPixmap(f"{hg.c_imagem}\\htifirma1.jpg")
#
# pixmap_redimensionado = imagem.scaled(350, 50)  # redimensiona a imagem para 100x100
# tela_venda_mont.empresa.setPixmap(pixmap_redimensionado)
# mmontador = ""
# mmontador1 = ""
mcomissao = 0
mquantidade = 0, 000
mpreco = 0, 00


def limpar_list_view():
    list_view = tela_venda.findChild(QListView, "listView")
    if list_view:
        model = list_view.model()
        if model:
            model.clear()


def criar_tela_venda():
    # print("criar tela_venda")
    # time.sleep(1)
    model = QtGui.QStandardItemModel()
    # model.clear()
    lbl_numero_pedido.setText(f" Numero Pedido: {mnum_ped}")
    hg.conexao_cursor.execute(
        f"SELECT pcod_merc, pmerc, pquantd, pvlr_fat FROM sacped_s WHERE pnum_ped = '{mnum_ped}' order by sr_recno"
    )
    resultados = hg.conexao_cursor.fetchall()
    hg.conexao_bd.commit()
    # resultados = []
    mtotal_geral = i = 0
    descricao = codigo_produto = ""
    if len(resultados) > 0:

        for resultado in resultados:
            i += 1
            pcod_merc, pmerc, pquantd, pvlr_fat = resultado
            # codigo_produto = pcod_merc
            mquantd = "{:9,.3f}".format(pquantd)
            mvalor = "{:10,.2f}".format(pvlr_fat)
            soma = pquantd * pvlr_fat
            mtotal_geral += soma
            descricao = pmerc
            msoma = "{:12,.2f}".format(soma)
            linha = f"  {i}   {pcod_merc}  {pmerc}"
            linha1 = f"                {mquantd} x {mvalor} = {msoma}"
            item = QtGui.QStandardItem(linha)
            model.appendRow(item)
            item = QtGui.QStandardItem(linha1)
            model.appendRow(item)
            # print(f"{hg.c_produto}\\{mcodigo}.jpg")
        if os.path.exists(f"{hg.c_imagem}\\htifirma.jpg"):
            imagem1 = QPixmap(f"{hg.c_imagem}\\htifirma.jpg")
        else:
            imagem1 = QPixmap(f"{hg.c_imagem}\\htifirma1.jpg")

        tela_venda.listView.setModel(model)
        # print(mtotal_geral)
        # mtotal_g = f"{mtotal_geral:12,.2f}"

        mtotal_g = "{:10,.2f}".format(mtotal_geral)
        linha1 = f"SUB-TOTAL:{mtotal_g}"
        lbl_sub_total.setText(linha1)
        lbl_produto.setText(descricao)
    else:
        lbl_produto.setText("        C A I X A   L I V R E ")


def fecha_tela_venda():
    # print("fecha")
    tela_venda.close()
    return


def on_close_event(event):
    # print("esc")
    tela_venda.close()
    event.accept()


tela_venda.closeEvent = on_close_event

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         m_informa_pedido = ["145082", "", "", "6 - ACEROLANDIA LTDA"]
#         executar_consulta(m_informa_pedido)

# def confirma_montador():
#     global mmontador, mmontador1
#     index = tela_venda_mont.cb_montador.currentIndex()
#     mop = tela_venda_mont.cb_montador.itemText(index)
#     mmontador = mop[0:3]
#     index = tela_venda_mont.cb_montador1.currentIndex()
#     mop = tela_venda_mont.cb_montador1.itemText(index)
#     mmontador1 = mop[0:3]
#     print(mmontador, mmontador1)
#     tela_venda_mont.close()
#     # confirma_produto()
#
#
# def informa_montador():
#     # tela_venda_mont.pb_confirma.clicked.connect(confirma_montador)
#     # # print(tela_venda.pb_confirma)
#     # hg.conexao_cursor.execute(f"SELECT scod_op, snome FROM insopera ORDER BY snome")
#     # arq_usuario = hg.conexao_cursor.fetchall()
#     # hg.conexao_bd.commit()
#     # item = "000 - "
#     # tela_venda_mont.cb_montador.addItem(item)
#     # tela_venda_mont.cb_montador1.addItem(item)
#     # for ret_usuario in arq_usuario:
#     #     item = f"{ret_usuario[0]} - {ret_usuario[1]}".strip("(),")
#     #     tela_venda_mont.cb_montador.addItem(item)
#     #     tela_venda_mont.cb_montador1.addItem(item)
#     # tela_venda_mont.cb_montador.setCurrentIndex(0)
#     # tela_venda_mont.cb_montador1.setCurrentIndex(0)
#     tela_venda_mont.show()


def confirma_produto():
    # print("confirma_produto")
    global mnum_ped, infor_pedido, mcomissao, mpreco, mquantidade, key_f10

    # hg.conexao_cursor.execute(
    #     f"SELECT desconto FROM saccli WHERE cod_cli = {infor_pedido[3][0:5]}"
    # )
    # ver_cliente = hg.conexao_cursor.fetchone()
    # hg.conexao_bd.commit()
    # tela_venda.bt_confirma.setEnabled(False)
    m_codigo = tela_venda.mcodigo.text()
    hg.conexao_cursor.execute(f"SELECT * FROM sacmerc WHERE cod_merc = '{m_codigo}'")
    ver_produto = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()
    if ver_produto is None:
        atencao("Produto nao encontrado ou estar em branco...")
        tela_venda.mcodigo.setFocus()
        return

    mpreco_txt = f"{ver_produto[45]:,.3f}"
    mpreco = float(ver_produto[45])
    mquantidade_txt = f"{mquantidade:,.3f}"
    mtot_itens = mquantidade * mpreco
    mtot_itens = f"{mtot_itens:,.2f}"
    lbl_preco.setText(mpreco_txt)
    lbl_quantidade.setText(mquantidade_txt)
    lbl_total_itens.setText(mtot_itens)
    lbl_produto.setText(ver_produto[8])
    m_codmerc = ver_produto[7]
    m_saldo_ant = float(ver_produto[55])
    m_saldo_pos = m_saldo_ant - mquantidade
    m_data_f = data_atual.toPyDateTime().date()
    data_formatada = m_data_f.strftime("%Y/%m/%d")
    mcomissao = ver_produto[25]
    tela_venda.mcodigo.setText(ver_produto[7])
    mhora = datetime.now().strftime("%H:%M:%S")
    # index = tela_venda_mont.cb_montador.currentIndex()
    # mop = tela_venda_mont.cb_montador.itemText(index)
    # mmontador = mop[0:3]
    # index = tela_venda_mont.cb_montador1.currentIndex()
    # mop = tela_venda_mont.cb_montador1.itemText(index)
    # mmontador1 = mop[0:3]

    hg.conexao_cursor.execute(
        f"UPDATE sacmerc SET saldo_mer = {m_saldo_pos}, "
        f"data_atu = '{data_formatada}' WHERE cod_merc = {m_codmerc}"
    )
    hg.conexao_bd.commit()

    sql = (
        "INSERT INTO logproduto ("
        "data_sis, "
        "data, "
        "hora, "
        "cod_prod, "
        "quantd, "
        "saldo_ant, "
        "saldo_pos, "
        "cod_oper, "
        "prog, "
        "terminal, "
        "processo, "
        "ent_sai, "
        "PRECO_V, "
        "PRECO_C, "
        "SR_DELETED) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) "
    )

    hg.conexao_cursor.execute(
        sql,
        (
            data_formatada,
            data_formatada,
            mhora,
            m_codmerc,
            mquantidade,
            m_saldo_ant,
            m_saldo_pos,
            hg.geral_cod_usuario,
            "VENDA",
            hg.nome_computador,
            f"INCLUSAO PD: '{mnum_ped}'",
            "S",
            float(ver_produto[45]),
            float(ver_produto[43]),
            " ",
        ),
    )
    hg.conexao_bd.commit()

    sql = (
        "INSERT INTO sacped_s ("
        "pempresa, "
        "pnum_ped, "
        "ptermina, "
        "pdat_ped, "
        "pgru_sub, "
        "pcod_merc, "
        "pmerc, "
        "punidade, "
        "pespecie, "
        "penvelope, "
        "ppeso, "
        "ppeso_liq, "
        "pgramatura, "
        "pquantd, "
        "ppacote, "
        "ppecas, "
        "ppre_dig, "
        "pdesc, "
        "pvlr_fat, "
        "ppre_venda, "
        "ppr_venda1, "
        "pcust_real, "
        "pcust_merc, "
        "pcod_cli, "
        "pcgc, "
        "pcpf, "
        "pplaca, "
        "pcarro, "
        "pmodelo, "
        "pkm, "
        "pcod_fab, "
        "pfabrica, "
        "pcod_oper, "
        "pcomi_oper, "
        "pcod_vend, "
        "pvendedor, "
        "palimento, "
        "pcod_fin, "
        "pcod_tab, "
        "pvlr_pres, "
        "pcond_veze, "
        "pcond_inte, "
        "phora, "
        "ptp_vend, "
        "pvlr_ent, "
        "pisento, "
        "ppromocao, "
        "pmontador, "
        "pmontador1, "
        "pcomissao, "
        "pcom_mont, "
        "pprazo, "
        "pbebida, "
        "pipi, "
        "pobs_prod, "
        "pind_icms, "
        "pstat_item, "
        "psit_trib, "
        "pobs1, "
        "pobs2, "
        "pobs3, "
        "pobs4, "
        "plocal, "
        "chassis, "
        "descri1, "
        "descri2, "
        "descri3, "
        "descri4, "
        "descri5, "
        "pproducao, "
        "pcod_tran, "
        "pos, "
        "data_so, "
        "convidado, "
        "cod_pres, "
        "tipo_ped, "
        "SR_DELETED) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
        "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
        "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
        "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
        "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
        "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
        "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
        "?, ?, ?, ?, ?, ?, ?) "
    )
    hg.conexao_cursor.execute(
        sql,
        (
            hg.mcodempresa,
            mnum_ped,
            hg.nome_computador,
            data_formatada,
            ver_produto[6],
            m_codmerc,
            ver_produto[8],
            ver_produto[13],
            ver_produto[14],
            "",
            ver_produto[16],
            ver_produto[15],
            ver_produto[73],
            mquantidade,
            0,
            0,
            mpreco,
            0,
            mpreco * 1,
            mpreco,
            float(ver_produto[46]),
            float(ver_produto[44]),
            float(ver_produto[43]),
            0,
            "",
            "",
            "",
            "",
            "",
            "",
            ver_produto[29],
            ver_produto[30],
            hg.geral_cod_usuario,
            0,
            0,
            "",
            ver_produto[20],
            "",
            "",
            0,
            0,
            "",
            mhora,
            "",
            0,
            ver_produto[60],
            float(ver_produto[22]),
            "",
            "",
            mcomissao,
            ver_produto[26],
            float(ver_produto[74]),
            float(ver_produto[61]),
            float(ver_produto[64]),
            "",
            ver_produto[81],
            "",
            ver_produto[82],
            "",
            "",
            "",
            "",
            ver_produto[72][:2],
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            None,
            "",
            "",
            1,
            " ",
        ),
    )
    hg.conexao_bd.commit()

    tela_venda.mcodigo.clear()
    tela_venda.mcodigo.setFocus()
    mquantidade = 1
    mpreco = f"{0:,.3f}"
    mquantidade_txt = f"{1:,.3f}"
    lbl_preco.setText(mpreco)
    lbl_total_itens.setText(mpreco)
    lbl_quantidade.setText(mquantidade_txt)
    criar_tela_venda()
    key_f10 = 1


# def verificar_preco():
#     global mcomissao, key_f5
#     # print("verificar_preco")
#     # tela_venda.mpreco_venda.editingFinished.disconnect()
#     key_f5 = 1
#     tela_venda.bt_confirma.setEnabled(True)
#
#     hg.conexao_cursor.execute(
#         f"SELECT desconto FROM saccli WHERE cod_cli = {infor_pedido[3][0:5]}"
#     )
#     ver_cliente = hg.conexao_cursor.fetchone()
#     hg.conexao_bd.commit()
#     if ver_cliente is None:
#         atencao(f"Cliente nao Encontrado Codigo: {infor_pedido[3][0:5]}")
#     m_codigo = tela_venda.mcodigo.text()
#     hg.conexao_cursor.execute(f"SELECT * FROM sacmerc WHERE cod_merc = '{m_codigo}'")
#     ver_produto = hg.conexao_cursor.fetchone()
#     hg.conexao_bd.commit()
#     if ver_produto is None:
#         return
#     # print(ver_produto)
#     # print(f"codigo: {m_codigo}")
#     # print(f"saldo {ver_produto[55]}")
#     # msaldo = f"{ver_produto[55]:,.3f}"
#     # lbl_saldo.setText(msaldo)
#     # m_quantidade = tela_venda.mquantidade.value()
#     # mvlr_fat = tela_venda.mpreco_venda.value()
#     # mp_venda = float(ver_produto[45])
#     lbl_produto.setText(ver_produto[8])
#     mcomissao = ver_produto[25]
#
#     # tela_venda.mpreco_venda.editingFinished.connect(verificar_preco)
#
#     # if 0 < hg.m_set[153] < m_quantidade:
#     #     atencao("QUANTIDADE Solicitada maior que o MAXIMO Permitido")
#     #     return
#
#     hg.conexao_cursor.execute(
#         f"SELECT sum(pquantd * pvlr_fat) FROM sacped_s WHERE pnum_ped = '{mnum_ped}'"
#     )
#     msubtotal = hg.conexao_cursor.fetchone()
#     hg.conexao_bd.commit()
#     if msubtotal[0] is None:
#         msub_total = 0
#     else:
#         msub_total = float(msubtotal[0])
#
#     # print(
#     #     f"compras: {infor_pedido[9]} subtotal: {msub_total} vlr_fat {mvlr_fat} qtd: {m_quantidade}"
#     # )
#     mvalor_somado = infor_pedido[9] + msub_total + (mvlr_fat * m_quantidade)
#     if mvalor_somado >= infor_pedido[8] > 0:
#         atencao(f"Limite do Cliente foi ultrapassado em R$: " f"{mvalor_somado}")
#         return
#
#     if mp_venda > mvlr_fat:
#         mdesconto = ((mp_venda - mvlr_fat) / mp_venda) * 100
#         if hg.m_set[112] > 0 and mdesconto >= hg.m_set[113]:
#             if hg.m_set[112] > 1:
#                 mcomissao = mcomissao * (hg.m_set[112] / 100)
#             else:
#                 mdesc = "{:,.2f}".format(mdesconto).rjust(7)
#                 mcomissao = mcomissao - (mdesc * hg.m_set[112])
#                 if mcomissao < 0:
#                     mcomissao = 0
#
#         mvalor_calculado = mp_venda - ((mvlr_fat / mp_venda) * 100)
#         if (
#             mvalor_calculado > hg.m_set[32] > 0
#             and ver_produto[79] == 0
#             and ver_cliente[0] == 0
#         ):
#             if not aut_sen(
#                 f"Codigo Produto.....: {ver_produto[7]} - {ver_produto[8]}\n"
#                 f"Valor Solicitado...: {mvlr_fat}\n"
#                 f"Preco de Venda.....: {mp_venda}\n"
#                 f"Desconto Solicitado: {((mp_venda - mvlr_fat) / mp_venda)*100} %"
#                 f"Desconto Autorizado: {hg.m_set[32]} %",
#                 "LIB_DESC",
#                 "",
#                 ver_produto[8],
#                 "",
#                 "",
#             ):
#                 # mquantd = 1
#                 return
#         elif ((mp_venda - mvlr_fat) / mp_venda) * 100 > ver_produto[79] > 0:
#             if not aut_sen(
#                 f"Cod.Prod..: {ver_produto[7]} - {ver_produto[8]}\n"
#                 f"Vlr.Solic.: {mvlr_fat}\n"
#                 f"'Pr.Venda..: {mp_venda}\n"
#                 f"Desc.Soli.:' {((mp_venda - mvlr_fat)/mp_venda)*100} %\n"
#                 f"Desc.Aut..: {ver_produto[79]} %",
#                 "LIB_DESC",
#                 "",
#                 ver_produto[7],
#                 "",
#                 "",
#             ):
#                 return
#         elif hg.m_set[37] == "C" and mvlr_fat < ver_produto[44]:
#             if not aut_sen(
#                 f"Cod.Prod..: {ver_produto[7]}\n"
#                 f"Vlr.Solic.: {mvlr_fat}\n"
#                 f"Pr.Custo..: {ver_produto[44]}",
#                 "LIB_DESC",
#                 "",
#                 ver_produto[7],
#                 "",
#                 "",
#             ):
#                 return
#         elif hg.m_set[37] == "V" and mvlr_fat < mp_venda:
#             if not aut_sen(
#                 f"Cod.Prod..: {ver_produto[7]}\n"
#                 f"Vlr.Solic.: {mvlr_fat}\n"
#                 f"Pr.Venda..: {mp_venda}",
#                 "LIB_DESC",
#                 "",
#                 ver_produto[7],
#                 "",
#                 "",
#             ):
#                 return
#     # if hg.m_set[36] == "S" and not hg.m_set[151] == "S":
#     #     informa_montador()
#
#     if hg.m_indiv[25] == "S":
#         tela_venda.mpreco_venda.setValue(float(ver_produto[45]))
#         confirma_produto()
#
#     # keyboard.add_hotkey("F5", confirma_produto)


def keyPressEvent(event):
    global key_f5, key_f10
    if (
        event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return
    ) and key_f5 == 1:
        confirma_produto()
        key_f5 = 0
    elif event.key() == Qt.Key.Key_Escape:
        # print("Esc pressionado")
        fecha_tela_venda()
    elif event.key() == Qt.Key.Key_F5 and key_f5 == 1:
        confirma_produto()
        key_f5 = 0

    # if (
    #     event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return
    # ) and key_f10 == 1:
    #     salva_venda()
    #     key_f10 = 0
    if event.key() == Qt.Key.Key_F10 and key_f10 == 1:
        # print('f12')
        salva_venda()
        key_f10 = 0


tela_venda.keyPressEvent = keyPressEvent


def verificar_produto():
    # print("verificar_produto")
    global mnum_ped, infor_pedido, mquantidade
    m_codigo = tela_venda.mcodigo.text()
    tela_venda.mcodigo.returnPressed.disconnect()
    # print(f"{hg.c_produto}\\{m_codigo}.jpg")
    if os.path.exists(f"{hg.c_produto}\\{m_codigo}.jpg"):
        imagem1 = QPixmap(f"{hg.c_produto}\\{m_codigo}.jpg")
    elif os.path.exists(f"{hg.c_produto}\\{m_codigo}.png"):
        imagem1 = QPixmap(f"{hg.c_produto}\\{m_codigo}.png")
    else:
        if os.path.exists(f"{hg.c_imagem}\\htifirma.jpg"):
            imagem1 = QPixmap(f"{hg.c_imagem}\\htifirma.jpg")
        else:
            imagem1 = QPixmap(f"{hg.c_imagem}\\htifirma1.jpg")

    pixmap_redim = imagem1.scaled(500, 350)  # redimensiona a imagem para 100x100
    tela_venda.foto_produto.setPixmap(pixmap_redim)
    tela_venda.mcodigo.returnPressed.connect(verificar_produto)

    # print(f"codigo: {m_codigo}")
    # if len(m_codigo) == 0:
    #     print("'lista de produto")
    #     instancia.listar_produto()
    #     return
    if len(m_codigo.strip()) == 0:
        return

    elif m_codigo[0] == "X" or m_codigo[0] == "x":
        # print(m_codigo[1:20])
        if len(m_codigo[1:20]) > 0:
            mquantidade = float(m_codigo[1:20])
            tela_venda.mcodigo.setText("")
            mquantidade_txt = f"{mquantidade:,.3f}"
            lbl_quantidade.setText(mquantidade_txt)

        return
    else:
        m_codigo = tela_venda.mcodigo.text().zfill(5)
        # print(infor_pedido[3][0:5])
        # hg.conexao_cursor.execute(
        #     f"SELECT desconto FROM saccli WHERE cod_cli = {infor_pedido[3][0:5]}"
        # )
        # ver_cliente = hg.conexao_cursor.fetchone()
        # hg.conexao_bd.commit()
        # if m_codigo[0:1] == "x":
        #     pass
        if len(m_codigo) <= 5:
            m_codigo = m_codigo.zfill(5)
            hg.conexao_cursor.execute(
                f"SELECT * FROM sacmerc WHERE cod_merc = '{m_codigo}'"
            )
        elif len(m_codigo) > 5:
            hg.conexao_cursor.execute(
                f"SELECT * FROM sacmerc WHERE cod_barr = '{m_codigo}'"
            )
        else:
            atencao("Produto nao encontrado....")
            return

        ver_produto = hg.conexao_cursor.fetchone()
        hg.conexao_bd.commit()

        if ver_produto is None:
            atencao("Produto nao encontrado...")
            return
        else:
            # print(ver_produto[55])
            mpreco_txt = f"{ver_produto[45]:,.3f}"
            lbl_preco.setText(mpreco_txt)
            lbl_produto.setText(ver_produto[8])
            # tela_venda.mpreco_venda.setValue(float(ver_produto[45]))
            tela_venda.mcodigo.setText(ver_produto[7])
            mpreco_venda = float(ver_produto[45])
            mqtd = float(mquantidade)
            mtot_itens = mpreco_venda * mqtd
            mtot_itens = f"{mtot_itens:,.2f}"
            # print(mtot_itens)
            lbl_total_itens.setText(mtot_itens)

            if mnum_ped == "":
                mnum_ped = gerar_numero_pedido()
            # if hg.m_indiv[25] == "S":
            #     verificar_preco()
            # else:
            #     # tela_venda.mquantidade.setFocus()
            #     # tela_venda.mquantidade.selectAll()
            #     return

    confirma_produto()
    # if hg.m_indiv[25] == "S":
    #     verificar_preco()


# def verificar_quantidade():
#     # print("verificar_quantidade")
#     global mquantidade
#     m_codigo = tela_venda.mcodigo.text()
#     hg.conexao_cursor.execute(f"SELECT * FROM sacmerc WHERE cod_merc = '{m_codigo}'")
#     ver_produto = hg.conexao_cursor.fetchone()
#     hg.conexao_bd.commit()
#     if ver_produto is None:
#         return
#
#     # m_quantidade = tela_venda.mquantidade.value()
#     if ver_produto[102] == "S" and mquantidade > ver_produto[55]:
#         atencao("MERCADORIA BLOQUEADA para nao vender com SALDO A MENOR")
#         return
#
#     if (
#         ver_produto[27] > 0
#         and ver_produto[27] >= (float(ver_produto[55]) - mquantidade)
#         and not ver_produto[8] == "DIVERSOS"
#         and (hg.m_set[106] == "P" or hg.m_set[106] == "2")
#         and not hg.m_indiv[25] == "T"
#     ):
#         atencao(
#             f"'SALDO esta menor que o ESTOQUE MINIMO: {ver_produto[27]} estipulado !!!"
#         )
#
#     if (
#         mquantidade > ver_produto[55]
#         and not ver_produto[8] == "DIVERSOS"
#         and (hg.m_set[106] == "P" or hg.m_set[106] == "2")
#         and not ver_produto[8][0:1] == "@"
#     ):
#         if not aut_sen(
#             f"Quantidade Solicitada: {mquantidade}\n Maior que saldo......: {ver_produto[55]}",
#             "LIB_SALDO",
#             "",
#             m_codigo,
#             "",
#             "",
#         ):
#             return
#
#         mlibera = "S"
#
#     if 0 < hg.m_set[152] < mquantidade:
#         if not aut_sen(
#             f"Quantidade Solicitada: {mquantidade} maior que Permitido pela ADM: {hg.m_set[152]} "
#             f"... Senha de autorizacao:",
#             "LIB_SALDOADM",
#             "",
#             m_codigo,
#             "",
#             "",
#         ):
#             return
#     # tela_venda.mpreco_venda.setFocus()
#     # tela_venda.mpreco_venda.selectAll()
#     # tela_venda.mquantidade.editingFinished.connect(verificar_quantidade)


def salva_venda():
    global mnum_ped, mquantidade, mpreco

    fechar_pedido(mnum_ped)
    mnum_ped = ""
    mquantidade = 1
    mpreco = f"{0:,.3f}"
    mquantidade_txt = f"{1:,.3f}"
    limpar_list_view()
    criar_tela_venda()
    lbl_preco.setText(mpreco)
    lbl_total_itens.setText(mpreco)
    lbl_quantidade.setText(mquantidade_txt)
    linha1 = f"SUB-TOTAL:      0,00"
    lbl_sub_total.setText(linha1)
    lbl_produto.setText("        C A I X A   L I V R E ")


# keyboard.add_hotkey("F10", salva_venda)


def buscar_produto():
    # from consulta_produto import consulta_produto
    mcod = ' '
    mcodigo_produto = consulta_produto(mcod)
    if mcodigo_produto is None:
        print(f"retorno: {mcodigo_produto}")
        tela_venda.mcodigo.setText(mcodigo_produto)


def executar_consulta(m_informa_pedido):
    global mnum_ped, infor_pedido, mpreco, mquantidade
    mpreco = 0
    mquantidade = 0
    keyboard.add_hotkey("ESC", fecha_tela_venda)
    # instancia = ConsultaProduto()
    infor_pedido = m_informa_pedido
    mpreco_txt = f"{mpreco:,.3f}"
    mquantidade_txt = f"{mquantidade:,.3f}"
    mtot_itens = f"{mquantidade * mpreco:,.2f}"
    lbl_preco.setText(mpreco_txt)
    lbl_quantidade.setText(mquantidade_txt)
    lbl_total_itens.setText(mtot_itens)
    # tela_venda.mquantidade.editingFinished.connect(verificar_quantidade)
    # tela_venda.mpreco_venda.editingFinished.connect(verificar_preco)
    tela_venda.mcodigo.returnPressed.connect(verificar_produto)
    tela_venda.mcodigo.setFocus()
    mnum_ped = m_informa_pedido[0]
    # group_box = tela_venda.findChild(QGroupBox, "gb_cliente")
    # # Altera o título do QGroupBox
    # group_box.setTitle(f"Codigo do Cliente: {m_informa_pedido[3]}")

    # quebra de linha em uma string
    # lbl_cliente.setText(f"{m_informa_pedido[0]}<br/>{m_informa_pedido[1]}")
    # lbl_cliente.setText(f"{m_informa_pedido[0]}\n{m_informa_pedido[1]}")
    if m_informa_pedido[6] == "A":
        tipo_venda = "Avista"
    else:
        tipo_venda = "Aprazo"

    # lbl_cliente.setText(
    #     f"Vendedor: {m_informa_pedido[4]} \nForma de pagamento: {m_informa_pedido[5]}\n"
    #     f"Tipo de Venda: {tipo_venda}"
    # )
    tela_venda.bt_buscar_produto.clicked.connect(buscar_produto)
    # tela_venda.bt_confirma.setEnabled(False)
    # tela_venda.bt_confirma.clicked.connect(confirma_produto)
    tela_venda.bt_fecha.clicked.connect(salva_venda)
    tela_venda.bt_sair.clicked.connect(fecha_tela_venda)

    tela_venda.bt_fecha.setIcon(icon_salvar)
    tela_venda.bt_sair.setIcon(icon_sair)
    tela_venda.bt_buscar_produto.setIcon(icon_consulta)
    tela_venda.show()
    criar_tela_venda()

    # tela_venda_mont.pb_confirma.clicked.connect(confirma_montador)
    # # print(tela_venda.pb_confirma)
    # hg.conexao_cursor.execute(f"SELECT scod_op, snome FROM insopera ORDER BY snome")
    # arq_usuario = hg.conexao_cursor.fetchall()
    # hg.conexao_bd.commit()
    # item = "000 - "
    # tela_venda_mont.cb_montador.addItem(item)
    # tela_venda_mont.cb_montador1.addItem(item)
    # for ret_usuario in arq_usuario:
    #     item = f"{ret_usuario[0]} - {ret_usuario[1]}".strip("(),")
    #     tela_venda_mont.cb_montador.addItem(item)
    #     tela_venda_mont.cb_montador1.addItem(item)
    # tela_venda_mont.cb_montador.setCurrentIndex(0)
    # tela_venda_mont.cb_montador1.setCurrentIndex(0)


# def pesquisa_produto():
#     nome_buscar = tela_venda.mcodigo.text()
#     if len(nome_buscar) <= 5:
#         hg.conexao_cursor.execute(
#             f"select cod_merc, merc, pr_venda FROM sacmerc "
#             f"WHERE cod_merc = '{nome_buscar}'"
#         )
#     else:
#         hg.conexao_cursor.execute(
#             f"select cod_merc, merc, pr_venda FROM sacmerc "
#             f"WHERE cod_barr = '{nome_buscar}'"
#         )
#     resutado_prod = hg.conexao_cursor.fetchone()
#     hg.conexao_bd.commit()
#     if resutado_prod is not None:
#         atencao(f"Pesquisa de PRODUTO, PRODUTO: {resutado_prod[0]}'")
#         # if not mnum_ped == "":
#         #     print(mnum_ped)
#         return
#     else:
#         atencao("PRODUTO nao encontrado...!!!")
#         return


# def venda():
#     tela_venda.mcodigo.textChanged.connect(pesquisa_produto)
#     return


if __name__ == "__main__":
    conexao_banco()
    # 145082
    m_informacao_pedido.append("")
    m_informacao_pedido.append("")
    m_informacao_pedido.append("")
    m_informacao_pedido.append("00006 - ACEROLANDIA")
    m_informacao_pedido.append("")
    m_informacao_pedido.append("")
    m_informacao_pedido.append("")
    m_informacao_pedido.append(0)
    m_informacao_pedido.append(0)
    m_informacao_pedido.append(0)
    executar_consulta(m_informacao_pedido)
    app.exec()
    hg.conexao_bd.close()
