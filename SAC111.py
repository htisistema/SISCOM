# ALTERACAO DE PRODUTOS

import os
from PyQt6 import uic, QtCore, QtWidgets
from PyQt6.QtGui import QIcon, QGuiApplication
from PyQt6.QtWidgets import QButtonGroup, QMessageBox, QRadioButton, QComboBox
from PyQt6.QtCore import QDate, QDateTime, QTime
from datetime import datetime, date
from hti_funcoes import conexao_banco
import hti_global as hg

titulo = "ALTERACAO DE PRODUTOS"

app = QtWidgets.QApplication([])
app.setStyleSheet(hg.style_sheet)
tela = uic.loadUi(f"{hg.c_ui}\\sac110.ui")
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

lbl_titulo_produto = tela.findChild(QtWidgets.QLabel, "tit_produto")
lbl_titulo_produto.setText(titulo)

# PEGA O NOME DO ARQUIVO EM EXECUCAO
nome_file_com = os.path.basename(__file__)
nome_file, ext = os.path.splitext(nome_file_com)

tela.statusBar.showMessage(f"<< {nome_file} >>")

conexao_banco()

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

# hg.conexao_cursor.execute(f"select gru_sub, merc from sacgrupo where gru_sub like '001%'"
#                                   f"and CHAR_LENGTH(trim(gru_sub)) = 5")
# arq_sub_grupo = hg.conexao_cursor.fetchall()
# hg.conexao_bd.commit()

# for ret_sub_grupo in arq_sub_grupo:
#     item = f'{ret_sub_grupo[0]} - {ret_sub_grupo[1]}'.strip('(),')
#     tela.comboBox_4.addItem(item)
# tela.comboBox_4.setCurrentIndex(0)

hg.conexao_cursor.execute(f"SELECT cod_forn, razao FROM sacforn WHERE forn_desp = 'F'")
arq_forn = hg.conexao_cursor.fetchall()
hg.conexao_bd.commit()

item = f'0000 - DEFAULT'.strip('(),')
tela.comboBox_2.addItem(item)
tela.comboBox_14.addItem(item)

for ret_forn in arq_forn:
    item = f'{ret_forn[0]} - {ret_forn[1]}'.strip('(),')
    tela.comboBox_2.addItem(item)
    tela.comboBox_14.addItem(item)
tela.comboBox_2.setCurrentIndex(0)
tela.comboBox_14.setCurrentIndex(0)

hg.conexao_cursor.execute(f"SELECT scod_op, snome FROM insopera ORDER BY snome")
# Recupere o resultado
arq_usuario = hg.conexao_cursor.fetchall()
hg.conexao_bd.commit()

# COMBOX
tela.comboBox_3.addItems(["1->Produto", "2->Materia Prima", "3->Isumos", "4->Consumo", "5->Outros"])
tela.comboBox_3.setCurrentIndex(0)  # coloca o focus no index

tela.cb_unidade.addItems(["UN ->Unidade", "AR ->Arroba", "CX ->Caixa", "FD ->Fardo", "KG ->Kilo", "MT ->Metro",
                          "TON->Tonelada"])
tela.cb_unidade.setCurrentIndex(0)  # coloca o focus no index

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

 


def on_close_event(event):
    tela.close()
    event.accept()
    tela.closeEvent = on_close_event


def salvar_produto():
    m_cod_merc = tela.mcod_merc.text()
    hg.conexao_cursor.execute(f"SELECT * FROM sacmerc WHERE cod_merc = {m_cod_merc} ")
    # # Recupere o resultado
    arq_prod_bal = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()

    m_merc = tela.mmerc.text().upper().strip()
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
    if m_data_cad_f ==  hg.data_vazia:
        m_data_cad = None

    m_cod_barr = tela.mcod_barr.text().upper()

    index = tela.comboBox.currentIndex()
    mop = tela.comboBox.itemText(index)
    m_grupo = mop[0:3]

    index = tela.comboBox_4.currentIndex()
    mop = tela.comboBox_4.itemText(index)
    m_sub_grupo = mop[0:5]

    index = tela.cb_unidade.currentIndex()
    mop = tela.cb_unidade.itemText(index)
    m_unidade = mop[0:3]

    m_pr_venda = tela.doubleSpinBox_2.value()

    m_comissao = tela.doubleSpinBox.value()
    m_com_mont = tela.doubleSpinBox_3.value()
    m_prazo = tela.doubleSpinBox_22.value()
    m_p_lucro = tela.doubleSpinBox_4.value()
    m_desc_merc = tela.doubleSpinBox_6.value()
    # m_pr_venda1 = tela.doubleSpinBox_7.value()
    m_peso_liq = tela.doubleSpinBox_8.value()
    m_peso = tela.doubleSpinBox_9.value()

    index = tela.comboBox_2.currentIndex()
    mop = tela.comboBox_2.itemText(index)
    m_cod_fab = mop[0:4]
    m_fabrica = mop[7:46].strip()

    index = tela.comboBox_3.currentIndex()
    mop = tela.comboBox_3.itemText(index)
    m_tipo_merc = mop[0:1]

    index = tela.comboBox_6.currentIndex()
    mop = tela.comboBox_6.itemText(index)
    m_especie = mop[0:4]

    m_ref = tela.mref.text().upper().strip()

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

    m_local = tela.mlocal.text().upper().strip()

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

    m_app_imagem = tela.mapp_imagem.text().upper().strip()
    m_aplic0 = tela.maplic0.text().upper().strip()
    m_aplic1 = tela.maplic1.text().upper().strip()
    m_aplic2 = tela.maplic2.text().upper().strip()
    m_aplic3 = tela.maplic3.text().upper().strip()
    m_descri1 = tela.mdescri1.text().upper().strip()

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

    m_data_cad_2 = datetime.strptime(tela.mdata_cad_2.text(), '%d/%m/%Y').date()
    m_data_cad_2 = m_data_cad_2.strftime('%Y-%m-%d')
    if m_data_cad_2 ==  hg.data_vazia:
        m_data_cad_2 = None

    mfiscal = tela.doubleSpinBox_35.value()
    mfisico = tela.doubleSpinBox_36.value()
    mpr_custo = tela.doubleSpinBox_27.value()
    mpr_venda = tela.doubleSpinBox_28.value()
    mcust_merc = tela.doubleSpinBox_26.value()
    mvlr_merc = tela.doubleSpinBox_25.value()
    mpr_venda1 = tela.doubleSpinBox_29.value()
    mvarejo = tela.doubleSpinBox_30.value()
    mpr_fat = tela.doubleSpinBox_31.value()

    ma_cust_mer = arq_prod_bal[36]
    ma_vlr_merc = arq_prod_bal[35]
    ma_cust_rea = arq_prod_bal[37]
    mcust_real = mpr_custo
    mpr_medio = mpr_custo

    mhora = datetime.now().strftime("%H:%M:%S")
    mopera_pr = hg.geral_cod_usuario

    mdata_atu = m_data_cad_2

    mdat_ult_e = None
    mdat_ult_s = None
    mul_alt_pr = None

    if not mfiscal == 0 or not mfisico == 0:
        if mfisico > 0 or mfiscal > 0:
            mdat_ult_e = m_data_cad_2
        else:
            mdat_ult_s = m_data_cad_2

    msaldo_fis = float(arq_prod_bal[54])
    msaldo_mer = float(arq_prod_bal[55])
    msaldo_fis = msaldo_fis + mfiscal
    msaldo_mer = msaldo_mer + mfisico

    # and ver_nivel('CUSTOREAL', 'BALANCO *** CORRECAO CUSTO REAL ***', '15',nivel_acess, '*'):
    if mpr_custo == arq_prod_bal[44]:
        ma_cust_rea = float(arq_prod_bal[37])
        mcust_real = mpr_custo
        mpr_medio = mpr_custo

    if not mpr_venda == arq_prod_bal[45]:
        mul_alt_pr = m_data_cad_2

    if not mpr_venda == arq_prod_bal[45] or not mpr_custo == arq_prod_bal[44]:
        mhora = datetime.now().strftime("%H:%M:%S")
        mopera_pr = hg.geral_cod_usuario

    if mcust_merc == arq_prod_bal[43]:
        ma_cust_mer = float(arq_prod_bal[36])

    if mvlr_merc == arq_prod_bal[42]:
        ma_vlr_merc = float(arq_prod_bal[35])

    sql = "UPDATE sacmerc SET empresa = ?, cod_barr = ?, " \
          "gru_sub = ?, cod_merc = ?, merc = ?, " \
          "unidade = ?, comissao = ?, " \
          "com_mont = ?, prazo = ?, p_lucro = ?, " \
          "desc_merc = ?, " \
          "cod_fab = ?, fabrica = ?, tipo_merc = ?, " \
          "peso_liq = ?, peso = ?, especie = ?, " \
          "ref = ?, disp = ?, descont = ?, " \
          "sld_neg = ?, est_min = ?, est_max = ?, " \
          "gramatura = ?, local = ?, balanca = ?, " \
          "pocket = ?, app_imagem = ?, aplic0 = ?, " \
          "aplic1 = ?, aplic2 = ?, aplic3 = ?, " \
          "descri1 = ?, sittrib = ?, nbm = ?, " \
          "iat = ?, ippt = ?, cod_clf = ?, " \
          "icm = ?, icm_sub = ?, desc_icm_sub = ?, " \
          "ipi = ?, desc_icm = ?, desc_icm1 = ?, " \
          "icm_sub2 = ?, cst_pis = ?, pis = ?, " \
          "cst_conf = ?, confis = ?, cfop_dent = ?, " \
          "cfop_fora = ?, volume = ?, " \
          "data_atu = ?, saldo_fis = ?, saldo_mer = ?, pr_venda = ?, pr_venda1 = ?, varejo = ?, pr_fat = ?, " \
          "dat_ult_e = ?, dat_ult_s = ?, a_cust_rea = ?, cust_real = ?, pr_medio = ?, ul_alt_pr = ?, hora = ?, " \
          "opera_pr = ?, a_cust_mer = ?, a_vlr_merc = ? " \
          "WHERE cod_merc = ?"

    values = (m_empresa, m_cod_barr,
              m_sub_grupo, m_cod_merc, m_merc,
              m_unidade, m_comissao,
              m_com_mont, m_prazo, m_p_lucro,
              m_desc_merc,
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
              m_cfop_fora, m_volume,
              mdata_atu, msaldo_fis, msaldo_mer, mpr_venda, mpr_venda1, mvarejo, mpr_fat, mdat_ult_e, mdat_ult_s,
              ma_cust_rea, mcust_real, mpr_medio, mul_alt_pr, mhora, mopera_pr, ma_cust_mer, ma_vlr_merc,
              m_cod_merc)

    # print(sql, values)

    hg.conexao_cursor.execute(sql, values)
    hg.conexao_bd.commit()

    # sql = f"UPDATE sacmerc SET data_atu = ?, saldo_fis = ? , saldo_mer = ?, pr_venda  = ?, pr_venda1 = ?, " \
    #       f"varejo = ?, pr_fat = ?, dat_ult_e = ?, mdat_ult_s = ?, a_cust_rea = ?, cust_real = ?, pr_medio = ?, " \
    #       f"ul_alt_pr = ?, hora = ?, opera_pr = ?, a_cust_mer = ?, a_vlr_merc = ? WHERE cod_merc = ?"
    #
    # values = (mdata_atu, msaldo_fis, msaldo_mer, mpr_venda, mpr_venda1, mvarejo, mpr_fat, mdat_ult_e, mdat_ult_s,
    #           ma_cust_rea, mcust_real, mpr_medio, mul_alt_pr,
    #           mhora, mopera_pr, ma_cust_mer, ma_vlr_merc, m_cod_merc)
    #
    # hg.conexao_cursor.execute(sql, values)
    # hg.conexao_bd.commit()

    QMessageBox.information(tela, "Altercao de PRODUTO", "Atualizacao feito com SUCESSO!")

    alteracao_produto(m_cod_merc)

    # exec('INSERT INTO logproduto (data_sis,data,' +;
        # 'hora,cod_prod,quantd,saldo_ant,saldo_pos,cod_oper,prog,terminal,' +;
        # 'processo,ent_sai,SR_DELETED )' +;
        # ' VALUES (' +;
        # DATE()) + ',' +; // 1
        # mdata_sis) + ',' +; // 2
        # TIME()) + ',' +; // 3
        # STRZERO(mcod_merc, 5)) + ',' +; // 4
        # if(mfisico > 0, mfisico, mfisico * -1)) + ',' +; // 5
        # m_merc[1, 56]) + ',' +; // 6
        # m_merc[1, 56] + mfisico) + ',' +; // 7
        # cod_operado) + ',' +; // 8
        # 'SACBAL1') + ',' +; // 9
        # LEFT(NETNAME(), 15)) + ',' +; // 12
        # 'BALANCO') + ',' +; // 11
        # if(mfisico > 0, 'E', 'S')) + ',' +; // 11
        # ' ')
        # if ! EMPTY(mfiscal)
        # sr_getconnection(): exec('INSERT INTO logprod_fis (data_sis,data,' +;
        # 'hora,cod_prod,quantd,saldo_ant,saldo_pos,cod_oper,prog,terminal,' +;
        # 'processo,ent_sai )' +;
        # ' VALUES (' +;
        # DATE()) + ',' +; // 1
        # mdata_sis) + ',' +; // 2
        # TIME()) + ',' +; // 3
        # STRZERO(mcod_merc, 5)) + ',' +; // 4
        # if(mfiscal > 0, mfiscal, mfiscal * -1)) + ',' +; // 5
        # m_merc[1, 55]) + ',' +; // 6
        # m_merc[1, 55] + mfiscal) + ',' +; // 7
        # cod_operado) + ',' +; // 8
        # 'SACBAL1') + ',' +; // 9
        # LEFT(NETNAME(), 15)) + ',' +; // 12
        # 'BALANCO') + ',' +; // 11
        # if(mfiscal > 0, 'E', 'S')) + ')',, .f.)


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


def carrega_ap_produto():
    m_cod_merc = tela.mcod_merc.text()
    m_merc = tela.mmerc.text().upper()

    lbl_ap_produto = tela.findChild(QtWidgets.QLabel, "ap_produto")
    lbl_ap_produto.setText(f"{m_cod_merc} - {m_merc}".strip())


def codigo_forn_objeto():
    tab_widget = tela.tabWidget  # Supondo que você tenha uma instância do QTabWidget chamada "tabWidget"
    current_index = tab_widget.currentIndex()
    hg.conexao_cursor.execute(f"SELECT cod_forn, razao FROM sacforn WHERE forn_desp = 'F'")
    arq_codigo = hg.conexao_cursor.fetchall()
    hg.conexao_bd.commit()
    if current_index == 2:
        tela.comboBox_2.clear()
        items = f'0000 - DEFAULT'.strip('(),')
        tela.comboBox_2.addItem(items)
        for ret_codigo in arq_codigo:
            items = f'{ret_codigo[0]} - {ret_codigo[1]}'.strip('(),')
            tela.comboBox_2.addItem(items)
        tela.comboBox_2.setCurrentIndex(0)
    elif current_index == 4:
        tela.comboBox_14.clear()
        items = f'0000 - DEFAULT'.strip('(),')
        tela.comboBox_14.addItem(items)
        for ret_codigo in arq_codigo:
            items = f'{ret_codigo[0]} - {ret_codigo[1]}'.strip('(),')
            tela.comboBox_14.addItem(items)
        tela.comboBox_14.setCurrentIndex(0)


def descricao_forn_objeto():
    tab_widget = tela.tabWidget  # Supondo que você tenha uma instância do QTabWidget chamada "tabWidget"
    current_index = tab_widget.currentIndex()
    hg.conexao_cursor.execute(f"SELECT razao, cod_forn FROM sacforn WHERE forn_desp = 'F'")
    # Recupere o resultado
    arq_codigo = hg.conexao_cursor.fetchall()
    hg.conexao_bd.commit()
    if current_index == 2:
        tela.comboBox_2.clear()
        items = f'DEFAULT - 0000'.strip('(),')
        tela.comboBox_2.addItem(items)
        for ret_codigo in arq_codigo:
            items = f'{ret_codigo[0]} - {ret_codigo[1]}'.strip('(),')
            tela.comboBox_2.addItem(items)
        tela.comboBox_2.setCurrentIndex(0)
    elif current_index == 4:
        tela.comboBox_14.clear()
        items = f'DEFAULT - 0000'.strip('(),')
        tela.comboBox_14.addItem(items)
        for ret_codigo in arq_codigo:
            items = f'{ret_codigo[0]} - {ret_codigo[1]}'.strip('(),')
            tela.comboBox_14.addItem(items)
        tela.comboBox_14.setCurrentIndex(0)


def fecha_tela():
    tela.close()
    tela.closeEvent = on_close_event
    return


def alteracao_produto(codigo_produto):
    # PEGAR O NUMERO QUE FALTA NA SEQUENCIA OU O ULTIMO NUMERO
    hg.conexao_cursor.execute(f"SELECT * FROM sacmerc WHERE cod_merc = {codigo_produto} ")
    arq_prod = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()
    hg.conexao_cursor.execute(f"SELECT SUM(pquantd) FROM sacped_s WHERE sr_deleted = ' ' AND "
                                      f"pcod_merc = {codigo_produto} AND (ppag IS NULL OR ppag = ' ')")
    arq_saldo_haver = hg.conexao_cursor.fetchone()
    hg.conexao_bd.commit()
    if arq_prod is not None:
        msaldo_haver = 0
    else:
        msaldo_haver = arq_saldo_haver[0]

    # print(arq_prod[8])
    lbl_ap_produto = tela.findChild(QtWidgets.QLabel, "ap_produto")
    mcodigo = str(codigo_produto)
    print(f"'{mcodigo}' - '{arq_prod[8]}'")
    lbl_ap_produto.setText(f"{mcodigo} - {arq_prod[8]}")

    tab_widget = tela.findChild(QtWidgets.QTabWidget, "tabWidget")
    tab_widget.setCurrentIndex(0)

    tela.mcod_merc.setText(str(codigo_produto))

    for i in range(tela.comboBox_15.count()):
        item_text = tela.comboBox_15.itemText(i)
        if str(arq_prod[0]).strip() in item_text:
            tela.comboBox_15.setCurrentIndex(i)
            break

    if arq_prod[12] is None:
        data_hora = QDateTime(QDate(1900, 1, 1), QTime(0, 0))
    else:
        # Converter o valor de data do Firebird para um objeto QDate
        data = QDate.fromString(str(arq_prod[12]), "yyyy-MM-dd")
        # Criar um objeto QDateTime com a data e um horário padrão
        data_hora = QDateTime(data, QTime(0, 0))
    tela.mdata_cad.setDateTime(data_hora)

    tela.mcod_barr.setText(str(arq_prod[1]))

    for i in range(tela.comboBox.count()):
        item_text = tela.comboBox.itemText(i)
        if str(arq_prod[6][1:3]).strip() in item_text:
            tela.comboBox.setCurrentIndex(i)
            break
    mbusca = arq_prod[6][1:3]
    hg.conexao_cursor.execute(f"select gru_sub, merc from sacgrupo where gru_sub like UPPER('%{mbusca}%') "
                                      f"and CHAR_LENGTH(trim(gru_sub)) = 5")
    arq_sub_grupo = hg.conexao_cursor.fetchall()
    hg.conexao_bd.commit()
    for ret_sub_grupo in arq_sub_grupo:
        items = f'{ret_sub_grupo[0]} - {ret_sub_grupo[1]}'.strip('(),')
        tela.comboBox_4.addItem(items)
    tela.comboBox_4.setCurrentIndex(0)

    for i in range(tela.comboBox_4.count()):
        item_text = tela.comboBox_4.itemText(i)
        if str(arq_prod[6]).strip() in item_text:
            tela.comboBox_4.setCurrentIndex(i)
            break

    tela.mmerc.setText(str(arq_prod[8]))

    for i in range(tela.cb_unidade.count()):
        item_text = tela.cb_unidade.itemText(i)
        if str(arq_prod[13]).strip() in item_text:
            tela.cb_unidade.setCurrentIndex(i)
            break

    tela.doubleSpinBox_2.setValue(float(arq_prod[45]))
    tela.doubleSpinBox.setValue(float(arq_prod[25]))
    tela.doubleSpinBox_3.setValue(float(arq_prod[26]))
    tela.doubleSpinBox_22.setValue(float(arq_prod[74]))
    tela.doubleSpinBox_4.setValue(float(arq_prod[21]))
    tela.doubleSpinBox_6.setValue(float(arq_prod[79]))

    for i in range(tela.comboBox_2.count()):
        item_text = tela.comboBox_2.itemText(i)
        if str(arq_prod[29]).strip() in item_text:
            tela.comboBox_2.setCurrentIndex(i)
            break

    for i in range(tela.comboBox_3.count()):
        item_text = tela.comboBox_3.itemText(i)
        if str(arq_prod[9]).strip() in item_text:
            tela.comboBox_3.setCurrentIndex(i)
            break

    tela.doubleSpinBox_8.setValue(float(arq_prod[15]))
    tela.doubleSpinBox_9.setValue(float(arq_prod[16]))

    for i in range(tela.comboBox_6.count()):
        item_text = tela.comboBox_6.itemText(i)
        if str(arq_prod[14]).strip() in item_text:
            tela.comboBox_6.setCurrentIndex(i)
            break

    tela.mref.setText(str(arq_prod[5]))

    rb_disponivel_group = QButtonGroup()
    rb_disponivel_group.addButton(tela.rb_disponivel_sim, id=1)
    rb_disponivel_group.addButton(tela.rb_disponivel_nao, id=2)
    if arq_prod[23] == 'S':
        tela.rb_disponivel_sim.setChecked(True)
    else:
        tela.rb_disponivel_nao.setChecked(True)

    rb_descontinuado_group = QButtonGroup()
    rb_descontinuado_group.addButton(tela.rb_descontinuado_sim, id=1)
    rb_descontinuado_group.addButton(tela.rb_descontinuado_nao, id=2)
    if arq_prod[103] == 'S':
        tela.rb_descontinuado_sim.setChecked(True)
    else:
        tela.rb_descontinuado_nao.setChecked(True)

    rb_saldo_neg_group = QButtonGroup()
    rb_saldo_neg_group.addButton(tela.rb_saldo_neg_sim, id=1)
    rb_saldo_neg_group.addButton(tela.rb_saldo_neg_nao, id=2)
    if arq_prod[102] == 'S':
        tela.rb_saldo_neg_sim.setChecked(True)
    else:
        tela.rb_saldo_neg_nao.setChecked(True)

    print(arq_prod[17])
    tela.doubleSpinBox_10.setValue(float(arq_prod[27]))
    tela.doubleSpinBox_11.setValue(float(arq_prod[28]))
    tela.doubleSpinBox_12.setValue(float(arq_prod[73]))
    tela.doubleSpinBox_13.setValue(float(arq_prod[17]))

    tela.mlocal.setText(str(arq_prod[72]))

    rb_balanca_group = QButtonGroup()
    rb_balanca_group.addButton(tela.rb_balanca_sim, id=1)
    rb_balanca_group.addButton(tela.rb_balanca_nao, id=2)
    if arq_prod[10] == 'S':
        tela.rb_balanca_sim.setChecked(True)
    else:
        tela.rb_balanca_nao.setChecked(True)

    rb_pocket_group = QButtonGroup()
    rb_pocket_group.addButton(tela.rb_pocket_sim, id=1)
    rb_pocket_group.addButton(tela.rb_pocket_nao, id=2)
    if arq_prod[10] == 'S':
        tela.rb_pocket_sim.setChecked(True)
    else:
        tela.rb_pocket_nao.setChecked(True)

    tela.mapp_imagem.setText(str(arq_prod[4]))
    tela.maplic0.setText(str(arq_prod[84]))
    tela.maplic1.setText(str(arq_prod[85]))
    tela.maplic2.setText(str(arq_prod[86]))
    tela.maplic3.setText(str(arq_prod[87]))
    tela.mdescri1.setText(str(arq_prod[3]))

    for i in range(tela.comboBox_7.count()):
        item_text = tela.comboBox_7.itemText(i)
        if str(arq_prod[67]).strip() in item_text:
            tela.comboBox_7.setCurrentIndex(i)
            break

    for i in range(tela.comboBox_8.count()):
        item_text = tela.comboBox_8.itemText(i)
        if str(arq_prod[69]).strip() in item_text:
            tela.comboBox_8.setCurrentIndex(i)
            break

    rb_iat_group = QButtonGroup()
    rb_iat_group.addButton(tela.rb_iat_a, id=1)
    rb_iat_group.addButton(tela.rb_iat_t, id=2)
    if arq_prod[80] == 'A':
        tela.rb_iat_a.setChecked(True)
    else:
        tela.rb_iat_t.setChecked(True)

    rb_ippt_group = QButtonGroup()
    rb_ippt_group.addButton(tela.rb_ippt_p, id=1)
    rb_ippt_group.addButton(tela.rb_ippt_t, id=2)
    if arq_prod[90] == 'P':
        tela.rb_ippt_p.setChecked(True)
    else:
        tela.rb_ippt_t.setChecked(True)

    for i in range(tela.comboBox_9.count()):
        item_text = tela.comboBox_9.itemText(i)
        if str(arq_prod[65]).strip() in item_text:
            tela.comboBox_9.setCurrentIndex(i)
            break

    tela.doubleSpinBox_14.setValue(float(arq_prod[59]))
    tela.doubleSpinBox_15.setValue(float(arq_prod[62]))
    tela.doubleSpinBox_16.setValue(float(arq_prod[115]))
    tela.doubleSpinBox_17.setValue(float(arq_prod[64]))

    rb_desc_icm_group = QButtonGroup()
    rb_desc_icm_group.addButton(tela.rb_desc_icm_sim, id=1)
    rb_desc_icm_group.addButton(tela.rb_desc_icm_nao, id=2)
    if arq_prod[70] == 'S':
        tela.rb_desc_icm_sim.setChecked(True)
    else:
        tela.rb_desc_icm_nao.setChecked(True)

    tela.doubleSpinBox_18.setValue(float(arq_prod[71]))
    tela.doubleSpinBox_19.setValue(float(arq_prod[63]))

    for i in range(tela.comboBox_10.count()):
        item_text = tela.comboBox_10.itemText(i)
        if str(arq_prod[104]).strip() in item_text:
            tela.comboBox_10.setCurrentIndex(i)
            break

    tela.doubleSpinBox_20.setValue(float(arq_prod[109]))

    for i in range(tela.comboBox_11.count()):
        item_text = tela.comboBox_11.itemText(i)
        if str(arq_prod[105]).strip() in item_text:
            tela.comboBox_11.setCurrentIndex(i)
            break

    for i in range(tela.comboBox_12.count()):
        item_text = tela.comboBox_12.itemText(i)
        if str(arq_prod[108]).strip() in item_text:
            tela.comboBox_12.setCurrentIndex(i)
            break

    for i in range(tela.comboBox_13.count()):
        item_text = tela.comboBox_13.itemText(i)
        if str(arq_prod[107]).strip() in item_text:
            tela.comboBox_13.setCurrentIndex(i)
            break

    radio_sim = tela.findChild(QRadioButton, "rb_desc_icm_sim")
    radio_sim.toggled.connect(habilitar_objeto)

    radio_nao = tela.findChild(QRadioButton, "rb_desc_icm_nao")
    radio_nao.toggled.connect(desabilitar_objeto)

    tela.doubleSpinBox_18.setEnabled(False)

    tela.mdata_cad_2.setDateTime(QtCore.QDateTime.currentDateTime())
    tela.doubleSpinBox_32.setValue(float(msaldo_haver))
    tela.doubleSpinBox_33.setValue(float(arq_prod[54]))
    tela.doubleSpinBox_34.setValue(float(arq_prod[55]))

    tela.doubleSpinBox_23.setValue(float(arq_prod[37]))
    tela.doubleSpinBox_24.setValue(float(arq_prod[40]))
    tela.doubleSpinBox_25.setValue(float(arq_prod[42]))
    tela.doubleSpinBox_26.setValue(float(arq_prod[43]))
    tela.doubleSpinBox_27.setValue(float(arq_prod[44]))
    tela.doubleSpinBox_28.setValue(float(arq_prod[45]))
    tela.doubleSpinBox_29.setValue(float(arq_prod[46]))
    tela.doubleSpinBox_30.setValue(float(arq_prod[49]))
    tela.doubleSpinBox_31.setValue(float(arq_prod[48]))

    tela.mnum_doc.setText(str(arq_prod[0]).zfill(6)+'  ')

    if arq_prod[55] > arq_prod[28] and arq_prod[28] > 0:
        lbl_ap_estoque = tela.findChild(QtWidgets.QLabel, "estoque")
        lbl_ap_estoque.setText(f"SALDO ACIMA DO MAXIMO".strip())

    if arq_prod[55] < arq_prod[27] and arq_prod[27] > 0:
        lbl_ap_estoque = tela.findChild(QtWidgets.QLabel, "estoque")
        lbl_ap_estoque.setText(f"SALDO ABAIXO MINIMO".strip())

    rb_forn_group = QButtonGroup()
    tela.rb_forn_codigo = QRadioButton("Código")
    tela.rb_forn_descricao = QRadioButton("Descrição")
    rb_forn_group.addButton(tela.rb_forn_codigo, id=1)
    rb_forn_group.addButton(tela.rb_forn_descricao, id=2)
    tela.rb_forn_codigo.setChecked(True)

    order_forn_codigo = tela.findChild(QRadioButton, "rb_forn_codigo")
    order_forn_codigo.toggled.connect(codigo_forn_objeto)
    order_forn_descricao = tela.findChild(QRadioButton, "rb_forn_descricao")
    order_forn_descricao.toggled.connect(descricao_forn_objeto)

    tela.mmerc.returnPressed.connect(carrega_ap_produto)
    tela.mmerc.editingFinished.connect(carrega_ap_produto)
    tela.mcod_merc.setEnabled(False)

    tela.comboBox.currentIndexChanged.connect(carregar_combobox_2)
    tela.bt_salvar.clicked.connect(salvar_produto)
    tela.bt_sair.clicked.connect(fecha_tela)
    tela.bt_sair.setIcon(icon_sair)
    tela.bt_salvar.setIcon(icon_salvar)

    # tela.doubleSpinBox_32.setEnabled(False)
    # tela.doubleSpinBox_33.setEnabled(False)
    # tela.doubleSpinBox_34.setEnabled(False)

    # DESABILITAR ESSES OBJETO
    # tela.bt_contas_receber.setEnabled(False)
    # tela.bt_pedidos.setEnabled(False)
    # tela.bt_nfe.setEnabled(False)
    # tela.bt_mov_produtos.setEnabled(False)
    # tela.bt_creditos.setEnabled(False)
    # tela.bt_gerar_autorizacao.setEnabled(False)
    # tela.bt_orcamentos.setEnabled(False)

    tela.show()


if __name__ == '__main__':
    alteracao_produto('00001')
    app.exec()
    hg.conexao_bd.close()
    hg.conexao_cursor.close()
    tela.close()
