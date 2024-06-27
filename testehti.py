import os
import sys
import fitz  # PyMuPDF
from PyQt6 import uic
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QLabel,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsPixmapItem,
    QScrollArea,
    QPushButton,
    QHBoxLayout,
)
from PyQt6.QtGui import QPixmap, QImage, QPainter
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtGui import QIcon, QGuiApplication
from PyQt6.QtCore import Qt
import hti_global as hg

app = QApplication([])
app.setStyleSheet(hg.style_sheet)
tela = uic.loadUi(f"{hg.c_ui}\\preview_print.ui")
icon = QIcon(f"{hg.c_imagem}\\htiico.ico")
tela.setWindowIcon(icon)
tela.setWindowTitle(
    f"MENU DE PREVIEW / IMPRIMIR         {hg.SISTEMA}  Versao: {hg.VERSAO}"
)
# Centraliza a janela na tela
qt_rectangle = tela.frameGeometry()
center_point = app.primaryScreen().availableGeometry().center()
qt_rectangle.moveCenter(center_point)
tela.move(qt_rectangle.topLeft())
icon_salvar = QIcon(f"{hg.c_imagem}\\confirma.png")
icon_sair = QIcon(f"{hg.c_imagem}\\sair.png")
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

if os.path.exists(f"{hg.c_imagem}\\htifirma.jpg"):
    imagem = QPixmap(f"{hg.c_imagem}\\htifirma.jpg")
else:
    imagem = QPixmap(f"{hg.c_imagem}\\htifirma1.jpg")

mcaminho_pdf = " "

scene = QGraphicsScene()
tela.graphicsView.setScene(scene)


def load_pdf(file_name, zoom_factor=1.0):
    pdf_file = fitz.open(file_name)
    return pdf_file, zoom_factor


def display_pages(pdf_file, zoom_factor):
    scene.clear()
    for page_num in range(len(pdf_file)):
        page = pdf_file.load_page(page_num)
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom_factor, zoom_factor))
        image = QImage(
            pix.samples, pix.width, pix.height, pix.stride, QImage.Format.Format_RGB888
        )
        pixmap = QPixmap.fromImage(image)

        item = QGraphicsPixmapItem(pixmap)
        item.setPos(0, page_num * pix.height)
        scene.addItem(item)

    tela.graphicsView.setSceneRect(0, 0, pix.width, pix.height* len(pdf_file))


def zoom_in(pdf_file, zoom_factor):
    zoom_factor += 0.1
    display_pages(pdf_file, zoom_factor)
    return zoom_factor


def zoom_out(pdf_file, zoom_factor):
    zoom_factor -= 0.1
    display_pages(pdf_file, zoom_factor)
    return zoom_factor


def print_pdf(pdf_file, zoom_factor):
    printer = QPrinter()
    print_dialog = QPrintDialog(printer)

    if print_dialog.exec() == QPrintDialog.Accepted:
        for page_num in range(len(pdf_file)):
            page = pdf_file.load_page(page_num)
            pix = page.get_pixmap(matrix=fitz.Matrix(zoom_factor, zoom_factor))
            image = QImage(
                pix.samples,
                pix.width,
                pix.height,
                pix.stride,
                QImage.Format.Format_RGB888,
            )

            printer.newPage()
            painter = QPainter(printer)
            rect = painter.viewport()
            size = image.size()
            size.scale(rect.size(), Qt.AspectRatioMode.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(image.rect())
            painter.drawImage(0, 0, image)
            painter.end()


def main(file_name):
    global mcaminho_pdf
    mcaminho_pdf = file_name

    pdf_file, zoom_factor = load_pdf(file_name)
    display_pages(pdf_file, zoom_factor)

    tela.bt_zoom_in.setIcon(icon_sair)
    tela.bt_zoom_in.setFocus()

    # Utilize uma função intermediária para manter o valor do zoom_factor
    def zoom_in_handler():
        nonlocal zoom_factor
        zoom_factor = zoom_in(pdf_file, zoom_factor)

    def zoom_out_handler():
        nonlocal zoom_factor
        zoom_factor = zoom_out(pdf_file, zoom_factor)

    tela.bt_zoom_in.clicked.connect(zoom_in_handler)
    tela.bt_zoom_out.clicked.connect(zoom_out_handler)
    tela.bt_imprimir.clicked.connect(lambda: print_pdf(pdf_file, zoom_factor))
    tela.show()


if __name__ == "__main__":
    cam_pdf = "C:\\HTI\\PYTHON\\SISCOM\\pdf\\REL_RESERVA.PDF"
    print(cam_pdf)
    main(cam_pdf)
    app.exec()
    hg.conexao_bd.close()
    tela.close()
