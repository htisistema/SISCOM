from PyQt6 import uic
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QButtonGroup
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QDateTime, QDate
from datetime import datetime, date
import os
import hti_global

hti_global.conexao_cursor.execute(f"SELECT * FROM sacsetup")
# Recupere o resultado
m_set = hti_global.conexao_cursor.fetchone()
hti_global.conexao_bd.commit()

hti_global.conexao_cursor.execute(f"SELECT cidade FROM saccid ORDER BY cidade")
arq_cidade = hti_global.conexao_cursor.fetchall()
hti_global.conexao_bd.commit()

app = QtWidgets.QApplication([])
app.setStyleSheet(hti_global.style_sheet)
tela = uic.loadUi(f"{hti_global.c_ui}\\empresa.ui")
tela.setWindowTitle('CADASTRO DA EMPRESA')
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

tela.statusBar = QtWidgets.QStatusBar()
tela.setStatusBar(tela.statusBar)

# PEGA O NOME DO ARQUIVO EM EXECUCAO
nome_file_com = os.path.basename(__file__)
nome_file, ext = os.path.splitext(nome_file_com)

tela.statusBar.showMessage(f"<< {nome_file} >>")

# lbl_nome_cliente = tela.findChild(QtWidgets.QLabel, "cadastro_empresa")
# lbl_nome_cliente.setText("CADASTRO DA EMPRESA")

data_vazia = date(1900, 1, 1)

tela.comboBox.addItems(hti_global.estados)

for ret_cidade in arq_cidade:
    item = f'{ret_cidade[0]}'.strip('(),')
    tela.comboBox_2.addItem(item)


def fecha_tela():
    tela.close()
    tela.closeEvent = on_close_event
    return


def on_close_event(event):
    # Esta função será chamada quando o usuário clicar no botão de fechar a janela
    tela.close()
    event.accept()
    tela.closeEvent = on_close_event


def salvar_empresa():
    m_nome_cab = 'F'
    m_dataini_f = datetime.strptime(tela.mdataini.text(), '%d/%m/%Y').date()
    m_dataini = m_dataini_f.strftime('%Y-%m-%d')
    if m_dataini_f == data_vazia:
        m_dataini = None

    if tela.rb_nome_cab_razao.isChecked():
        m_nome_cab = 'R'
    elif tela.rb_nome_cab_fantasia.isChecked():
        m_nome_cab = 'F'

    index = tela.comboBox.currentIndex()
    mop = tela.comboBox.itemText(index)
    m_uf = mop[0]+mop[1]

    index = tela.comboBox_2.currentIndex()
    mop = tela.comboBox_2.itemText(index)
    m_cidade = mop[0:25]

    m_razao = tela.mrazao.text().upper()
    m_fantasia = tela.mfantasia.text().upper()
    m_cgc = tela.mcgc.text()
    m_cgc = ''.join(filter(str.isdigit, m_cgc))
    m_insc = tela.minsc.text().upper()
    m_insc_mun = tela.minsc_mun.text().upper()
    m_cnae = tela.mcnae.text().upper()
    m_end_firma = tela.mend_firma.text()
    m_numero = tela.mnumero.text()
    m_complemento = tela.mcomplemento.text()
    m_bairro = tela.mbairro.text().upper()
    m_cep = tela.mcep.text()
    m_cep = ''.join(filter(str.isdigit, m_cep))

    m_fone = tela.mfone.text()
    m_email = tela.memail.text()
    m_contato = tela.mcontato.text()
    m_cont_cpf = ''.join(filter(str.isdigit, m_cgc))
    m_logradouro = tela.mlogradouro.text()
    m_cont_numer = tela.mcont_numer.text()

    m_cont_compl = tela.mcont_compl.text()
    m_cont_bairr = tela.mcont_bairr.text()
    m_cont_tel = tela.mcont_tel.text()
    m_cod_acess = tela.mcod_acess.text().upper()
    m_serie = tela.mserie.text().upper()

    # ATUALIZA OS DADOS DO CLIENTE
    sql = "UPDATE sacsetup SET dataini = ?, razao = ?,  fantasia = ?, nome_cab = ?, " \
          "insc = ?, insc_mun = ?, cnae = ?, end_firma = ?, numero = ?, complemento = ?, bairro = ?, cidade = ? , " \
          "uf = ?, cep = ?, fone = ?, email = ?, "\
          "contato = ?, cont_cpf = ?, logradouro = ?, cont_numer = ?, cont_compl = ?, cont_bairr = ?, cont_tel = ?, " \
          "cod_acess = ?, serie = ?"

    values = (m_dataini, m_razao, m_fantasia, m_nome_cab,
              m_insc, m_insc_mun, m_cnae, m_end_firma, m_numero, m_complemento, m_bairro, m_cidade,
              m_uf, m_cep, m_fone, m_email,
              m_contato, m_cont_cpf, m_logradouro, m_cont_numer, m_cont_compl, m_cont_bairr, m_cont_tel,
              m_cod_acess, m_serie)

    hti_global.conexao_cursor.execute(sql, values)
    hti_global.conexao_bd.commit()
    QMessageBox.information(tela, "Cadastro da EMPRESA", "Atualizacao feito com SUCESSO!")

    cadastro_empresa()


def cadastro_empresa():
    # mdataini
    if m_set[137] is None:
        data_hora = QDateTime(QDate(1900, 1, 1))
    else:
        tela.mdataini.setDisabled(True)
        data_hora = QtCore.QDateTime(m_set[137])
    tela.mdataini.setDateTime(data_hora)

    tela.mrazao.setText(str(m_set[128]).strip())
    tela.mfantasia.setText(str(m_set[129]).strip())
    # ENVIA PARA POCKET
    rb_app_group = QButtonGroup()
    rb_app_group.addButton(tela.rb_nome_cab_razao, id=1)
    rb_app_group.addButton(tela.rb_nome_cab_fantasia, id=2)
    if m_set[130] == 'F':
        tela.rb_nome_cab_fantasia.setChecked(True)
    else:
        tela.rb_nome_cab_razao.setChecked(True)
    mcnpj = str(m_set[122])
    mcnpj = mcnpj[:14]
    tela.mcgc.setText(mcnpj)    # .strip())
    tela.minsc.setText(str(m_set[127]).strip())
    tela.minsc_mun.setText(str(m_set[155]).strip())
    tela.mcnae.setText(str(m_set[156]).strip())
    tela.mend_firma.setText(str(m_set[131]).strip())
    tela.mnumero.setText(str(m_set[160]).strip())
    tela.mbairro.setText(str(m_set[132]).strip())

    for i in range(tela.comboBox_2.count()):
        item_text = tela.comboBox_2.itemText(i)
        if str(m_set[133]).strip() in item_text:
            tela.comboBox_2.setCurrentIndex(i)
            break

    for i in range(tela.comboBox.count()):
        item_text = tela.comboBox.itemText(i)
        if str(m_set[18]).strip() in item_text:
            tela.comboBox.setCurrentIndex(i)
            break

    tela.mcep.setText(str(m_set[134]).strip())
    tela.mfone.setText(str(m_set[135]).strip())
    tela.memail.setText(str(m_set[136]).strip())
    tela.mcontato.setText(str(m_set[143]).strip())
    tela.mcont_cpf.setText(str(m_set[145]).strip())
    tela.mlogradouro.setText(str(m_set[138]).strip())
    tela.mcont_numer.setText(str(m_set[139]).strip())
    tela.mcont_compl.setText(str(m_set[140]).strip())
    tela.mcont_bairr.setText(str(m_set[141]).strip())
    tela.mcont_tel.setText(str(m_set[144]).strip())
    tela.mcod_acess.setText(str(m_set[179]).strip())
    mserie_ = str(m_set[122])
    mserie_ = mserie_[14:]
    tela.mserie.setText(mserie_)

    tela.mdataini.editingFinished.connect(lambda: tela.mrazao.setFocus())
    tela.mrazao.editingFinished.connect(lambda: tela.mfantasia.setFocus())
    tela.mfantasia.editingFinished.connect(lambda: tela.mcgc.setFocus())
    tela.mcgc.editingFinished.connect(lambda: tela.minsc.setFocus())
    tela.minsc.editingFinished.connect(lambda: tela.minsc_mun.setFocus())
    tela.minsc_mun.editingFinished.connect(lambda: tela.mcnae.setFocus())
    tela.mcnae.editingFinished.connect(lambda: tela.mend_firma.setFocus())
    tela.mend_firma.editingFinished.connect(lambda: tela.mnumero.setFocus())
    tela.mnumero.editingFinished.connect(lambda: tela.mcomplemento.setFocus())
    tela.mcomplemento.editingFinished.connect(lambda: tela.mbairro.setFocus())
    tela.mbairro.editingFinished.connect(lambda: tela.mcep.setFocus())
    tela.mcep.editingFinished.connect(lambda: tela.mfone.setFocus())
    tela.mfone.editingFinished.connect(lambda: tela.memail.setFocus())
    tela.memail.editingFinished.connect(lambda: tela.mcontato.setFocus())
    tela.mcontato.editingFinished.connect(lambda: tela.mcont_cpf.setFocus())
    tela.mcont_cpf.editingFinished.connect(lambda: tela.mlogradouro.setFocus())
    tela.mlogradouro.editingFinished.connect(lambda: tela.mcont_numer.setFocus())
    tela.mcont_numer.editingFinished.connect(lambda: tela.mcont_compl.setFocus())
    tela.mcont_compl.editingFinished.connect(lambda: tela.mcont_bairr.setFocus())
    tela.mcont_bairr.editingFinished.connect(lambda: tela.mcont_tel.setFocus())
    tela.mcont_tel.editingFinished.connect(lambda: tela.mcod_acess.setFocus())
    tela.mcod_acess.editingFinished.connect(lambda: tela.mserie.setFocus())
    # ORDENAR OS CAMPOS
    # CAMPOS DADOS PESSOAIS
    tela.setTabOrder(tela.mrazao, tela.mfantasia)
    tela.setTabOrder(tela.mfantasia, tela.mcgc)
    tela.setTabOrder(tela.mcgc, tela.minsc)
    tela.setTabOrder(tela.minsc, tela.minsc_mun)
    tela.setTabOrder(tela.minsc_mun, tela.mcnae)
    tela.setTabOrder(tela.mcnae, tela.mend_firma)
    tela.setTabOrder(tela.mend_firma, tela.mnumero)
    tela.setTabOrder(tela.mnumero, tela.mcomplemento)
    tela.setTabOrder(tela.mcomplemento, tela.mbairro)
    tela.setTabOrder(tela.mbairro, tela.comboBox_2)
    tela.setTabOrder(tela.comboBox_2, tela.comboBox)
    tela.setTabOrder(tela.comboBox, tela.mcep)
    tela.setTabOrder(tela.mcep, tela.mfone)
    tela.setTabOrder(tela.mfone, tela.memail)
    tela.setTabOrder(tela.memail, tela.mcontato)
    tela.setTabOrder(tela.mcontato, tela.mcont_cpf)
    tela.setTabOrder(tela.mcont_cpf, tela.mlogradouro)
    tela.setTabOrder(tela.mlogradouro, tela.mcont_numer)
    tela.setTabOrder(tela.mcont_numer, tela.mcont_compl)
    tela.setTabOrder(tela.mcont_compl, tela.mcont_bairr)
    tela.setTabOrder(tela.mcont_bairr, tela.mcont_tel)
    tela.setTabOrder(tela.mcont_tel, tela.mcod_acess)
    tela.setTabOrder(tela.mcod_acess, tela.mserie)
    tela.bt_salvar.clicked.connect(salvar_empresa)
    tela.bt_sair.clicked.connect(fecha_tela)
    tela.show()
    app.exec()


if __name__ == '__main__':
    # listar_dados()
    cadastro_empresa()
    hti_global.conexao_bd.close()
