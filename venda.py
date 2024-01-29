from PyQt6 import uic, QtWidgets, QtGui
from PyQt6.QtGui import QIcon, QGuiApplication, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QGroupBox,
)
from PyQt6.QtCore import QDateTime
from datetime import datetime
import keyboard
from hti_funcoes import conexao_banco, gerar_numero_pedido, ver_serie
from autorizacao_senha import aut_sen
import hti_global as hg
import os
from ATENCAO import atencao

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

mnum_ped = ""
infor_pedido = []
tela.mquantidade.setValue(1)
lbl_produto = tela.findChild(QtWidgets.QLabel, "produto")
lbl_cabecalho = tela.findChild(QtWidgets.QLabel, "cabecalho")
lbl_saldo = tela.findChild(QtWidgets.QLabel, "saldo")
data_atual = QDateTime.currentDateTime()

tela1 = uic.loadUi(f"{hg.c_ui}\\f4_merc.ui")
tela1.setWindowTitle("PRODUTOS CADASTRADO")
# icon = QIcon(f"{hg.c_imagem}\\htiico.jpg")
# icon_sair = QIcon(f"{hg.c_imagem}\\sair.png")
# icon_incluir = QIcon(f"{hg.c_imagem}\\incluir.png")
tela1.setWindowIcon(icon)
tabela1 = tela1.tableWidget


def fecha_tela():
    tela.close()
    return


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        m_informa_pedido = ["145082", "", "", "6 - ACEROLANDIA LTDA"]
        tela.show()
        app.exec()
        conexao_banco()
        executar_consulta(m_informa_pedido)


def criar_tela():
    print("ok")
    tela.textBrowser.clear()
    lbl_numero_pedido.setText(f" Numero Pedido: {mnum_ped}")
    lbl_cabecalho.setText(f"Itens  Codigo   Descricao                  ")
    # try:
    hg.conexao_cursor.execute(
        f"SELECT pcod_merc, pmerc, pquantd, pvlr_fat FROM sacped_s WHERE pnum_ped = '{mnum_ped}'"
    )
    # # 145082Recupere o resultado
    resultados = hg.conexao_cursor.fetchall()
    hg.conexao_bd.commit()
    lbl_sub_total = tela.findChild(QtWidgets.QLabel, "sub_total")
    # lbl_produto = tela.findChild(QtWidgets.QLabel, "produto")
    fonte = QtGui.QFont()
    fonte.setFamily("Courier")
    fonte.setPointSize(9)
    tela.textBrowser.setFont(fonte)

    # tela.textBrowser.append("Itens Codigo   Descricao                  ")
    # tela.textBrowser.append('Quant.   Valor R$   Total R$')
    # tela.textBrowser.append(
    #     "--------------------------------------------------------"
    # )
    mtotal_geral = 0
    i = 0
    descricao = ""
    codigo_produto = ""
    # Exibir os resultados no QTextEdit
    if len(resultados) > 0:
        for resultado in resultados:
            i += 1
            pcod_merc, pmerc, pquantd, pvlr_fat = resultado
            # pcod_merc
            mquantd = "{:9,.3f}".format(pquantd)
            mvalor = "{:10,.2f}".format(pvlr_fat)
            soma = pquantd * pvlr_fat
            codigo_produto = pcod_merc
            descricao = pmerc
            # ic(soma)
            msoma = "{:12,.2f}".format(soma)
            linha = f"  {i}   {pcod_merc}  {pmerc}"  # Formatar o campo valor como float com 2 casas decimais
            linha1 = f"                {mquantd} x {mvalor} = {msoma}"  # Formatar o campo valor como float com 2 casas decimais
            mtotal_geral += soma
            # linha = ' '.join(map(str, resultado))
            tela.textBrowser.append(linha)
            tela.textBrowser.append(linha1)
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
        mtotal_g = "{:12,.2f}".format(mtotal_geral)
        linha1 = f"SUB-TOTAL: {mtotal_g}"
        lbl_sub_total.setText(linha1)
        lbl_produto.setText(descricao)
    else:
        lbl_produto.setText("C A I X A   L I V R E ")

    # except Exception as e:
    #     print(f"Erro ao executar a consulta: {e}")


class ConsultaProduto(QMainWindow):
    def __init__(self):
        super().__init__()
        conexao_banco()
        tela1.show()
        # app.exec()

    # app1 = QtWidgets.QApplication([])
    # app1.setStyleSheet(hg.style_sheet)
    # tela1 = uic.loadUi(f"{hg.c_ui}\\f4_merc.ui")
    # tela1.setWindowTitle("PRODUTOS CADASTRADO")
    # icon = QIcon(f"{hg.c_imagem}\\htiico.jpg")
    # icon_sair = QIcon(f"{hg.c_imagem}\\sair.png")
    # icon_incluir = QIcon(f"{hg.c_imagem}\\incluir.png")
    # tela1.setWindowIcon(icon)
    # tabela1 = tela1.tableWidget

    # PEGA O NOME DO ARQUIVO EM EXECUCAO
    nome_file_com = os.path.basename(__file__)
    nome_file, ext = os.path.splitext(nome_file_com)
    # AJUSTAR A TELA EM RELACAO AO MONITOR
    qt_rectangle = tela1.frameGeometry()
    center_point = app.primaryScreen().availableGeometry().center()
    qt_rectangle.moveCenter(center_point)

    if hg.mtp_tela == "G":
        primary_screen = QGuiApplication.primaryScreen()
        if primary_screen is not None:
            screen_geometry = primary_screen.geometry()
            tela1.setGeometry(screen_geometry)

    tela1.statusBar.showMessage(f"<< {nome_file} >>")
    if os.path.exists(f"{hg.c_imagem}\\htifirma.jpg"):
        imagem = QPixmap(f"{hg.c_imagem}\\htifirma.jpg")
    else:
        imagem = QPixmap(f"{hg.c_imagem}\\htifirma1.jpg")

    pixmap_redimensionado = imagem.scaled(350, 50)  # redimensiona a imagem para 100x100
    tela1.empresa.setPixmap(pixmap_redimensionado)
    # mconsulta_inclusao = ""

    # Define a função para ajustar as colunas da tabela
    # def ajustar_colunas_tabela(self, x):
    #     # print(x)
    #     header = tabela1.horizontalHeader()
    #     header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
    #     header.setStretchLastSection(False)

    def editar_prod(self, row):
        # rb_tipo_consulta = None
        tela1.tableWidget.itemDoubleClicked.disconnect()
        tela1.tableWidget.cellActivated.disconnect()
        # print(f"linha: {row}")
        # item = tela1.tableWidget.item(row, 0)
        item = tela1.tableWidget.item(row, 0)
        tela.mcodigo.setText(item.text())
        tela1.close()
        print(f"item {item.text()}")
        tela1.tableWidget.cellActivated.connect(
            lambda row, col: self.editar_prod(item.row())
        )

        tela1.tableWidget.itemDoubleClicked.connect(
            lambda item: self.editar_prod(item.row())
        )
        # verificar_produto()
        # criar_tela()
        return

    def pesquisa_prod(self):
        if hg.mtipo_temrinal == "L":
            valor_aprazo_calculado = "pr_venda * ((varejo / 100) + 1)"
        else:
            valor_aprazo_calculado = (
                "iif(pr_venda1 > 0, pr_venda1, pr_venda * ((varejo / 100) + 1))"
            )

        nome_buscar = tela1.pesquisa.text()
        hg.conexao_cursor.execute(
            f"SELECT CAST(cod_merc as char(5)) as cod_merc, COALESCE(merc, ' ') as merc, "
            f"REPLACE(CAST(saldo_mer AS DECIMAL(12, 2)), '.', ',') as saldomer, "
            f"REPLACE(CAST(pr_venda AS DECIMAL(12, 2)), '.', ',') as prvenda, "
            f"REPLACE(CAST({valor_aprazo_calculado} AS DECIMAL(12, 2)), '.', ','), "
            f"COALESCE(unidade, ' '), "
            f"COALESCE(cod_barr, ' '), COALESCE(ref, ' ') FROM sacmerc "
            f"WHERE (cod_merc LIKE UPPER('%{nome_buscar}%') OR "
            f"merc LIKE UPPER('%{nome_buscar}%') OR cod_barr LIKE UPPER('%{nome_buscar}%') "
            f"OR ref LIKE UPPER('%{nome_buscar}%')) ORDER BY cod_merc"
        )
        return

    def listar_produto(self):
        self.pesquisa_prod()
        dados_lidos = hg.conexao_cursor.fetchall()
        hg.conexao_bd.commit()
        tela1.tableWidget.setRowCount(len(dados_lidos))
        tela1.tableWidget.setColumnCount(8)
        for i, linha in enumerate(dados_lidos):
            for j, valor in enumerate(linha):
                valor = str(valor) if valor is not None else ""
                item = QtWidgets.QTableWidgetItem(valor)
                tela1.tableWidget.setItem(i, j, item)
        header = tabela1.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setStretchLastSection(False)

        tela1.tableWidget.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers
        )
        tela1.bt_sair.clicked.connect(fecha_tela)
        tela1.bt_sair.setIcon(icon_sair)

        tela1.pesquisa.textChanged.connect(self.pesquisa_prod)
        tela1.tableWidget.cellActivated.connect(
            lambda row, col: self.editar_prod(item.row())
        )
        tela1.tableWidget.itemDoubleClicked.connect(
            lambda item: self.editar_prod(item.row())
        )


def verificar_produto():
    global mnum_ped, infor_pedido
    instancia = ConsultaProduto()
    # ic()
    m_codigo = tela.mcodigo.text()
    print(m_codigo)
    if len(m_codigo) == 0:
        instancia.listar_produto()
        return
    if m_codigo[0] == "X":
        tela.mquantidade.setValue(float(m_codigo[1:20]))
        tela.mcodigo.setText("")
        return
    else:
        # print(infor_pedido[3][0:5])
        hg.conexao_cursor.execute(
            f"SELECT desconto FROM saccli WHERE cod_cli = {infor_pedido[3][0:5]}"
        )
        ver_cliente = hg.conexao_cursor.fetchone()
        hg.conexao_bd.commit()
        if len(m_codigo) <= 5:
            m_codigo = m_codigo.zfill(5)
            hg.conexao_cursor.execute(
                f"SELECT * FROM sacmerc WHERE cod_merc = '{m_codigo}'"
            )
        else:
            hg.conexao_cursor.execute(
                f"SELECT * FROM sacmerc WHERE cod_barr = '{m_codigo}'"
            )
        ver_produto = hg.conexao_cursor.fetchone()
        hg.conexao_bd.commit()
        if ver_produto is None:
            atencao("Produto nao encontrado...")
        else:
            if mnum_ped == "":
                mnum_ped = gerar_numero_pedido()

            if hg.m_indiv[25] == "S":
                tela.mpreco_venda.setValue(float(ver_produto[45]))

            # msaldo = f"{ver_produto[55]:,.3f}".replace(",", " ").replace(".", ",")
            msaldo = f"{ver_produto[55]:,.3f}"
            lbl_saldo.setText(msaldo)
            # tela.mpreco_venda.Value()
            m_quantidade = tela.mquantidade.value()
            mvlr_fat = tela.mpreco_venda.value()
            mp_venda = float(ver_produto[45])
            lbl_produto.setText(ver_produto[8])
            m_codmerc = ver_produto[7]
            m_saldo_ant = float(ver_produto[55])
            m_saldo_pos = m_saldo_ant - m_quantidade
            # m_data_f = datetime.strptime(data_atual.text(), "%d/%m/%Y").date()
            m_data_f = data_atual.toPyDateTime().date()
            data_formatada = m_data_f.strftime("%Y/%m/%d")
            # mhora = data_atual.toString("hh:mm:ss")
            mcomissao = ver_produto[25]
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
                        mquantd = 1
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

                if 0 < hg.m_set[153] < m_quantidade:
                    atencao("QUANTIDADE Solicitada maior que o MAXIMO Permitido")
                    return

                hg.conexao_cursor.execute(
                    f"SELECT sum(pquantd * pvlr_fat) FROM sacped_s WHERE pnum_ped = '{mnum_ped}'"
                )
                msubtotal = hg.conexao_cursor.fetchone()
                hg.conexao_bd.commit()

                if (
                    (infor_pedido[9] + msubtotal + (mvlr_fat * m_quantidade))
                    >= infor_pedido[8]
                    > 0
                ):
                    atencao(
                        f"Limite do Cliente foi ultrapassado em R$: "
                        f"{(infor_pedido[9] + msubtotal + (mvlr_fat * m_quantidade))}"
                    )
                    return

            mhora = datetime.now().strftime("%H:%M:%S")
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

    tela.mcodigo.setText("")
    tela.mpreco_venda.setValue(float(0))
    mcomissao = mcomissao
    msaldo = f"{0:,.3f}"
    lbl_saldo.setText(msaldo)
    criar_tela()


def fecha_pedido():
    from venda_fecha import fechar_pedido

    fechar_pedido(mnum_ped)


keyboard.add_hotkey("F10", fecha_pedido)


def executar_consulta(m_informa_pedido):
    global mnum_ped, infor_pedido
    infor_pedido = m_informa_pedido
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
    tela.bt_fecha.clicked.connect(fecha_pedido)
    tela.bt_fecha.setIcon(icon_salvar)
    tela.bt_sair.clicked.connect(fecha_tela)
    tela.bt_sair.setIcon(icon_sair)
    # tela.recupera_pedido = QLineEdit(tela)
    # tela.recupera_pedido.setGeometry(500, 500, 140, 40)
    # tela.textBrowser.itemDoubleClicked.connect(lambda item: editar_item(item.row()))
    criar_tela()


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
    m_informacao_pedido = []
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
    MainWindow()
    hg.conexao_bd.close()
