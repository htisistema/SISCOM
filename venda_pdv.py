from PyQt6 import uic, QtWidgets, QtGui, QtCore
from PyQt6.QtGui import QIcon, QGuiApplication, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QListView,
    QMainWindow,
    QTableWidgetItem,
)
from PyQt6.QtCore import QDateTime, Qt
from PyQt6.QtCore import QEventLoop, pyqtSlot
from datetime import datetime
import keyboard
from hti_funcoes import conexao_banco, gerar_numero_pedido

from autorizacao_senha import aut_sen
import hti_global as hg
import os
from ATENCAO import atencao
from venda_pdvcx import fechar_pedido

app = QApplication([])
app.setStyleSheet(hg.style_sheet)
tela_venda = uic.loadUi(f"{hg.c_ui}\\venda_pdv.ui")
# BLOQUEIA O "X" DA TELA
tela_venda.setWindowFlags(
    tela_venda.windowFlags() & ~Qt.WindowType.WindowCloseButtonHint
)
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
mnum_ped = ""
key_f5 = 0
key_f10 = 0
mcomissao = 0
mquantidade = 1
mpreco = 0


class TelaProduto(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dados_lidos = []
        self.mcod_produto = ""
        self.init_ui()

    def init_ui(self):
        self.tela = uic.loadUi(f"{hg.c_ui}\\f4_merc.ui", self)
        self.setWindowTitle("PRODUTOS CADASTRADO")
        icon = QIcon(f"{hg.c_imagem}\\htiico.ico")
        self.setWindowIcon(icon)
        self.tabela1 = self.tela.tableWidget

        if hg.mtp_tela == "G":
            primary_screen = QGuiApplication.primaryScreen()
            if primary_screen is not None:
                screen_geometry = primary_screen.geometry()
                self.setGeometry(screen_geometry)

        if os.path.exists(f"{hg.c_imagem}\\htifirma.jpg"):
            imagem = QPixmap(f"{hg.c_imagem}\\htifirma.jpg")
        else:
            imagem = QPixmap(f"{hg.c_imagem}\\htifirma1.jpg")

        pixmap_redimensionado = imagem.scaled(350, 50)
        self.tela.empresa.setPixmap(pixmap_redimensionado)

        self.tela.pesquisa.textChanged.connect(self.pesquisa_prod)
        self.tela.bt_sair.clicked.connect(self.close)
        self.tabela1.cellActivated.connect(lambda row, col: self.editar_prod(row))
        self.tabela1.itemDoubleClicked.connect(
            lambda item: self.editar_prod(item.row())
        )

    def carregar_dados(self):
        valor_aprazo_calculado = (
            "pr_venda * ((varejo / 100) + 1)"
            if hg.mtipo_temrinal == "L"
            else "iif(pr_venda1 > 0, pr_venda1, pr_venda * ((varejo / 100) + 1))"
        )

        hg.conexao_cursor.execute(
            f"SELECT CAST(cod_merc as char(5)) as cod_merc, COALESCE(merc, ' ') as merc, "
            f"REPLACE(CAST(saldo_mer AS DECIMAL(12, 2)), '.', ',') as saldomer, "
            f"REPLACE(CAST(pr_venda AS DECIMAL(12, 2)), '.', ',') as prvenda, "
            f"REPLACE(CAST({valor_aprazo_calculado} AS DECIMAL(12, 2)), '.', ','), "
            f"COALESCE(unidade, ' '), "
            f"COALESCE(cod_barr, ' '), COALESCE(ref, ' ') FROM sacmerc "
            f"ORDER BY merc"
        )
        self.dados_lidos = hg.conexao_cursor.fetchall()
        hg.conexao_bd.commit()

    def editar_prod(self, row):
        item = self.tabela1.item(row, 0)
        self.mcod_produto = item.text()
        print(f"editar {self.mcod_produto}")
        self.close()

    def pesquisa_prod(self):

        nome_buscar = self.tela.pesquisa.text().strip().upper()
        resultados = (
            [dado for dado in self.dados_lidos if nome_buscar in dado[1]]
            if nome_buscar.startswith("*") and len(nome_buscar) > 1
            else [dado for dado in self.dados_lidos if dado[1].startswith(nome_buscar)]
        )
        self.listar_produto(resultados)

    def listar_produto(self, resultados):
        self.tela.pesquisa.setFocus()
        self.tabela1.setRowCount(len(resultados))
        self.tabela1.setColumnCount(8)
        for i, linha_p in enumerate(resultados):
            for j, valor in enumerate(linha_p):
                valor = str(valor) if valor is not None else ""
                item = QTableWidgetItem(valor)
                self.tabela1.setItem(i, j, item)
        header = self.tabela1.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setStretchLastSection(False)

        self.tabela1.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers
        )

    def consulta_produto(self):
        print("consulta produto")
        self.carregar_dados()
        self.listar_produto(self.dados_lidos)
        self.show()
        # Bloquear o loop de eventos principal até a janela ser fechada
        loop = QEventLoop()
        self.loop = loop
        self.show()
        loop.exec()
        print(f"consulta {self.mcod_produto}")
        tela_venda.mcodigo.setText(self.mcod_produto)
        tela_venda.mcodigo.setFocus()
        return self.mcod_produto

    def closeEvent(self, event):
        if hasattr(self, "loop"):
            self.loop.quit()
        event.accept()


def buscar_produto():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    tela_produto = TelaProduto()
    resultado = tela_produto.consulta_produto()
    return resultado


class AlterarProduto(QMainWindow):
    def __init__(self):
        super().__init__()
        print("AlterarProduto")
        self.dados_pdv = []
        self.init_ui()

    def init_ui(self):
        print("init_ui")
        self.tela = uic.loadUi(f"{hg.c_ui}\\alteracao_pdv.ui", self)
        self.setWindowTitle("ALTERACAO DE PRODUTO PDV")
        icon = QIcon(f"{hg.c_imagem}\\htiico.ico")
        self.setWindowIcon(icon)
        self.tabela1 = self.tela.tableWidget
        if os.path.exists(f"{hg.c_imagem}\\htifirma.jpg"):
            imagem = QPixmap(f"{hg.c_imagem}\\htifirma.jpg")
        else:
            imagem = QPixmap(f"{hg.c_imagem}\\htifirma1.jpg")

        pixmap_redimensionado = imagem.scaled(350, 50)
        self.tela.empresa.setPixmap(pixmap_redimensionado)

        self.tela.bt_sair.clicked.connect(self.close)
        self.tabela1.cellActivated.connect(lambda row, col: self.editar_prod(row))
        self.tabela1.itemDoubleClicked.connect(
            lambda item: self.editar_prod(item.row())
        )
        self.tela.ds_quantidade.setAlignment(Qt.AlignmentFlag.AlignRight)
        # self.tela.preco.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        # self.tela.preco.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.consulta_pdv()

    def carregar_pdv(self):
        print("carregar_pdv")
        hg.conexao_cursor.execute(
            f"SELECT pcod_merc, pmerc, REPLACE(CAST(pquantd AS DECIMAL(12, 3)), '.', ','), "
            f"REPLACE(CAST(pvlr_fat AS DECIMAL(12, 2)), '.', ','), sr_recno FROM sacped_s "
            f"WHERE pnum_ped = '{mnum_ped}' order by sr_recno"
        )
        self.dados_pdv = hg.conexao_cursor.fetchall()
        hg.conexao_bd.commit()

    def editar_prod(self, row):
        print("editar_prod")
        self.tela.ds_quantidade.setFocus()
        self.tela.ds_quantidade.selectAll()

        item = self.tabela1.item(row, 0)
        self.msr_recno = self.tabela1.item(row, 4).text()
        self.qtd = self.tabela1.item(row, 2).text()
        preco = self.tabela1.item(row, 3).text()
        self.qtd = self.qtd.replace(",", ".")
        print(f"quantidade: {self.qtd}")
        lbl_produto = self.tela.findChild(QtWidgets.QLabel, "produto")
        lbl_preco = self.tela.findChild(QtWidgets.QLabel, "preco")
        self.mcodigo = self.tabela1.item(row, 0).text()
        mdescri = self.tabela1.item(row, 1).text()
        lbl_produto.setText(f"{self.mcodigo} {mdescri}")
        lbl_preco.setText(preco)

        self.tela.ds_quantidade.setValue(float(self.qtd))
        print(f"editar {self.mcodigo}")
        # self.close()

    def atualizar_pdv(self):
        hg.conexao_cursor.execute(
            f"SELECT pcod_merc, pmerc, pquantd, sr_recno FROM sacped_s "
            f"WHERE sr_recno = {self.msr_recno}"
        )
        consulta_ped = hg.conexao_cursor.fetchone()
        hg.conexao_bd.commit()

        hg.conexao_cursor.execute(
            f"SELECT saldo_mer, PR_VENDA, CUST_MERC FROM sacmerc WHERE cod_merc = '{self.mcodigo}'"
        )
        self.qtd = self.tela.ds_quantidade.value()
        ver_produto = hg.conexao_cursor.fetchone()
        hg.conexao_bd.commit()
        m_data_f = data_atual.toPyDateTime().date()
        data_formatada = m_data_f.strftime("%Y/%m/%d")
        mhora = datetime.now().strftime("%H:%M:%S")
        mqtd_digitada = float(consulta_ped[2])
        msaldo_produto = float(ver_produto[0])
        mdif_qtd = mqtd_digitada - float(self.qtd)
        if mqtd_digitada > self.qtd:
            # if not aut_sen("Quantidade menor que o Solicitador Anteriormente:",
            #                "LIB_ALTSLDPED","","","","AMBIE"):
            #     return
            status = "E"
            mdif_qtd = mqtd_digitada - float(self.qtd)
            m_saldo_pos = msaldo_produto + mdif_qtd
        else:

            status = "S"
            mdif_qtd = mqtd_digitada - float(self.qtd)
            m_saldo_pos = msaldo_produto + mdif_qtd

        # print(
        #     f"saldo atual: {msaldo_produto} qtd solicitado: {mqtd_digitada} qtd alterado: {self.qtd} "
        #     f"saldo pos: {m_saldo_pos} diferenca: {mdif_qtd} status {status}"
        # )

        hg.conexao_cursor.execute(
            f"UPDATE sacmerc SET saldo_mer = {m_saldo_pos}, "
            f"data_atu = '{data_formatada}' WHERE cod_merc = {self.mcodigo}"
        )
        hg.conexao_bd.commit()
        hg.conexao_cursor.execute(
            f"UPDATE sacped_s SET pquantd = {self.qtd} "
            f"WHERE sr_recno = {self.msr_recno}"
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
                self.mcodigo,
                mquantidade,
                msaldo_produto,
                m_saldo_pos,
                hg.geral_cod_usuario,
                "VENDA",
                hg.nome_computador,
                f"ALTERACAO PD: '{mnum_ped}'",
                status,
                float(ver_produto[1]),
                float(ver_produto[2]),
                " ",
            ),
        )
        hg.conexao_bd.commit()
        print("atualizacao com sucesso")
        if hasattr(self, "loop"):
            self.loop.quit()
        self.tela.close()
        criar_tela_venda()
        # return

    def listar_pdv(self, resultados):
        self.tabela1.setRowCount(len(resultados))
        self.tabela1.setColumnCount(5)
        for i, linha_p in enumerate(resultados):
            for j, valor in enumerate(linha_p):
                valor = str(valor) if valor is not None else ""
                item = QTableWidgetItem(valor)
                self.tabela1.setItem(i, j, item)
        header = self.tabela1.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
        header.setStretchLastSection(False)

        self.tabela1.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.tela.bt_salvar.clicked.connect(self.atualizar_pdv)
        # self.tela.bt_sair.clicked.connect(sair_alteracao)

    def consulta_pdv(self):
        print("consulta pdv")
        self.carregar_pdv()
        self.listar_pdv(self.dados_pdv)
        self.show()
        # Bloquear o loop de eventos principal até a janela ser fechada
        loop = QEventLoop()
        self.loop = loop
        self.show()
        loop.exec()
        return

    def closeEvent(self, event):
        print("closeEvent")
        if hasattr(self, "loop"):
            self.loop.quit()
        event.accept()


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
    descricao = ""
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


def confirma_produto():
    # print("confirma_produto")
    global mnum_ped, mcomissao, mpreco, mquantidade, key_f10, key_f5
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
    mhora = datetime.now().strftime("%H:%M:%S")
    mcomissao = ver_produto[25]
    tela_venda.mcodigo.setText(ver_produto[7])

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
    key_f5 = 1


def keyPressEvent(event):
    global key_f5, key_f10
    print("keyPressEvent")
    # if (
    #     event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return
    # ) and key_f5 == 1:
    #     # confirma_produto()
    #     AlterarProduto()
    #     key_f5 = 0
    # elif event.key() == Qt.Key.Key_Escape:
    #     # print("Esc pressionado")
    #     fecha_tela_venda()

    if event.key() == Qt.Key.Key_F5 and key_f5 == 1:
        print("f5")
        app = QApplication.instance()
        if app is None:
            app = QApplication([])

        AlterarProduto()
        # confirma_produto()
        key_f5 = 0

    if event.key() == Qt.Key.Key_F10 and key_f10 == 1:
        # print('f12')
        salva_venda()
        key_f10 = 0


tela_venda.keyPressEvent = keyPressEvent


def verificar_produto():
    # print("verificar_produto")
    global mnum_ped, mquantidade
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

    confirma_produto()
    # if hg.m_indiv[25] == "S":
    #     verificar_preco()


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


def venda_pdv():
    global mnum_ped, mpreco, mquantidade
    mpreco = 0
    mquantidade = 1
    keyboard.add_hotkey("ESC", fecha_tela_venda)
    # instancia = ConsultaProduto()
    mpreco_txt = f"{mpreco:,.3f}"
    mquantidade_txt = f"{mquantidade:,.3f}"
    mtot_itens = f"{mquantidade * mpreco:,.2f}"
    lbl_preco.setText(mpreco_txt)
    lbl_quantidade.setText(mquantidade_txt)
    lbl_total_itens.setText(mtot_itens)
    tela_venda.mcodigo.returnPressed.connect(verificar_produto)
    tela_venda.mcodigo.setFocus()
    mnum_ped = ""
    # if m_informa_pedido[6] == "A":
    #     tipo_venda = "Avista"
    # else:
    #     tipo_venda = "Aprazo"

    # tela_venda.bt_buscar_produto.clicked.connect(TelaProduto)
    tela_venda.bt_buscar_produto.clicked.connect(buscar_produto)
    tela_venda.bt_fecha.clicked.connect(salva_venda)
    tela_venda.bt_sair.clicked.connect(fecha_tela_venda)

    tela_venda.bt_fecha.setIcon(icon_salvar)
    tela_venda.bt_sair.setIcon(icon_sair)
    tela_venda.bt_buscar_produto.setIcon(icon_consulta)
    tela_venda.show()
    criar_tela_venda()
    # app.exec()


if __name__ == "__main__":
    tela_venda.show()
    conexao_banco()
    # 145082
    venda_pdv()
    app.exec()
    hg.conexao_bd.close()
