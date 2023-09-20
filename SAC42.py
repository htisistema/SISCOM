from PyQt6 import uic, QtWidgets, QtCore
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QButtonGroup, QLineEdit, QComboBox, QRadioButton
from PyQt6.QtCore import QDate, QDateTime, QTime
from datetime import datetime, date
import os
import hti_global

app = QtWidgets.QApplication([])
app.setStyleSheet(hti_global.style_sheet)
tela = uic.loadUi(f"{hti_global.c_ui}\\hticliente.ui")
icon = QIcon(f"{hti_global.c_imagem}\\htiico.jpg")
icon_cancelar = QIcon(f"{hti_global.c_imagem}\\cancelar.png")
icon_sair = QIcon(f"{hti_global.c_imagem}\\sair.png")
icon_salvar = QIcon(f"{hti_global.c_imagem}\\salvar.png")
icon_incluir = QIcon(f"{hti_global.c_imagem}\\incluir.png")

tela.setWindowTitle('CONSULTA DE CLIENTE')
tela.setWindowIcon(icon)
# Centraliza a janela na tela
qt_rectangle = tela.frameGeometry()
center_point = app.primaryScreen().availableGeometry().center()
qt_rectangle.moveCenter(center_point)
tela.move(qt_rectangle.topLeft())
lbl_nome_cliente = tela.findChild(QtWidgets.QLabel, "tit_cliente")
lbl_nome_cliente.setText("CONSULTA DE CLIENTES")

# PEGA O NOME DO ARQUIVO EM EXECUCAO
nome_file_com = os.path.basename(__file__)
nome_file, ext = os.path.splitext(nome_file_com)

tela.statusBar.showMessage(f"<< {nome_file} >>")

hti_global.conexao_cursor.execute(f"SELECT * FROM sacsetup")
# Recupere o resultado
m_set = hti_global.conexao_cursor.fetchone()
hti_global.conexao_bd.commit()

hti_global.conexao_cursor.execute(f"SELECT cidade FROM saccid ORDER BY cidade")
arq_cidade = hti_global.conexao_cursor.fetchall()
hti_global.conexao_bd.commit()

hti_global.conexao_cursor.execute(f"SELECT cod_profi, profi FROM sacprofi")
# Recupere o resultado
arq_profi = hti_global.conexao_cursor.fetchall()
hti_global.conexao_bd.commit()

hti_global.conexao_cursor.execute(f"SELECT scod_op, snome FROM insopera ORDER BY snome")
# Recupere o resultado
arq_usuario = hti_global.conexao_cursor.fetchall()
hti_global.conexao_bd.commit()

hti_global.conexao_cursor.execute(f"SELECT codigo, descri FROM sactabpg ORDER BY codigo")
# Recupere o resultado
arq_sactabpg = hti_global.conexao_cursor.fetchall()
hti_global.conexao_bd.commit()

hti_global.conexao_cursor.execute(f"SELECT codigo, regiao FROM regiao")
arq_regiao = hti_global.conexao_cursor.fetchall()
hti_global.conexao_bd.commit()

tela.comboBox_2.addItems(hti_global.estados)

data_vazia = date(1900, 1, 1)

for ret_cidade in arq_cidade:
    item = f'{ret_cidade[0]}'.strip('(),')
    tela.comboBox_3.addItem(item)
    tela.comboBox_7.addItem(item)
    tela.comboBox_8.addItem(item)

tela.comboBox.addItems(["C->Cliente", "R->Revenda", "P->Potencial", "F->Filial", "U->Funcionarios", "A->Associado",
                        "O->Outros", "E->Excluido", "S->Supermercado"])

for ret_profi in arq_profi:
    item = f'{ret_profi[0]} - {ret_profi[1]}'.strip('(),')
    tela.comboBox_5.addItem(item)

for ret_usuario in arq_usuario:
    item = f'{ret_usuario[0]} - {ret_usuario[1]}'.strip('(),')
    tela.comboBox_13.addItem(item)
    tela.comboBox_14.addItem(item)
    tela.comboBox_15.addItem(item)


def on_close_event(event):
    # Esta função será chamada quando o usuário clicar no botão de fechar a janela
    tela.close()
    event.accept()
    tela.closeEvent = on_close_event


def consulta_cliente(codigo_cliente):
    hti_global.conexao_cursor.execute(f"SELECT * FROM saccli WHERE cod_cli = {codigo_cliente} ")
    arq_cli = hti_global.conexao_cursor.fetchone()
    hti_global.conexao_bd.commit()
    tab_widget = tela.findChild(QtWidgets.QTabWidget, "tabWidget")
    tab_widget.setCurrentIndex(0)
    tela.mcgc.setText(str(arq_cli[31]))

    if arq_cli[4] is None:
        data_hora = QDateTime(QDate(1900, 1, 1), QTime(0, 0))
    else:
        data = QDate.fromString(str(arq_cli[4]), "yyyy-MM-dd")
        data_hora = QDateTime(data, QTime(0, 0))
    tela.mdata_cad.setDateTime(data_hora)

    tela.mcod_cli.setText(str(codigo_cliente))

    # mdata_nas
    if arq_cli[8] is None:
        data_hora = QDateTime(QDate(1900, 1, 1), QTime(0, 0))
    else:
        data = QDate.fromString(str(arq_cli[8]), "yyyy-MM-dd")
        data_hora = QDateTime(data, QTime(0, 0))
    tela.mdata_nas.setDateTime(data_hora)

    tela.mrazao.setText(str(arq_cli[2]).strip())
    tela.mnome.setText(str(arq_cli[3]).strip())
    if arq_cli[7] == 'C':
        tela.comboBox.setCurrentIndex(0)
    elif arq_cli[7] == 'R':
        tela.comboBox.setCurrentIndex(1)
    elif arq_cli[7] == 'P':
        tela.comboBox.setCurrentIndex(2)
    elif arq_cli[7] == 'F':
        tela.comboBox.setCurrentIndex(3)
    elif arq_cli[7] == 'U':
        tela.comboBox.setCurrentIndex(4)
    elif arq_cli[7] == 'A':
        tela.comboBox.setCurrentIndex(5)
    elif arq_cli[7] == 'O':
        tela.comboBox.setCurrentIndex(6)
    elif arq_cli[7] == 'E':
        tela.comboBox.setCurrentIndex(7)
    elif arq_cli[7] == 'S':
        tela.comboBox.setCurrentIndex(8)
    # ENVIA PARA POCKET
    rb_app_group = QButtonGroup()
    rb_app_group.addButton(tela.RB_pocket_sim, id=1)
    rb_app_group.addButton(tela.RB_pocket_nao, id=2)
    if arq_cli[133] == 'S':
        tela.RB_pocket_sim.setChecked(True)
    else:
        tela.RB_pocket_nao.setChecked(True)

    tela.mnaturalidade.setText(str(arq_cli[115]).strip())
    tela.memail.setText(str(arq_cli[26]).strip())

    for i in range(tela.comboBox_5.count()):
        item_text = tela.comboBox_5.itemText(i)
        if str(arq_cli[134]).strip() in item_text:
            tela.comboBox_5.setCurrentIndex(i)
            break

    tela.minsc.setText(str(arq_cli[32]).strip())
    tela.mcpf.setText(str(arq_cli[33]).strip())
    tela.mrg.setText(str(arq_cli[34]).strip())
    tela.morgao.setText(str(arq_cli[35]).strip())
    if arq_cli[36] is None:
        data_hora = QDateTime(QDate(1900, 1, 1), QTime(0, 0))
    else:
        data = QDate.fromString(str(arq_cli[36]), "yyyy-MM-dd")
        data_hora = QDateTime(data, QTime(0, 0))
    tela.mdat_emi.setDateTime(data_hora)

    tela.mtel1.setText(str(arq_cli[28]).strip())
    tela.mtel2.setText(str(arq_cli[29]).strip())
    tela.mfax.setText(str(arq_cli[30]).strip())
    tela.mpai.setText(str(arq_cli[97]).strip())
    tela.mmae.setText(str(arq_cli[98]).strip())
    tela.mobs.setText(str(arq_cli[47]).strip())

    tela.mendereco.setText(str(arq_cli[20]).strip())
    tela.mnumero.setText(str(arq_cli[135]).strip())
    tela.mcomplemento.setText(str(arq_cli[136]).strip())
    tela.mbairro.setText(str(arq_cli[21]).strip())
    # PROCURA A CIDADE NO COMBOBOX
    for i in range(tela.comboBox_3.count()):
        item_text = tela.comboBox_3.itemText(i)
        if str(arq_cli[23]).strip() in item_text:
            tela.comboBox_3.setCurrentIndex(i)
            break

    # PROCURA A UF NO COMBOBOX
    for i in range(tela.comboBox_2.count()):
        item_text = tela.comboBox_2.itemText(i)
        # print(str(arq_cli[24]).strip())
        if str(arq_cli[24]).strip() in item_text:
            tela.comboBox_2.setCurrentIndex(i)
            break

    for i in range(tela.comboBox_13.count()):
        item_text = tela.comboBox_13.itemText(i)
        if str(arq_cli[105]).strip() in item_text:
            tela.comboBox_13.setCurrentIndex(i)
            break

    for i in range(tela.comboBox_14.count()):
        item_text = tela.comboBox_14.itemText(i)
        if str(arq_cli[106]).strip() in item_text:
            tela.comboBox_14.setCurrentIndex(i)
            break

    for i in range(tela.comboBox_15.count()):
        item_text = tela.comboBox_15.itemText(i)
        if str(arq_cli[147]).strip() in item_text:
            tela.comboBox_15.setCurrentIndex(i)
            break

    for i in range(tela.comboBox_16.count()):
        item_text = tela.comboBox_16.itemText(i)
        # print(str(arq_cli[24]).strip())
        if str(arq_cli[132]).strip() in item_text:
            tela.comboBox_16.setCurrentIndex(i)
            break

    tela.mcep.setText(str(arq_cli[25]).strip())

    tela.mrota.setText(str(arq_cli[27]).strip())
    tela.mrota1.setText(str(arq_cli[139]).strip())

    tela.mcomprado.setText(str(arq_cli[37]).strip())
    tela.mcontato.setText(str(arq_cli[38]).strip())
    tela.mprazo_pag.setText(str(arq_cli[39]).strip())

    if arq_cli[137] is None:
        data_hora = QDateTime(QDate(1900, 1, 1), QTime(0, 0))
    else:
        data = QDate.fromString(str(arq_cli[137]), "yyyy-MM-dd")
        data_hora = QDateTime(data, QTime(0, 0))
    tela.mdata_bloq.setDateTime(data_hora)

    tela.mnome1.setText(str(arq_cli[48]))

    if arq_cli[49] is None:
        data_hora = QDateTime(QDate(1900, 1, 1), QTime(0, 0))
    else:
        data = QDate.fromString(str(arq_cli[49]), "yyyy-MM-dd")
        data_hora = QDateTime(data, QTime(0, 0))
    tela.mdata_nas1.setDateTime(data_hora)

    tela.mnome2.setText(str(arq_cli[50]).strip())

    if arq_cli[51] is None:
        data_hora = QDateTime(QDate(1900, 1, 1), QTime(0, 0))
    else:
        data = QDate.fromString(str(arq_cli[51]), "yyyy-MM-dd")
        data_hora = QDateTime(data, QTime(0, 0))
    tela.mdata_nas2.setDateTime(data_hora)

    tela.mnome3.setText(str(arq_cli[52]).strip())

    if arq_cli[53] is None:
        data_hora = QDateTime(QDate(1900, 1, 1), QTime(0, 0))
    else:
        data = QDate.fromString(str(arq_cli[53]), "yyyy-MM-dd")
        data_hora = QDateTime(data, QTime(0, 0))
    tela.mdata_nas3.setDateTime(data_hora)

    tela.mnome4.setText(str(arq_cli[54]).strip())

    if arq_cli[55] is None:
        data_hora = QDateTime(QDate(1900, 1, 1), QTime(0, 0))
    else:
        data = QDate.fromString(str(arq_cli[55]), "yyyy-MM-dd")
        data_hora = QDateTime(data, QTime(0, 0))
    tela.mdata_nas4.setDateTime(data_hora)

    tela.mnome5.setText(str(arq_cli[56]).strip())

    if arq_cli[57] is None:
        data_hora = QDateTime(QDate(1900, 1, 1), QTime(0, 0))
    else:
        data = QDate.fromString(str(arq_cli[57]), "yyyy-MM-dd")
        data_hora = QDateTime(data, QTime(0, 0))
    tela.mdata_nas5.setDateTime(data_hora)

    tela.mempre_c.setText(str(arq_cli[65]).strip())
    tela.mcargo_c.setText(str(arq_cli[66]).strip())
    tela.mend_c.setText(str(arq_cli[68]).strip())
    tela.mbairro_c.setText(str(arq_cli[69]).strip())
    tela.mcep_c.setText(str(arq_cli[72]).strip())
    tela.mfone_c1.setText(str(arq_cli[73]).strip())
    tela.mfone_c2.setText(str(arq_cli[74]).strip())

    rb_bloqueio_group = QButtonGroup()
    rb_bloqueio_group.addButton(tela.rb_bloqueio_sim, id=1)
    rb_bloqueio_group.addButton(tela.rb_bloqueio_nao, id=2)
    if arq_cli[40] == 'S':
        tela.rb_bloqueio_sim.setChecked(True)
    else:
        tela.rb_bloqueio_nao.setChecked(True)

    rb_boleto_group = QButtonGroup()
    rb_boleto_group.addButton(tela.rb_boleto_sim, id=1)
    rb_boleto_group.addButton(tela.rb_boleto_nao, id=2)
    if arq_cli[40] == 'S':
        tela.rb_boleto_sim.setChecked(True)
    else:
        tela.rb_boleto_nao.setChecked(True)

    rb_spc_group = QButtonGroup()
    rb_spc_group.addButton(tela.rb_spc_sim, id=1)
    rb_spc_group.addButton(tela.rb_spc_nao, id=2)
    if arq_cli[41] == 'S':
        tela.rb_spc_sim.setChecked(True)
    else:
        tela.rb_spc_nao.setChecked(True)

    rb_atac_vare_group = QButtonGroup()
    rb_atac_vare_group.addButton(tela.rb_vare, id=1)
    rb_atac_vare_group.addButton(tela.rb_atac, id=2)
    if arq_cli[41] == 'V':
        tela.rb_vare.setChecked(True)
    else:
        tela.rb_atac.setChecked(True)

    tela.comboBox_4.addItems(hti_global.estados)
    tela.comboBox_4.setCurrentIndex(16)    # coloca o focus no index

    tela.comboBox_6.addItems(hti_global.estados)
    tela.comboBox_6.setCurrentIndex(16)    # coloca o focus no index

    for widget in tela.findChildren((QLineEdit, QComboBox, QRadioButton)):
        widget.setEnabled(False)

    tab_widget.setTabOrder(tela.bt_contas_receber, tela.bt_pedidos)
    tab_widget.setTabOrder(tela.bt_pedidos, tela.bt_nfe)
    tab_widget.setTabOrder(tela.bt_nfe, tela.bt_mov_produtos)
    tab_widget.setTabOrder(tela.bt_mov_produtos, tela.bt_creditos)
    tab_widget.setTabOrder(tela.bt_creditos, tela.bt_orcamentos)
    tab_widget.setTabOrder(tela.bt_orcamentos, tela.bt_gerar_autorizacao)
    tab_widget.setTabOrder(tela.bt_gerar_autorizacao, tela.bt_sair)

    tela.bt_contas_receber.setFocus()
    tela.bt_salvar.setEnabled(False)
    tela.bt_sair.clicked.connect(fecha_tela)
    tela.bt_sair.setIcon(icon_sair)
    tela.bt_salvar.setIcon(icon_salvar)
    tela.show()
    app.exec()


def fecha_tela():
    tela.close()
    tela.closeEvent = on_close_event
    return


if __name__ == '__main__':
    from hti_funcoes import conexao_banco
    conexao_banco()
    # listar_dados()
    consulta_cliente(10)
    hti_global.conexao_bd.close()

