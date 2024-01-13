# INCLUSAO DE PRODUTOS

import os
from PyQt6 import uic
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QButtonGroup, QMessageBox, QRadioButton
from PyQt6.QtGui import QGuiApplication
from datetime import datetime
from datetime import date
import hti_global as hg

titulo = "INCLUSÃO DE PRODUTOS" 
app = QtWidgets.QApplication([])
app.setStyleSheet(hg.style_sheet)
tela = uic.loadUi(f"{hg.c_ui}\\sac110.ui")
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

lbl_titulo_produto = tela.findChild(QtWidgets.QLabel, "tit_produto")
lbl_titulo_produto.setText(titulo)
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

# hg.conexao_cursor.execute(f"SELECT * FROM sacsetup")
# # Recupere o resultado
# m_set = hg.conexao_cursor.fetchone()
# hg.conexao_bd.commit()

hg.conexao_cursor.execute(f"SELECT gru_sub, merc FROM sacgrupo WHERE CHAR_LENGTH(trim(gru_sub)) = 3")
# Recupere o resultado
arq_grupo = hg.conexao_cursor.fetchall()
hg.conexao_bd.commit()

for ret_grupo in arq_grupo:
    item = f'{ret_grupo[0]} - {ret_grupo[1]}'.strip('(),')
    tela.comboBox.addItem(item)
tela.comboBox.setCurrentIndex(0)

hg.conexao_cursor.execute(f"select gru_sub, merc from sacgrupo where gru_sub like '001%'"
                                  f"and CHAR_LENGTH(trim(gru_sub)) = 5")
arq_sub_grupo = hg.conexao_cursor.fetchall()
hg.conexao_bd.commit()

for ret_sub_grupo in arq_sub_grupo:
    item = f'{ret_sub_grupo[0]} - {ret_sub_grupo[1]}'.strip('(),')
    tela.comboBox_4.addItem(item)
tela.comboBox_4.setCurrentIndex(0)

hg.conexao_cursor.execute(f"SELECT cod_forn, razao FROM sacforn WHERE forn_desp = 'F'")
# Recupere o resultado
arq_forn = hg.conexao_cursor.fetchall()
hg.conexao_bd.commit()

for ret_forn in arq_forn:
    item = f'{ret_forn[0]} - {ret_forn[1]}'.strip('(),')
    tela.comboBox_2.addItem(item)
tela.comboBox_2.setCurrentIndex(0)

hg.conexao_cursor.execute(f"SELECT scod_op, snome FROM insopera ORDER BY snome")
# Recupere o resultado
arq_usuario = hg.conexao_cursor.fetchall()
hg.conexao_bd.commit()

# COMBOX
tela.comboBox_3.addItems(["1->Produto", "2->Matria Prima", "3->Isumos", "4->Consumo", "5->Outros"])
tela.comboBox_3.setCurrentIndex(0)  # coloca o focus no index

tela.comboBox_5.addItems(["UN ->Unidade", "AR ->Arroba", "CX ->Caixa", "FD ->Fardo", "KG ->Kilo", "MT ->Metro",
                          "TON->Tonelada"])
tela.comboBox_5.setCurrentIndex(0)  # coloca o focus no index

hg.conexao_cursor.execute(f"SELECT cod_espe, descri FROM sacespe")
arq_espe = hg.conexao_cursor.fetchall()
hg.conexao_bd.commit()

for ret_espe in arq_espe:
    item = f'{ret_espe[0]} - {ret_espe[1]}'.strip('(),')
    tela.comboBox_6.addItem(item)
tela.comboBox_6.setCurrentIndex(0)

hg.conexao_cursor.execute(f"SELECT CAST(cst as char(4)), CAST(descri as char(120)), "
                                  f"iif(sittrib = 'I', 'I - Inseto', "
                                  f"iif(sittrib = 'T', 'T - Tributada', "
                                  f"iif(sittrib = 'N', 'N - Nao tributada', "
                                  f"iif(sittrib = 'F', 'F - Substituicao tributaria', 'S - Servicos')))) "
                                  f"FROM saccst")

arq_cst = hg.conexao_cursor.fetchall()
hg.conexao_bd.commit()

for ret_cst in arq_cst:
    item = f'{ret_cst[0]} - {ret_cst[1]} - {ret_cst[2]}'.strip('(),')
    tela.comboBox_7.addItem(item)
    tela.comboBox_10.addItem(item)
    tela.comboBox_11.addItem(item)
tela.comboBox_7.setCurrentIndex(0)
tela.comboBox_10.setCurrentIndex(0)
tela.comboBox_11.setCurrentIndex(0)

# , substring(descri from 1 for 50)
hg.conexao_cursor.execute(f"SELECT codigo FROM sacncm")
arq_ncm = hg.conexao_cursor.fetchall()
hg.conexao_bd.commit()

for ret_ncm in arq_ncm:
    # item = f'{ret_ncm[0]} - {ret_ncm[1]}'.strip('(),')
    item = f'{ret_ncm[0]}'.strip('(),')
    tela.comboBox_8.addItem(item)
tela.comboBox_8.setCurrentIndex(0)

hg.conexao_cursor.execute(f"SELECT cod_obs, obs FROM sacobs")
arq_obs = hg.conexao_cursor.fetchall()
hg.conexao_bd.commit()

for ret_obs in arq_obs:
    item = f'{ret_obs[0]} - {ret_obs[1]}'.strip('(),')
    tela.comboBox_9.addItem(item)
tela.comboBox_9.setCurrentIndex(0)

hg.conexao_cursor.execute(f"SELECT CAST(operacao as char(5)), "
                                  f"CAST(descr_op as char(40)), "
                                  f"iif(credito = 'S','Debito ou Credito','Sem Movimentacao'), "
                                  f"iif(sai_ent = 'S', 'Nota de Saida', 'Nota de Entrada'), "
                                  f"iif(tipo = '1', '1 - NFe NORMAL', iif(tipo = '2', '2 - NFe COMPLEMENTAR', "
                                  f"iif(tipo = '3', '3 - NFe AJUSTE', '4 - DEVOLUCAO/RETORNO')))  "
                                  f" FROM sacop WHERE operacao like '5%' ORDER BY operacao")

arq_cfop = hg.conexao_cursor.fetchall()
hg.conexao_bd.commit()

for ret_cfop in arq_cfop:
    item = f'{ret_cfop[0]} - {ret_cfop[1]} - {ret_cfop[2]} - {ret_cfop[3]} - {ret_cfop[4]}'.strip('(),')
    tela.comboBox_12.addItem(item)
tela.comboBox_12.setCurrentIndex(0)
hg.conexao_cursor.execute(f"SELECT CAST(operacao as char(5)), "
                                  f"CAST(descr_op as char(40)), "
                                  f"iif(credito = 'S','Debito ou Credito','Sem Movimentacao'), "
                                  f"iif(sai_ent = 'S', 'Nota de Saida', 'Nota de Entrada'), "
                                  f"iif(tipo = '1', '1 - NFe NORMAL', iif(tipo = '2', '2 - NFe COMPLEMENTAR', "
                                  f"iif(tipo = '3', '3 - NFe AJUSTE', '4 - DEVOLUCAO/RETORNO')))  "
                                  f" FROM sacop WHERE operacao like '6%' ORDER BY operacao")

# hg.conexao_cursor.execute("SELECT operacao, descr_op, sai_ent, tipo FROM sacop WHERE operacao like '6%' or "
#                                   "operacao like '2%'")
arq_cfop = hg.conexao_cursor.fetchall()
hg.conexao_bd.commit()

for ret_cfop in arq_cfop:
    # item = f'{ret_cfop[0]} - {ret_cfop[1]} - {ret_cfop[2]} - {ret_cfop[3]} - {ret_cfop[4]}'.strip('(),')
    item = f'{ret_cfop[0]} - {ret_cfop[1]} - {ret_cfop[2]} - {ret_cfop[3]} - {ret_cfop[4]}'
    tela.comboBox_13.addItem(item)

tela.comboBox_13.setCurrentIndex(0)

hg.conexao_cursor.execute(f"SELECT codemp, razao FROM sacemp")
arq_emp = hg.conexao_cursor.fetchall()
hg.conexao_bd.commit()

for ret_emp in arq_emp:
    item = f'{ret_emp[0]} - {ret_emp[1]}'.strip('(),')
    tela.comboBox_15.addItem(item)
tela.comboBox_15.setCurrentIndex(0)

# # acbr_dll = ctypes.CDLL('C:\HTI\PYTHON\SISCOM\MT\Cdecl\ACBrConsultaCNPJ64.dll')
# # acbr_dll = ctypes.CDLL('C:\HTI\PYTHON\SISCOM\MT\StdCall\ACBrConsultaCNPJ64.dll')
# # acbr_dll = ctypes.CDLL('C:\HTI\PYTHON\SISCOM\StdCall\ACBrConsultaCNPJ64.dll')
# caminho_acbr = 'C:\HTI\PYTHON\SISCOM\ACBR'
# # caminho_dll = 'C:\HTI\PYTHON\SISCOM\MT\Cdecl\ACBrConsultaCNPJ64.dll'
# # caminho_dll = 'C:\HTI\PYTHON\SISCOM\MT\StdCall\ACBrConsultaCNPJ64.dll'
# caminho_dll = 'C:\HTI\PYTHON\SISCOM\Cdecl\ACBrConsultaCNPJ64.dll'
# # caminho_dll = 'C:\HTI\PYTHON\SISCOM\StdCall\ACBrConsultaCNPJ64.dll'
# if os.path.exists(caminho_dll):
#     try:
#         acbr_dll = ctypes.CDLL(caminho_dll)
#         # inicializa = acbr_dll.CNPJ_Inicializar(r'C:\HTI\PYTHON\SISCOM\ACBrNFeServicos.ini'.encode("utf-8"))
#         print(acbr_dll)
#         # inicializa = acbr_dll.CNPJ_Inicializar(f'{caminho_acbr}\\ACBrLib.ini'.encode("utf-8"))
#         inicializa = acbr_dll.CNPJ_Inicializar(' '.encode("utf-8"))
#         if inicializa == 0:
#             print(f'arquivo .INI inicializada com sucesso {inicializa}')
#         else:
#             print(f'arquivo .INI NAO inicializada com sucesso {inicializa}')
#         resposta = '                            '
#         captcha = acbr_dll.CNPJ_ConsultarCaptcha(f'{caminho_acbr}\\TEMP', resposta, 30)
#         if captcha == 0:
#             print(f'ok {captcha}')
#         else:
#             print(f'nao {captcha}')
#
#         acbr_dll.CNPJ_Finalizar()
#     except OSError as e:
#         print("Erro ao carregar a DLL:", e)
#     else:
#         print("DLL carregada com sucesso!")
# else:
#     print(f'DLL nao encontrada neste camihno: {caminho_dll}')
# Chama a função da DLL

# imagem = QPixmap("Captcha")
# pixmap_redimensionado = imagem.scaled(160, 160)  # redimensiona a imagem para 100x100
# tela.imagem_Captcha.setPixmap(pixmap_redimensionado)

# resultado = acbr_dll.minha_dll.minha_funcao( CNPJ_Consultar('536170610406', eCaptcha, sResposta, esTamanho))

data_vazia = date(1900, 1, 1)


def on_close_event(event):
    tela.close()
    event.accept()
    tela.closeEvent = on_close_event


def salvar_produto():
    m_cod_merc = tela.mcod_merc.text()
    hg.conexao_cursor.execute(f"SELECT cod_merc FROM sacmerc WHERE cod_merc = {m_cod_merc} ")
    # # Recupere o resultado
    arq_ver_merc = hg.conexao_cursor.fetchone()
    # hg.conexao_bd.commit()
    if arq_ver_merc is not None:
        QMessageBox.information(tela, "INCLUSAO de produto", "produto ja CADASTRADO !")
        return

    m_merc = tela.mmerc.text().upper()

    if len(m_merc) == 0:
        QMessageBox.critical(tela, "Campo Obrigatorio", "Razao Social !")
        tab_widget = tela.findChild(QtWidgets.QTabWidget, "tabWidget")
        tab_widget.setCurrentIndex(0)
        tela.mmerc.setFocus()
        return
    index = tela.comboBox_15.currentIndex()
    mop = tela.comboBox_15.itemText(index)
    m_empresa = mop[0:3]

    m_data_cad_f = datetime.strptime(tela.mdata_cad.text(), '%d/%m/%Y').date()
    m_data_cad = m_data_cad_f.strftime('%Y-%m-%d')
    if m_data_cad_f == data_vazia:
        m_data_cad = None

    m_cod_barr = tela.mcod_barr.text().upper()

    index = tela.comboBox.currentIndex()
    mop = tela.comboBox.itemText(index)
    m_grupo = mop[0:3]

    index = tela.comboBox_4.currentIndex()
    mop = tela.comboBox_4.itemText(index)
    m_sub_grupo = mop[0:5]

    index = tela.comboBox_5.currentIndex()
    mop = tela.comboBox_5.itemText(index)
    m_unidade = mop[0:3]

    m_pr_venda = tela.doubleSpinBox_2.value()

    m_comissao = tela.doubleSpinBox.value()
    m_com_mont = tela.doubleSpinBox_3.value()
    m_prazo = tela.doubleSpinBox_22.value()
    m_p_lucro = tela.doubleSpinBox_4.value()
    m_varejo = tela.doubleSpinBox_5.value()
    m_desc_merc = tela.doubleSpinBox_6.value()
    m_pr_venda1 = tela.doubleSpinBox_7.value()

    index = tela.comboBox_2.currentIndex()
    mop = tela.comboBox_2.itemText(index)
    m_cod_fab = mop[0:4]
    m_fabrica = mop[7:46]

    index = tela.comboBox_3.currentIndex()
    mop = tela.comboBox_3.itemText(index)
    m_tipo_merc = mop[0:1]

    m_peso_liq = tela.doubleSpinBox_8.value()
    m_peso = tela.doubleSpinBox_9.value()

    index = tela.comboBox_6.currentIndex()
    mop = tela.comboBox_6.itemText(index)
    m_especie = mop[0:4]

    m_ref = tela.mref.text().upper()

    m_disp = None
    if tela.rb_disponivel_sim.isChecked():
        m_disp = 'S'
    elif tela.rb_disponivel_nao.isChecked():
        m_disp = 'N'

    m_descont = None
    if tela.rb_descontinuado_sim.isChecked():
        m_descont = 'S'
    elif tela.rb_descontinuado_nao.isChecked():
        m_descont = 'N'

    m_sld_neg = None
    if tela.rb_saldo_neg_sim.isChecked():
        m_sld_neg = 'S'
    elif tela.rb_saldo_neg_nao.isChecked():
        m_sld_neg = 'N'

    m_est_min = tela.doubleSpinBox_10.value()
    m_est_max = tela.doubleSpinBox_11.value()
    m_gramatura = tela.doubleSpinBox_12.value()
    m_volume = tela.doubleSpinBox_13.value()

    m_local = tela.mlocal.text().upper()

    m_balanca = None
    if tela.rb_balanca_sim.isChecked():
        m_balanca = 'S'
    elif tela.rb_balanca_nao.isChecked():
        m_balanca = 'N'

    m_pocket = None
    if tela.rb_pocket_sim.isChecked():
        m_pocket = 'S'
    elif tela.rb_pocket_nao.isChecked():
        m_pocket = 'N'

    m_app_imagem = tela.mapp_imagem.text().upper()
    m_aplic0 = tela.maplic0.text().upper()
    m_aplic1 = tela.maplic1.text().upper()
    m_aplic2 = tela.maplic2.text().upper()
    m_aplic3 = tela.maplic3.text().upper()
    m_descri1 = tela.mdescri1.text().upper()

    index = tela.comboBox_7.currentIndex()
    mop = tela.comboBox_7.itemText(index)
    m_sittrib = mop[0:4]

    index = tela.comboBox_8.currentIndex()
    mop = tela.comboBox_8.itemText(index)
    m_nbm = mop[0:8]

    m_iat = None
    if tela.rb_iat_a.isChecked():
        m_iat = 'A'
    elif tela.rb_iat_t.isChecked():
        m_iat = 'T'

    m_ippt = None
    if tela.rb_ippt_p.isChecked():
        m_ippt = 'P'
    elif tela.rb_ippt_t.isChecked():
        m_ippt = 'T'

    index = tela.comboBox_9.currentIndex()
    mop = tela.comboBox_9.itemText(index)
    m_cod_clf = mop[0:2]

    m_icm = tela.doubleSpinBox_14.value()
    m_icm_sub = tela.doubleSpinBox_15.value()
    m_desc_icm_sub = tela.doubleSpinBox_16.value()
    m_ipi = tela.doubleSpinBox_17.value()
    m_desc_icm = None
    if tela.rb_desc_icm_sim.isChecked():
        m_desc_icm = 'S'
    elif tela.rb_desc_icm_nao.isChecked():
        m_desc_icm = 'N'

    m_desc_icm1 = tela.doubleSpinBox_18.value()
    m_icm_sub2 = tela.doubleSpinBox_19.value()

    index = tela.comboBox_10.currentIndex()
    mop = tela.comboBox_10.itemText(index)
    m_cst_pis = mop[0:2]

    m_pis = tela.doubleSpinBox_20.value()

    index = tela.comboBox_11.currentIndex()
    mop = tela.comboBox_11.itemText(index)
    m_cst_conf = mop[0:2]

    m_confis = tela.doubleSpinBox_21.value()

    index = tela.comboBox_12.currentIndex()
    mop = tela.comboBox_12.itemText(index)
    m_cfop_dent = mop[0:4]

    index = tela.comboBox_13.currentIndex()
    mop = tela.comboBox_13.itemText(index)
    m_cfop_fora = mop[0:4]

    sql = "INSERT INTO sacmerc (empresa, data_cad, cod_barr, " \
          "gru_sub, cod_merc, merc, " \
          "unidade, pr_venda, comissao, " \
          "com_mont, prazo, p_lucro, " \
          "varejo, desc_merc, pr_venda1, "\
          "cod_fab, fabrica, tipo_merc, " \
          "peso_liq, peso, especie, " \
          "ref, disp, descont, " \
          "sld_neg, est_min, est_max, " \
          "gramatura, local, balanca, " \
          "pocket, app_imagem, aplic0, " \
          "aplic1, aplic2, aplic3, " \
          "descri1, sittrib, nbm, " \
          "iat, ippt, cod_clf, " \
          "icm, icm_sub, desc_icm_sub, " \
          "ipi, desc_icm, desc_icm1, " \
          "icm_sub2, cst_pis, pis, " \
          "cst_conf, confis, cfop_dent, " \
          "cfop_fora, volume,  sr_deleted) "\
          " VALUES (?, ?, ?, " \
          "?, ?, ?, " \
          "?, ?, ?, " \
          "?, ?, ?, " \
          "?, ?, ?, " \
          "?, ?, ?, " \
          "?, ?, ?, " \
          "?, ?, ?, " \
          "?, ?, ?, " \
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

    hg.conexao_cursor.execute(sql, (m_empresa, m_data_cad, m_cod_barr,
                                            m_sub_grupo, m_cod_merc, m_merc,
                                            m_unidade, m_pr_venda, m_comissao,
                                            m_com_mont, m_prazo, m_p_lucro,
                                            m_varejo, m_desc_merc, m_pr_venda1,
                                            m_cod_fab, m_fabrica, m_tipo_merc,
                                            m_peso_liq, m_peso, m_especie,
                                            m_ref, m_disp, m_descont,
                                            m_sld_neg, m_est_min, m_est_max,
                                            m_gramatura, m_local, m_balanca,
                                            m_pocket, m_app_imagem, m_aplic0,
                                            m_aplic1, m_aplic2, m_aplic3,
                                            m_descri1, m_sittrib, m_nbm,
                                            m_iat, m_ippt, m_cod_clf,
                                            m_icm, m_icm_sub, m_desc_icm_sub,
                                            m_ipi, m_desc_icm, m_desc_icm1,
                                            m_icm_sub2, m_cst_pis, m_pis,
                                            m_cst_conf, m_confis, m_cfop_dent,
                                            m_cfop_fora, m_volume, ' '))

    hg.conexao_bd.commit()
    QMessageBox.information(tela, "Inclusao de produto", "Cadastro feito com SUCESSO!")

    m_merc = tela.mmerc.text().upper()

    inclusao_produto()


def carregar_combobox_2():
    index = tela.comboBox.currentIndex()
    mop = tela.comboBox.itemText(index)
    m_grupo = mop[0:3]
    tela.comboBox_4.clear()
    hg.conexao_cursor.execute(f"select gru_sub, merc from sacgrupo where gru_sub like upper('{m_grupo}%') "
                                      f"and CHAR_LENGTH(trim(gru_sub)) = 5")
    arq_sub_g = hg.conexao_cursor.fetchall()
    hg.conexao_bd.commit()

    for ret_sub_g in arq_sub_g:
        items = f'{ret_sub_g[0]} - {ret_sub_g[1]}'.strip('(),')
        tela.comboBox_4.addItem(items)
    tela.comboBox_4.setCurrentIndex(0)


def atualizar_descri1(text):
    tela.mdescri1.setText(text)


def habilitar_objeto():
    tela.doubleSpinBox_18.setEnabled(True)


def desabilitar_objeto():
    tela.doubleSpinBox_18.setEnabled(False)


def inclusao_produto():
    # PEGAR O NUMERO QUE FALTA NA SEQUENCIA OU O ULTIMO NUMERO
    hg.conexao_cursor.execute(f"select first 1 t.id_ant + 1 "
                                      f"from (select (select first 1 cast(a1.cod_merc as int) from sacmerc a1 "
                                      f"where cast(a1.cod_merc as int) < cast(a.cod_merc as int) "
                                      f"order by cast(a1.cod_merc as int) desc) as id_ant, "
                                      f"cast(a.cod_merc as int) as cod_merc from sacmerc a order by "
                                      f"cast(a.cod_merc as int)) t "
                                      f"where coalesce(t.id_ant,0) <> cast(t.cod_merc as int) - 1 ")
    # # Recupere o resultado
    arq_prod = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()

    if arq_prod is None:
        hg.conexao_cursor.execute(f"select cast(max(cod_merc) as int) + 1 from sacmerc ")
        # # Recupere o resultado
        arq_prod = hg.conexao_cursor.fetchone()
        hg.conexao_bd.commit()
        # arq_prod[0] = (arq_prod[0]) + 1
    # string_numero = str(arq_prod[0]).zfill(5)
    tela.mcod_merc.setText(str(arq_prod[0]).zfill(5))

    tab_widget = tela.findChild(QtWidgets.QTabWidget, "tabWidget")
    tab_widget.setCurrentIndex(0)

    tela.mcod_barr.setText('')
    tela.mmerc.setText('')
    tela.mapp_imagem.setText('')
    tela.mdata_cad.setDateTime(QtCore.QDateTime.currentDateTime())
    tela.maplic0.setText('')
    tela.maplic1.setText('')
    tela.maplic2.setText('')
    tela.maplic3.setText('')
    tela.mdescri1.setText('')

    tela.comboBox.currentIndexChanged.connect(carregar_combobox_2)

    tela.mdata_cad.setDateTime(QtCore.QDateTime.currentDateTime())
    tela.mcod_barr.setText('')

    # tela.mmerc.setText('')
    tela.mmerc.textChanged.connect(atualizar_descri1)

    # RADIO BUTTON
    rb_disponivel_group = QButtonGroup()
    rb_disponivel_group.addButton(tela.rb_disponivel_sim, id=1)
    rb_disponivel_group.addButton(tela.rb_disponivel_nao, id=2)
    tela.rb_disponivel_sim.setChecked(True)

    rb_descontinuado_group = QButtonGroup()
    rb_descontinuado_group.addButton(tela.rb_descontinuado_sim, id=1)
    rb_descontinuado_group.addButton(tela.rb_descontinuado_nao, id=2)
    tela.rb_descontinuado_nao.setChecked(True)

    rb_saldo_neg_group = QButtonGroup()
    rb_saldo_neg_group.addButton(tela.rb_saldo_neg_sim, id=1)
    rb_saldo_neg_group.addButton(tela.rb_saldo_neg_nao, id=2)
    tela.rb_saldo_neg_nao.setChecked(True)

    rb_balanca_group = QButtonGroup()
    rb_balanca_group.addButton(tela.rb_balanca_sim, id=1)
    rb_balanca_group.addButton(tela.rb_balanca_nao, id=2)
    tela.rb_balanca_nao.setChecked(True)

    rb_pocket_group = QButtonGroup()
    rb_pocket_group.addButton(tela.rb_pocket_sim, id=1)
    rb_pocket_group.addButton(tela.rb_pocket_nao, id=2)
    tela.rb_pocket_sim.setChecked(True)

    rb_iat_group = QButtonGroup()
    rb_iat_group.addButton(tela.rb_iat_a, id=1)
    rb_iat_group.addButton(tela.rb_iat_t, id=2)
    tela.rb_iat_a.setChecked(True)

    rb_ippt_group = QButtonGroup()
    rb_ippt_group.addButton(tela.rb_ippt_p, id=1)
    rb_ippt_group.addButton(tela.rb_ippt_t, id=2)
    tela.rb_ippt_t.setChecked(True)

    rb_desc_icm_group = QButtonGroup()
    rb_desc_icm_group.addButton(tela.rb_desc_icm_sim, id=1)
    rb_desc_icm_group.addButton(tela.rb_desc_icm_nao, id=2)
    tela.rb_desc_icm_nao.setChecked(True)

    radio_sim = tela.findChild(QRadioButton, "rb_desc_icm_sim")
    radio_sim.toggled.connect(habilitar_objeto)

    radio_nao = tela.findChild(QRadioButton, "rb_desc_icm_nao")
    radio_nao.toggled.connect(desabilitar_objeto)

    tela.doubleSpinBox_18.setEnabled(False)

    tela.bt_salvar.clicked.connect(salvar_produto)
    tela.bt_salvar.setIcon(icon_salvar)
    tela.bt_sair.clicked.connect(fecha_tela)
    tela.bt_sair.setIcon(icon_sair)

    # DESABILITAR ESSES OBJETO
    # tela.bt_contas_receber.setEnabled(False)
    # tela.bt_pedidos.setEnabled(False)
    # tela.bt_nfe.setEnabled(False)
    # tela.bt_mov_produtos.setEnabled(False)
    # tela.bt_creditos.setEnabled(False)
    # tela.bt_gerar_autorizacao.setEnabled(False)
    # tela.bt_orcamentos.setEnabled(False)

    tela.show()
    app.exec()


def fecha_tela():
    tela.close()
    tela.closeEvent = on_close_event
    return


if __name__ == '__main__':
    inclusao_produto()
    hg.conexao_bd.close()
