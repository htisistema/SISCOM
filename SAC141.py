from PyQt6 import uic
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtGui import QIcon, QGuiApplication
from PyQt6.QtWidgets import QButtonGroup, QMessageBox
from datetime import datetime, date
import os
import hti_global as hg

titulo = "ALTERACAO DE FORNECEDOR"
app = QtWidgets.QApplication([])
app.setStyleSheet(hg.style_sheet)
tela = uic.loadUi(f"{hg.c_ui}\\htifornecedor.ui")
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

tela.setWindowTitle(titulo)
lbl_titulo_fornecedor = tela.findChild(QtWidgets.QLabel, "tit_fornecedor")
lbl_titulo_fornecedor.setText(titulo)

tela.statusBar = QtWidgets.QStatusBar()
tela.setStatusBar(tela.statusBar)
# PEGA O NOME DO ARQUIVO EM EXECUCAO
nome_file_com = os.path.basename(__file__)
nome_file, ext = os.path.splitext(nome_file_com)

tela.statusBar.showMessage(f"<< {nome_file} >>")

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

for ret_desp in arq_desp:
    item = f'{ret_desp[0]} - {ret_desp[1]}'.strip('(),')
    tela.comboBox.addItem(item)
tela.comboBox.setCurrentIndex(0)

for ret_cidade in arq_cidade:
    item = f'{ret_cidade[0]} - {ret_cidade[1]}'.strip('(),')
    tela.comboBox_2.addItem(item)

data_vazia = date(1900, 1, 1)


def on_close_event(event):
    tela.close()
    event.accept()
    # hg.conexao_cursor.close()
    tela.closeEvent = on_close_event


def salvar_fornecedor():
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

    m_cod_forn = tela.mcod_forn.text()
    m_cod_forn = m_cod_forn.zfill(4)
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

    sql = "UPDATE sacforn SET data_cad = ?, cod_forn = ?, razao = ?, fantasia = ?, tipo = ?, cgc = ?, cpf = ?, " \
          "insc = ?, endereco = ?, bairro = ?, cidade = ?, uf = ?, cep = ?, " \
          "local = ?, email = ?, tel1 = ?, tel2 = ?, fax = ?, " \
          "ct_cobran = ?, prazo_pag = ?, ct_gerente = ?, ct_fatura = ?, ct_vendedo = ?, pocket = ?, " \
          "obs = ?, obs1 = ?, obs2 = ?, obs3 = ?, obs4 = ?, obs5 = ?, limite = ?, forn_desp = ? " \
          "WHERE cod_forn = ?"

    values = (m_data_cad, m_cod_forn, m_razao, m_fantasia, m_tipo, m_cgc, m_cpf,
              m_insc, m_endereco, m_bairro, m_mcidade, m_muf, m_cep,
              m_local, m_email, m_tel1, m_tel2, m_fax,
              m_ct_cobran, m_prazo_pag, m_ct_gerente, m_ct_fatura, m_ct_vendedor, m_pocket,
              m_obs, m_obs1, m_obs2, m_obs3, m_obs4, m_obs5, m_limite, m_forn_desp, m_cod_forn)
    hg.conexao_cursor.execute(sql, values)
    hg.conexao_bd.commit()
    QMessageBox.information(tela, "alteracao de fornecedor", "Cadastro feito com SUCESSO!")

    alteracao_fornecedor(m_cod_forn)


def alteracao_fornecedor(codigo_fornecedor):
    hg.conexao_cursor.execute(f"SELECT * FROM sacforn WHERE cod_forn = {codigo_fornecedor}")
    arq_forn = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()
    tab_widget = tela.findChild(QtWidgets.QTabWidget, "tabWidget")
    tab_widget.setCurrentIndex(0)

    if arq_forn is None:
        QMessageBox.information(tela, "alteracao de fornecedor", "Fornecedor nao CADASTRADO !")
        return

    if arq_forn[3] is None:
        data = QtCore.QDate(1900, 1, 1)
    else:
        data_str = arq_forn[3].strftime("%Y-%m-%d")
        data = QtCore.QDate.fromString(data_str, "yyyy-MM-dd")
        data = QtCore.QDateTime(data, QtCore.QTime(0, 0, 0))

    tela.mdata_cad.setDateTime(data)

    tela.mcod_forn.setText(str(arq_forn[0]))
    tela.mrazao.setText(str(arq_forn[1]).strip())
    tela.mcgc.setText(str(arq_forn[15]))
    tela.mfantasia.setText(str(arq_forn[34]).strip())

    # ENVIA PARA POCKET
    rb_app_group = QButtonGroup()
    rb_app_group.addButton(tela.rb_pocket_sim, id=1)
    rb_app_group.addButton(tela.rb_pocket_nao, id=2)
    if arq_forn[33] == 'S':
        tela.rb_pocket_sim.setChecked(True)
    else:
        tela.rb_pocket_nao.setChecked(True)

    rb_tipo = QButtonGroup()
    rb_tipo.addButton(tela.rb_tipo_forn, id=1)
    rb_tipo.addButton(tela.rb_tipo_desp, id=2)
    if arq_forn[37] == 'F':
        tela.rb_tipo_forn.setChecked(True)
    else:
        tela.rb_tipo_desp.setChecked(True)

    for i in range(tela.comboBox.count()):
        item_text = tela.comboBox.itemText(i)
        if str(arq_forn[2]).strip() in item_text:
            tela.comboBox.setCurrentIndex(i)
            break

    tela.minsc.setText(str(arq_forn[16]).strip())
    tela.mcpf.setText(str(arq_forn[17]).strip())

    tela.mendereco.setText(str(arq_forn[5]).strip())
    tela.mbairro.setText(str(arq_forn[6]).strip())
    # PROCURA A CIDADE NO COMBOBOX
    for i in range(tela.comboBox_2.count()):
        item_text = tela.comboBox_2.itemText(i)
        if str(arq_forn[7]).strip() in item_text:
            tela.comboBox_2.setCurrentIndex(i)
            break

    # PROCURA A UF NO COMBOBOX
    for i in range(tela.comboBox_3.count()):
        item_text = tela.comboBox_3.itemText(i)
        # print(str(arq_forn[24]).strip())
        if str(arq_forn[8]).strip() in item_text:
            tela.comboBox_3.setCurrentIndex(i)
            break

    tela.mcep.setText(str(arq_forn[9]).strip())
    tela.mlocal.setText(str(arq_forn[32]).strip())
    tela.memail.setText(str(arq_forn[11]).strip())
    tela.mtel1.setText(str(arq_forn[12]).strip())
    tela.mtel2.setText(str(arq_forn[13]).strip())
    tela.mfax.setText(str(arq_forn[14]).strip())

    tela.mprazo_pag.setText(str(arq_forn[20]).strip())

    tela.doubleSpinBox.setValue(float(arq_forn[25]))

    tela.mct_cobran.setText(str(arq_forn[24]).strip())
    tela.mct_gerente.setText(str(arq_forn[21]).strip())
    tela.mct_fatura.setText(str(arq_forn[23]).strip())
    tela.mct_vendedor.setText(str(arq_forn[22]).strip())
    tela.mobs.setText(str(arq_forn[26]).strip())
    tela.mobs1.setText(str(arq_forn[27]).strip())
    tela.mobs2.setText(str(arq_forn[28]).strip())
    tela.mobs3.setText(str(arq_forn[29]).strip())
    tela.mobs4.setText(str(arq_forn[30]).strip())
    tela.mobs5.setText(str(arq_forn[31]).strip())

    tela.mrazao.setFocus()

    tela.mcod_forn.setDisabled(True)
    tela.bt_salvar.clicked.connect(salvar_fornecedor)
    tela.bt_sair.clicked.connect(fecha_tela)
    tela.bt_sair.setIcon(icon_sair)
    tela.bt_salvar.setIcon(icon_salvar)
    tela.show()


def fecha_tela():
    tela.close()
    tela.closeEvent = on_close_event
    return


if __name__ == '__main__':
    alteracao_fornecedor('0001')
    app.exec()
    hg.conexao_cursor.close()
    hg.conexao_bd.close()
