from PyQt6 import uic, QtWidgets, QtGui
from PyQt6.QtGui import QIcon, QGuiApplication, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QGroupBox,
)
from PyQt6.QtCore import QDateTime
from datetime import datetime
import keyboard
from hti_funcoes import conexao_banco, gerar_numero_pedido
from autorizacao_senha import aut_sen
import hti_global as hg
import os
from ATENCAO import atencao
from consulta_produto import listar_produto

# import time

app = QApplication([])
app.setStyleSheet(hg.style_sheet)
tela = uic.loadUi(f"{hg.c_ui}\\venda_pdv.ui")
icon = QIcon(f"{hg.c_imagem}\\htiico.jpg")
tela.setWindowIcon(icon)
tela.setWindowTitle(f"PEDIDO DE VENDA         {hg.SISTEMA}  Versao: {hg.VERSAO}")
# Centraliza a janela na tela
qt_rectangle = tela.frameGeometry()
center_point = app.primaryScreen().availableGeometry().center()
qt_rectangle.moveCenter(center_point)
tela.move(qt_rectangle.topLeft())
icon_sair = QIcon(f"{hg.c_imagem}\\sair.png")
icon_salvar = QIcon(f"{hg.c_imagem}\\confirma.png")
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

logohti = QPixmap(f"{hg.c_imagem}\\LOGOhti.png")
pixmap_redimensionado = logohti.scaled(85, 85)  # redimensiona a imagem para 100x100
tela.logohti.setStyleSheet(
    "background-color: rgb(190, 216, 255);border-width: 0px;border-radius: 0px;"
)
tela.logohti.setPixmap(pixmap_redimensionado)

if os.path.exists(f"{hg.c_imagem}\\htifirma.jpg"):
    imagem = QPixmap(f"{hg.c_imagem}\\htifirma.jpg")
else:
    imagem = QPixmap(f"{hg.c_imagem}\\htifirma1.jpg")

pixmap_redimensionado = imagem.scaled(450, 350)  # redimensiona a imagem para 100x100
tela.foto_produto.setPixmap(pixmap_redimensionado)
# print(f"{hg.c_usuario}\\{hg.geral_cod_usuario}.jpg")

lbl_operador = tela.findChild(QtWidgets.QLabel, "operador")
if os.path.exists(f"{hg.c_usuario}\\{hg.geral_cod_usuario}.jpg"):
    usuario = QPixmap(f"{hg.c_usuario}\\{hg.geral_cod_usuario}.jpg")

else:
    usuario = QPixmap(f"{hg.c_usuario}\\htiusu.jpg")
pixmap_redimensionado = usuario.scaled(125, 130)  # redimensiona a imagem para 100x100
tela.usuario.setPixmap(pixmap_redimensionado)
lbl_operador.setText(f" Operador: {hg.geral_cod_usuario}")
lbl_numero_pedido = tela.findChild(QtWidgets.QLabel, "numero_pedido")
lbl_cliente = tela.findChild(QtWidgets.QLabel, "lb_cliente")
tela.mquantidade.setValue(1)
lbl_produto = tela.findChild(QtWidgets.QLabel, "produto")
lbl_cabecalho = tela.findChild(QtWidgets.QLabel, "cabecalho")
lbl_saldo = tela.findChild(QtWidgets.QLabel, "saldo")
data_atual = QDateTime.currentDateTime()
lbl_sub_total = tela.findChild(QtWidgets.QLabel, "sub_total")
lbl_cabecalho.setText(f"Itens  Codigo   Descricao                  ")
m_informacao_pedido = []
mnum_ped = ""
infor_pedido = []

# # tela do montador
# tela_mont = uic.loadUi(f"{hg.c_ui}\\montador.ui")
# tela_mont.setWindowTitle("Inclusao de Montadores")
# # icon = QIcon(f"{hg.c_imagem}\\htiico.jpg")
# # icon_sair = QIcon(f"{hg.c_imagem}\\sair.png")
# # icon_incluir = QIcon(f"{hg.c_imagem}\\incluir.png")
# tela_mont.setWindowIcon(icon)
# if hg.mtp_tela == "G":
#     primary_screen = QGuiApplication.primaryScreen()
#     if primary_screen is not None:
#         screen_geometry = primary_screen.geometry()
#         tela_mont.setGeometry(screen_geometry)
#
# if os.path.exists(f"{hg.c_imagem}\\htifirma.jpg"):
#     imagem = QPixmap(f"{hg.c_imagem}\\htifirma.jpg")
# else:
#     imagem = QPixmap(f"{hg.c_imagem}\\htifirma1.jpg")
#
# pixmap_redimensionado = imagem.scaled(350, 50)  # redimensiona a imagem para 100x100
# tela_mont.empresa.setPixmap(pixmap_redimensionado)
mmontador = ""
mmontador1 = ""
mcomissao = 0


def criar_tela():
    print("criar tela")
    # time.sleep(1)
    lbl_numero_pedido.setText(f" Numero Pedido: {mnum_ped}")
    hg.conexao_cursor.execute(
        f"SELECT pcod_merc, pmerc, pquantd, pvlr_fat FROM sacped_s WHERE pnum_ped = '{mnum_ped}' order by sr_recno"
    )
    resultados = hg.conexao_cursor.fetchall()
    hg.conexao_bd.commit()
    # resultados = []
    model = QtGui.QStandardItemModel()
    mtotal_geral = i = 0
    descricao = codigo_produto = ""
    if len(resultados) > 0:
        for resultado in resultados:
            i += 1
            pcod_merc, pmerc, pquantd, pvlr_fat = resultado
            codigo_produto = pcod_merc
            mquantd = "{:9,.3f}".format(pquantd)
            mvalor = "{:10,.2f}".format(pvlr_fat)
            soma = pquantd * pvlr_fat
            descricao = pmerc
            msoma = "{:12,.2f}".format(soma)
            linha = f"  {i}   {pcod_merc}  {pmerc}"
            linha1 = f"                {mquantd} x {mvalor} = {msoma}"
            mtotal_geral += soma
            item = QtGui.QStandardItem(linha)
            model.appendRow(item)
            item = QtGui.QStandardItem(linha1)
            model.appendRow(item)
            # print(f"{hg.c_produto}\\{mcodigo}.jpg")
        if os.path.exists(f"{hg.c_produto}\\{codigo_produto}.jpg"):
            imagem1 = QPixmap(f"{hg.c_produto}\\{codigo_produto}.jpg")
        else:
            if os.path.exists(f"{hg.c_imagem}\\htifirma.jpg"):
                imagem1 = QPixmap(f"{hg.c_imagem}\\htifirma.jpg")
            else:
                imagem1 = QPixmap(f"{hg.c_imagem}\\htifirma1.jpg")

        pixmap_redim = imagem1.scaled(500, 350)  # redimensiona a imagem para 100x100
        tela.foto_produto.setPixmap(pixmap_redim)
        tela.listView.setModel(model)
        mtotal_g = "{:12,.2f}".format(mtotal_geral)
        linha1 = f"SUB-TOTAL: {mtotal_g}"
        lbl_sub_total.setText(linha1)
        lbl_produto.setText(descricao)
    else:
        lbl_produto.setText("        C A I X A   L I V R E ")

    # tela.mcodigo.returnPressed.connect(verificar_produto)
    # tela.mcodigo.returnPressed.connect(verificar_quantidade)
    # tela.mcodigo.returnPressed.connect(verificar_preco)
    # tela.mcodigo.setText("")
    # tela.mcodigo.setFocus()
    # tela.mpreco_venda.setValue(float(0))
    # tela.mquantidade.setValue(float(1))
    # msaldo = f"{0:,.3f}"
    # lbl_saldo.setText(msaldo)
    # tela.show()
    # verificar_produto()
    print("h2")


def fecha_tela():
    tela.close()
    return


# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         m_informa_pedido = ["145082", "", "", "6 - ACEROLANDIA LTDA"]
#         executar_consulta(m_informa_pedido)

# def confirma_montador():
#     global mmontador, mmontador1
#     index = tela_mont.cb_montador.currentIndex()
#     mop = tela_mont.cb_montador.itemText(index)
#     mmontador = mop[0:3]
#     index = tela_mont.cb_montador1.currentIndex()
#     mop = tela_mont.cb_montador1.itemText(index)
#     mmontador1 = mop[0:3]
#     print(mmontador, mmontador1)
#     tela_mont.close()
#     # confirma_produto()
#
#
# def informa_montador():
#     # tela_mont.pb_confirma.clicked.connect(confirma_montador)
#     # # print(tela.pb_confirma)
#     # hg.conexao_cursor.execute(f"SELECT scod_op, snome FROM insopera ORDER BY snome")
#     # arq_usuario = hg.conexao_cursor.fetchall()
#     # hg.conexao_bd.commit()
#     # item = "000 - "
#     # tela_mont.cb_montador.addItem(item)
#     # tela_mont.cb_montador1.addItem(item)
#     # for ret_usuario in arq_usuario:
#     #     item = f"{ret_usuario[0]} - {ret_usuario[1]}".strip("(),")
#     #     tela_mont.cb_montador.addItem(item)
#     #     tela_mont.cb_montador1.addItem(item)
#     # tela_mont.cb_montador.setCurrentIndex(0)
#     # tela_mont.cb_montador1.setCurrentIndex(0)
#     tela_mont.show()


def confirma_produto():
    print("confirma_produto")
    global mnum_ped, infor_pedido, mmontador, mmontador1, mcomissao

    # hg.conexao_cursor.execute(
    #     f"SELECT desconto FROM saccli WHERE cod_cli = {infor_pedido[3][0:5]}"
    # )
    # ver_cliente = hg.conexao_cursor.fetchone()
    # hg.conexao_bd.commit()
    m_codigo = tela.mcodigo.text()
    hg.conexao_cursor.execute(f"SELECT * FROM sacmerc WHERE cod_merc = '{m_codigo}'")
    ver_produto = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()
    if ver_produto is None:
        atencao("Produto nao encontrado ou estar em branco...")
        tela.mcodigo.setFocus()
        return

    msaldo = f"{ver_produto[55]:,.3f}"
    lbl_saldo.setText(msaldo)
    m_quantidade = tela.mquantidade.value()
    mp_venda = float(ver_produto[45])
    lbl_produto.setText(ver_produto[8])
    m_codmerc = ver_produto[7]
    m_saldo_ant = float(ver_produto[55])
    m_saldo_pos = m_saldo_ant - m_quantidade
    m_data_f = data_atual.toPyDateTime().date()
    data_formatada = m_data_f.strftime("%Y/%m/%d")
    mcomissao = ver_produto[25]
    tela.mcodigo.setText(ver_produto[7])
    mhora = datetime.now().strftime("%H:%M:%S")
    # index = tela_mont.cb_montador.currentIndex()
    # mop = tela_mont.cb_montador.itemText(index)
    # mmontador = mop[0:3]
    # index = tela_mont.cb_montador1.currentIndex()
    # mop = tela_mont.cb_montador1.itemText(index)
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
            m_quantidade,
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
            m_quantidade,
            0,
            0,
            mp_venda,
            0,
            mp_venda * 1,
            mp_venda,
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
            mmontador,
            mmontador1,
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

    tela.mcodigo.clear()
    tela.mcodigo.setFocus()
    tela.mpreco_venda.setValue(float(0))
    tela.mquantidade.setValue(float(1))
    msaldo = f"{0:,.3f}"
    lbl_saldo.setText(msaldo)
    criar_tela()


def verificar_preco():
    global mcomissao
    print("verificar_preco")
    # tela.mpreco_venda.editingFinished.disconnect()

    hg.conexao_cursor.execute(
        f"SELECT desconto FROM saccli WHERE cod_cli = {infor_pedido[3][0:5]}"
    )
    ver_cliente = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()
    if ver_cliente is None:
        atencao(f"Cliente nao Encontrado Codigo: {infor_pedido[3][0:5]}")
    m_codigo = tela.mcodigo.text()
    hg.conexao_cursor.execute(f"SELECT * FROM sacmerc WHERE cod_merc = '{m_codigo}'")
    ver_produto = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()
    if ver_produto is None:
        return
    # print(ver_produto)
    print(f"codigo: {m_codigo}")
    print(f"saldo {ver_produto[55]}")
    msaldo = f"{ver_produto[55]:,.3f}"
    lbl_saldo.setText(msaldo)
    m_quantidade = tela.mquantidade.value()
    mvlr_fat = tela.mpreco_venda.value()
    mp_venda = float(ver_produto[45])
    lbl_produto.setText(ver_produto[8])
    mcomissao = ver_produto[25]

    # tela.mpreco_venda.editingFinished.connect(verificar_preco)

    if 0 < hg.m_set[153] < m_quantidade:
        atencao("QUANTIDADE Solicitada maior que o MAXIMO Permitido")
        return

    hg.conexao_cursor.execute(
        f"SELECT sum(pquantd * pvlr_fat) FROM sacped_s WHERE pnum_ped = '{mnum_ped}'"
    )
    msubtotal = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()
    if msubtotal[0] is None:
        msub_total = 0
    else:
        msub_total = float(msubtotal[0])

    print(
        f"compras: {infor_pedido[9]} subtotal: {msub_total} vlr_fat {mvlr_fat} qtd: {m_quantidade}"
    )
    mvalor_somado = infor_pedido[9] + msub_total + (mvlr_fat * m_quantidade)
    if mvalor_somado >= infor_pedido[8] > 0:
        atencao(f"Limite do Cliente foi ultrapassado em R$: " f"{mvalor_somado}")
        return

    if mp_venda > mvlr_fat:
        mdesconto = ((mp_venda - mvlr_fat) / mp_venda) * 100
        if hg.m_set[112] > 0 and mdesconto >= hg.m_set[113]:
            if hg.m_set[112] > 1:
                mcomissao = mcomissao * (hg.m_set[112] / 100)
            else:
                mdesc = "{:,.2f}".format(mdesconto).rjust(7)
                mcomissao = mcomissao - (mdesc * hg.m_set[112])
                if mcomissao < 0:
                    mcomissao = 0

        mvalor_calculado = mp_venda - ((mvlr_fat / mp_venda) * 100)
        if (
            mvalor_calculado > hg.m_set[32] > 0
            and ver_produto[79] == 0
            and ver_cliente[0] == 0
        ):
            if not aut_sen(
                f"Cod.Prod..: {ver_produto[7]} - {ver_produto[8]}\n"
                f"Vlr.Solic.: {mvlr_fat}\n"
                f"Pr.Venda .: {mp_venda}\n"
                f"Desc.Soli.: {((mp_venda - mvlr_fat) / mp_venda)*100} %"
                f"Desc.Aut..: {hg.m_set[32]} %",
                "LIB_DESC",
                "",
                ver_produto[8],
                "",
                "",
            ):
                # mquantd = 1
                return
        elif ((mp_venda - mvlr_fat) / mp_venda) * 100 > ver_produto[79] > 0:
            if not aut_sen(
                f"Cod.Prod..: {ver_produto[7]} - {ver_produto[8]}\n"
                f"Vlr.Solic.: {mvlr_fat}\n"
                f"'Pr.Venda..: {mp_venda}\n"
                f"Desc.Soli.:' {((mp_venda - mvlr_fat)/mp_venda)*100} %\n"
                f"Desc.Aut..: {ver_produto[79]} %",
                "LIB_DESC",
                "",
                ver_produto[7],
                "",
                "",
            ):
                return
        elif hg.m_set[37] == "C" and mvlr_fat < ver_produto[44]:
            if not aut_sen(
                f"Cod.Prod..: {ver_produto[7]}\n"
                f"Vlr.Solic.: {mvlr_fat}\n"
                f"Pr.Custo..: {ver_produto[44]}",
                "LIB_DESC",
                "",
                ver_produto[7],
                "",
                "",
            ):
                return
        elif hg.m_set[37] == "V" and mvlr_fat < mp_venda:
            if not aut_sen(
                f"Cod.Prod..: {ver_produto[7]}\n"
                f"Vlr.Solic.: {mvlr_fat}\n"
                f"Pr.Venda..: {mp_venda}",
                "LIB_DESC",
                "",
                ver_produto[7],
                "",
                "",
            ):
                return
    # if hg.m_set[36] == "S" and not hg.m_set[151] == "S":
    #     informa_montador()

    if hg.m_indiv[25] == "S":
        tela.mpreco_venda.setValue(float(ver_produto[45]))
        confirma_produto()

    keyboard.add_hotkey("F5", confirma_produto)
    tela.bt_confirma.setEnabled(True)


def verificar_produto():
    print("verificar_produto")
    global mnum_ped, infor_pedido
    m_codigo = tela.mcodigo.text()
    tela.mcodigo.returnPressed.disconnect()
    # print(f"codigo: {m_codigo}")
    # if len(m_codigo) == 0:
    #     print("'lista de produto")
    #     instancia.listar_produto()
    #     return
    if len(m_codigo.strip()) == 0:
        return
    elif m_codigo[0] == "X" or m_codigo[0] == "x":
        if len(m_codigo[1:20]) > 0:
            tela.mquantidade.setValue(float(m_codigo[1:20]))
            tela.mcodigo.setText("")
        else:
            tela.mcodigo.setText("")
            tela.mcodigo.setFocus()
            tela.mpreco_venda.setValue(float(0))
            tela.mquantidade.setValue(float(1))
            msaldo = f"{0:,.3f}"
            lbl_saldo.setText(msaldo)
        return
    else:
        # print(infor_pedido[3][0:5])
        # hg.conexao_cursor.execute(
        #     f"SELECT desconto FROM saccli WHERE cod_cli = {infor_pedido[3][0:5]}"
        # )
        # ver_cliente = hg.conexao_cursor.fetchone()
        # hg.conexao_bd.commit()
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
            print(ver_produto[55])
            msaldo = f"{ver_produto[55]:,.3f}"
            lbl_saldo.setText(msaldo)
            lbl_produto.setText(ver_produto[8])
            tela.mpreco_venda.setValue(float(ver_produto[45]))
            tela.mcodigo.returnPressed.connect(verificar_produto)
            tela.mcodigo.setText(ver_produto[7])
            if mnum_ped == "":
                mnum_ped = gerar_numero_pedido()
            if hg.m_indiv[25] == "S":
                verificar_preco()
            else:
                tela.mquantidade.setFocus()
                tela.mquantidade.selectAll()
                return

        # if hg.m_indiv[25] == "S":
        #     verificar_preco()


def verificar_quantidade():
    print("verificar_quantidade")
    tela.mquantidade.editingFinished.disconnect()
    m_codigo = tela.mcodigo.text()
    hg.conexao_cursor.execute(f"SELECT * FROM sacmerc WHERE cod_merc = '{m_codigo}'")
    ver_produto = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()
    if ver_produto is None:
        return

    m_quantidade = tela.mquantidade.value()
    if ver_produto[102] == "S" and m_quantidade > ver_produto[55]:
        atencao("MERCADORIA BLOQUEADA para nao vender com SALDO A MENOR")
        return

    if (
        ver_produto[27] > 0
        and ver_produto[27] >= (ver_produto[55] - m_quantidade)
        and not ver_produto[8] == "DIVERSOS"
        and (hg.m_set[106] == "P" or hg.m_set[106] == "2")
        and not hg.m_indiv[25] == "T"
    ):
        atencao(
            f"'SALDO esta menor que o ESTOQUE MINIMO: {ver_produto[27]} estipulado !!!"
        )

    if (
        m_quantidade > ver_produto[55]
        and not ver_produto[8] == "DIVERSOS"
        and (hg.m_set[106] == "P" or hg.m_set[106] == "2")
        and not ver_produto[8][0:1] == "@"
    ):
        if not aut_sen(
            f"Quantidade Solicitada: {m_quantidade}\n Maior que saldo......: {ver_produto[55]}",
            "LIB_SALDO",
            "",
            m_codigo,
            "",
            "",
        ):
            return

        mlibera = "S"

    if 0 < hg.m_set[152] < m_quantidade:
        if not aut_sen(
            f"Quantidade Solicitada: {m_quantidade} maior que Permitido pela ADM: {hg.m_set[152]} "
            f"... Senha de autorizacao:",
            "LIB_SALDOADM",
            "",
            m_codigo,
            "",
            "",
        ):
            return
    tela.mpreco_venda.setFocus()
    tela.mpreco_venda.selectAll()
    tela.mquantidade.editingFinished.connect(verificar_quantidade)


def fecha_pedido():
    from venda_fecha import fechar_pedido

    fechar_pedido(mnum_ped)


keyboard.add_hotkey("F10", fecha_pedido)


def buscar_produto():
    mcodigo_produto = listar_produto()
    tela.mcodigo.setText(mcodigo_produto)


def inclusao_produto():


def executar_consulta(m_informa_pedido):
    global mnum_ped, infor_pedido
    keyboard.add_hotkey("ESC", fecha_tela)
    # instancia = ConsultaProduto()
    infor_pedido = m_informa_pedido
    tela.mquantidade.editingFinished.connect(verificar_quantidade)
    tela.mpreco_venda.editingFinished.connect(verificar_preco)
    tela.mcodigo.returnPressed.connect(verificar_produto)
    tela.mcodigo.setFocus()
    mnum_ped = m_informa_pedido[0]
    group_box = tela.findChild(QGroupBox, "gb_cliente")
    # Altera o título do QGroupBox
    group_box.setTitle(f"Codigo do Cliente: {m_informa_pedido[3]}")

    # quebra de linha em uma string
    # lbl_cliente.setText(f"{m_informa_pedido[0]}<br/>{m_informa_pedido[1]}")
    # lbl_cliente.setText(f"{m_informa_pedido[0]}\n{m_informa_pedido[1]}")
    lbl_cliente.setText(m_informa_pedido[1])
    tela.bt_buscar_produto.clicked.connect(buscar_produto)
    tela.bt_confirma.setEnabled(False)
    tela.bt_confirma.clicked.connect(confirma_produto)
    tela.bt_fecha.clicked.connect(fecha_pedido)
    tela.bt_sair.clicked.connect(fecha_tela)

    tela.bt_fecha.setIcon(icon_salvar)
    tela.bt_sair.setIcon(icon_sair)
    tela.show()
    criar_tela()

    # tela_mont.pb_confirma.clicked.connect(confirma_montador)
    # # print(tela.pb_confirma)
    # hg.conexao_cursor.execute(f"SELECT scod_op, snome FROM insopera ORDER BY snome")
    # arq_usuario = hg.conexao_cursor.fetchall()
    # hg.conexao_bd.commit()
    # item = "000 - "
    # tela_mont.cb_montador.addItem(item)
    # tela_mont.cb_montador1.addItem(item)
    # for ret_usuario in arq_usuario:
    #     item = f"{ret_usuario[0]} - {ret_usuario[1]}".strip("(),")
    #     tela_mont.cb_montador.addItem(item)
    #     tela_mont.cb_montador1.addItem(item)
    # tela_mont.cb_montador.setCurrentIndex(0)
    # tela_mont.cb_montador1.setCurrentIndex(0)


def pesquisa_produto():
    nome_buscar = tela.mcodigo.text()
    if len(nome_buscar) <= 5:
        hg.conexao_cursor.execute(
            f"select cod_merc, merc, pr_venda FROM sacmerc "
            f"WHERE cod_merc = '{nome_buscar}'"
        )
    else:
        hg.conexao_cursor.execute(
            f"select cod_merc, merc, pr_venda FROM sacmerc "
            f"WHERE cod_barr = '{nome_buscar}'"
        )
    resutado_prod = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()
    if resutado_prod is not None:
        atencao(f"Pesquisa de PRODUTO, PRODUTO: {resutado_prod[0]}'")
        # if not mnum_ped == "":
        #     print(mnum_ped)
        return
    else:
        atencao("PRODUTO nao encontrado...!!!")
        return


# def venda():
#     tela.mcodigo.textChanged.connect(pesquisa_produto)
#     return


if __name__ == "__main__":
    conexao_banco()
    m_informacao_pedido.append("145082")
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
