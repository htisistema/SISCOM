# INCLUSAO DE FINANCIAMENTO

from PyQt6 import uic
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtGui import QIcon, QGuiApplication
from PyQt6.QtWidgets import QButtonGroup, QMessageBox
import os
import hti_global as hg
from SAC1FIN import listar_financiamento

app = QtWidgets.QApplication([])
app.setStyleSheet(hg.style_sheet)
tela = uic.loadUi(f"{hg.c_ui}\\htifinanciamento.ui")
tela.setWindowTitle('INCLUSAO FINANCIAMENTO')
icon = QIcon(f"{hg.c_imagem}\\htiico.jpg")
icon_cancelar = QIcon(f"{hg.c_imagem}\\cancelar.png")
icon_sair = QIcon(f"{hg.c_imagem}\\sair.png")
icon_salvar = QIcon(f"{hg.c_imagem}\\salvar.png")
icon_incluir = QIcon(f"{hg.c_imagem}\\incluir.png")
tela.setWindowIcon(icon)
# Centraliza a janela na tela
qt_rectangle = tela.frameGeometry()
center_point = app.primaryScreen().availableGeometry().center()
qt_rectangle.moveCenter(center_point)
tela.move(qt_rectangle.topLeft())
if hg.mtp_tela == 'G':
    primary_screen = QGuiApplication.primaryScreen()
    if primary_screen is not None:
        screen_geometry = primary_screen.geometry()
        tela.setGeometry(screen_geometry)


tela.statusBar = QtWidgets.QStatusBar()
tela.setStatusBar(tela.statusBar)

lbl_titulo_cartao = tela.findChild(QtWidgets.QLabel, "titulo")
lbl_titulo_cartao.setText("INCLUSÃO DE FINANCIAMENTO")

# PEGA O NOME DO ARQUIVO EM EXECUCAO
nome_file_com = os.path.basename(__file__)
nome_file, ext = os.path.splitext(nome_file_com)

tela.statusBar.showMessage(f"<< {nome_file} >>")


def fecha_tela():
    print('ok')
    tela.close()
    tela.closeEvent = on_close_event
    listar_financiamento()


def on_close_event(event):
    print('ok1')
    tela.close()
    event.accept()
    tela.closeEvent = on_close_event
    return


def salvar_financiamento():
    m_cobra_fin = ' '
    m_cod_fin = tela.mcod_fin.text().strip()

    m_tipo_fin = tela.mtipo_fin.text()
    m_tipo_fin = ''.join(filter(str.isdigit, m_tipo_fin))

    # m_tipo_fin = tela.mtipo_fin.text()
    # m_tipo_fin = m_tipo_fin.replace("+", "")

    # print(m_tipo_fin)
    hg.conexao_cursor.execute(f"SELECT * FROM sacfin WHERE cod_fin = {m_cod_fin} AND tipo_fin = {m_tipo_fin} ")
    arq_ver_cart = hg.conexao_cursor.fetchone()
    hg.conexao_bd.rollback()

    if arq_ver_cart is not None:
        QMessageBox.information(tela, "alteracao de financiamento", "financiamento ja CADASTRADO !")
        return

    m_desc_fin = tela.mdesc_fin.text().upper()
    m_taxa_fin = tela.doubleSpinBox_3.value()
    m_taxa_adm = tela.doubleSpinBox_2.value()
    m_aliq_fin = tela.doubleSpinBox.value()

    if tela.rb_cobra_fin_sim.isChecked():
        m_cobra_fin = 'S'
    elif tela.rb_cobra_fin_nao.isChecked():
        m_cobra_fin = 'N'

    sql = "INSERT INTO sacfin (cod_fin, desc_fin, cobra_fin, taxa_fin, taxa_adm, aliq_fin, tipo_fin, " \
          "sr_deleted) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

    hg.conexao_cursor.execute(sql, (m_cod_fin, m_desc_fin, m_cobra_fin, m_taxa_fin, m_taxa_adm, m_aliq_fin,
                                            m_tipo_fin, ' '))

    hg.conexao_bd.commit()
    QMessageBox.information(tela, "Inclusao de financiamento", "Cadastro feito com SUCESSO!")

    return
    # inclusao_financiamento()


def inclusao_financiamento():
    # PEGAR O ULTIMO NUMERO DOS financiamento E ACRESCENTA 1
    hg.conexao_cursor.execute(f"SELECT max(cod_fin) FROM sacfin")
    arq_finan = hg.conexao_cursor.fetchone()
    if arq_finan[0] is not None:
        codigo = int(arq_finan[0]) + 1
    else:
        codigo = 1

    tela.mcod_fin.setText(str(codigo).zfill(3))
    tela.mdesc_fin.setText('')
    tela.mtipo_fin.setText('000')
    tela.doubleSpinBox.setValue(0)
    tela.doubleSpinBox_2.setValue(0)
    tela.doubleSpinBox_3.setValue(0)

    # RADIO BUTTON

    rb_cobra_fin_group = QButtonGroup()
    rb_cobra_fin_group.addButton(tela.rb_cobra_fin_sim, id=1)
    rb_cobra_fin_group.addButton(tela.rb_cobra_fin_nao, id=2)
    tela.rb_cobra_fin_nao.setChecked(True)

    tela.mdesc_fin.setFocus()

    tela.bt_salvar.clicked.connect(salvar_financiamento)
    tela.bt_sair.clicked.connect(fecha_tela)
    tela.mcod_fin.setDisabled(True)
    tela.bt_sair.setIcon(icon_sair)
    tela.bt_salvar.setIcon(icon_salvar)

    tela.show()


if __name__ == '__main__':
    from hti_funcoes import conexao_banco
    conexao_banco()
    inclusao_financiamento()
    app.exec()
    hg.conexao_bd.close()
