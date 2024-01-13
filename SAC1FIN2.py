# ALTERACAO DE FINANCIAMENTO

from PyQt6 import uic
from PyQt6 import QtWidgets
from PyQt6.QtGui import QIcon, QGuiApplication
from PyQt6.QtWidgets import QButtonGroup, QMessageBox
import os
import hti_global as hg
from SAC1FIN import listar_financiamento

app = QtWidgets.QApplication([])
app.setStyleSheet(hg.style_sheet)
tela = uic.loadUi(f"{hg.c_ui}\\htifinanciamento.ui")
tela.setWindowTitle('ALTERACAO de FINANCIAMENTO')
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
lbl_titulo_cartao.setText("ALTERACAO DE FINANCIAMENTO")

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

    # print(m_tipo_fin)
    # hg.conexao_cursor.execute(f"SELECT * FROM sacfin WHERE cod_fin = {m_cod_fin} AND tipo_fin = {m_tipo_fin} ")
    # arq_ver_cart = hg.conexao_cursor.fetchone()
    # hg.conexao_bd.rollback()
    #
    # if arq_ver_cart is not None:
    #     QMessageBox.information(tela, "alteracao de financiamento", "financiamento ja CADASTRADO !")
    #     return

    m_desc_fin = tela.mdesc_fin.text().upper()
    m_taxa_fin = tela.doubleSpinBox_3.value()
    m_taxa_adm = tela.doubleSpinBox_2.value()
    m_aliq_fin = tela.doubleSpinBox.value()

    if tela.rb_cobra_fin_sim.isChecked():
        m_cobra_fin = 'S'
    elif tela.rb_cobra_fin_nao.isChecked():
        m_cobra_fin = 'N'

    sql = "UPDATE sacfin SET desc_fin = ?, cobra_fin = ?, taxa_fin = ?, taxa_adm = ? WHERE cod_fin = ?"

    hg.conexao_cursor.execute(sql, (m_desc_fin, m_cobra_fin, m_taxa_fin, m_taxa_adm, m_cod_fin))
    hg.conexao_bd.commit()
    QMessageBox.information(tela, "alteracao de financiamento", "Cadastro feito com SUCESSO!")
    return
    # alteracao_financiamento()


def alteracao_financiamento(codigo_finan):
    # PEGAR O ULTIMO NUMERO DOS financiamento E ACRESCENTA 1
    hg.conexao_cursor.execute(f"SELECT * FROM sacfin WHERE cod_fin = {codigo_finan}")
    arq_finan = hg.conexao_cursor.fetchone()

    tela.mcod_fin.setText((str(arq_finan[0]).zfill(3)))
    tela.mdesc_fin.setText(arq_finan[1])
    tela.doubleSpinBox_3.setValue(float(arq_finan[3]))
    tela.doubleSpinBox_2.setValue(float(arq_finan[4]))
    tela.doubleSpinBox.setValue(0)

    tela.mtipo_fin.setText(' ')

    # RADIO BUTTON

    rb_cobra_fin_group = QButtonGroup()
    rb_cobra_fin_group.addButton(tela.rb_cobra_fin_sim, id=1)
    rb_cobra_fin_group.addButton(tela.rb_cobra_fin_nao, id=2)
    tela.rb_cobra_fin_nao.setChecked(True)
    if arq_finan[2] == 'S':
        tela.rb_cobra_fin_sim.setChecked(True)
    else:
        tela.rb_cobra_fin_nao.setChecked(True)

    tela.mdesc_fin.setFocus()

    tela.bt_salvar.clicked.connect(salvar_financiamento)
    tela.bt_sair.clicked.connect(fecha_tela)
    tela.mcod_fin.setDisabled(True)
    tela.doubleSpinBox.setDisabled(True)
    tela.mtipo_fin.setDisabled(True)
    tela.bt_sair.setIcon(icon_sair)
    tela.bt_salvar.setIcon(icon_salvar)

    tela.show()
    app.exec()


if __name__ == '__main__':
    from hti_funcoes import conexao_banco
    conexao_banco()
    alteracao_financiamento('0001')
    hg.conexao_bd.close()
