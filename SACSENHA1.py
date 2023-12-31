# INCLUSAO DE USUARIO

from PyQt6 import uic
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtGui import QIcon, QGuiApplication
from PyQt6.QtWidgets import QButtonGroup, QMessageBox
from datetime import datetime, date
from hti_funcoes import cripto
import os
import hti_global

titulo = "INCLUSÃO DE USUARIOS"
app = QtWidgets.QApplication([])
app.setStyleSheet(hti_global.style_sheet)
tela = uic.loadUi(f"{hti_global.c_ui}\\htiusuario.ui")
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

lbl_titulo_usuario = tela.findChild(QtWidgets.QLabel, "tit_usuario")
lbl_titulo_usuario.setText(titulo)

# PEGA O NOME DO ARQUIVO EM EXECUCAO
nome_file_com = os.path.basename(__file__)
nome_file, ext = os.path.splitext(nome_file_com)

tela.statusBar.showMessage(f"<< {nome_file} >>")

hti_global.conexao_cursor.execute("SELECT * FROM sacsetup")
m_set = hti_global.conexao_cursor.fetchone()
# hti_global.conexao_db.commit()

hti_global.conexao_cursor.execute("SELECT cidade, uf, cep FROM saccid ORDER BY cidade")
arq_cidade = hti_global.conexao_cursor.fetchall()
# hti_global.conexao_cursor.commit()

# COMBOX
tela.comboBox_2.addItems(hti_global.estados)
tela.comboBox_2.setCurrentIndex(16)  # coloca o focus no index

for ret_cidade in arq_cidade:
    item = f'{ret_cidade[0]} - {ret_cidade[1]}'.strip('(),')
    tela.comboBox.addItem(item)

tela.comboBox_3.addItems(["A->Administrador", "G->Gerente", "O->Operador", "V->Vendedor", "B->Bloqueado"])
tela.comboBox_3.setCurrentIndex(0)  # coloca o focus no index

tela.comboBox_4.addItems(["S->Siscom", "V->Venda", "C->Caixa", "M->Caixa e Venda"])
tela.comboBox_4.setCurrentIndex(0)  # coloca o focus no index

tela.comboBox_5.addItems([" ", "1", "2", "3", "4", "5", "6", "7", "8", '9'])
tela.comboBox_5.setCurrentIndex(0)  # coloca o focus no index

tela.comboBox_6.addItems([" ", "1", "2", "3", "4", "5", "6", "7", "8", '9'])
tela.comboBox_6.setCurrentIndex(0)  # coloca o focus no index

data_vazia = date(1900, 1, 1)


def fecha_tela():
    tela.close()
    # hti_global.conexao_cursor.close()
    tela.closeEvent = on_close_event


def on_close_event(event):
    tela.close()
    event.accept()
    # hti_global.conexao_cursor.close()
    tela.closeEvent = on_close_event


def salvar_usuario():
    m_scod_op = tela.mscod_op.text()
    hti_global.conexao_cursor.execute(f"SELECT * FROM insopera WHERE scod_op = {m_scod_op}")
    arq_ver_usu = hti_global.conexao_cursor.fetchone()
    # hti_global.conexao_db.rollback()
    if arq_ver_usu is not None:
        QMessageBox.information(tela, "INCLUSAO DE USUARIO", "Usuario ja CADASTRADO !")
        return

    m_ssenha = tela.mssenha.text().strip()
    m_conf_senha = tela.conf_senha.text().strip()
    senha = cripto(m_ssenha)

    if not m_ssenha == m_conf_senha:
        QMessageBox.information(tela, "INCLUSAO de USUARIO", "Senha nao CONFERE !")
        tab_widget = tela.findChild(QtWidgets.QTabWidget, "tabWidget")
        tab_widget.setCurrentIndex(0)
        tela.mssenha.setText('')
        tela.conf_senha.setText('')
        tela.mssenha.setFocus()
        return

    m_snome = tela.msnome.text().upper()

    if len(m_snome) == 0:
        QMessageBox.critical(tela, "Campo Obrigatorio", "Nome do Usuario !")
        tab_widget = tela.findChild(QtWidgets.QTabWidget, "tabWidget")
        tab_widget.setCurrentIndex(0)
        tela.msnome.setFocus()
        return

    m_doc_apagar = m_estoq_min = m_dat_aniv = m_ver_pocket = None

    m_sdata_cad_f = datetime.strptime(tela.msdata_cad.text(), '%d/%m/%Y').date()
    m_sdata_cad = m_sdata_cad_f.strftime('%Y-%m-%d')
    if m_sdata_cad_f == data_vazia:
        m_sdata_cad = None

    index = tela.comboBox_3.currentIndex()
    mop = tela.comboBox_3.itemText(index)
    m_stipo = mop[0]

    index = tela.comboBox_4.currentIndex()
    mop = tela.comboBox_4.itemText(index)
    m_stipo_sis = mop[0]

    index = tela.comboBox_5.currentIndex()
    mop = tela.comboBox_5.itemText(index)
    m_snivel = mop[0]

    index = tela.comboBox_6.currentIndex()
    mop = tela.comboBox_6.itemText(index)
    m_snivel1 = mop[0]

    m_ssenha = tela.mssenha.text().upper()

    m_scomissao = tela.doubleSpinBox.value()

    m_scom_praz = tela.doubleSpinBox_2.value()

    m_scom_oper = tela.doubleSpinBox_3.value()

    m_scota = tela.doubleSpinBox_4.value()

    m_sexpira_ = int(tela.doubleSpinBox_5.value())

    m_estoq_med = int(tela.doubleSpinBox_5.value())

    if tela.rb_alerta_doc_sim.isChecked():
        m_doc_apagar = 'S'
    elif tela.rb_alerta_doc_nao.isChecked():
        m_doc_apagar = 'N'

    if tela.rb_alerta_estmin_sim.isChecked():
        m_estoq_min = 'S'
    elif tela.rb_alerta_estmin_nao.isChecked():
        m_estoq_min = 'N'

    if tela.rb_alerta_aniv_sim.isChecked():
        m_dat_aniv = 'S'
    elif tela.rb_alerta_aniv_nao.isChecked():
        m_dat_aniv = 'N'

    if tela.rb_pocket_sim.isChecked():
        m_ver_pocket = 'S'
    elif tela.rb_pocket_nao.isChecked():
        m_ver_pocket = 'N'

    m_email = tela.memail.text()
    m_endereco = tela.mendereco.text().upper()
    m_numero = tela.mnumero.text().upper()
    m_complemento = tela.mcomplemento.text().upper()
    m_bairro = tela.mbairro.text().upper()

    index = tela.comboBox.currentIndex()
    mop = tela.comboBox.itemText(index)
    m_cidade = mop[0:25]

    index = tela.comboBox_2.currentIndex()
    mop = tela.comboBox_2.itemText(index)
    m_uf = mop[0] + mop[1]
    m_fone = tela.mfone.text()
    m_cpf = tela.mcpf.text()
    m_cpf = ''.join(filter(str.isdigit, m_cpf))
    m_rg = tela.mrg.text()

    m_preco_perc = tela.doubleSpinBox_6.value()

    m_desc_max = tela.doubleSpinBox_7.value()

    sql = "INSERT INTO insopera (sdata_cad, scod_op, snome, stipo, " \
          "stipo_sis, snivel, ssenha, scomissao, " \
          "scom_praz, scom_oper, scota, sexpira, " \
          "doc_apagar, estoq_min, estoq_med, dat_aniv, " \
          "ver_pocket, email, endereco, numero, " \
          "complemento, bairro, cidade, uf, " \
          "fone, cpf, rg, preco_perc, " \
          "desc_max, sr_deleted) " \
          "VALUES (?, ?, ?, ?, " \
          "?, ?, ?, ?, " \
          "?, ?, ?, ?, " \
          "?, ?, ?, ?, " \
          "?, ?, ?, ?, " \
          "?, ?, ?, ?, " \
          "?, ?, ?, ?, " \
          "?, ?) "

    mnivel = m_snivel + m_snivel1
    hti_global.conexao_cursor.execute(sql, (m_sdata_cad, m_scod_op, m_snome, m_stipo,
                                            m_stipo_sis, mnivel, senha, m_scomissao,
                                            m_scom_praz, m_scom_oper, m_scota, m_sexpira_,
                                            m_doc_apagar, m_estoq_min, m_estoq_med, m_dat_aniv,
                                            m_ver_pocket, m_email, m_endereco, m_numero,
                                            m_complemento, m_bairro, m_cidade, m_uf,
                                            m_fone, m_cpf, m_rg, m_preco_perc,
                                            m_desc_max, ' '))

    hti_global.conexao_bd.commit()
    QMessageBox.information(tela, "Inclusao de usuario", "Cadastro feito com SUCESSO!")

    inclusao_usuario()


def inclusao_usuario():
    # PEGAR O ULTIMO NUMERO DOS usuario E ACRESCENTA 1
    hti_global.conexao_cursor.execute(f"SELECT max(scod_op) FROM insopera WHERE NOT scod_op = '999'")
    arq_usu = hti_global.conexao_cursor.fetchone()
    tab_widget = tela.findChild(QtWidgets.QTabWidget, "tabWidget")
    tab_widget.setCurrentIndex(0)

    tela.msdata_cad.setDateTime(QtCore.QDateTime.currentDateTime())
    if arq_usu[0] is not None:
        codigo = int(arq_usu[0]) + 1
    else:
        codigo = 1
    tela.mscod_op.setText(str(codigo).zfill(3))

    tela.msnome.setText('')
    tela.mssenha.setText('')

    # RADIO BUTTON

    rb_alerta_doc_group = QButtonGroup()
    rb_alerta_doc_group.addButton(tela.rb_alerta_doc_sim, id=1)
    rb_alerta_doc_group.addButton(tela.rb_alerta_doc_nao, id=2)
    tela.rb_alerta_doc_nao.setChecked(True)

    rb_alerta_estmin_group = QButtonGroup()
    rb_alerta_estmin_group.addButton(tela.rb_alerta_estmin_sim, id=1)
    rb_alerta_estmin_group.addButton(tela.rb_alerta_estmin_nao, id=2)
    tela.rb_alerta_estmin_nao.setChecked(True)

    rb_alerta_aniv_group = QButtonGroup()
    rb_alerta_aniv_group.addButton(tela.rb_alerta_aniv_sim, id=1)
    rb_alerta_aniv_group.addButton(tela.rb_alerta_aniv_nao, id=2)
    tela.rb_alerta_aniv_nao.setChecked(True)

    rb_pocket_group = QButtonGroup()
    rb_pocket_group.addButton(tela.rb_pocket_sim, id=1)
    rb_pocket_group.addButton(tela.rb_pocket_nao, id=2)
    tela.rb_pocket_nao.setChecked(True)

    tela.memail.setText('')
    tela.mendereco.setText('')
    tela.mnumero.setText('')
    tela.mcomplemento.setText('')
    tela.mbairro.setText('')
    tela.mfone.setText('')
    tela.mcpf.setText('')
    tela.mrg.setText('')

    tela.mscod_op.setFocus()

    tela.bt_salvar.clicked.connect(salvar_usuario)
    tela.bt_sair.clicked.connect(fecha_tela)
    tela.bt_sair.setIcon(icon_sair)
    tela.bt_salvar.setIcon(icon_salvar)
    tela.msenha_atual.setDisabled(True)

    tela.show()
    app.exec()


if __name__ == '__main__':
    inclusao_usuario()
    hti_global.conexao_bd.close()
