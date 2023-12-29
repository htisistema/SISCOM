from PyQt6 import uic, QtWidgets, QtGui
from PyQt6.QtGui import QIcon, QGuiApplication, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from hti_funcoes import conexao_banco
import hti_global
import os

app = QApplication([])
app.setStyleSheet(hti_global.style_sheet)
tela = uic.loadUi(f"{hti_global.c_ui}\\venda_pdv.ui")
icon = QIcon(f"{hti_global.c_imagem}\\htiico.jpg")
tela.setWindowIcon(icon)
tela.setWindowTitle(f'PEDIDO DE VENDA         {hti_global.SISTEMA}  Versao: {hti_global.VERSAO}')
# Centraliza a janela na tela
qt_rectangle = tela.frameGeometry()
center_point = app.primaryScreen().availableGeometry().center()
qt_rectangle.moveCenter(center_point)
tela.move(qt_rectangle.topLeft())
icon_sair = QIcon(f"{hti_global.c_imagem}\\sair.png")
tela.setWindowIcon(icon)
# Centraliza a janela na tela
# AJUSTAR A TELA EM RELACAO AO MONITOR
qt_rectangle = tela.frameGeometry()
center_point = app.primaryScreen().availableGeometry().center()
qt_rectangle.moveCenter(center_point)
tela.move(qt_rectangle.topLeft())

if hti_global.mtp_tela == 'G':
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

logohti = QPixmap(f"{hti_global.c_imagem}\\LOGOhti.png")
pixmap_redimensionado = logohti.scaled(150, 150)  # redimensiona a imagem para 100x100
tela.logohti.setStyleSheet("background-color: rgb(190, 216, 255);border-width: 0px;border-radius: 0px;")
tela.logohti.setPixmap(pixmap_redimensionado)

if os.path.exists(f"{hti_global.c_imagem}\\htifirma.jpg"):
    imagem = QPixmap(f"{hti_global.c_imagem}\\htifirma.jpg")
else:
    imagem = QPixmap(f"{hti_global.c_imagem}\\htifirma1.jpg")

pixmap_redimensionado = imagem.scaled(450, 350)  # redimensiona a imagem para 100x100
tela.foto_produto.setPixmap(pixmap_redimensionado)
print(f"{hti_global.c_usuario}\\{hti_global.geral_cod_usuario}.jpg")

lbl_operador = tela.findChild(QtWidgets.QLabel, "operador")
if os.path.exists(f"{hti_global.c_usuario}\\{hti_global.geral_cod_usuario}.jpg"):
    usuario = QPixmap(f"{hti_global.c_usuario}\\{hti_global.geral_cod_usuario}.jpg")

else:
    usuario = QPixmap(f"{hti_global.c_usuario}\\htiusu.jpg")
pixmap_redimensionado = usuario.scaled(185, 190)  # redimensiona a imagem para 100x100
tela.usuario.setPixmap(pixmap_redimensionado)
lbl_operador.setText(f" Operador: {hti_global.geral_cod_usuario}")
lbl_numero_pedido = tela.findChild(QtWidgets.QLabel, "numero_pedido")

mnum_ped = ''


def executar_consulta():
    # tela.mcodigo.textChanged.connect(pesquisa_produto)
    tela.mcodigo.returnPressed.connect(pesquisa_produto)
    lbl_numero_pedido.setText(f" Numero Pedido: {mnum_ped}")

    try:
        hti_global.conexao_cursor.execute(f"SELECT pcod_merc, pmerc, pquantd, pvlr_fat, "
                                          f"sum(pquantd * pvlr_fat) as soma "
                                          f"FROM sacped_s WHERE pnum_ped = '{mnum_ped}' group by 1,2,3,4")
        # # 145082Recupere o resultado
        resultados = hti_global.conexao_cursor.fetchall()
        hti_global.conexao_bd.commit()

        lbl_sub_total = tela.findChild(QtWidgets.QLabel, "sub_total")
        lbl_produto = tela.findChild(QtWidgets.QLabel, "produto")
        fonte = QtGui.QFont()
        fonte.setFamily("Courier")
        fonte.setPointSize(9)
        tela.textBrowser.setFont(fonte)

        tela.textBrowser.append('Itens Codigo   Descricao                  ')
        # tela.textBrowser.append('Quant.   Valor R$   Total R$')
        tela.textBrowser.append('--------------------------------------------------------')
        mtotal_geral = 0
        i = 0
        # Exibir os resultados no QTextEdit
        if len(resultados) > 0:
            for resultado in resultados:
                i += 1
                pcod_merc, pmerc, pquantd, pvlr_fat, soma = resultado
                mcodigo = pcod_merc
                mquantd = "{:9,.3f}".format(pquantd)
                mvalor = '{:10,.2f}'.format(pvlr_fat)
                msoma = "{:12,.2f}".format(soma)
                linha = f"  {i}   {pcod_merc}  {pmerc}"  # Formatar o campo valor como float com 2 casas decimais
                linha1 = f"                   {mquantd} x {mvalor} = {msoma}"  # Formatar o campo valor como float com 2 casas decimais
                mtotal_geral += soma
                # linha = ' '.join(map(str, resultado))
                tela.textBrowser.append(linha)
                tela.textBrowser.append(linha1)
                # print(f"{hti_global.c_produto}\\{mcodigo}.jpg")
            if os.path.exists(f"{hti_global.c_produto}\\{mcodigo}.jpg"):
                imagem1 = QPixmap(f"{hti_global.c_produto}\\{mcodigo}.jpg")
            else:
                if os.path.exists(f"{hti_global.c_imagem}\\htifirma.jpg"):
                    imagem1 = QPixmap(f"{hti_global.c_imagem}\\htifirma.jpg")
                else:
                    imagem1 = QPixmap(f"{hti_global.c_imagem}\\htifirma1.jpg")

            pixmap_redim = imagem1.scaled(500, 350)  # redimensiona a imagem para 100x100
            tela.foto_produto.setPixmap(pixmap_redim)
            mtotal_g = "{:12,.2f}".format(mtotal_geral)
            linha1 = f"SUB-TOTAL: {mtotal_g}"
            lbl_sub_total.setText(linha1)
            lbl_produto.setText(pmerc)
        else:
            lbl_produto.setText('C A I X A   L I V R E ')

            # mtotal_g = "{:12,.2f}".format(mtotal_geral)
            # linha1 = f"SUB-TOTAL: {mtotal_g}"
            # lbl_sub_total.setText(linha1)
            # lbl_produto.setText(pmerc)
            # lcd = tela.findChild(QtWidgets.QLCDNumber, "lcdNumber")
            # valor_sem_virgula = mtotal_g.replace(',', '')
            # valor_numerico = float(valor_sem_virgula)
            # lcd.display(float(valor_numerico))
        tela.show()
        app.exec()

    except Exception as e:
        print(f"Erro ao executar a consulta: {e}")


def pesquisa_produto():
    nome_buscar = tela.mcodigo.text()
    if len(nome_buscar) <= 5:
        hti_global.conexao_cursor.execute(f"select cod_merc, merc, pr_venda FROM sacmerc "
                                          f"WHERE cod_merc = '{nome_buscar}'")
    else:
        hti_global.conexao_cursor.execute(f"select cod_merc, merc, pr_venda FROM sacmerc "
                                          f"WHERE cod_barr = '{nome_buscar}'")
    resutado_prod = hti_global.conexao_cursor.fetchone()
    hti_global.conexao_bd.commit()
    if resutado_prod is not None:
        QMessageBox.information(tela, "Pesquisa de PRODUTO", f"PRODUTO: '{resutado_prod[0]}'")
        if not mnum_ped == '':
            print(mnum_ped)
        return
    else:
        QMessageBox.information(tela, "Pesquisa de PRODUTO", "PRODUTO nao encontrado...!!!")
        return


# def venda():
#     tela.mcodigo.textChanged.connect(pesquisa_produto)
#     return

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # locale.setlocale(locale.LC_NUMERIC, '')
        # Executar a consulta
        conexao_banco()
        executar_consulta()


if __name__ == '__main__':
    # from hti_funcoes import conexao_banco
    # conexao_banco()
    mnum_ped = '145082'
    MainWindow()
    # tela.show()
    # app.exec()
    hti_global.conexao_bd.close()
