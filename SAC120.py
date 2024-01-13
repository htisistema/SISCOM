# INCLUSAO TRANSPORTADORA

import os
from PyQt6 import uic, QtWidgets, QtCore
from PyQt6.QtGui import QIcon, QGuiApplication
from PyQt6.QtWidgets import QButtonGroup, QMessageBox
from datetime import datetime, date
from hti_funcoes import ver_nivel
import hti_global as hg

titulo = 'Inclusao de transportadora'
app = QtWidgets.QApplication([])
app.setStyleSheet(hg.style_sheet)
tela = uic.loadUi(f"{hg.c_ui}\\htitransportadora.ui")
tela.setWindowTitle(titulo)
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

lbl_titulo_transportadora = tela.findChild(QtWidgets.QLabel, "tit_transportadora")
lbl_titulo_transportadora.setText(titulo)

# PEGA O NOME DO ARQUIVO EM EXECUCAO
nome_file_com = os.path.basename(__file__)
nome_file, ext = os.path.splitext(nome_file_com)

tela.statusBar.showMessage(f"<< {nome_file} >>")


data_vazia = date(1900, 1, 1)


def on_close_event(event):
    tela.close()
    event.accept()
    # hg.conexao_cursor.close()
    tela.closeEvent = on_close_event


def salvar_transportadora():
    m_cod_tran = tela.mcod_tran.text().strip()
    hg.conexao_cursor.execute(f"SELECT * FROM sactran WHERE cod_tran = {m_cod_tran} ")
    # # Recupere o resultado
    arq_ver_forn = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()
    if arq_ver_forn is not None:
        QMessageBox.information(tela, "alteracao de transportadora", "transportadora ja CADASTRADO !")
        return
    m_carteira = None
    m_banco = None
    if tela.rb_banco.isChecked():
        m_carteira = ' '
        m_banco = 'X'
    elif tela.rb_carteira.isChecked():
        m_carteira = 'X'
        m_banco = ' '

    index = tela.comboBox_2.currentIndex()
    mop = tela.comboBox_2.itemText(index)
    m_mcidade = mop[0:25]

    index = tela.comboBox_3.currentIndex()
    mop = tela.comboBox_3.itemText(index)
    m_muf = mop[0] + mop[1]

    index = tela.comboBox.currentIndex()
    mop = tela.comboBox.itemText(index)
    m_uf_placa = mop[0] + mop[1]

    m_razao = tela.mrazao.text().upper()

    if len(m_razao) == 0:
        QMessageBox.critical(tela, "Campo Obrigatorio", "Razao Social !")
        return

    m_data_cad_f = datetime.strptime(tela.mdata_cad.text(), '%d/%m/%Y').date()
    m_data_cad = m_data_cad_f.strftime('%Y-%m-%d')
    if m_data_cad_f == data_vazia:
        m_data_cad = None
    m_placa = tela.mplaca.text().upper()
    m_antt = tela.mantt.text().upper()
    m_apolice = tela.mapolice.text().upper()

    m_endereco = tela.mendereco.text().upper()
    m_bairro = tela.mbairro.text().upper()
    m_cep = tela.mcep.text()
    m_cep = ''.join(filter(str.isdigit, m_cep))
    m_tel1 = tela.mtel1.text()
    m_tel2 = tela.mtel2.text()
    m_fax = tela.mfax.text()
    m_cgc = tela.mcgc.text()
    m_cgc = ''.join(filter(str.isdigit, m_cgc))
    m_insc = tela.minsc.text()
    m_cpf = tela.mcpf.text()
    m_cpf = ''.join(filter(str.isdigit, m_cpf))
    m_prazo_pag = tela.mprazo_pag.text()
    m_prazo_pag = ''.join(filter(str.isdigit, m_prazo_pag))
    m_obs = tela.mobs.text().upper()
    m_ct_cobran = tela.mct_cobran.text().upper()
    m_ct_gerente = tela.mct_gerente.text().upper()
    m_ct_fatura = tela.mct_fatura.text().upper()
    m_ct_vendedo = tela.mct_vendedo.text().upper()

    sql = "INSERT INTO sactran (data_cad, cod_tran, razao, " \
          "cgc, cpf, insc, obs," \
          "placa, uf_placa, antt, apolice, " \
          "endereco, bairro, cidade, uf, " \
          "cep, tel1, tel2, fax, " \
          "carteira, banco, prazo_pag, " \
          "ct_gerente, ct_fatura, ct_cobran, ct_vendedo, " \
          "Sr_deleted) " \
          "VALUES (?, ?, ?, " \
          "?, ?, ?, ?, " \
          "?, ?, ?, ?, " \
          "?, ?, ?, ?," \
          "?, ?, ?, ?," \
          "?, ?, ?, " \
          "?, ?, ?, ?, " \
          "?) "

    hg.conexao_cursor.execute(sql, (m_data_cad, m_cod_tran, m_razao,
                                            m_cgc, m_cpf, m_insc, m_obs,
                                            m_placa, m_uf_placa, m_antt, m_apolice,
                                            m_endereco, m_bairro, m_mcidade, m_muf,
                                            m_cep, m_tel1, m_tel2, m_fax,
                                            m_carteira, m_banco, m_prazo_pag,
                                            m_ct_gerente, m_ct_fatura, m_ct_cobran, m_ct_vendedo,
                                            ' '))

    hg.conexao_bd.commit()
    QMessageBox.information(tela, "Inclusao de transportadora", "Cadastro feito com SUCESSO!")

    inclusao_transportadora()


def fecha_tela():
    tela.close()
    tela.closeEvent = on_close_event
    return


def inclusao_transportadora():
    # hg.conexao_cursor.execute("SELECT * FROM sacsetup")
    # # Recupere o resultado
    # m_set = hg.conexao_cursor.fetchone()
    # hg.conexao_bd.commit()

    hg.conexao_cursor.execute("SELECT cidade, uf, cep FROM saccid ORDER BY cidade")
    # Recupere o resultado
    arq_cidade = hg.conexao_cursor.fetchall()
    hg.conexao_bd.commit()

    # COMBOX
    tela.comboBox.addItems(hg.estados)
    tela.comboBox.setCurrentIndex(16)  # coloca o focus no index

    tela.comboBox_3.addItems(hg.estados)
    tela.comboBox_3.setCurrentIndex(16)  # coloca o focus no index

    for ret_cidade in arq_cidade:
        item = f'{ret_cidade[0]} - {ret_cidade[1]}'.strip('(),')
        tela.comboBox_2.addItem(item)

    nivel_acess = hg.geral_nivel_usuario
    if not ver_nivel(nome_file, 'INCLUSAO DE TRANSPORTADORA', '15', nivel_acess, 'AMBIE', '  '):
        tela.close()
        tela.closeEvent = on_close_event
        return

    # PEGAR O ULTIMO NUMERO DOS transportadora E ACRESCENTA 1
    hg.conexao_cursor.execute("SELECT max(cod_tran) FROM sactran")
    # # Recupere o resultado
    arq_tran = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()
    tab_widget = tela.findChild(QtWidgets.QTabWidget, "tabWidget")
    tab_widget.setCurrentIndex(0)
    # ORDENAR OS CAMPOS
    tela.mcgc.setText('')
    if arq_tran[0] is not None:
        codigo = int(arq_tran[0]) + 1
    else:
        codigo = 1

    tela.mcod_tran.setText(str(codigo).zfill(4))
    tela.mrazao.setText('')
    tela.mdata_cad.setDateTime(QtCore.QDateTime.currentDateTime())
    tela.mcgc.setText('')
    tela.minsc.setText('')
    tela.mcpf.setText('')
    tela.mobs.setText('')
    tela.mplaca.setText('')
    tela.mantt.setText('')
    tela.mapolice.setText('')
    tela.mendereco.setText('')
    tela.mbairro.setText('')
    tela.mcep.setText(str(hg.m_set[134]))
    tela.mtel1.setText('')
    tela.mtel2.setText('')
    tela.mfax.setText('')
    tela.mprazo_pag.setText('')
    tela.mct_gerente.setText('')
    tela.mct_fatura.setText('')
    tela.mct_cobran.setText('')
    tela.mct_vendedo.setText('')

    # RADIO BUTTON

    rb_app_group = QButtonGroup()
    rb_app_group.addButton(tela.rb_banco, id=1)
    rb_app_group.addButton(tela.rb_carteira, id=2)
    tela.rb_banco.setChecked(True)
    tela.mrazao.setFocus()
    tela.mcod_tran.setEnabled(False)

    tela.bt_salvar.clicked.connect(salvar_transportadora)
    tela.bt_sair.clicked.connect(fecha_tela)
    tela.bt_sair.setIcon(icon_sair)
    tela.bt_salvar.setIcon(icon_salvar)
    tela.show()
    app.exec()


if __name__ == '__main__':
    from hti_funcoes import conexao_banco
    conexao_banco()
    inclusao_transportadora()
    hg.conexao_bd.close()
