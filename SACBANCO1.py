# INCLUSAO BANCO

import os
from PyQt6 import uic, QtWidgets
from PyQt6.QtGui import QIcon, QGuiApplication
from PyQt6.QtWidgets import QMessageBox
from hti_funcoes import ver_nivel
from hti_funcoes import conexao_banco, verificar_conexao
import hti_global as hg

titulo = "INCLUSÃO DE BANCO"
app = QtWidgets.QApplication([])
app.setStyleSheet(hg.style_sheet)
tela = uic.loadUi(f"{hg.c_ui}\\htibanco.ui")
icon = QIcon(f"{hg.c_imagem}\\htiico.ico")
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

tela.setWindowTitle(titulo)
lbl_titulo_banco = tela.findChild(QtWidgets.QLabel, "tit_banco")
lbl_titulo_banco.setText(titulo)

# PEGA O NOME DO ARQUIVO EM EXECUCAO
nome_file_com = os.path.basename(__file__)
nome_file, ext = os.path.splitext(nome_file_com)

tela.statusBar.showMessage(f"<< {nome_file} >>")


def on_close_event(event):
    tela.close()
    event.accept()
    # hg.conexao_cursor.close()
    tela.closeEvent = on_close_event


def fecha_tela():
    tela.close()
    tela.closeEvent = on_close_event
    return


def salvar_banco():
    m_cod_banco = tela.mcod_banco.text()
    hg.conexao_cursor.execute(f"SELECT cod_banco FROM sacbanco WHERE cod_banco = {m_cod_banco} ")
    # # Recupere o resultado
    arq_ver_banco = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()
    if arq_ver_banco is not None:
        QMessageBox.information(tela, "alteracao de banco", "banco ja CADASTRADO !")
        return
    m_num_banco = tela.mnum_banco.text().upper().strip()
    m_nome_banco = tela.mnome_banco.text().upper().strip()
    m_agencia = tela.magencia.text().upper().strip()
    m_dv_ag = tela.mdv_ag.text().upper().strip()
    m_c_c = tela.mc_c.text().upper().strip()
    m_dv_cc = tela.mdv_cc.text().upper().strip()
    m_dig_ag_cc = tela.mdig_ag_cc.text().upper().strip()
    m_modalidade = tela.mmodalidade.text().upper().strip()
    m_n_conv = tela.mn_conv.text().upper().strip()
    m_cod_cedente = tela.mcod_cedente.text().upper().strip()
    m_carteira = tela.mcarteira.text().upper().strip()
    m_cod_trans = tela.mcod_trans.text().upper().strip()
    m_local_pg = tela.mlocal_pg.text().upper().strip()
    m_diasprot = tela.doubleSpinBox_3.value()
    m_despesa = tela.doubleSpinBox_2.value()

    sql = "INSERT INTO sacbanco (cod_banco, num_banco, nome_banco, agencia, " \
          "dv_ag, c_c, dv_cc, " \
          "dig_ag_cc, modalidade, n_conv, " \
          "cod_cedente, carteira, cod_trans, " \
          "local_pg, diasprot, despesa, Sr_deleted) " \
          "VALUES (?, ?, ?, ?, " \
          "?, ?, ?, " \
          "?, ?, ?, " \
          "?, ?, ?, " \
          "?, ?, ?, ?)"

    hg.conexao_cursor.execute(sql, (m_cod_banco, m_num_banco, m_nome_banco, m_agencia,
                                            m_dv_ag, m_c_c, m_dv_cc,
                                            m_dig_ag_cc, m_modalidade, m_n_conv,
                                            m_cod_cedente, m_carteira, m_cod_trans,
                                            m_local_pg, m_diasprot, m_despesa, ' '))

    hg.conexao_bd.commit()
    QMessageBox.information(tela, "Inclusao de banco", "Cadastro feito com SUCESSO!")

    inclusao_banco()


def inclusao_banco():
    # nivel_acess = hg.geral_nivel_usuario
    # if not ver_nivel(nome_file, 'CADASTRO DE BANCOS ', '15', nivel_acess, 'AMBIE', '  '):
    #     tela.close()
    #     tela.closeEvent = on_close_event
    #     return

    # PEGAR O ULTIMO NUMERO DOS banco E ACRESCENTA 1
    hg.conexao_cursor.execute("SELECT max(cod_banco) FROM sacbanco")
    # # Recupere o resultado
    arq_banco = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()
    if arq_banco[0] is not None:
        codigo = int(arq_banco[0]) + 1
    else:
        codigo = 1
    tela.mcod_banco.setText(str(codigo).zfill(3))
    tela.mcod_banco.setEnabled(False)
    tela.mnum_banco.setText('')
    tela.mnome_banco.setText('')
    tela.magencia.setText('')
    tela.mdv_ag.setText('')
    tela.mc_c.setText('')
    tela.mdv_cc.setText('')
    tela.mdig_ag_cc.setText('')
    tela.mmodalidade.setText('')
    tela.mn_conv.setText('')
    tela.mcod_cedente.setText('')
    tela.mcarteira.setText('')
    tela.mcod_trans.setText('')
    tela.mlocal_pg.setText('')
    tela.doubleSpinBox_3.setValue(0)
    tela.doubleSpinBox_2.setValue(0)
    tela.mnum_banco.setFocus()

    tela.bt_salvar.clicked.connect(salvar_banco)
    tela.bt_sair.clicked.connect(fecha_tela)
    tela.bt_sair.setIcon(icon_sair)
    tela.bt_salvar.setIcon(icon_salvar)
    tela.show()


if __name__ == '__main__':
    conexao_banco()
    verificar_conexao()
    inclusao_banco()
    app.exec()
    hg.conexao_bd.close()
