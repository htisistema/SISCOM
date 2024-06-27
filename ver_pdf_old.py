# import os
# import sys
# import fitz  # PyMuPDF
# from PyQt6 import uic
# from PyQt6.QtWidgets import (
#     QApplication,
#     QMainWindow,
#     QVBoxLayout,
#     QWidget,
#     QLabel,
#     QScrollArea,
#     QPushButton,
#     QHBoxLayout,
#     QStatusBar,
#     QDialog
# )
# from PyQt6.QtGui import QPixmap, QImage, QPainter
# from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
# from PyQt6.QtGui import QIcon, QGuiApplication, QPixmap
# from PyQt6.QtCore import Qt
# import hti_global as hg
#
# app = QApplication([])
# app.setStyleSheet(hg.style_sheet)
# tela = uic.loadUi(f"{hg.c_ui}\\preview_print.ui")
# icon = QIcon(f"{hg.c_imagem}\\htiico.ico")
# tela.setWindowIcon(icon)
# tela.setWindowTitle(
#     f"MENU DE PREVIEW / IMPRIMIR         {hg.SISTEMA}  Versao: {hg.VERSAO}"
# )
# # Centraliza a janela na tela
# qt_rectangle = tela.frameGeometry()
# center_point = app.primaryScreen().availableGeometry().center()
# qt_rectangle.moveCenter(center_point)
# tela.move(qt_rectangle.topLeft())
# icon_salvar = QIcon(f"{hg.c_imagem}\\confirma.png")
# icon_sair = QIcon(f"{hg.c_imagem}\\sair.png")
# # Centraliza a janela na tela
# # AJUSTAR A TELA EM RELACAO AO MONITOR
# if hg.mtp_tela == "G":
#     primary_screen = QGuiApplication.primaryScreen()
#     if primary_screen is not None:
#         screen_geometry = primary_screen.geometry()
#         tela.setGeometry(screen_geometry)
#
# # PEGA O NOME DO ARQUIVO EM EXECUCAO
# nome_file_com = os.path.basename(__file__)
# nome_file, ext = os.path.splitext(nome_file_com)
# # status_bar = QStatusBar()
# # tela.setStatusBar(status_bar)
#
# # tela.statusbar.showMessage(f"<< {nome_file} >>")
#
# if os.path.exists(f"{hg.c_imagem}\\htifirma.jpg"):
#     imagem = QPixmap(f"{hg.c_imagem}\\htifirma.jpg")
# else:
#     imagem = QPixmap(f"{hg.c_imagem}\\htifirma1.jpg")
#
# # pixmap_redimensionado = imagem.scaled(350, 50)  # redimensiona a imagem para 100x100
# # tela.empresa.setPixmap(pixmap_redimensionado)
#
# mcaminho_pdf = " "
#
#
# def load_pdf(file_name, zoom_factor=1.0):
#     pdf_file = fitz.open(file_name)
#     return pdf_file, zoom_factor
#
#
# def display_pages(pdf_file, layout, zoom_factor):
#     # Clear existing widgets
#     for i in reversed(range(layout.count())):
#         widget_to_remove = layout.itemAt(i).widget()
#         layout.removeWidget(widget_to_remove)
#         widget_to_remove.setParent(None)
#
#     for page_num in range(len(pdf_file)):
#         page = pdf_file.load_page(page_num)
#         pix = page.get_pixmap(matrix=fitz.Matrix(zoom_factor, zoom_factor))
#         image = QImage(
#             pix.samples, pix.width, pix.height, pix.stride, QImage.Format.Format_RGB888
#         )
#         pixmap = QPixmap.fromImage(image)
#
#         label = QLabel()
#         label.setPixmap(pixmap)
#         layout.addWidget(label)
#
#
# def zoom_in(pdf_file, layout, zoom_factor):
#     zoom_factor += 0.1
#     display_pages(pdf_file, layout, zoom_factor)
#     return zoom_factor
#
#
# def zoom_out(pdf_file, layout, zoom_factor):
#     zoom_factor -= 0.1
#     display_pages(pdf_file, layout, zoom_factor)
#     return zoom_factor
#
#
# def print_pdf(pdf_file, zoom_factor):
#     printer = QPrinter()
#     print_dialog = QPrintDialog(printer)
#
#     if print_dialog.exec() == QPrintDialog.Accepted:
#         for page_num in range(len(pdf_file)):
#             page = pdf_file.load_page(page_num)
#             pix = page.get_pixmap(matrix=fitz.Matrix(zoom_factor, zoom_factor))
#             image = QImage(
#                 pix.samples,
#                 pix.width,
#                 pix.height,
#                 pix.stride,
#                 QImage.Format.Format_RGB888,
#             )
#
#             printer.newPage()
#             painter = QPainter(printer)
#             rect = painter.viewport()
#             size = image.size()
#             size.scale(rect.size(), Qt.AspectRatioMode.KeepAspectRatio)
#             painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
#             painter.setWindow(image.rect())
#             painter.drawImage(0, 0, image)
#             painter.end()
#
#
# def create_pdf_viewer():
#     print(mcaminho_pdf)
#     main_window = QMainWindow()
#     central_widget = QWidget()
#     main_window.setCentralWidget(central_widget)
#
#     main_layout = QVBoxLayout()
#     central_widget.setLayout(main_layout)
#
#     scroll_area = QScrollArea()
#     main_layout.addWidget(scroll_area)
#
#     container = QWidget()
#     scroll_area.setWidget(container)
#     scroll_area.setWidgetResizable(True)
#
#     v_layout = QVBoxLayout(container)
#     container.setLayout(v_layout)
#
#     pdf_file, zoom_factor = load_pdf(mcaminho_pdf)
#     display_pages(pdf_file, v_layout, zoom_factor)
#
#     main_window.resize(1200, 800)  # Tamanho inicial da janela
#
#     # Adicionar botões de controle
#     button_layout = QHBoxLayout()
#
#     zoom_in_button = QPushButton("Zoom In")
#     zoom_in_button.clicked.connect(
#         lambda: globals().update(zoom_factor=zoom_in(pdf_file, v_layout, zoom_factor))
#     )
#     button_layout.addWidget(zoom_in_button)
#
#     zoom_out_button = QPushButton("Zoom Out")
#     zoom_out_button.clicked.connect(
#         lambda: globals().update(zoom_factor=zoom_out(pdf_file, v_layout, zoom_factor))
#     )
#     button_layout.addWidget(zoom_out_button)
#
#     print_button = QPushButton("Print")
#     print_button.clicked.connect(lambda: print_pdf(pdf_file, zoom_factor))
#     button_layout.addWidget(print_button)
#
#     main_layout.addLayout(button_layout)
#
#     return main_window
#
#
# def main(file_name):
#     global mcaminho_pdf
#     mcaminho_pdf = file_name
#     tela.bt_preview.setIcon(icon_sair)
#     tela.bt_imprimir.setFocus()
#
#     tela.bt_preview.clicked.connect(create_pdf_viewer)
#     tela.bt_imprimir.clicked.connect(create_pdf_viewer)
#     tela.show()
#
#
# if __name__ == "__main__":
#     # cam_pdf = f"{hg.c_pdf}\\{mnumero_pedido}.pdf"
#     cam_pdf = "C:\\HTI\\PYTHON\\SISCOM\\pdf\\REL_RESERVA.PDF"
#     print(cam_pdf)
#     main(cam_pdf)
#     app.exec()
#     hg.conexao_bd.close()
#     tela.close()

# app = (
#     QApplication.instance()
# )  # Use QApplication.instance() para evitar múltiplas instâncias
# if app is None:
#     app = QApplication(sys.argv)
#
# main_window = create_pdf_viewer(file_name)
# main_window.show()
#
# if QApplication.instance().thread().isRunning():
#     app.exec()


# import sys
# import fitz  # PyMuPDF
# from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QScrollArea, QPushButton
# , QHBoxLayout)
# from PyQt6.QtGui import QPixmap, QImage, QPainter
# from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
# from PyQt6.QtCore import Qt
#
#
# def load_pdf(file_name, zoom_factor=1.0):
#     pdf_file = fitz.open(file_name)
#     return pdf_file, zoom_factor
#
#
# def display_pages(pdf_file, layout, zoom_factor):
#     # Clear existing widgets
#     for i in reversed(range(layout.count())):
#         widget_to_remove = layout.itemAt(i).widget()
#         layout.removeWidget(widget_to_remove)
#         widget_to_remove.setParent(None)
#
#     for page_num in range(len(pdf_file)):
#         page = pdf_file.load_page(page_num)
#         pix = page.get_pixmap(matrix=fitz.Matrix(zoom_factor, zoom_factor))
#         image = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format.Format_RGB888)
#         pixmap = QPixmap.fromImage(image)
#
#         label = QLabel()
#         label.setPixmap(pixmap)
#         layout.addWidget(label)
#
#
# def zoom_in(pdf_file, layout, zoom_factor):
#     zoom_factor += 0.1
#     display_pages(pdf_file, layout, zoom_factor)
#     return zoom_factor
#
#
# def zoom_out(pdf_file, layout, zoom_factor):
#     zoom_factor -= 0.1
#     display_pages(pdf_file, layout, zoom_factor)
#     return zoom_factor
#
#
# def print_pdf(pdf_file, zoom_factor):
#     printer = QPrinter()
#     print_dialog = QPrintDialog(printer)
#
#     if print_dialog.exec() == QPrintDialog.Accepted:
#         for page_num in range(len(pdf_file)):
#             page = pdf_file.load_page(page_num)
#             pix = page.get_pixmap(matrix=fitz.Matrix(zoom_factor, zoom_factor))
#             image = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format.Format_RGB888)
#
#             printer.newPage()
#             painter = QPainter(printer)
#             rect = painter.viewport()
#             size = image.size()
#             size.scale(rect.size(), Qt.AspectRatioMode.KeepAspectRatio)
#             painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
#             painter.setWindow(image.rect())
#             painter.drawImage(0, 0, image)
#             painter.end()
#
#
# def main(file_name):
#     app = QApplication(sys.argv)
#     main_window = QMainWindow()
#     central_widget = QWidget()
#     main_window.setCentralWidget(central_widget)
#
#     main_layout = QVBoxLayout()
#     central_widget.setLayout(main_layout)
#
#     scroll_area = QScrollArea()
#     main_layout.addWidget(scroll_area)
#
#     container = QWidget()
#     scroll_area.setWidget(container)
#     scroll_area.setWidgetResizable(True)
#
#     v_layout = QVBoxLayout(container)
#     container.setLayout(v_layout)
#
#     pdf_file, zoom_factor = load_pdf(file_name)
#     display_pages(pdf_file, v_layout, zoom_factor)
#
#     main_window.resize(1200, 800)  # Tamanho inicial da janela
#
#     # Adicionar botões de controle
#     button_layout = QHBoxLayout()
#
#     zoom_in_button = QPushButton("Zoom In")
#     zoom_in_button.clicked.connect(lambda: globals().update(zoom_factor=zoom_in(pdf_file, v_layout, zoom_factor)))
#     button_layout.addWidget(zoom_in_button)
#
#     zoom_out_button = QPushButton("Zoom Out")
#     zoom_out_button.clicked.connect(lambda: globals().update(zoom_factor=zoom_out(pdf_file, v_layout, zoom_factor)))
#     button_layout.addWidget(zoom_out_button)
#
#     print_button = QPushButton("Print")
#     print_button.clicked.connect(lambda: print_pdf(pdf_file, zoom_factor))
#     button_layout.addWidget(print_button)
#
#     main_layout.addLayout(button_layout)
#
#     main_window.show()
#     sys.exit(app.exec())
#
#
# if __name__ == "__main__":
#     if len(sys.argv) == 2:
#         file_name = sys.argv[1]
#     else:
#         file_name = "C:\\HTI\\PYTHON\\SISCOM\\pdf\\REL_RESERVA.PDF"
#
#     main(file_name)


import sys
import fitz  # PyMuPDF
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QLabel,
    QScrollArea,
    QPushButton,
    QHBoxLayout,
)
from PyQt6.QtGui import QPixmap, QImage, QPainter
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6 import Qt


class PDFViewer(QMainWindow):
    print("pdf")

    def __init__(self, file_name):
        super().__init__()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        main_layout = QVBoxLayout()
        self.central_widget.setLayout(main_layout)

        self.zoom_factor = 1.0  # Initial zoom factor

        self.scroll_area = QScrollArea()
        main_layout.addWidget(self.scroll_area)

        self.container = QWidget()
        self.scroll_area.setWidget(self.container)
        self.scroll_area.setWidgetResizable(True)

        self.v_layout = QVBoxLayout(self.container)
        self.container.setLayout(self.v_layout)

        self.load_pdf(file_name)

        self.resize(1200, 800)  # Initial window size

        # Add control buttons
        button_layout = QHBoxLayout()

        self.zoom_in_button = QPushButton("Zoom In")
        self.zoom_in_button.clicked.connect(self.zoom_in)
        button_layout.addWidget(self.zoom_in_button)

        self.zoom_out_button = QPushButton("Zoom Out")
        self.zoom_out_button.clicked.connect(self.zoom_out)
        button_layout.addWidget(self.zoom_out_button)

        self.print_button = QPushButton("Print")
        self.print_button.clicked.connect(self.print_pdf)
        button_layout.addWidget(self.print_button)

        main_layout.addLayout(button_layout)

        self.show()

    def load_pdf(self, file_name):
        self.pdf_file = fitz.open(file_name)
        self.display_pages()

    def display_pages(self):
        # Clear existing widgets
        for i in reversed(range(self.v_layout.count())):
            widget_to_remove = self.v_layout.itemAt(i).widget()
            self.v_layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

        for page_num in range(len(self.pdf_file)):
            page = self.pdf_file.load_page(page_num)
            pix = page.get_pixmap(
                matrix=fitz.Matrix(self.zoom_factor, self.zoom_factor)
            )
            image = QImage(
                pix.samples,
                pix.width,
                pix.height,
                pix.stride,
                QImage.Format.Format_RGB888,
            )
            pixmap = QPixmap.fromImage(image)

            label = QLabel()
            label.setPixmap(pixmap)
            self.v_layout.addWidget(label)

    def zoom_in(self):
        self.zoom_factor += 0.1
        self.display_pages()

    def zoom_out(self):
        self.zoom_factor -= 0.1
        self.display_pages()

    def print_pdf(self):
        printer = QPrinter()
        print_dialog = QPrintDialog(printer, self)

        if print_dialog.exec() == QPrintDialog.Accepted:
            for page_num in range(len(self.pdf_file)):
                page = self.pdf_file.load_page(page_num)
                pix = page.get_pixmap(
                    matrix=fitz.Matrix(self.zoom_factor, self.zoom_factor)
                )
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    file_name = "C:\\HTI\\PYTHON\\SISCOM\\pdf\\REL_RESERVA.PDF"  # Nome do arquivo PDF
    viewer = PDFViewer(file_name)
    sys.exit(app.exec())
