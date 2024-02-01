# INCLUSAO FORNECEDOR

import os
from PyQt6 import uic, QtWidgets, QtCore
from PyQt6.QtGui import QIcon, QGuiApplication, QPixmap
from PyQt6.QtWidgets import QButtonGroup, QMessageBox
from datetime import datetime, date
from hti_funcoes import ver_nivel, conexao_banco, verificar_conexao
import hti_global as hg


titulo = "INCLUSÃO DE FORNECEDOR"
app = QtWidgets.QApplication([])
app.setStyleSheet(hg.style_sheet)
tela = uic.loadUi(f"{hg.c_ui}\\sac140.ui")
icon = QIcon(f"{hg.c_imagem}\\htiico.jpg")
icon_cancelar = QIcon(f"{hg.c_imagem}\\cancelar.png")
icon_sair = QIcon(f"{hg.c_imagem}\\sair.png")
icon_salvar = QIcon(f"{hg.c_imagem}\\salvar.png")
icon_incluir = QIcon(f"{hg.c_imagem}\\incluir.png")
tela.setWindowIcon(icon)
print('ok')
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
lbl_titulo_fornecedor = tela.findChild(QtWidgets.QLabel, "tit_fornecedor")
lbl_titulo_fornecedor.setText(titulo)

# PEGA O NOME DO ARQUIVO EM EXECUCAO
nome_file_com = os.path.basename(__file__)
nome_file, ext = os.path.splitext(nome_file_com)

tela.statusBar.showMessage(f"<< {nome_file} >>")
if os.path.exists(f"{hg.c_imagem}\\htifirma.jpg"):
    imagem = QPixmap(f"{hg.c_imagem}\\htifirma.jpg")
else:
    imagem = QPixmap(f"{hg.c_imagem}\\htifirma1.jpg")

pixmap_redimensionado = imagem.scaled(350, 50)  # redimensiona a imagem para 100x100
tela.empresa.setPixmap(pixmap_redimensionado)


data_vazia = date(1900, 1, 1)


def sac140():
    # hg.conexao_cursor.execute("SELECT * FROM sacsetup")
    # # Recupere o resultado
    # m_set = hg.conexao_cursor.fetchone()
    # hg.conexao_bd.commit()

    hg.conexao_cursor.execute("SELECT cidade, uf, cep FROM saccid ORDER BY cidade")
    # Recupere o resultado
    arq_cidade = hg.conexao_cursor.fetchall()
    hg.conexao_bd.commit()

    hg.conexao_cursor.execute("SELECT codigo, desc1 FROM sacdesp ORDER BY codigo")
    # Recupere o resultado
    arq_desp = hg.conexao_cursor.fetchall()
    hg.conexao_bd.commit()

    # COMBOX
    tela.comboBox_3.addItems(hg.estados)
    tela.comboBox_3.setCurrentIndex(16)  # coloca o focus no index

    tela.comboBox.addItem('0000 - DEFAULT')
    for ret_desp in arq_desp:
        item = f'{ret_desp[0]} - {ret_desp[1]}'.strip('(),')
        tela.comboBox.addItem(item)
    tela.comboBox.setCurrentIndex(0)

    for ret_cidade in arq_cidade:
        item = f'{ret_cidade[0]} - {ret_cidade[1]}'.strip('(),')
        tela.comboBox_2.addItem(item)

    inclusao_fornecedor()


def on_close_event(event):
    tela.close()
    event.accept()
    # hg.conexao_cursor.close()
    tela.closeEvent = on_close_event


def fecha_tela():
    tela.close()
    tela.closeEvent = on_close_event
    return


def salvar_fornecedor():
    m_cod_forn = tela.mcod_forn.text().strip()
    hg.conexao_cursor.execute(f"SELECT * FROM sacforn WHERE cod_forn = {m_cod_forn} ")
    # # Recupere o resultado
    arq_ver_forn = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()
    if arq_ver_forn is not None:
        QMessageBox.information(tela, "alteracao de fornecedor", "Fornecedor ja CADASTRADO !")
        return

    m_pocket = None
    if tela.rb_pocket_sim.isChecked():
        m_pocket = 'S'
    elif tela.rb_pocket_nao.isChecked():
        m_pocket = 'N'

    m_forn_desp = None
    if tela.rb_tipo_forn.isChecked():
        m_forn_desp = 'F'
    elif tela.rb_tipo_desp.isChecked():
        m_forn_desp = 'D'

    index = tela.comboBox.currentIndex()
    mop = tela.comboBox.itemText(index)
    m_tipo = mop[0:4]

    index = tela.comboBox_2.currentIndex()
    mop = tela.comboBox_2.itemText(index)
    m_mcidade = mop[0:25]

    index = tela.comboBox_3.currentIndex()
    mop = tela.comboBox_3.itemText(index)
    m_muf = mop[0] + mop[1]

    m_razao = tela.mrazao.text().upper()
    if len(m_razao) == 0:
        QMessageBox.critical(tela, "Campo Obrigatorio", "Razao Social !")
        return

    m_fantasia = tela.mfantasia.text().upper()

    m_limite = tela.doubleSpinBox.value()

    m_data_cad_f = datetime.strptime(tela.mdata_cad.text(), '%d/%m/%Y').date()
    m_data_cad = m_data_cad_f.strftime('%Y-%m-%d')
    if m_data_cad_f == data_vazia:
        m_data_cad = None

    m_endereco = tela.mendereco.text().upper()
    m_bairro = tela.mbairro.text().upper()
    m_cep = tela.mcep.text()
    m_cep = ''.join(filter(str.isdigit, m_cep))
    m_email = tela.memail.text()
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
    m_obs1 = tela.mobs1.text().upper()
    m_obs2 = tela.mobs2.text().upper()
    m_obs3 = tela.mobs3.text().upper()
    m_obs4 = tela.mobs4.text().upper()
    m_obs5 = tela.mobs5.text().upper()
    m_local = tela.mlocal.text().upper()
    m_ct_cobran = tela.mct_cobran.text().upper()
    m_ct_gerente = tela.mct_gerente.text().upper()
    m_ct_fatura = tela.mct_fatura.text().upper()
    m_ct_vendedor = tela.mct_vendedor.text().upper()

    sql = "INSERT INTO sacforn (data_cad, cod_forn, razao, " \
          "fantasia, tipo, cgc, " \
          "cpf, insc, endereco, " \
          "bairro, cidade, uf, " \
          "cep, local, email, " \
          "tel1, tel2, fax, " \
          "ct_cobran, prazo_pag, limite, " \
          "ct_gerente, ct_fatura, ct_vendedo, " \
          "pocket, obs, obs1, " \
          "obs2, obs3, obs4, " \
          "obs5, Sr_deleted, forn_desp) " \
          "VALUES (?, ?, ?, " \
          "?, ?, ?, " \
          "?, ?, ?, " \
          "?, ?, ?, " \
          "?, ?, ?, " \
          "?, ?, ?, " \
          "?, ?, ?, " \
          "?, ?, ?, " \
          "?, ?, ?, " \
          "?, ?, ?, " \
          "?, ?, ?) "

    hg.conexao_cursor.execute(sql, (m_data_cad, m_cod_forn, m_razao,
                                            m_fantasia, m_tipo, m_cgc,
                                            m_cpf, m_insc, m_endereco,
                                            m_bairro, m_mcidade, m_muf,
                                            m_cep, m_local, m_email,
                                            m_tel1, m_tel2, m_fax,
                                            m_ct_cobran, m_prazo_pag, m_limite,
                                            m_ct_gerente, m_ct_fatura, m_ct_vendedor,
                                            m_pocket, m_obs, m_obs1,
                                            m_obs2, m_obs3, m_obs4,
                                            m_obs5, m_forn_desp, ' '))

    hg.conexao_bd.commit()
    QMessageBox.information(tela, "Inclusao de fornecedor", "Cadastro feito com SUCESSO!")

    inclusao_fornecedor()


def inclusao_fornecedor():
    # global mprg
    # mprg = 'SAC140'
    # nivel_acess = hg.geral_nivel_usuario
    # if not ver_nivel(nome_file, 'INCLUSAO DE FORNECEDOR/CONTA APAGAR', '15', nivel_acess, 'AMBIE', '  '):
    #     tela.close()
    #     tela.closeEvent = on_close_event
    #     return

    # PEGAR O ULTIMO NUMERO DOS fornecedor E ACRESCENTA 1
    hg.conexao_cursor.execute("SELECT max(cod_forn) FROM sacforn")
    # # Recupere o resultado
    arq_forn = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()
    tab_widget = tela.findChild(QtWidgets.QTabWidget, "tabWidget")
    tab_widget.setCurrentIndex(0)
    # ORDENAR OS CAMPOS
    tela.mcgc.setText('')
    if arq_forn[0] is not None:
        codigo = int(arq_forn[0]) + 1
    else:
        codigo = 1
    tela.mcod_forn.setText(str(codigo).zfill(4))
    tela.mrazao.setText('')
    tela.mfantasia.setText('')
    tela.mdata_cad.setDateTime(QtCore.QDateTime.currentDateTime())
    tela.memail.setText('')
    tela.minsc.setText('')
    tela.mcpf.setText('')
    tela.mtel1.setText('')
    tela.mtel2.setText('')
    tela.mfax.setText('')
    tela.mobs.setText('')
    tela.mobs1.setText('')
    tela.mobs2.setText('')
    tela.mobs3.setText('')
    tela.mobs4.setText('')
    tela.mobs5.setText('')

    tela.mendereco.setText('')
    tela.mbairro.setText('')
    tela.mcep.setText(str(hg.m_set[134]))

    tela.mprazo_pag.setText('')

    # RADIO BUTTON

    rb_app_group = QButtonGroup()
    rb_app_group.addButton(tela.rb_pocket_sim, id=1)
    rb_app_group.addButton(tela.rb_pocket_nao, id=2)
    tela.rb_pocket_sim.setChecked(True)

    rb_tipo = QButtonGroup()
    rb_tipo.addButton(tela.rb_tipo_forn, id=1)
    rb_tipo.addButton(tela.rb_tipo_desp, id=2)
    tela.rb_tipo_forn.setChecked(True)

    tela.mcod_forn.setFocus()

    tela.bt_conta_apagar.setEnabled(False)
    tela.bt_movimento_produto.setEnabled(False)

    tela.bt_salvar.clicked.connect(salvar_fornecedor)
    tela.bt_sair.clicked.connect(fecha_tela)
    tela.bt_sair.setIcon(icon_sair)
    tela.bt_salvar.setIcon(icon_salvar)
    tela.show()


if __name__ == '__main__':
    conexao_banco()
    verificar_conexao()
    sac140()
    app.exec()
    hg.conexao_bd.close()
