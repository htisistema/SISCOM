# ALTERACAO BANCO

import os
from PyQt6 import uic, QtWidgets
from PyQt6.QtGui import QIcon, QGuiApplication
from PyQt6.QtWidgets import QMessageBox
from hti_funcoes import ver_nivel
from hti_funcoes import conexao_banco, verificar_conexao
import hti_global

titulo = "ALTERACAO DE BANCO"
app = QtWidgets.QApplication([])
app.setStyleSheet(hti_global.style_sheet)
tela = uic.loadUi(f"{hti_global.c_ui}\\htibanco.ui")
icon = QIcon(f"{hti_global.c_imagem}\\htiico.jpg")
icon_cancelar = QIcon(f"{hti_global.c_imagem}\\cancelar.png")
icon_sair = QIcon(f"{hti_global.c_imagem}\\sair.png")
icon_salvar = QIcon(f"{hti_global.c_imagem}\\salvar.png")
icon_incluir = QIcon(f"{hti_global.c_imagem}\\incluir.png")
tela.setWindowIcon(icon)
# Centraliza a janela na tela
qt_rectangle = tela.frameGeometry()
center_point = app.primaryScreen().availableGeometry().center()
qt_rectangle.moveCenter(center_point)
tela.move(qt_rectangle.topLeft())

if hti_global.mtp_tela == 'G':
    primary_screen = QGuiApplication.primaryScreen()
    if primary_screen is not None:
        screen_geometry = primary_screen.geometry()
        tela.setGeometry(screen_geometry)


tela.setWindowTitle(titulo)

tela.statusBar = QtWidgets.QStatusBar()
tela.setStatusBar(tela.statusBar)
lbl_titulo_banco = tela.findChild(QtWidgets.QLabel, "tit_banco")
lbl_titulo_banco.setText(titulo)

# PEGA O NOME DO ARQUIVO EM EXECUCAO
nome_file_com = os.path.basename(__file__)
nome_file, ext = os.path.splitext(nome_file_com)

tela.statusBar.showMessage(f"<< {nome_file} >>")


def on_close_event(event):
    tela.close()
    event.accept()
    # hti_global.conexao_cursor.close()
    tela.closeEvent = on_close_event


def fecha_tela():
    tela.close()
    tela.closeEvent = on_close_event
    return


def salvar_banco():
    m_cod_banco = tela.mcod_banco.text()
    hti_global.conexao_cursor.execute(f"SELECT cod_banco FROM sacbanco WHERE cod_banco = {m_cod_banco} ")
    # # Recupere o resultado
    arq_ver_banco = hti_global.conexao_cursor.fetchone()
    hti_global.conexao_bd.commit()
    if arq_ver_banco is None:
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

    sql = "UPDATE sacbanco SET num_banco = ?, nome_banco = ?, agencia = ?, " \
          "dv_ag = ?, c_c = ?, dv_cc = ?, " \
          "dig_ag_cc = ?, modalidade = ?, n_conv = ?, " \
          "cod_cedente = ?, carteira = ?, cod_trans = ?, " \
          "local_pg = ?, diasprot = ?, despesa = ? WHERE cod_banco = ? "

    values = (m_num_banco, m_nome_banco, m_agencia,
              m_dv_ag, m_c_c, m_dv_cc,
              m_dig_ag_cc, m_modalidade, m_n_conv,
              m_cod_cedente, m_carteira, m_cod_trans,
              m_local_pg, m_diasprot, m_despesa, m_cod_banco)

    hti_global.conexao_cursor.execute(sql, values)
    hti_global.conexao_bd.commit()
    QMessageBox.information(tela, "alteracao de banco", "ALTERACAO feito com SUCESSO!")

    alteracao_banco(m_cod_banco)


def alteracao_banco(mcodigo):
    # nivel_acess = hti_global.geral_nivel_usuario
    # if not ver_nivel(nome_file, 'CADASTRO DE BANCOS ', '15', nivel_acess, 'AMBIE', '  '):
    #     tela.close()
    #     tela.closeEvent = on_close_event
    #     return

    # PEGAR O ULTIMO NUMERO DOS banco E ACRESCENTA 1
    hti_global.conexao_cursor.execute(f"SELECT * FROM sacbanco WHERE cod_banco = {mcodigo}")
    # # Recupere o resultado
    arq_banco = hti_global.conexao_cursor.fetchone()
    hti_global.conexao_bd.commit()
    if arq_banco is None:
        QMessageBox.information(tela, "alteracao de BANCO", "Banco nao CADASTRADO !")
        return

    tela.mcod_banco.setText(str(mcodigo))
    tela.mcod_banco.setEnabled(False)
    tela.mnum_banco.setText(arq_banco[2])
    tela.mnome_banco.setText(arq_banco[1])
    tela.magencia.setText(arq_banco[3])
    tela.mdv_ag.setText(arq_banco[9])
    tela.mc_c.setText(arq_banco[4])
    tela.mdv_cc.setText(arq_banco[8])
    tela.mdig_ag_cc.setText(arq_banco[18])
    tela.mmodalidade.setText(arq_banco[19])
    tela.mn_conv.setText(arq_banco[17])
    tela.mcod_cedente.setText(arq_banco[10])
    tela.mcarteira.setText(arq_banco[16])
    tela.mcod_trans.setText(arq_banco[6])
    tela.mlocal_pg.setText(arq_banco[12])
    tela.doubleSpinBox_3.setValue(float(arq_banco[11]))
    tela.doubleSpinBox_2.setValue(float(arq_banco[13]))
    tela.mnum_banco.setFocus()

    tela.bt_salvar.clicked.connect(salvar_banco)
    tela.bt_sair.clicked.connect(fecha_tela)
    tela.bt_sair.setIcon(icon_sair)
    tela.bt_salvar.setIcon(icon_salvar)
    tela.show()
    app.exec()


if __name__ == '__main__':
    conexao_banco()
    verificar_conexao()
    alteracao_banco('002')
    hti_global.conexao_bd.close()
