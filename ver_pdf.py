import sys
import fitz  # PyMuPDF
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QScrollArea, QPushButton,
                             QHBoxLayout)
from PyQt6.QtGui import QPixmap, QImage, QPainter
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6 import Qt

class PDFViewer(QMainWindow):
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
            pix = page.get_pixmap(matrix=fitz.Matrix(self.zoom_factor, self.zoom_factor))
            image = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format.Format_RGB888)
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
                pix = page.get_pixmap(matrix=fitz.Matrix(self.zoom_factor, self.zoom_factor))
                image = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format.Format_RGB888)

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





