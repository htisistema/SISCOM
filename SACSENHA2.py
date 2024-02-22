# ALTERACAO USUARIO

from PyQt6 import uic, QtWidgets, QtCore
from PyQt6.QtGui import QIcon, QGuiApplication
from PyQt6.QtWidgets import QButtonGroup, QMessageBox
from datetime import datetime, date
import os
from hti_funcoes import dcripto, cripto
import hti_global as hg

# PEGA O NOME DO ARQUIVO EM EXECUCAO
nome_file_com = os.path.basename(__file__)
nome_file, ext = os.path.splitext(nome_file_com)

titulo = "ALTERACAO DE USUARIOS"
app = QtWidgets.QApplication([])
app.setStyleSheet(hg.style_sheet)
tela = uic.loadUi(f"{hg.c_ui}\\htiusuario.ui")
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

tela.setWindowTitle(titulo)
tela.statusBar = QtWidgets.QStatusBar()
tela.setStatusBar(tela.statusBar)

# tela.showMaximized()
lbl_titulo_usuario = tela.findChild(QtWidgets.QLabel, "tit_usuario")
lbl_titulo_usuario.setText(titulo)

tela.statusBar.showMessage(f"<< {nome_file} >>")

# hg.conexao_cursor.execute("SELECT * FROM sacsetup")
# # Recupere o resultado
# m_set = hg.conexao_cursor.fetchone()
# hg.conexao_bd.commit()

hg.conexao_cursor.execute("SELECT cidade, uf, cep FROM saccid ORDER BY cidade")
# Recupere o resultado
arq_cidade = hg.conexao_cursor.fetchall()
hg.conexao_bd.commit()

# COMBOX
tela.comboBox_2.addItems(hg.estados)
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
    tela.closeEvent = on_close_event
    return


def on_close_event(event):
    tela.close()
    event.accept()
    tela.closeEvent = on_close_event


def habilita_senha():
    m_scod_op = tela.mscod_op.text().strip()
    m_senha_atual = tela.msenha_atual.text().strip()
    hg.conexao_cursor.execute(f"SELECT ssenha FROM insopera WHERE scod_op = {m_scod_op}")
    # # Recupere o resultado
    arq_usu1 = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()
    senha = arq_usu1[0]
    senha = dcripto(senha)
    # print(senha)
    if senha == m_senha_atual:
        tela.mssenha.setDisabled(False)
        tela.conf_senha.setDisabled(False)
        tela.mssenha.setText('')
        tela.mssenha.setFocus()
    else:
        tela.msenha_atual.setDisabled(True)
        tela.mssenha.setDisabled(True)
        tela.conf_senha.setDisabled(True)
        tela.msnome.setFocus()
        QMessageBox.information(tela, "ALTERACAO de USUARIO", "Senha ATUAL nao CONFERE !")
        return


def salvar_usuario():
    m_ssenha = tela.mssenha.text().strip()
    m_conf_senha = tela.conf_senha.text().strip()
    senha = cripto(m_ssenha)
    if not m_ssenha == m_conf_senha:
        QMessageBox.information(tela, "ALTERACAO de USUARIO", "Senha nao CONFERE !")
        tab_widget = tela.findChild(QtWidgets.QTabWidget, "tabWidget")
        tab_widget.setCurrentIndex(0)
        tela.mssenha.setText('')
        tela.conf_senha.setText('')
        tela.mssenha.setFocus()
        return
        
    m_scod_op = tela.mscod_op.text().strip()
    m_doc_apagar = m_estoq_min = m_estoq_med = m_dat_aniv = m_ver_pocket = None
    m_data_cad_f = datetime.strptime(tela.msdata_cad.text(), '%d/%m/%Y').date()
    m_sdata_cad = m_data_cad_f.strftime('%Y-%m-%d')
    if m_data_cad_f == data_vazia:
        m_sdata_cad = None

    m_snome = tela.msnome.text().upper()

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

    sql = "UPDATE insopera SET sdata_cad = ?, scod_op = ?, snome = ?, stipo = ?, " \
          "stipo_sis = ?, snivel = ?, ssenha = ?, scomissao = ?, " \
          "scom_praz = ?, scom_oper = ?, scota = ?, sexpira = ?, " \
          "doc_apagar = ?, estoq_min = ?, estoq_med = ?, dat_aniv = ?, " \
          "ver_pocket = ?, email = ?, endereco = ?, numero = ?, " \
          "complemento = ?, bairro = ?, cidade = ?, uf = ?, " \
          "fone = ?, cpf = ?, rg = ?, preco_perc = ?, " \
          "desc_max = ?  " \
          "WHERE scod_op = ?"

    mnivel = m_snivel + m_snivel1
    values = (m_sdata_cad, m_scod_op, m_snome, m_stipo,
              m_stipo_sis, mnivel, senha, m_scomissao,
              m_scom_praz, m_scom_oper, m_scota, m_sexpira_,
              m_doc_apagar, m_estoq_min, m_estoq_med, m_dat_aniv,
              m_ver_pocket, m_email, m_endereco, m_numero,
              m_complemento, m_bairro, m_cidade, m_uf,
              m_fone, m_cpf, m_rg, m_preco_perc,
              m_desc_max, m_scod_op)

    hg.conexao_cursor.execute(sql, values)
    hg.conexao_bd.commit()
    QMessageBox.information(tela, "alteracao de usuario", "Cadastro feito com SUCESSO!")

    alteracao_usuario(m_scod_op)


def alterar_senha():
    tela.msenha_atual.setDisabled(False)
    tela.msenha_atual.setFocus()


def alteracao_usuario(codigo_usuario):
    # PEGAR O ULTIMO NUMERO DOS usuario E ACRESCENTA 1
    hg.conexao_cursor.execute(f"SELECT * FROM insopera WHERE scod_op = {codigo_usuario}")
    # # Recupere o resultado
    arq_usu = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()
    tab_widget = tela.findChild(QtWidgets.QTabWidget, "tabWidget")
    tab_widget.setCurrentIndex(0)
    # senha = dcripto(arq_usu[4])
    # print(senha)
    if arq_usu is None:
        QMessageBox.information(tela, "alteracao de Usuario", "Usuario nao CADASTRADO !")
        return

    if arq_usu[5] is None:
        data = QtCore.QDate(1900, 1, 1)
    else:
        data_str = arq_usu[5].strftime("%Y-%m-%d")
        data = QtCore.QDate.fromString(data_str, "yyyy-MM-dd")
        data = QtCore.QDateTime(data, QtCore.QTime(0, 0, 0))
    tela.msdata_cad.setDateTime(data)

    # if arq_usu[5] is None:
    #     data = QtCore.QDate(1900, 1, 1)
    # else:
    #     data = QtCore.QDateTime.fromString(arq_usu[5], "dd-MM-yyyy").date()
    # tela.msdata_cad.setDateTime(data)

    tela.mscod_op.setText(str(arq_usu[0]))
    tela.msnome.setText(str(arq_usu[1]).strip())
    senha1 = dcripto(str(arq_usu[4]))
    tela.mssenha.setText(senha1.strip())
    # PROCURA A UF NO COMBOBOX
    for i in range(tela.comboBox_3.count()):
        item_text = tela.comboBox_3.itemText(i)
        if str(arq_usu[2]).strip() in item_text:
            tela.comboBox_3.setCurrentIndex(i)
            break

    for i in range(tela.comboBox_4.count()):
        item_text = tela.comboBox_4.itemText(i)
        if str(arq_usu[3]).strip() in item_text:
            tela.comboBox_4.setCurrentIndex(i)
            break

    for i in range(tela.comboBox_5.count()):
        item_text = tela.comboBox_5.itemText(i)
        if str(arq_usu[12][0]).strip() in item_text:
            tela.comboBox_5.setCurrentIndex(i)
            break

    for i in range(tela.comboBox_6.count()):
        item_text = tela.comboBox_6.itemText(i)
        if str(arq_usu[12][1]).strip() in item_text:
            tela.comboBox_6.setCurrentIndex(i)
            break

    tela.doubleSpinBox.setValue(float(arq_usu[6]))
    tela.doubleSpinBox_2.setValue(float(arq_usu[7]))
    tela.doubleSpinBox_3.setValue(float(arq_usu[8]))
    tela.doubleSpinBox_4.setValue(float(arq_usu[9]))
    tela.doubleSpinBox_5.setValue(float(arq_usu[17]))

    tela.memail.setText(str(arq_usu[33]).strip())
    tela.mendereco.setText(str(arq_usu[36]).strip())
    tela.mnumero.setText(str(arq_usu[37]).strip())
    tela.mcomplemento.setText(str(arq_usu[38]).strip())
    tela.mbairro.setText(str(arq_usu[39]).strip())
    for i in range(tela.comboBox.count()):
        item_text = tela.comboBox.itemText(i)
        if str(arq_usu[40]).strip() in item_text:
            tela.comboBox.setCurrentIndex(i)
            break
    for i in range(tela.comboBox_2.count()):
        item_text = tela.comboBox_2.itemText(i)
        if str(arq_usu[41]).strip() in item_text:
            tela.comboBox_2.setCurrentIndex(i)
            break
    tela.mfone.setText(str(arq_usu[42]).strip())
    tela.mcpf.setText(str(arq_usu[43]).strip())
    tela.mrg.setText(str(arq_usu[44]).strip())

    # RADIO BUTTON
    rb_alerta_doc_group = QButtonGroup()
    rb_alerta_doc_group.addButton(tela.rb_alerta_doc_sim, id=1)
    rb_alerta_doc_group.addButton(tela.rb_alerta_doc_nao, id=2)
    if arq_usu[27] == 'S':
        tela.rb_alerta_doc_sim.setChecked(True)
    else:
        tela.rb_alerta_doc_nao.setChecked(True)

    rb_alerta_estmin_group = QButtonGroup()
    rb_alerta_estmin_group.addButton(tela.rb_alerta_estmin_sim, id=1)
    rb_alerta_estmin_group.addButton(tela.rb_alerta_estmin_nao, id=2)
    if arq_usu[28] == 'S':
        tela.rb_alerta_estmin_sim.setChecked(True)
    else:
        tela.rb_alerta_estmin_nao.setChecked(True)

    rb_alerta_aniv_group = QButtonGroup()
    rb_alerta_aniv_group.addButton(tela.rb_alerta_aniv_sim, id=1)
    rb_alerta_aniv_group.addButton(tela.rb_alerta_aniv_nao, id=2)
    if arq_usu[34] == 'S':
        tela.rb_alerta_aniv_sim.setChecked(True)
    else:
        tela.rb_alerta_aniv_nao.setChecked(True)

    rb_pocket_group = QButtonGroup()
    rb_pocket_group.addButton(tela.rb_pocket_sim, id=1)
    rb_pocket_group.addButton(tela.rb_pocket_nao, id=2)
    if arq_usu[35] == 'S':
        tela.rb_pocket_sim.setChecked(True)
    else:
        tela.rb_pocket_nao.setChecked(True)

    tela.mscod_op.setDisabled(True)
    tela.msenha_atual.setDisabled(True)
    tela.mssenha.setDisabled(True)
    tela.conf_senha.setDisabled(True)

    tela.msnome.setFocus()

    tela.msenha_atual.returnPressed.connect(habilita_senha)
    tela.msenha_atual.editingFinished.connect(habilita_senha)
    tela.bt_salvar.clicked.connect(salvar_usuario)
    tela.bt_sair.clicked.connect(fecha_tela)
    tela.bt_sair.setIcon(icon_sair)
    tela.bt_salvar.setIcon(icon_salvar)

    tela.bt_alterar_senha.clicked.connect(alterar_senha)

    tela.show()


if __name__ == '__main__':
    alteracao_usuario('999')
    app.exec()
    hg.conexao_bd.close()
