import sys
import ctypes
from icecream import ic
import hti_global
from PyQt6.QtPrintSupport import QPrintDialog, QPrinter
from PyQt6.QtWidgets import QMainWindow, QApplication

# Constantes para a função ShellExecuteEx
SEE_MASK_INVOKEIDLIST = 0x0000000C
SEE_MASK_FLAG_DDEWAIT = 0x00000100

# Estrutura SHELLEXECUTEINFO


class SHELLEXECUTEINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", ctypes.wintypes.DWORD),
        ("fMask", ctypes.c_ulong),
        ("hwnd", ctypes.wintypes.HWND),
        ("lpVerb", ctypes.c_wchar_p),
        ("lpFile", ctypes.c_wchar_p),
        ("lpParameters", ctypes.c_wchar_p),
        ("lpDirectory", ctypes.c_wchar_p),
        ("nShow", ctypes.c_int),
        ("hInstApp", ctypes.wintypes.HINSTANCE),
        ("lpIDList", ctypes.c_void_p),
        ("lpClass", ctypes.c_wchar_p),
        ("hkeyClass", ctypes.wintypes.HKEY),
        ("dwHotKey", ctypes.wintypes.DWORD),
        ("hIcon", ctypes.wintypes.HANDLE),
        ("hProcess", ctypes.wintypes.HANDLE),
    ]


class ImpressaoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.arquivo_pdf = f"{hti_global.c_pdf}\\{hti_global.arquivo_impressao}"
        # print(self.arquivo_pdf)
        self.mnome_impressora = ""
        printer = QPrinter()
        printer.setResolution(300)
        impressora_padrao = QPrinter()
        nome_impressora_padrao = impressora_padrao.printerName()
        print_dialog = QPrintDialog(printer, self)
        if print_dialog.exec() == QPrintDialog.DialogCode.Accepted:
            # Criar um pintor para a impressão
            self.mnome_impressora = printer.printerName()

        self.imp_pdf()

        # self.impressora.triggered.connect(imprimir_pdf)
        # self.imprimir_pdf()

    def imp_pdf(self):
        # Configurar a estrutura SHELLEXECUTEINFO
        sei = SHELLEXECUTEINFO()
        sei.cbSize = ctypes.sizeof(sei)
        sei.fMask = SEE_MASK_INVOKEIDLIST | SEE_MASK_FLAG_DDEWAIT
        sei.lpFile = self.arquivo_pdf
        sei.lpParameters = f'/t "{self.mnome_impressora}"'
        sei.lpVerb = "print"
        sei.nShow = 1  # SW_SHOWNORMAL
        # ic(self.mnome_impressora)
        # Chamar a função ShellExecuteEx
        shell32 = ctypes.windll.shell32
        shell32.ShellExecuteExW(ctypes.byref(sei))
        return

    # def imprimir_pdf(self):
    #     printer = QPrinter()
    #     printer.setResolution(300)
    #     impressora_padrao = QPrinter()
    #     nome_impressora_padrao = impressora_padrao.printerName()
    #     print_dialog = QPrintDialog(printer, self)
    #     if print_dialog.exec() == QPrintDialog.DialogCode.Accepted:
    #         # Criar um pintor para a impressão
    #         self.mnome_impressora = printer.printerName()
    #
    #     self.imp_pdf()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImpressaoApp()
    # window.setGeometry(10, 10, 800, 600)
    # window.show()
    sys.exit(app.exec())

    # ImpressaoApp()
    # lista_impressoras = win32print.EnumPrinters(2)
    # impressora1 = lista_impressoras[4]
    # nome_imp = impressora1[2]
    # arquivo_pdf = f"{hti_global.c_pdf}\\helio.pdf"
    # imprimir_pdf(arquivo_pdf, nome_imp)
