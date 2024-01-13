from PyQt6 import uic, QtWidgets, QtGui
from PyQt6.QtGui import QIcon, QGuiApplication, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow
import hti_global as hg
import os

app = QApplication([])
app.setStyleSheet(hg.style_sheet)
tela = uic.loadUi(f"{hg.c_ui}\\venda_pdv.ui")
icon = QIcon(f"{hg.c_imagem}\\htiico.jpg")
tela.setWindowIcon(icon)
tela.setWindowTitle(f'VENDA         {hg.SISTEMA}  Versao: {hg.VERSAO}')
# Centraliza a janela na tela
qt_rectangle = tela.frameGeometry()
center_point = app.primaryScreen().availableGeometry().center()
qt_rectangle.moveCenter(center_point)
tela.move(qt_rectangle.topLeft())
icon_sair = QIcon(f"{hg.c_imagem}\\sair.png")
icon_login = QIcon(f"{hg.c_imagem}\\login.png")
tela.setWindowIcon(icon)
# Centraliza a janela na tela
# AJUSTAR A TELA EM RELACAO AO MONITOR
qt_rectangle = tela.frameGeometry()
center_point = app.primaryScreen().availableGeometry().center()
qt_rectangle.moveCenter(center_point)
tela.move(qt_rectangle.topLeft())

if hg.mtp_tela == 'G':
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

logohti = QPixmap(f"{hg.c_imagem}\\logoHTI.png")
pixmap_redimensionado = logohti.scaled(180, 180)  # redimensiona a imagem para 100x100
tela.logohti.setPixmap(pixmap_redimensionado)

if os.path.exists(f"{hg.c_imagem}\\htifirma.jpg"):
    imagem = QPixmap(f"{hg.c_imagem}\\htifirma.jpg")
else:
    imagem = QPixmap(f"{hg.c_imagem}\\htifirma1.jpg")

pixmap_redimensionado = imagem.scaled(450, 350)  # redimensiona a imagem para 100x100
tela.foto_produto.setPixmap(pixmap_redimensionado)


def executar_consulta():
    try:
        hg.conexao_cursor.execute(f"SELECT pcod_merc, pmerc, pquantd, pvlr_fat, "
                                          f"sum(pquantd * pvlr_fat) as soma "
                                          f"FROM sacped_s WHERE pnum_ped = '145082' group by 1,2,3,4")
        # # Recupere o resultado
        resultados = hg.conexao_cursor.fetchall()
        hg.conexao_bd.commit()

        lbl_sub_total = tela.findChild(QtWidgets.QLabel, "sub_total")
        fonte = QtGui.QFont()
        fonte.setFamily("Courier")
        fonte.setPointSize(10)
        tela.textBrowser.setFont(fonte)

        tela.textBrowser.append(' Codigo   Descricao                  ')
        # tela.textBrowser.append('Quant.   Valor R$   Total R$')
        tela.textBrowser.append('-------------------------------------------------')
        mtotal_geral = 0
        # Exibir os resultados no QTextEdit
        for resultado in resultados:
            pcod_merc, pmerc, pquantd, pvlr_fat, soma = resultado
            mcodigo = pcod_merc
            mquantd = "{:9,.3f}".format(pquantd)
            mvalor = '{:10,.2f}'.format(pvlr_fat)
            msoma = "{:12,.2f}".format(soma)
            linha = f"  {pcod_merc}  {pmerc}"  # Formatar o campo valor como float com 2 casas decimais
            linha1 = f"  {mquantd} x {mvalor} = {msoma}"  # Formatar o campo valor como float com 2 casas decimais
            mtotal_geral += soma
            # linha = ' '.join(map(str, resultado))
            tela.textBrowser.append(linha)
            tela.textBrowser.append(linha1)
            print(f"{hg.c_produto}\\{mcodigo}.jpg")
            if os.path.exists(f"{hg.c_produto}\\{mcodigo}.jpg"):
                imagem1 = QPixmap(f"{hg.c_produto}\\{mcodigo}.jpg")
            else:
                if os.path.exists(f"{hg.c_imagem}\\htifirma.jpg"):
                    imagem1 = QPixmap(f"{hg.c_imagem}\\htifirma.jpg")
                else:
                    imagem1 = QPixmap(f"{hg.c_imagem}\\htifirma1.jpg")

            pixmap_redim = imagem1.scaled(450, 350)  # redimensiona a imagem para 100x100
            tela.foto_produto.setPixmap(pixmap_redim)

        # lbl_sub_total = tela.findChild(QtWidgets.QLabel, "sub_total")
        mtotal_g = "{:12,.2f}".format(mtotal_geral)
        linha1 = f"SUB-TOTAL: {mtotal_g}"
        lbl_sub_total.setText(linha1)
        # lcd = tela.findChild(QtWidgets.QLCDNumber, "lcdNumber")
        # valor_sem_virgula = mtotal_g.replace(',', '')
        # valor_numerico = float(valor_sem_virgula)
        # lcd.display(float(valor_numerico))

    except Exception as e:
        print(f"Erro ao executar a consulta: {e}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # locale.setlocale(locale.LC_NUMERIC, '')
        # Executar a consulta
        executar_consulta()


if __name__ == '__main__':
    from hti_funcoes import conexao_banco
    conexao_banco()
    MainWindow()
    tela.show()
    app.exec()
    hg.conexao_bd.close()
