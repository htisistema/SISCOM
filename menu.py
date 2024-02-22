# MENU PRINCIPAL

import os
from PyQt6 import uic
from PyQt6 import QtWidgets
from PyQt6.QtGui import QIcon
from PyQt6.QtGui import QPixmap
from PyQt6.QtGui import QGuiApplication
from SISCOM import nome_computador, endereco_ip
import hti_global as hg

# PEGA O NOME DO ARQUIVO EM EXECUCAO
nome_file_com = os.path.basename(__file__)
nome_file, ext = os.path.splitext(nome_file_com)

app = QtWidgets.QApplication([])
app.setStyleSheet(hg.style_sheet)

tela = uic.loadUi(f"{hg.c_ui}\\menu.ui")
icon = QIcon(f"{hg.c_imagem}\\htiico.ico")
# tela.move(15, 10)

if hg.mtp_tela == 'G':
    primary_screen = QGuiApplication.primaryScreen()
    if primary_screen is not None:
        screen_geometry = primary_screen.geometry()
        tela.setGeometry(screen_geometry)

tela.setWindowIcon(icon)

imagem = QPixmap(f"{hg.c_imagem}\\htifirma1.jpg")
pixmap_redimensionado = imagem.scaled(450, 250)  # redimensiona a imagem para 100x100
tela.imagem_menu.setPixmap(pixmap_redimensionado)
# tela.showMaximized()

logohti = QPixmap(f"{hg.c_imagem}\\logoHTI.png")
pixmap_redimensionado = logohti.scaled(195, 190)  # redimensiona a imagem para 100x100
tela.logohti.setPixmap(pixmap_redimensionado)


if os.path.exists(f"{hg.c_imagem}\\{hg.geral_cod_usuario}.jpg"):
    usuario = QPixmap(f"{hg.c_imagem}\\{hg.geral_cod_usuario}.jpg")
else:
    usuario = QPixmap(f"{hg.c_imagem}\\htiusu.jpg")

pixmap_redimensionado = usuario.scaled(120, 110)  # redimensiona a imagem para 100x100
tela.usuario.setPixmap(pixmap_redimensionado)

lbl_nome_usuario = tela.findChild(QtWidgets.QLabel, "nome_usuario")
lbl_nome_usuario.setText(f"Codigo: {hg.geral_cod_usuario} - {hg.geral_nivel_usuario}")

lbl_versao = tela.findChild(QtWidgets.QLabel, "versao_menu")
lbl_versao.setText(f'Versao: {hg.VERSAO}')
tela.statusBar = QtWidgets.QStatusBar()
tela.setStatusBar(tela.statusBar)

nome_file_com = os.path.basename(__file__)
nome_file, ext = os.path.splitext(nome_file_com)

tela.statusBar.showMessage(f"<< {nome_file} >>  -  Nome do Computador: {nome_computador}   -   "
                           f"Caminho do Servidor BD: {hg.host}   -   IP: {endereco_ip}")


def on_close_event(event):
    hg.conexao_bd.close()
    hg.conexao_cursor.close()
    tela.close()
    event.accept()
    tela.quit()
    app.quit()
    tela.closeEvent = on_close_event


def sair():
    # print('sair')
    hg.conexao_bd.close()
    hg.conexao_cursor.close()
    tela.close()
    app.quit()
    # tela.quit()


def incluir_venda():
    from venda_ini import pedido_inicial
    pedido_inicial()


def m_produto():
    from F4_MERC import listar_produto
    listar_produto()


def m_cadcli():
    from F7_CLI import listar_cliente
    listar_cliente()


def m_usuario():
    from SACSENHA import listar_usuario
    listar_usuario()


def m_fornecedor():
    from F6_FORN import listar_fornecedor
    listar_fornecedor()


def m_cartao():
    from SAC19 import listar_cartao
    listar_cartao()


def m_cond_pag():
    from SAC20 import listar_cond_pag
    listar_cond_pag()


def m_despesas():
    from SAC17 import listar_despesa
    listar_despesa()


def m_transportadora():
    from SAC12 import listar_transportadora
    listar_transportadora()


def m_financeira():
    from SAC1FIN import listar_financiamento
    listar_financiamento()


def m_banco():
    from SACBANCO import listar_banco
    listar_banco()


def m_especie():
    from SACESPE import listar_especie
    listar_especie()


def m_despesa():
    from SAC17 import listar_despesa
    listar_despesa()


def m_estado():
    from SAC18 import listar_estados
    listar_estados()


def m_cidade():
    from SACCID import listar_cidade
    listar_cidade()


def m_obs():
    from SACOBS import listar_observacao
    listar_observacao()


def m_profi():
    from SACPROFI import listar_profissao
    listar_profissao()


def m_cfop():
    from SAC1OP import listar_cfop
    listar_cfop()


def m_ncm():
    from SAC_NCM import listar_ncm
    listar_ncm()


def m_cst():
    from SACCST import listar_cst
    listar_cst()


def m_documento():
    from SACTIPDC import listar_documento
    listar_documento()


def m_grupo():
    from SAC10 import listar_grupo
    listar_grupo()


def m_regiao():
    from SACREG import listar_regiao
    listar_regiao()


def criar_menu():
    # hg.conexao_cursor.execute(f"SELECT * FROM sacsetup")
    # m_set = hg.conexao_cursor.fetchone()
    # hg.conexao_bd.commit()
    empresa = str(hg.m_set[128])
    empresa = empresa.strip()
    cnpj = str(hg.m_set[122])
    cnpj = cnpj[:14]
    tela.setWindowTitle(f'{empresa} - CNPJ: {cnpj}                    {hg.SISTEMA}   Versao: {hg.VERSAO}')
    tela.actionProduto.triggered.connect(m_produto)
    tela.actionCliente.triggered.connect(m_cadcli)
    tela.actionUsuarios.triggered.connect(m_usuario)
    tela.actionFornecedor.triggered.connect(m_fornecedor)
    tela.actionCartoes.triggered.connect(m_cartao)
    tela.actionCondicoes_de_Pagamento.triggered.connect(m_cond_pag)
    tela.actionDespesas.triggered.connect(m_despesas)
    tela.actionTransportadora.triggered.connect(m_transportadora)
    tela.actionFinanceira.triggered.connect(m_financeira)
    tela.actionCadastro_de_Bancos_Boletos.triggered.connect(m_banco)
    tela.actionEspecie_do_Produto.triggered.connect(m_especie)
    tela.actionConta_Despesas_plano_de_conta.triggered.connect(m_despesas)
    tela.actionEstados_Imposto.triggered.connect(m_estado)
    tela.actionCadastro_de_Cidade.triggered.connect(m_cidade)
    tela.actionMensagem_para_Observacao.triggered.connect(m_obs)
    tela.actionProfissao_Ramo_Atividade.triggered.connect(m_profi)
    tela.actionCFOP.triggered.connect(m_cfop)
    tela.actionNCM.triggered.connect(m_ncm)
    tela.actionCST_CSOSN.triggered.connect(m_cst)
    tela.actionTipos_de_Documentos.triggered.connect(m_documento)
    tela.actionGrupos_Sub_Grupo.triggered.connect(m_grupo)
    tela.actionRegiao_vendedor.triggered.connect(m_regiao)
    tela.bt_venda.clicked.connect(incluir_venda)
    # tela.actionTipos_de_Documentos.triggered.connect(m_documento)
    # tela.actionTipos_de_Documentos.triggered.connect(m_documento)
    # tela.actionTipos_de_Documentos.triggered.connect(m_documento)
    # tela.actionTipos_de_Documentos.triggered.connect(m_documento)
    tela.actionSAIR.triggered.connect(sair)
    tela.show()


if __name__ == '__main__':
    from hti_funcoes import conexao_banco
    conexao_banco()
    criar_menu()
    app.exec()
    hg.conexao_cursor.close()
    tela.close()
    hg.conexao_bd.close()
    app.quit()
