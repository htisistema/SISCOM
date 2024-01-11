from PyQt6 import uic, QtWidgets, QtGui
from PyQt6.QtGui import QIcon, QGuiApplication, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QButtonGroup
from PyQt6.QtCore import QDateTime, Qt
# import keyboard
# from datetime import datetime
from hti_funcoes import conexao_banco
import hti_global
import os
from icecream import ic

app = QApplication([])
app.setStyleSheet(hti_global.style_sheet)
tela = uic.loadUi(f"{hti_global.c_ui}\\venda_fecha.ui")
icon = QIcon(f"{hti_global.c_imagem}\\htiico.jpg")
tela.setWindowIcon(icon)
tela.setWindowTitle(
    f"FECHAMENTO DO PEDIDO DE VENDA         {hti_global.SISTEMA}  Versao: {hti_global.VERSAO}"
)
# Centraliza a janela na tela
qt_rectangle = tela.frameGeometry()
center_point = app.primaryScreen().availableGeometry().center()
qt_rectangle.moveCenter(center_point)
tela.move(qt_rectangle.topLeft())
icon_salvar = QIcon(f"{hti_global.c_imagem}\\confirma.png")
icon_sair = QIcon(f"{hti_global.c_imagem}\\sair.png")
tela.setWindowIcon(icon)
# Centraliza a janela na tela
# AJUSTAR A TELA EM RELACAO AO MONITOR
qt_rectangle = tela.frameGeometry()
center_point = app.primaryScreen().availableGeometry().center()
qt_rectangle.moveCenter(center_point)
tela.move(qt_rectangle.topLeft())

if hti_global.mtp_tela == "G":
    primary_screen = QGuiApplication.primaryScreen()
    if primary_screen is not None:
        screen_geometry = primary_screen.geometry()
        tela.setGeometry(screen_geometry)

# PEGA O NOME DO ARQUIVO EM EXECUCAO
nome_file_com = os.path.basename(__file__)
nome_file, ext = os.path.splitext(nome_file_com)
tela.statusbar.showMessage(f"<< {nome_file} >>")

if os.path.exists(f"{hti_global.c_imagem}\\htifirma.jpg"):
    imagem = QPixmap(f"{hti_global.c_imagem}\\htifirma.jpg")
else:
    imagem = QPixmap(f"{hti_global.c_imagem}\\htifirma1.jpg")

pixmap_redimensionado = imagem.scaled(350, 50)  # redimensiona a imagem para 100x100
tela.empresa.setPixmap(pixmap_redimensionado)

# logohti = QPixmap(f"{hti_global.c_imagem}\\LOGOhti.png")
# pixmap_redimensionado = logohti.scaled(85, 85)  # redimensiona a imagem para 100x100
# tela.logohti.setStyleSheet(
#     "background-color: rgb(190, 216, 255);border-width: 0px;border-radius: 0px;"
# )
# tela.logohti.setPixmap(pixmap_redimensionado)

# if os.path.exists(f"{hti_global.c_imagem}\\htifirma.jpg"):
#     imagem = QPixmap(f"{hti_global.c_imagem}\\htifirma.jpg")
# else:
#     imagem = QPixmap(f"{hti_global.c_imagem}\\htifirma1.jpg")
#
# pixmap_redimensionado = imagem.scaled(450, 350)  # redimensiona a imagem para 100x100
# tela.foto_produto.setPixmap(pixmap_redimensionado)
# print(f"{hti_global.c_usuario}\\{hti_global.geral_cod_usuario}.jpg")

# lbl_operador = tela.findChild(QtWidgets.QLabel, "operador")
# if os.path.exists(f"{hti_global.c_usuario}\\{hti_global.geral_cod_usuario}.jpg"):
#     usuario = QPixmap(f"{hti_global.c_usuario}\\{hti_global.geral_cod_usuario}.jpg")
#
# else:
#     usuario = QPixmap(f"{hti_global.c_usuario}\\htiusu.jpg")
# pixmap_redimensionado = usuario.scaled(125, 130)  # redimensiona a imagem para 100x100
# tela.usuario.setPixmap(pixmap_redimensionado)
# lbl_operador.setText(f" Operador: {hti_global.geral_cod_usuario}")
lbl_numero_pedido = tela.findChild(QtWidgets.QLabel, "numero_pedido")

mnum_ped = ""
lbl_produto = tela.findChild(QtWidgets.QLabel, "produto")
lbl_produto.setText("F E C H A M E N T O   D O   P E D I D O")
lbl_cabecalho = tela.findChild(QtWidgets.QLabel, "cabecalho")
data_atual = QDateTime.currentDateTime()

conexao_banco()
hti_global.conexao_cursor.execute("SELECT * FROM sacsetup")
# # 145082Recupere o resultado
m_set = hti_global.conexao_cursor.fetchone()
hti_global.conexao_bd.commit()

hti_global.conexao_cursor.execute(f"SELECT cod_cli, razao FROM saccli")
arq_cli = hti_global.conexao_cursor.fetchall()
hti_global.conexao_bd.commit()
for ret_cli in arq_cli:
    item = f'{ret_cli[0]} - {ret_cli[1]}'.strip('(),')
    tela.cb_cliente.addItem(item)
tela.cb_cliente.setCurrentIndex(0)


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


def criar_tela(mnum_pedido):
    tela.textBrowser.clear()
    lbl_numero_pedido.setText(f" Numero Pedido: {mnum_pedido}")
    lbl_cabecalho.setText(f"Itens  Codigo   Descricao                  ")
    try:
        hti_global.conexao_cursor.execute(
            f"SELECT pcod_merc, pmerc, pquantd, pvlr_fat FROM sacped_s WHERE pnum_ped = '{mnum_pedido}'"
        )
        # # 145082Recupere o resultado
        resultados = hti_global.conexao_cursor.fetchall()
        hti_global.conexao_bd.commit()

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
                # print(f"{hti_global.c_produto}\\{mcodigo}.jpg")
            mtotal_g = "{:12,.2f}".format(mtotal_geral)
            linha1 = f"SUB-TOTAL: {mtotal_g}"
            lbl_sub_total.setText(linha1)

    except Exception as e:
        print(f"Erro ao executar a consulta: {e}")


def salva_pedido():
    ic()


def verifica_condicao():
    tela.ds_vlr_entrada.setValue(float(0))
    tela.ds_entrada.setValue(float(0))
    tela.ds_qtd_dias.setValue(float(0))

    index = tela.cb_forma_pg.currentIndex()
    mop = tela.cb_forma_pg.itemText(index)
    m_tipo_pag = mop[0:1]
    ic(m_tipo_pag)
    if m_tipo_pag == '3':
        tela.ds_qtd_dias.setEnabled(True)
        tela.ds_qtd_dias.setFocus()
        tela.ds_qtd_dias.selectAll()
    elif m_tipo_pag == '4' or m_tipo_pag == '5':
        tela.ds_entrada.setEnabled(True)
        tela.ds_qtd_dias.setEnabled(True)
        tela.ds_entrada.setFocus()
        tela.ds_entrada.selectAll()

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
    hti_global.conexao_cursor.execute(f"SELECT pcod_cli FROM sacped_s WHERE pnum_ped = '{mnum_pedido}'")
    res_pedido = hti_global.conexao_cursor.fetchone()
    hti_global.conexao_bd.commit()
    # ic(res_pedido[0])
    if res_pedido[0] == 0:
        mcod_cli = m_set[83]
    else:
        mcod_cli = res_pedido[0]

    for i in range(tela.cb_cliente.count()):
        item_text = tela.cb_cliente.itemText(i)
        if str(mcod_cli).strip() in item_text:
            tela.cb_cliente.setCurrentIndex(i)
            break
    liberar_campos()
    tela.cb_forma_pg.currentIndexChanged.connect(verifica_condicao)
    tela.ds_qtd_dias.valueChanged.connect(liberar_campos)

    tela.bt_fecha.clicked.connect(salva_pedido)
    tela.bt_fecha.setIcon(icon_salvar)
    tela.bt_sair.clicked.connect(fecha_tela)
    tela.bt_sair.setIcon(icon_sair)

    # tela.mcodigo.returnPressed.connect(verificar_produto)
    # tela.mcodigo.setFocus()
    # tela.textBrowser.itemDoubleClicked.connect(lambda item: editar_item(item.row()))
    criar_tela(mnum_pedido)
    tela.show()
    app.exec()


if __name__ == "__main__":
    mnum_ped = "145082"
    fechar_pedido(mnum_ped)
    hti_global.conexao_bd.close()

                # IF m_set[1,37] = 'S'
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
