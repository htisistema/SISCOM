from PyQt6 import uic, QtWidgets, QtGui
from PyQt6.QtGui import QIcon, QGuiApplication, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox  # , QLineEdit
from PyQt6.QtCore import QDateTime
from datetime import datetime
import keyboard
from hti_funcoes import conexao_banco, gerar_numero_pedido
import hti_global as hg
import os
# from icecream import ic


app = QApplication([])
app.setStyleSheet(hg.style_sheet)
tela = uic.loadUi(f"{hg.c_ui}\\venda_pdv.ui")
icon = QIcon(f"{hg.c_imagem}\\htiico.jpg")
tela.setWindowIcon(icon)
tela.setWindowTitle(
    f"PEDIDO DE VENDA         {hg.SISTEMA}  Versao: {hg.VERSAO}"
)
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

mnum_ped = ''
tela.mquantidade.setValue(1)
lbl_produto = tela.findChild(QtWidgets.QLabel, "produto")
lbl_cabecalho = tela.findChild(QtWidgets.QLabel, "cabecalho")
lbl_saldo = tela.findChild(QtWidgets.QLabel, "saldo")
data_atual = QDateTime.currentDateTime()


def fecha_tela():
    tela.close()
    return


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        conexao_banco()
        executar_consulta()


def criar_tela():
    tela.textBrowser.clear()
    lbl_numero_pedido.setText(f" Numero Pedido: {mnum_ped}")
    lbl_cabecalho.setText(f"Itens  Codigo   Descricao                  ")
    try:
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
        # Exibir os resultados no QTextEdit
        if len(resultados) > 0:
            for resultado in resultados:
                i += 1
                pcod_merc, pmerc, pquantd, pvlr_fat = resultado
                # pcod_merc
                mquantd = "{:9,.3f}".format(pquantd)
                mvalor = "{:10,.2f}".format(pvlr_fat)
                soma = pquantd * pvlr_fat
                # ic(soma)
                msoma = "{:12,.2f}".format(soma)
                linha = f"  {i}   {pcod_merc}  {pmerc}"  # Formatar o campo valor como float com 2 casas decimais
                linha1 = f"                {mquantd} x {mvalor} = {msoma}"  # Formatar o campo valor como float com 2 casas decimais
                mtotal_geral += soma
                # linha = ' '.join(map(str, resultado))
                tela.textBrowser.append(linha)
                tela.textBrowser.append(linha1)
                # print(f"{hg.c_produto}\\{mcodigo}.jpg")
            if os.path.exists(f"{hg.c_produto}\\{pcod_merc}.jpg"):
                imagem1 = QPixmap(f"{hg.c_produto}\\{pcod_merc}.jpg")
            else:
                if os.path.exists(f"{hg.c_imagem}\\htifirma.jpg"):
                    imagem1 = QPixmap(f"{hg.c_imagem}\\htifirma.jpg")
                else:
                    imagem1 = QPixmap(f"{hg.c_imagem}\\htifirma1.jpg")

            pixmap_redim = imagem1.scaled(
                500, 350
            )  # redimensiona a imagem para 100x100
            tela.foto_produto.setPixmap(pixmap_redim)
            mtotal_g = "{:12,.2f}".format(mtotal_geral)
            linha1 = f"SUB-TOTAL: {mtotal_g}"
            lbl_sub_total.setText(linha1)
            lbl_produto.setText(pmerc)
        else:
            lbl_produto.setText("C A I X A   L I V R E ")

    except Exception as e:
        print(f"Erro ao executar a consulta: {e}")


def verificar_produto():
    global mnum_ped
    # print(tela.mcodigo.text())
    # ic()
    m_codigo = tela.mcodigo.text()
    if m_codigo[0] == "X":
        tela.mquantidade.setValue(float(m_codigo[1:20]))
        tela.mcodigo.setText("")
        return
    else:
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
            QMessageBox.critical(tela, "ATENCAO", 'Produto nao encontrado...')
        else:
            if mnum_ped == '':
                mnum_ped = gerar_numero_pedido()

            # msaldo = f"{ver_produto[55]:,.3f}".replace(",", " ").replace(".", ",")
            msaldo = f"{ver_produto[55]:,.3f}"
            lbl_saldo.setText(msaldo)
            tela.mpreco_venda.setValue(float(ver_produto[45]))
            m_quantidade = tela.mquantidade.value()
            m_pre_venda = tela.mpreco_venda.value()
            lbl_produto.setText(ver_produto[8])
            m_codmerc = ver_produto[7]
            m_saldo_ant = float(ver_produto[55])
            m_saldo_pos = m_saldo_ant - m_quantidade
            # m_data_f = datetime.strptime(data_atual.text(), "%d/%m/%Y").date()
            m_data_f = data_atual.toPyDateTime().date()
            data_formatada = m_data_f.strftime("%Y/%m/%d")
            # mhora = data_atual.toString("hh:mm:ss")

            mhora = datetime.now().strftime("%H:%M:%S")
            hg.conexao_cursor.execute(f"UPDATE sacmerc SET saldo_mer = {m_saldo_pos}, "
                                              f"data_atu = '{data_formatada}' WHERE cod_merc = {m_codmerc}")
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

            hg.conexao_cursor.execute(sql, (
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
                    " "))
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
                    '',
                    ver_produto[16],
                    ver_produto[15],
                    ver_produto[73],
                    m_quantidade,
                    0,
                    0,
                    m_pre_venda,
                    0,
                    m_pre_venda * 1,
                    m_pre_venda,
                    float(ver_produto[46]),
                    float(ver_produto[44]),
                    float(ver_produto[43]),
                    0,
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    ver_produto[29],
                    ver_produto[30],
                    hg.geral_cod_usuario,
                    0,
                    0,
                    '',
                    ver_produto[20],
                    '',
                    '',
                    0,
                    0,
                    '',
                    mhora,
                    '',
                    0,
                    ver_produto[60],
                    float(ver_produto[22]),
                    '',
                    '',
                    0,
                    ver_produto[26],
                    float(ver_produto[74]),
                    float(ver_produto[61]),
                    float(ver_produto[64]),
                    '',
                    ver_produto[81],
                    '',
                    ver_produto[82],
                    '',
                    '',
                    '',
                    '',
                    ver_produto[72][:2],
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    None,
                    '',
                    '',
                    1,
                    " "))
            hg.conexao_bd.commit()

    tela.mcodigo.setText("")
    tela.mpreco_venda.setValue(float(0))
    msaldo = f"{0:,.3f}"
    lbl_saldo.setText(msaldo)
    criar_tela()


def fecha_pedido():
    from venda_fecha import fechar_pedido
    fechar_pedido(mnum_ped)


keyboard.add_hotkey('F10', fecha_pedido)


def executar_consulta():
    tela.mcodigo.returnPressed.connect(verificar_produto)
    tela.mcodigo.setFocus()
    tela.bt_fecha.clicked.connect(fecha_pedido)
    tela.bt_fecha.setIcon(icon_salvar)
    tela.bt_sair.clicked.connect(fecha_tela)
    tela.bt_sair.setIcon(icon_sair)
    # tela.recupera_pedido = QLineEdit(tela)
    # tela.recupera_pedido.setGeometry(500, 500, 140, 40)
    # tela.textBrowser.itemDoubleClicked.connect(lambda item: editar_item(item.row()))
    criar_tela()
    tela.show()
    app.exec()


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
        QMessageBox.information(
            tela, "Pesquisa de PRODUTO", f"PRODUTO: '{resutado_prod[0]}'"
        )
        if not mnum_ped == "":
            print(mnum_ped)
        return
    else:
        QMessageBox.information(
            tela, "Pesquisa de PRODUTO", "PRODUTO nao encontrado...!!!"
        )
        return

# def venda():
#     tela.mcodigo.textChanged.connect(pesquisa_produto)
#     return


if __name__ == "__main__":
    mnum_ped = "145082"
    MainWindow()
    hg.conexao_bd.close()
