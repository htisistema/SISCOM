from PyQt6 import uic, QtWidgets
from PyQt6.QtGui import QIcon, QGuiApplication
import keyboard
from SISCOM import SISTEMA, VERSAO
from hti_funcoes import ver_nivel, dcripto
import hti_global
import time

app = QtWidgets.QApplication([])
app.setStyleSheet(hti_global.style_sheet)
tela = uic.loadUi(f"{hti_global.c_ui}\\hti_autorizacao_senha.ui")
tela.setWindowTitle('Consulta de fornecedor')
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
mcod_aut = ' '
ambiente = ''


def sair_programa():
    tela.close()
    return False


def solicita_autorizacao(sope, scli, sprod, smen, samb):
    global mcod_aut
    index = tela.comboBox.currentIndex()
    mop = tela.comboBox.itemText(index)
    mcod_op = mop[0:3]

    lb_status = tela.findChild(QtWidgets.QLabel, "mensagem_status")

    if not scli == '':
        hti_global.conexao_cursor.execute(f"UPDATE insopera SET sstatus = 'S',sope = {sope}, scliente = {scli}, "
                                          f"smensagem = {smen} WHERE scod_op = {mcod_op}")
        hti_global.conexao_cursor.commit()

    elif not sprod == '':
        hti_global.conexao_cursor.execute(f"UPDATE insopera SET sstatus = 'S',sope = {sope}, sproduto = {sprod}, "
                                          f"smensagem = {smen} WHERE scod_op = {mcod_op}")
        hti_global.conexao_cursor.commit()

    elif not samb == '':
        hti_global.conexao_cursor.execute(f"UPDATE insopera SET sstatus = 'S',sope = {sope}, sambiente = {samb}, "
                                          f"smensagem = {smen} WHERE scod_op = {mcod_op}")
        hti_global.conexao_cursor.commit()

    tela.statusBar().showMessage('SOLICITANTO AUTORIZACAO')

    while True:
        hti_global.conexao_cursor.execute(f"SELECT sstatus,scod_aut FROM insopera WHERE scod_op =  {mcod_op}")
        arq_usu = hti_global.conexao_cursor.fetchone()
        # hti_global.conexao_cursor.commit()
        # print(arq_usu[0])

        if arq_usu is None:
            mcod_aut = 'NEGATIVO'
            tela.close()
            lb_status.setText(" ")
            return False

        if arq_usu[0] == 'S':
            print('pedido Solicitacao')
            lb_status.setText("Aguarde solicitanto AUTORIZACAO...")
            # tela.statusBar().showMessage('Aguarde solicitanto AUTORIZACAO ')

        elif arq_usu[0] == 'A':
            print('pedido Analise')
            lb_status.setText("Aguarde um momento  em  ANALISE...")

        elif arq_usu[0] == 'L':
            lb_status.setText(" ")
            print('pedido LIBERADO')
            mcod_aut = arq_usu[0][1:6]
            tela.close()
            return True

        elif arq_usu[0] == 'N':
            lb_status.setText(" ")
            print('pedido NEGATIVO')
            mcod_aut = 'NEGATIVO'
            tela.close()
            return False

        QtWidgets.QApplication.processEvents()

        if keyboard.is_pressed('esc') or not tela.isVisible():
            lb_status.setText(" ")
            break
            # sair_programa()
            # sys.exit(0)

        time.sleep(1)


def autorizar_senha():
    global tela
    # tela.statusBar().showMessage('Aguarde um momento  em  ANALISE ')
    index = tela.comboBox.currentIndex()
    mop = tela.comboBox.itemText(index)
    mcod_op = mop[0:3]
    hti_global.conexao_cursor.execute(f"SELECT * FROM sacconf WHERE TRIM(modulo) = '{mmodulo.strip()}'")
    arq_conf = hti_global.conexao_cursor.fetchone()

    hti_global.conexao_cursor.execute(f"SELECT scod_aut,ssenha,snivel FROM insopera WHERE scod_op = '{mcod_op}'")
    arq_usu = hti_global.conexao_cursor.fetchone()
    maut_oper = mcod_op
    m_aut_senha = tela.maut_senha.text()

    print(f'senha digitada: {m_aut_senha} e Senha do Operador: {dcripto(arq_usu[1])}')
    mok = ' '

    if m_aut_senha == dcripto(arq_usu[1]):
        letra1 = arq_usu[2][0]
        letra2 = arq_usu[2][1]
        presente1 = False
        presente2 = False
        if not letra1 == ' ':
            presente1 = letra1 in arq_conf[2]

        if not letra2 == ' ':
            presente2 = letra2 in arq_conf[2]

        print(f'nivel {arq_conf[2]}')
        print(f'Letra1 {letra1}')
        print(f'Letra2 {letra2}')
        print(f'presente1 {presente1}')
        print(f'presente2 {presente2}')

        if presente1 or presente2 or hti_global.geral_cod_usuario == '999':
            print("if not presente1 and not presente2 or hti_global.geral_cod_usuario == '999'")
            hti_global.m_autorizado = True
            tela.close()
            return True

        # print('senha')
        if mmodulo == 'LIB_SALDO':
            if ver_nivel(mmodulo, 'LIBERACAO DE QUANTD.SOLICITADA MAIOR QUE O SALDO DO PRODUTO', '15', arq_usu[2], 1,
                         maut_oper):
                mok = '*'

        elif mmodulo == 'LIBTABPAG':
            if ver_nivel(mmodulo, 'LIBERACAO DE TABELA DE CONDICAO PAGAMENTO DifERENTE', '15', arq_usu[2], 1,
                         maut_oper):
                mok = '*'

        elif mmodulo == 'LIB_EXPPROD':
            if ver_nivel(mmodulo, 'LIBERACAO DE ESTORNO DE EXPEDICAO DE PRODUTO NO PEDIDO', '15', arq_usu[2], 1,
                         maut_oper):
                mok = '*'
        elif mmodulo == 'LIB_N_NOTA':
            if ver_nivel(mmodulo, 'LIBERACAO DA ALTERACAO NO NUMERO NOTA FISCAL', '135', arq_usu[2], 1, maut_oper, 3):
                mok = '*'
        elif mmodulo == 'LIB_SALDOADM':
            if ver_nivel(mmodulo, 'LIBERACAO DE QUANTD.SOLICITADA MAIOR QUE A QUANTIDADE MAXIMA DA ADM', '15', arq_usu[2], 
                         1, maut_oper): 
                mok = '*'
        elif mmodulo == 'OPER_PED':
            if ver_nivel(mmodulo, 'LIBERACAO DE OPERADOR COM PEDIDOS PEDENTES', '1', arq_usu[2], 1, maut_oper):
                mok = '*'
        elif mmodulo == 'ALT_DADOS':
            if ver_nivel(mmodulo, 'LIBERACAO P/ALTERACAO NA ENTRADA DE MERCADORIA', '1', arq_usu[2], 1, maut_oper):
                mok = '*'

        elif mmodulo == 'LIB_DESC':
            if ver_nivel(mmodulo, 'LIBERACAO DE DESCONTO A MAIOR NO PRECO DE VENDA PRODUTO', '15', arq_usu[2], 1,
                                  maut_oper):
                mok = '*'
        elif mmodulo == 'LIBDESC_PED':
            if ver_nivel(mmodulo, 'LIBERACAO DE DESCONTO A MAIOR DO QUE O MAXIMO PERMITIDO', '15', arq_usu[2], 1,
                                  maut_oper):
                mok = '*'
        elif mmodulo == 'LIB_AJUST':
            if ver_nivel(mmodulo, 'LIBERACAO DE AJUSTE DE SALDO DOS PRODUTOS', '1', arq_usu[2], 1, maut_oper):
                mok = '*'
        elif mmodulo == 'LIBSLDNF':
                if ver_nivel(mmodulo, 'LIBERACAO DE SALDO A MENOR NA NOTA FISCAL', '15', arq_usu[2], 1, maut_oper):
                    mok = '*'
        elif mmodulo == 'LIB_ALTSENHA':
            if ver_nivel(mmodulo, 'LIBERACAO P/ALTERAR A SENHA', '1', arq_usu[2], 1, maut_oper): 
                mok = '*'
        elif mmodulo == 'LIB_AMB':
            if ver_nivel(mmodulo, 'LIBERACAO DE AMBIENTE NAO AUTORIZADO', '1', arq_usu[2], 1, maut_oper):
                mok = '*'
        elif mmodulo == 'LIB_DATA_ENT':
            if ver_nivel(mmodulo, 'LIBERACAO DA DATA DE ENTRADA DO SISTEMA', '1', arq_usu[2], 1, maut_oper):
                mok = '*'
        elif mmodulo == 'DESC_CX':
            if ver_nivel(mmodulo, 'LIBERACAO DE DESCONTO NO RECEBIMENTO DO PEDIDO (CAIXA)', '1', arq_usu[2], 1,
                                  maut_oper):
                mok = '*'
                # mn_ped = mnum_ped
        elif mmodulo == 'LIB_ALTSLDPED':
            if ver_nivel(mmodulo, 'LIBERACAO DA QUANTIDADE NA ALTERACAO DO PEDIDO IMPRESSO', '1', arq_usu[2], 1,
                                  maut_oper):
                mok = '*'
                # mn_ped = mnum_ped

        elif mmodulo == 'LIB_PED_LIB':
            if ver_nivel(mmodulo, 'LIBERACAO DE PEDIDO JA LIBERADOR PELO FINANCEIRO', '1', arq_usu[2], 1, maut_oper):
                mok = '*'
                # mn_ped = mnum_ped

        elif mmodulo == 'PRZ_REC':
            if ver_nivel(mmodulo, 'LIBERACAO DE PRAZO MAIOR QUE ESTIPULADO NO PEDIDO', '1', arq_usu[2], 1, maut_oper):
                mok = '*'
                # mn_ped = mnum_ped
                # mc_cli = mnum_cli

        elif mmodulo == 'LIB_DEV':
            if ver_nivel(mmodulo, 'LIBERACAO DE CLIENTE DEVEDOR, CHQ.S/FUNDO OU LIMITE ESTOURADO', '1', arq_usu[2], 1,
                                  maut_oper):
                mok = '*'
                # mc_cli = mnum_cli

        elif mmodulo == 'LIB_TAX':
            if ver_nivel(mmodulo, 'LIBERACAO DA TAXA DE ACRESCIMO NO PEDIDO', '1', arq_usu[2], 1, maut_oper):
                mok = '*'
                # mc_cli = mnum_cli

        elif mmodulo == 'LIB_PRZ':
            if ver_nivel(mmodulo, 'LIBERACAO DE PRAZO A MAIOR QUE O PERMITIDO', '1', arq_usu[2], 1, maut_oper):
                mok = '*'
                # mc_cli = mnum_cli

        elif mmodulo == 'CHQ_DEV':
            if ver_nivel(mmodulo, 'LIBERACAO DE CLIENTE COM *** CHEQUE SEM FUNDOS ***', '1', arq_usu[2], 1, maut_oper):
                mok = '*'
                # mc_cli = mnum_cli

        elif mmodulo == 'LIMIT_EST':
            if ver_nivel(mmodulo, 'LIBERACAO DE CLIENTE COM *** LIMITE ESTOURADO ***', '1', arq_usu[2], 1, maut_oper):
                mok = '*'
                # mc_cli = mnum_cli

        elif mmodulo == 'LIB_RECE':
            if ver_nivel(mmodulo, 'LIBERACAO DE SALDO A RECEBER POR CONTA', '1', arq_usu[2], 1, maut_oper):
                mok = '*'

        elif mmodulo == 'LIB_ORCA':
            if ver_nivel(mmodulo, 'LIBERACAO DE ORCAMENTO PRECO CUSTO', '1', arq_usu[2], 1, maut_oper):
                mok = '*'

        elif mmodulo == 'LIB_INSC':
            if ver_nivel(mmodulo, 'LIBERACAO DE INSCRICAO ESTADUAL', '1', arq_usu[2], 1, maut_oper):
                mok = '*'

        elif mmodulo == 'LIBCLIVEN':
            if ver_nivel(mmodulo, 'LIBERACAO DE VENDEDOR DifERENTE DO VENDEDOR RESP.PELO CLIENTE', '1', arq_usu[2], 1,
                                  maut_oper):
                mok = '*'

        elif mmodulo == 'EST_PEDEXP':
            if ver_nivel(mmodulo, 'ESTORNO DE PEDIDO EXPEDIDO', '1', arq_usu[2], 1, maut_oper):
                mok = '*'

        elif mmodulo == 'LIB_PED':
            if ver_nivel(mmodulo, 'LIBERAR OU CANCELAR PEDIDOS', '1', arq_usu[2], 1, maut_oper):
                mok = '*'
                # mn_ped = mnum_ped

        elif mmodulo == 'LIB_PED_VLR':
            if ver_nivel(mmodulo, 'LIBERAR VALOR MAIOR DO QUE O PEDIDO', '1', arq_usu[2], 1, maut_oper):
                mok = '*'
                # mn_ped = mnum_ped

        elif mmodulo == 'LIB_2VIAPED':
            if ver_nivel(mmodulo, 'LIBERAR 2a.VIA PEDIDO JA EMITIDO NOTA FISCAL', '1', arq_usu[2], 1, maut_oper):
                mok = '*'

        elif mmodulo == 'SAC101EXC':
            if ver_nivel(mmodulo, 'EXCLUSAO DE SUB-GRUPO', '1', arq_usu[2], 1, maut_oper):
                mok = '*'

        elif mmodulo == 'SAC10EXC':
            if ver_nivel(mmodulo, 'EXCLUSAO DE GRUPO', '1', arq_usu[2], 1, maut_oper):
                mok = '*'

        elif mmodulo == 'BALSLSAIDA':
            if ver_nivel(mmodulo, 'BALANCO ** CORRECAO DE SALDO (SAIDA) **', '1', arq_usu[2], 1, maut_oper):
                mok = '*'

        elif mmodulo == 'FORMPAGPED':
            if ver_nivel(mmodulo, 'LIBERACAO DA FORMA DE PAG. NA ALTERCAO DO PEDIDO (AV -> AP)', '1', arq_usu[2], 1,
                                  maut_oper):
                mok = '*'
                # mn_ped = mnum_ped

        elif mmodulo == 'LIB_FORMA_PG':
            if ver_nivel(mmodulo, 'LIBERA FORMA DE PAGAMENTO NO RECEBIMENTO DE AVISTA P/APRAZO', '1', arq_usu[2], 1,
                                  maut_oper):
                mok = '*'
                # mc_cli = mnum_cli
                # mn_ped = mnum_ped

        elif mmodulo == 'Sair_REC':
            if ver_nivel(mmodulo, 'LIBERA PARA Sair O RECEBIMENTO DO PEDIDO', '15', arq_usu[2], 1, maut_oper):
                mok = '*'
                # mc_cli = mnum_cli
                # mn_ped = mnum_ped

        elif mmodulo == 'LIB_CONDPAG':
            if ver_nivel(mmodulo, 'LIBERACAO PARA ALTERAR A CONDICAO DE PAGAMENTO PRE FIXADA DO CLIENTE', '15', arq_usu[2], 1,
                                  maut_oper):
                mok = '*'
                # mc_cli = mnum_cli

        elif mmodulo == 'LIMP_MOV':
            if ver_nivel(mmodulo, 'LIBERACAO PARA LIMPEZA DO ARQUIVO MOVIMENTO E INTEGRIDADE', '1', arq_usu[2], 1,
                                  maut_oper):
                mok = '*'

        elif mmodulo == 'LIB_REC_ENTE':
            if ver_nivel(mmodulo, 'LIBERACAO PARA 2a.VIA DO RECIBO DE ENTREGA', '1', arq_usu[2], 1, maut_oper):
                mok = '*'

        elif mmodulo == 'LIB_ATU_PRECO':
            if ver_nivel(mmodulo, 'LIBERACAO DE ATUALIZACAO DE PRECOS (ENTRADA DE MERCADORIA)', '15', arq_usu[2], 1,
                                  maut_oper):
                mok = '*'

        elif mmodulo == 'CAN_CUPOM':
            if ver_nivel(mmodulo, 'LIBERACAO DE CANCELAMENTO DE CUPOM FISCAL', '15', arq_usu[2], 1, maut_oper):
                mok = '*'

        elif mmodulo == 'EXCPRDMOV':
            if ver_nivel(mmodulo, 'AUTORIZACAO PARA EXCLUSAO DE PRODUTO COM MOVIMENTO', '1', arq_usu[2], 1, maut_oper):
                mok = '*'

        elif mmodulo == 'LIB_MULTAJURO':
            if ver_nivel(mmodulo, 'AUTORIZACAO PARA LIBERAR JUROS E MULTA A RECEBER', '1', arq_usu[2], 1, maut_oper):
                mok = '*'

        if mok == '*':
            print("mok == '*'")
            mautoriza = '   '
            mautoriza = mcod_op
            return True
    else:
        print('senha errada')
        return False


# sr_getconnection(): exec(
#     'INSERT INTO saclog (data_sis,data,hora,tipo,documento,cod_cli,aut_oper,cod_oper,modulo,descri,cod_aut,terminal' +;
# ',cod_prod,SR_DELETED )' +;
# ' VALUES (' +;
# sr_cdbvalue(DATE()) + ',' +; // 1
# sr_cdbvalue(mdata_sis) + ',' +; // 2
# sr_cdbvalue(TIME()) + ',' +; // 3
# sr_cdbvalue('AUTORIZACA') + ',' +; // 4
# sr_cdbvalue(mn_ped) + ',' +; // 5
# sr_cdbvalue(if mnum_cli=NIL, 0, mnum_cli)) + ',' +; // 6
# sr_cdbvalue(maut_oper) + ',' +; // 7
# sr_cdbvalue(cod_operado) + ',' +; // 8
# sr_cdbvalue(if mdl=NIL, '', mdl)) + ',' +; // 9
# sr_cdbvalue(
#     SUBSTR(if LEN(mcons_nivel) > 0, ALLTRIM(mcons_nivel[1, 2]), '') + if mnum_pedido=NIL, '', ' ' + mnum_pedido), 1,
#            60)) + ',' +; // 10
# sr_cdbvalue(mcodaux) + ',' +; // 11
# sr_cdbvalue(LEFT(NETNAME(), 15)) + ',' +; // 12
# sr_cdbvalue(if mnum_prod=NIL, '', mnum_prod)) + ',' +; // 13
# sr_cdbvalue(' ') + ')',, .f.)
# 
# sr_getconnection(): exec("COMMIT",, .f.)
# ** ** ** ** ** ** ** ** ** ** *
# SELE(msel_sen);
# if mord_sen > 0, ORDSETFOCUS(mord_sen), )
# ** ** ** ** ** ** ** ** ** ** *
# wvw_lclosewindow()
# RETURN.T.
# 
# atencao('Cod. Operador:' + maut_oper + ' - Operador nao Autorizada !!!')
# mcont + +
# LOOP
# ELSE
# atencao('Senha nao Autorizada 2 !!!')
# mcont + +
# LOOP


def aut_sen(mensagem, mdl, mnum_cli, mnum_prod, mamb, mnum_pedido):
    global ambiente
    global mmodulo
    ambiente = mamb
    mmodulo = mdl
    # tela.setWindowFlag(Qt.WindowCloseButtonHint, False)
    tela.setWindowTitle(f'MODULO DE LIBERACAO P/SENHA <<Modulo: {mdl} >>         {SISTEMA}  Versao: {VERSAO}')
    hti_global.conexao_cursor.execute(f"SELECT * FROM sacconf WHERE TRIM(modulo) = '{mdl.strip()}'")
    arq_nivel = hti_global.conexao_cursor.fetchone()
    tela.statusBar().showMessage('Digite a SENHA ou SOLICITAR AUTORIZACAO')
    # print(f'Autorizado: {m_autorizado}')
    tela.maut_senha.setFocus()
    # if not m_autorizado == '':
    #     print(f'Autorizado: {m_autorizado}')
    #     if m_autorizado:
    #         print('sim')
    #         return True
    #     else:
    #         print('nao')
    #         return False

    if arq_nivel is not None and arq_nivel[2][0] == '0':
        return True

    hti_global.conexao_cursor.execute(f"SELECT scod_op,snome FROM insopera")
    arq_insopera = hti_global.conexao_cursor.fetchall()
    hti_global.conexao_bd.commit()

    for ret_insopera in arq_insopera:
        item = f'{ret_insopera[0]} - {ret_insopera[1]}'.strip('(),')
        tela.comboBox.addItem(item)

    text_browser = tela.findChild(QtWidgets.QTextBrowser, "textBrowser")
    text_browser.setText(f'{mensagem}')
    lb_modulo = tela.findChild(QtWidgets.QLabel, "modulo")
    lb_modulo.setText(f'Modulo: {mdl}')

    tela.solicitacao_nao.setChecked(True)
    # Altera o texto do textBrowser
    tela.enviar_solicitacao.clicked.connect(autorizar_senha)
    # print('autorizar_senha')
    tela.sair.clicked.connect(sair_programa)
    tela.show()
    app.exec()


if tela.solicitacao_sim.isChecked():
    if solicita_autorizacao(mcod_op, '', '', '', ambiente):
        print('Aut: True')
        hti_global.m_autorizado = True
    else:
        print('Aut: False')
        hti_global.m_autorizado = False

    tela.solicitacao_nao.setChecked(True)
    tela.maut_senha.setFocus()

    aut_sen('', '', '', '', '', '')


if __name__ == '__main__':
    nivel_acess = hti_global.geral_nivel_usuario
    # resposta = aut_sen('INCLUSAO DE FORNECEDOR/CONTA APAGAR', 'SAC140', '', '', '', '')
    # print(resposta)
    # if resposta:
    #     print('LIBEROU')
    # else:
    #     print('NEGATIVO')

    # presente1 = False
    # presente2 = False
    # if presente1 or presente2:
    #     print("if not presente1 and not presente2 or hti_global.geral_cod_usuario == '999'")

    aut_sen('INCLUSAO DE FORNECEDOR/CONTA APAGAR', 'SAC140', '', '', '', '')
    print(f'Autorizado: {hti_global.m_autorizado}')
    if hti_global.m_autorizado:
        print('LIBEROU')
    else:
        print('NEGATIVO')

