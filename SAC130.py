# CLIENTES

import os
from PyQt6 import uic, QtWidgets, QtCore
from PyQt6.QtGui import QIcon, QGuiApplication
from PyQt6.QtWidgets import QButtonGroup, QRadioButton, QMessageBox
from datetime import datetime, date
import hti_global

titulo = "INCLUSÃO DE CLIENTES"
app = QtWidgets.QApplication([])
app.setStyleSheet(hti_global.style_sheet)
tela = uic.loadUi(f"{hti_global.c_ui}\\hticliente.ui")
icon = QIcon(f"{hti_global.c_imagem}\\htiico.jpg")
icon_sair = QIcon(f"{hti_global.c_imagem}\\sair.png")
icon_salvar = QIcon(f"{hti_global.c_imagem}\\salvar.png")
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
lbl_titulo_cliente = tela.findChild(QtWidgets.QLabel, "tit_cliente")
lbl_titulo_cliente.setText(titulo)
# PEGA O NOME DO ARQUIVO EM EXECUCAO
nome_file_com = os.path.basename(__file__)
nome_file, ext = os.path.splitext(nome_file_com)

tela.statusBar.showMessage(f"<< {nome_file} >>")


hti_global.conexao_cursor.execute(f"SELECT * FROM sacsetup")
# Recupere o resultado
m_set = hti_global.conexao_cursor.fetchone()
hti_global.conexao_bd.commit()

hti_global.conexao_cursor.execute(f"SELECT cidade FROM saccid ORDER BY cidade")
# Recupere o resultado
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

hti_global.conexao_cursor.execute(f"SELECT uf, estado FROM sacuf ORDER BY uf")
arq_estado = hti_global.conexao_cursor.fetchall()
hti_global.conexao_bd.commit()

# COMBOX
tela.comboBox.addItems(["C->Cliente", "R->Revenda", "P->Potencial", "F->Filial", "U->Funcionarios", "A->Associado",
                        "O->Outros", "E->Excluido", "S->Supermercado"])
tela.comboBox.setCurrentIndex(0)  # coloca o focus no index

for ret_cidade in arq_cidade:
    item = f'{ret_cidade[0]}'.strip('(),')
    tela.comboBox_3.addItem(item)
    tela.comboBox_7.addItem(item)
    tela.comboBox_8.addItem(item)

for i in range(tela.comboBox_3.count()):
    item_text = tela.comboBox_3.itemText(i)
    # Verifica se o texto de busca está contido no item
    if str(m_set[133]).strip() in item_text:
        # Seleciona o item encontrado
        tela.comboBox_3.setCurrentIndex(i)
        tela.comboBox_7.setCurrentIndex(i)
        tela.comboBox_8.setCurrentIndex(i)
        break

tela.comboBox_5.addItem('00000 - DEFAULT')
for ret_profi in arq_profi:
    item = f'{ret_profi[0]} - {ret_profi[1]}'.strip('(),')
    tela.comboBox_5.addItem(item)

tela.comboBox_9.addItem('00 - DEFAULT')
for ret_regiao in arq_regiao:
    item = f'{ret_regiao[0]} - {ret_regiao[1]}'.strip('(),')
    tela.comboBox_9.addItem(item)

for ret_usuario in arq_usuario:
    item = f'{ret_usuario[0]} - {ret_usuario[1]}'.strip('(),')
    tela.comboBox_13.addItem(item)
    tela.comboBox_14.addItem(item)
    tela.comboBox_15.addItem(item)

tela.comboBox_13.setCurrentIndex(0)
tela.comboBox_14.setCurrentIndex(0)
tela.comboBox_15.setCurrentIndex(0)

tela.comboBox_16.addItem('000 - DEFAULT')
for ret_sactabpg in arq_sactabpg:
    item = f'{ret_sactabpg[0]} - {ret_sactabpg[1]}'.strip('(),')
    tela.comboBox_16.addItem(item)

for ret_estado in arq_estado:
    item = f'{ret_estado[0]} - {ret_estado[1]}'.strip('(),')
    tela.comboBox_2.addItem(item)
    tela.comboBox_4.addItem(item)
    tela.comboBox_6.addItem(item)
    tela.comboBox_16.addItem(item)

tela.comboBox_2.setCurrentIndex(16)  # coloca o focus no index
tela.comboBox_4.setCurrentIndex(16)  # coloca o focus no index
tela.comboBox_6.setCurrentIndex(16)    # coloca o focus no index
tela.comboBox_16.setCurrentIndex(16)    # coloca o focus no index

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
#         # inicializa = acbr_dll.CNPJ_Inicializar(f'{caminho_acbr}\ACBrLib.ini'.encode("utf-8"))
#         inicializa = acbr_dll.CNPJ_Inicializar(' '.encode("utf-8"))
#         if inicializa == 0:
#             print(f'arquivo .INI inicializada com sucesso {inicializa}')
#         else:
#             print(f'arquivo .INI NAO inicializada com sucesso {inicializa}')
#         resposta = '                            '
#         captcha = acbr_dll.CNPJ_ConsultarCaptcha(f'{caminho_acbr}\TEMP', resposta, 30)
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


def salvar_cliente():
    m_cod_cli = int(tela.mcod_cli.text())
    hti_global.conexao_cursor.execute(f"SELECT * FROM saccli WHERE cod_cli = {m_cod_cli} ")
    # # Recupere o resultado
    arq_ver_cli = hti_global.conexao_cursor.fetchone()
    hti_global.conexao_bd.commit()
    if arq_ver_cli is not None:
        QMessageBox.information(tela, "alteracao de fornecedor", "Cliente ja CADASTRADO !")
        return

    m_razao = tela.mrazao.text().upper()
    if len(m_razao) == 0:
        QMessageBox.critical(tela, "Campo Obrigatorio", "Razao Social !")
        return

    rb_mbloqueio = None
    rb_mpocket = None
    rb_mboleto = None
    rb_mspc = None
    rb_matc_vare = None
    if tela.RB_pocket_sim.isChecked():
        rb_mpocket = 'S'
    elif tela.RB_pocket_nao.isChecked():
        rb_mpocket = 'N'

    if tela.rb_boleto_sim.isChecked():
        rb_mboleto = 'S'
    elif tela.rb_boleto_nao.isChecked():
        rb_mboleto = 'N'

    if tela.rb_bloqueio_sim.isChecked():
        rb_mbloqueio = 'S'
    elif tela.rb_bloqueio_nao.isChecked():
        rb_mbloqueio = 'N'

    if tela.rb_spc_sim.isChecked():
        rb_mspc = 'S'
    elif tela.rb_spc_nao.isChecked():
        rb_mspc = 'N'

    if tela.rb_vare.isChecked():
        rb_matc_vare = 'V'
    elif tela.rb_atac.isChecked():
        rb_matc_vare = 'A'

    index = tela.comboBox.currentIndex()
    mop = tela.comboBox.itemText(index)
    cb_mtipo = mop[0]

    index = tela.comboBox_2.currentIndex()
    mop = tela.comboBox_2.itemText(index)
    cb_muf = mop[0]+mop[1]

    index = tela.comboBox_3.currentIndex()
    mop = tela.comboBox_3.itemText(index)
    cb_mcidade = mop[0:25]

    index = tela.comboBox_5.currentIndex()
    mop = tela.comboBox_5.itemText(index)
    cb_mprof = mop[0:5]

    index = tela.comboBox_6.currentIndex()
    mop = tela.comboBox_6.itemText(index)
    cb_muf_c = mop[0]+mop[1]

    index = tela.comboBox_7.currentIndex()
    mop = tela.comboBox_7.itemText(index)
    m_cidade_c = mop[0:25]

    index = tela.comboBox_9.currentIndex()
    mop = tela.comboBox_9.itemText(index)
    m_regiao = mop[0:2]

    index = tela.comboBox_16.currentIndex()
    mop = tela.comboBox_16.itemText(index)
    m_cod_cond = mop[0:3]

    index = tela.comboBox_15.currentIndex()
    mop = tela.comboBox_15.itemText(index)
    m_promotor = mop[0:3]

    m_nome = tela.mnome.text().upper()

    m_limite = tela.doubleSpinBox.value()

    m_data_nas_f = datetime.strptime(tela.mdata_nas.text(), '%d/%m/%Y').date()
    m_data_nas = m_data_nas_f.strftime('%Y-%m-%d')
    if m_data_nas_f == data_vazia:
        m_data_nas = None

    m_data_cad_f = datetime.strptime(tela.mdata_cad.text(), '%d/%m/%Y').date()
    m_data_cad = m_data_cad_f.strftime('%Y-%m-%d')
    if m_data_cad_f == data_vazia:
        m_data_cad = None

    # m_data_cad_f = datetime.strptime(tela.mdata_cad.text(), '%d/%m/%Y').date()
    # m_data_cad = m_data_cad_f.strftime('%Y-%m-%d')

    m_data_bloq_f = datetime.strptime(tela.mdata_bloq.text(), '%d/%m/%Y').date()
    m_data_bloq = m_data_nas_f.strftime('%Y-%m-%d')
    if m_data_bloq_f == data_vazia:
        m_data_bloq = None

    m_obs_bloq = tela.mobs_bloq.text().upper()
    m_endereco = tela.mendereco.text().upper()
    m_numero = tela.mnumero.text().upper()
    m_complemento = tela.mcomplemento.text().upper()
    m_bairro = tela.mbairro.text().upper()

    m_cep = tela.mcep.text()
    m_cep = ''.join(filter(str.isdigit, m_cep))
    m_email = tela.memail.text()
    m_rota = tela.mrota.text()
    m_rota1 = tela.mrota1.text()
    m_tel1 = tela.mtel1.text()
    m_tel2 = tela.mtel2.text()
    m_fax = tela.mfax.text()
    m_cgc = tela.mcgc.text()
    m_cgc = ''.join(filter(str.isdigit, m_cgc))
    m_insc = tela.minsc.text()
    m_cpf = tela.mcpf.text()
    m_cpf = ''.join(filter(str.isdigit, m_cpf))
    m_rg = tela.mrg.text()
    m_orgao = tela.morgao.text().upper()

    m_dat_emi_f = datetime.strptime(tela.mdat_emi.text(), '%d/%m/%Y').date()
    m_dat_emi = m_dat_emi_f.strftime('%Y-%m-%d')
    if m_dat_emi_f == data_vazia:
        m_dat_emi = None

    m_comprado = tela.mcomprado.text().upper()
    m_contato = tela.mcontato.text().upper()
    m_prazo_pag = tela.mprazo_pag.text()
    m_prazo_pag = ''.join(filter(str.isdigit, m_prazo_pag))
    m_area = tela.marea.text().upper()
    m_obs = tela.mobs.text().upper()

    m_nome1 = tela.mnome1.text().upper()

    m_data_nas1_f = datetime.strptime(tela.mdata_nas1.text(), '%d/%m/%Y').date()
    m_data_nas1 = m_data_nas1_f.strftime('%Y-%m-%d')
    if m_data_nas1_f == data_vazia:
        m_data_nas1 = None

    m_nome2 = tela.mnome2.text().upper()

    m_data_nas2_f = datetime.strptime(tela.mdata_nas2.text(), '%d/%m/%Y').date()
    m_data_nas2 = m_data_nas2_f.strftime('%Y-%m-%d')
    if m_data_nas2_f == data_vazia:
        m_data_nas2 = None

    m_nome3 = tela.mnome3.text().upper()

    m_data_nas3_f = datetime.strptime(tela.mdata_nas3.text(), '%d/%m/%Y').date()
    m_data_nas3 = m_data_nas3_f.strftime('%Y-%m-%d')
    if m_data_nas3_f == data_vazia:
        m_data_nas3 = None

    m_nome4 = tela.mnome4.text().upper()

    m_data_nas4_f = datetime.strptime(tela.mdata_nas4.text(), '%d/%m/%Y').date()
    m_data_nas4 = m_data_nas4_f.strftime('%Y-%m-%d')
    if m_data_nas4_f == data_vazia:
        m_data_nas4 = None

    m_nome5 = tela.mnome5.text().upper()

    m_data_nas5_f = datetime.strptime(tela.mdata_nas5.text(), '%d/%m/%Y').date()
    m_data_nas5 = m_data_nas5_f.strftime('%Y-%m-%d')
    if m_data_nas5_f == data_vazia:
        m_data_nas5 = None

    m_desconto = tela.doubleSpinBox_2.value()

    m_empre_c = tela.mempre_c.text().upper()
    m_cargo_c = tela.mcargo_c.text().upper()

    msalario_c = tela.doubleSpinBox_3.value()

    m_end_c = tela.mend_c.text().upper()
    m_bairro_c = tela.mbairro_c.text().upper()
    m_cep_c = tela.mcep_c.text()
    m_cep_c = ''.join(filter(str.isdigit, m_cep_c))
    m_fone_c1 = tela.mfone_c1.text()
    m_fone_c2 = tela.mfone_c2.text()

    m_loja1 = tela.mloja1.text().upper()
    m_loja2 = tela.mloja2.text().upper()

    m_nome_r1 = tela.mnome_r1.text().upper()
    m_fone_r1 = tela.mfone_r1.text()
    m_nome_r2 = tela.mnome_r2.text().upper()
    m_fone_r2 = tela.mfone_r2.text()

    # m_banco1_ = tela.mbanco1.text()
    # m_ag1_ = tela.mag1.text()
    # m_conta1_ = tela.mconta1.text()
    # m_banco2_ = tela.mbanco2.text()
    # m_ag2_ = tela.mag2.text()
    # m_conta2 = tela.mconta2.text()

    m_cartao1 = tela.mcartao1.text().upper()
    m_no1 = tela.mno1.text()
    m_venc1_f = datetime.strptime(tela.mvenc1.text(), '%d/%m/%Y').date()
    m_venc1 = m_venc1_f.strftime('%Y-%m-%d')
    if m_venc1_f == data_vazia:
        m_venc1 = None

    m_cartao2 = tela.mcartao2.text().upper()
    m_no2 = tela.mno2.text()

    m_venc2_f = datetime.strptime(tela.mvenc2.text(), '%d/%m/%Y').date()
    m_venc2 = m_venc2_f.strftime('%Y-%m-%d')
    if m_venc2_f == data_vazia:
        m_venc2 = None

    m_pai_ = tela.mpai.text().upper()
    m_mae_ = tela.mmae.text().upper()

    m_end_cob = tela.mend_cob.text().upper()

    index = tela.comboBox_8.currentIndex()
    mop = tela.comboBox_8.itemText(index)
    m_cidade_cob = mop[0:25]

    index = tela.comboBox_4.currentIndex()
    mop = tela.comboBox_4.itemText(index)
    m_uf_cob = mop[0]+mop[1]

    m_bairro_cob = tela.mbairro_cob.text().upper()
    m_cep_cob = tela.mcep_cob.text()
    m_cep_cob = ''.join(filter(str.isdigit, m_cep_cob))
    m_fone_cob = tela.mfone_cob.text()
    m_naturalidade = tela.mnaturalidade.text().upper()

    index = tela.comboBox_13.currentIndex()
    mop = tela.comboBox_13.itemText(index)
    m_codvend = mop[0:3]

    index = tela.comboBox_14.currentIndex()
    mop = tela.comboBox_14.itemText(index)
    m_codoper = mop[0:3]

    m_desde1_f = datetime.strptime(tela.mdesde1.text(), '%d/%m/%Y').date()
    m_desde1 = m_desde1_f.strftime('%Y-%m-%d')
    if m_desde1_f == data_vazia:
        m_desde1 = None

    m_desde2_f = datetime.strptime(tela.mdesde2.text(), '%d/%m/%Y').date()
    m_desde2 = m_desde2_f.strftime('%Y-%m-%d')
    if m_desde2_f == data_vazia:
        m_desde2 = None

    sql = "INSERT INTO saccli (cod_cli, razao, nome,  data_cad, tipo, nascimento, " \
          "endereco, numero, complemento, bairro, cidade, uf, cep, "\
          "email, rota, rota1, tel1, tel2, fax, " \
          "cgc, insc, cpf, rg, orgao, dat_emi, " \
          "comprado, contato, prazo_pag, bloqueio, spc, area, "\
          "data_bloq, obs_bloq, " \
          "limite, atac_vare, obs, " \
          "nome1, data_nas1, nome2, data_nas2, nome3, data_nas3, nome4, data_nas4, " \
          "nome5, data_nas5, desconto, " \
          "empre_c, cargo_c, salario_c, end_c, bairro_c, cidade_c, " \
          "uf_c, cep_c, fone_c1, fone_c2, " \
          "loja1, desde1, loja2, desde2, " \
          "nome_r1, fone_r1, nome_r2, fone_r2, " \
          "cartao1, no1, venc1, cartao2, no2, venc2, " \
          "pai, mae, " \
          "end_cob, bairro_cob, cidade_cob, uf_cob, cep_cob, fone_cob, " \
          "codvend, codoper, naturalidade, regiao, " \
          "cod_cond, pocket, cod_profi, promotor, sr_deleted) " \
          " VALUES (?, ?, ?, ?, ?, ?, " \
          "?, ?, ?, ?, ?, ?, ?, " \
          "?, ?, ?, ?, ?, ?, " \
          "?, ?, ?, ?, ?, ?, " \
          "?, ?, ?, ?, ?, ?, "\
          "?, ?, "\
          "?, ?, ?, "\
          "?, ?, ?, ?, ?, ?, ?, ?, "\
          "?, ?, ?, "\
          "?, ?, ?, ?, ?, ?, " \
          "?, ?, ?, ?, "\
          "?, ?, ?, ?, "\
          "?, ?, ?, ?, "\
          "?, ?, ?, ?, ?, ?, "\
          "?, ?, "\
          "?, ?, ?, ?, ?, ?, "\
          "?, ?, ?, ?, "\
          "?, ?, ?, ?, ?) "

    hti_global.conexao_cursor.execute(sql, (m_cod_cli, m_razao, m_nome,  m_data_cad, cb_mtipo, m_data_nas,
                                            m_endereco, m_numero, m_complemento, m_bairro, cb_mcidade, cb_muf, m_cep,
                                            m_email, m_rota, m_rota1, m_tel1, m_tel2, m_fax,
                                            m_cgc, m_insc, m_cpf, m_rg, m_orgao, m_dat_emi,
                                            m_comprado, m_contato, m_prazo_pag + rb_mboleto, rb_mbloqueio, rb_mspc, m_area,
                                            m_data_bloq, m_obs_bloq,
                                            m_limite, rb_matc_vare, m_obs,
                                            m_nome1, m_data_nas1, m_nome2, m_data_nas2, m_nome3, m_data_nas3, m_nome4, m_data_nas4,
                                            m_nome5, m_data_nas5, m_desconto,
                                            m_empre_c, m_cargo_c, msalario_c, m_end_c, m_bairro_c, m_cidade_c,
                                            cb_muf_c, m_cep_c, m_fone_c1, m_fone_c2,
                                            m_loja1, m_desde1, m_loja2, m_desde2,
                                            m_nome_r1, m_fone_r1, m_nome_r2, m_fone_r2,
                                            m_cartao1, m_no1, m_venc1, m_cartao2, m_no2, m_venc2,
                                            m_pai_, m_mae_,
                                            m_end_cob, m_bairro_cob, m_cidade_cob, m_uf_cob, m_cep_cob, m_fone_cob,
                                            m_codvend, m_codoper, m_naturalidade, m_regiao,
                                            m_cod_cond, rb_mpocket, cb_mprof, m_promotor, ' '))

    # m_banco1_, m_ag1_, m_conta1_, m_banco2_, m_ag2_, m_conta2_,

    hti_global.conexao_bd.commit()
    QMessageBox.information(tela, "Inclusao de CLIENTE", "Cadastro feito com SUCESSO!")

    inclusao_cliente()


def habilitar_objeto():
    tela.mdata_bloq.setEnabled(True)
    tela.mobs_bloq.setEnabled(True)


def desabilitar_objeto():
    tela.mdata_bloq.setEnabled(False)
    tela.mobs_bloq.setEnabled(False)


def inclusao_cliente():
    # PEGAR O ULTIMO NUMERO DOS CLIENTE E ACRESCENTA 1
    hti_global.conexao_cursor.execute(f"SELECT max(cod_cli) FROM saccli ")
    arq_cli = hti_global.conexao_cursor.fetchone()
    hti_global.conexao_bd.commit()
    tab_widget = tela.findChild(QtWidgets.QTabWidget, "tabWidget")
    tab_widget.setCurrentIndex(0)
    tela.mcgc.setText('')
    tela.mcod_cli.setText(str(arq_cli[0] + 1))
    tela.mrazao.setText('')
    tela.mnome.setText('')
    tela.mdata_cad.setDateTime(QtCore.QDateTime.currentDateTime())
    # tela.mdata_nas.setDateTime(QtCore.QDateTime.currentDateTime())
    tela.mnaturalidade.setText('')
    tela.memail.setText('')
    tela.mrota.setText('')
    tela.mrota1.setText('')
    tela.minsc.setText('')
    tela.mcpf.setText('')
    tela.mrg.setText('')
    tela.morgao.setText('')
    # tela.mdat_emi.setDateTime(QtCore.QDateTime.currentDateTime())
    tela.mtel1.setText('')
    tela.mtel2.setText('')
    tela.mfax.setText('')
    tela.mpai.setText('')
    tela.mmae.setText('')
    tela.mobs.setText('')

    tela.mendereco.setText('')
    tela.mnumero.setText('')
    tela.mcomplemento.setText('')
    tela.mbairro.setText('')
    tela.mcep.setText(str(m_set[134]))

    tela.mprazo_pag.setText('')
    tela.marea.setText('')
    tela.mobs_bloq.setText('')
    # tela.mdata_bloq.setDateTime(QtCore.QDateTime.currentDateTime())

    tela.mcomprado.setText('')
    tela.mcontato.setText('')
    tela.mend_cob.setText('')
    tela.mbairro_cob.setText('')
    tela.mcep_cob.setText('')

    tela.mempre_c.setText('')
    tela.mcargo_c.setText('')
    tela.mend_c.setText('')
    tela.mbairro_c.setText('')
    tela.mcep_c.setText('')
    tela.mfone_c1.setText('')
    tela.mfone_c2.setText('')

    tela.mnome_r1.setText('')
    tela.mfone_r1.setText('')
    tela.mnome_r2.setText('')
    tela.mfone_r2.setText('')
    tela.mloja1.setText('')
    tela.mloja2.setText('')
    tela.mbanco1.setText('')
    tela.mag1.setText('')
    tela.mconta1.setText('')
    tela.mbanco2.setText('')
    tela.mag2.setText('')
    tela.mconta2.setText('')
    tela.mcartao1.setText('')
    tela.mno1.setText('')
    tela.mcartao2.setText('')
    tela.mno2.setText('')

    tela.mnome1.setText('')
    tela.mnome2.setText('')
    tela.mnome3.setText('')
    tela.mnome4.setText('')
    tela.mnome5.setText('')

    # RADIO BUTTON
    rb_app_group = QButtonGroup()
    rb_app_group.addButton(tela.RB_pocket_sim, id=1)
    rb_app_group.addButton(tela.RB_pocket_nao, id=2)
    tela.RB_pocket_sim.setChecked(True)

    rb_bloqueio_group = QButtonGroup()
    rb_bloqueio_group.addButton(tela.rb_bloqueio_sim, id=1)
    rb_bloqueio_group.addButton(tela.rb_bloqueio_nao, id=2)
    tela.rb_bloqueio_sim.setChecked(True)

    rb_boleto_group = QButtonGroup()
    rb_boleto_group.addButton(tela.rb_boleto_sim, id=1)
    rb_boleto_group.addButton(tela.rb_boleto_nao, id=2)
    tela.rb_boleto_sim.setChecked(True)

    rb_spc_group = QButtonGroup()
    rb_spc_group.addButton(tela.rb_spc_sim, id=1)
    rb_spc_group.addButton(tela.rb_spc_nao, id=2)
    tela.rb_spc_sim.setChecked(True)

    rb_atac_vare_group = QButtonGroup()
    rb_atac_vare_group.addButton(tela.rb_vare, id=1)
    rb_atac_vare_group.addButton(tela.rb_atac, id=2)
    tela.rb_vare.setChecked(True)
    tela.mcgc.setFocus()

    radio_sim = tela.findChild(QRadioButton, "rb_bloqueio_sim")
    radio_sim.toggled.connect(habilitar_objeto)

    radio_nao = tela.findChild(QRadioButton, "rb_bloqueio_nao")
    radio_nao.toggled.connect(desabilitar_objeto)

    # DESABILITAR ESSES OBJETO
    tela.bt_contas_receber.setEnabled(False)
    tela.bt_pedidos.setEnabled(False)
    tela.bt_nfe.setEnabled(False)
    tela.bt_mov_produtos.setEnabled(False)
    tela.bt_creditos.setEnabled(False)
    tela.bt_gerar_autorizacao.setEnabled(False)
    tela.bt_orcamentos.setEnabled(False)

    tela.bt_salvar.clicked.connect(salvar_cliente)
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
    inclusao_cliente()
    hti_global.conexao_bd.close()
