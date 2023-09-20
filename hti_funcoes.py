import fdb
import hti_global


def conexao_banco():
    # Conecte-se ao banco de dados
    print('conexao')
    hti_global.conexao_bd = fdb.connect(dsn=hti_global.host, user='SYSDBA', password='masterkey')
    hti_global.conexao_cursor = hti_global.conexao_bd.cursor()
    return


def verificar_conexao():
    conexao_banco()
    hti_global.conexao_cursor.execute("SELECT rdb$get_context('SYSTEM', 'ENGINE_VERSION') FROM rdb$database;")
    resultado = hti_global.conexao_cursor.fetchone()
    if resultado:
        print(f"Conexão estabelecida com sucesso! Versão do Firebird: {resultado[0]}")
    else:
        print("Não foi possível recuperar a versão do Firebird.")


def ver_nivel(mmodulo, mdescri, mnivel, mconf_nivel, mamb, mopera):
    from autorizacao_senha import aut_sen
    # print(mmodulo)
    hti_global.conexao_cursor.execute(f"SELECT * FROM sacconf WHERE TRIM(modulo) = '{mmodulo.strip()}'")
    arq_conf = hti_global.conexao_cursor.fetchone()
    # hti_global.conexao_db.commit()

    if arq_conf is not None and arq_conf[2][0] == '0':
        print('achou1')
        return True
    if arq_conf is not None:
        sql = "UPDATE sacconf SET descri = ? WHERE modulo = ?"
        values = (mdescri, mmodulo)
        hti_global.conexao_cursor.execute(sql, values)
        hti_global.conexao_bd.commit()
        print(f'opera: {mopera} - global: {hti_global.geral_cod_usuario}')
        if mopera == '999' or hti_global.geral_cod_usuario == '999':
            print('achou2')
            return True

        letra1 = mconf_nivel[0]
        letra2 = mconf_nivel[1]
        presente1 = False
        presente2 = False
        if not letra1 == ' ':
            presente1 = letra1 in arq_conf[2]

        if not letra2 == ' ':
            presente2 = letra2 in arq_conf[2]

        # presente2 = letra2 in arq_conf[2]
        # print(f'letra1 {letra1}')
        # print(f'letra2 {letra2}')
        # print(f'presente1 {presente1}')
        # print(f'presente2 {presente2}')

        if not presente1 and not presente2:
            if mamb is None:
                print(f'{mdescri}  - ACESSO NAO AUTORIZADO PARA ESTE AMBIENTE - NIVEL: {mconf_nivel}')
                # return False
                aut_sen(f'{mdescri} - Senha de Liberacao do Ambiente:', 'LIB_AMB', '', '', '', 'AMBIE')
                if hti_global.m_autorizado:
                    print('LIBEROU AMB')
                    return True
                else:
                    print('NEGATIVO AMB')
                    return False
            else:
                aut_sen(f'{mdescri} - Senha de Liberacao do Ambiente:', 'LIB_AMB', '', '', '', 'AMBIE')
                if hti_global.m_autorizado:
                    print('LIBEROU')
                    hti_global.m_autorizado = False
                    return True
                else:
                    print('NEGATIVO')
                    return False

                # print('LIBEROU')
                # return True
                # print(f'{mdescri}  - ACESSO NAO AUTORIZADO PARA ESTE AMBIENTE - Niveis do Usuario: {mconf_nivel} -
                # Niveis Autorizado: {arq_conf[2]}')
                # return False
        else:
            print('achou4')
            return True
    else:
        print('achou5')
        sql = "INSERT INTO sacconf SET ( modulo, descri, nivel, SR_DELETED) VALUES (?, ?, ?, ?)"
        hti_global.conexao_cursor.execute(sql, (mmodulo, mdescri, mnivel, ' '))
        hti_global.conexao_db.commit()
        return False


def criar_tabelas():
    import fdb

    def tabela_existe(nome_tabela):
        try:
            hti_global.conexao_cursor.execute(
                f"SELECT RDB$RELATION_NAME FROM RDB$RELATIONS WHERE RDB$RELATION_NAME='{nome_tabela.upper()}'")
            return True
        except fdb.fbcore.DatabaseError:
            return False

    if not tabela_existe('SACMERC1'):
        hti_global.conexao_cursor.execute(
            "CREATE TABLE sachelio(empresa char(3), cod_barr char(14), cod_barr1 char(14), descri1 char(50), "
            "app_imagem varchar(100), ref char(13), gru_sub char(5), cod_merc char(5) not null, "
            "merc char(40), tipo_merc char(1), balanca char(1), data_atu date, "
            "data_cad date, unidade char(3), especie char(4), peso_liq decimal(8, 3), peso  decimal(8, 3))")
        hti_global.conexao_db.commit()
        print('A tabela criada com sucesso no banco de dados.')
        return True

# FUNCAO PARA DES-CRIPTOGRAFA


def dcripto(mexp):
    mletra = []
    maux = []
    msenha = ''

    for i in range(len(mexp)):
        if not mexp[i] == ' ':
            mletra.append(mexp[i])

    if not mletra:
        return None

    for i in range(len(mletra)):
        # print(mletra[i])
        if mletra[i] == chr(189):
            maux.append('A')
        elif mletra[i] == chr(184):
            maux.append('B')
        elif mletra[i] == chr(154):
            maux.append('C')
        elif mletra[i] == chr(181):
            maux.append('D')
        elif mletra[i] == chr(228):
            maux.append('E')
        elif mletra[i] == chr(230):
            maux.append('F')
        elif mletra[i] == chr(232):
            maux.append('G')
        elif mletra[i] == chr(218):
            maux.append('H')
        elif mletra[i] == chr(204):
            maux.append('I')
        elif mletra[i] == chr(236):
            maux.append('J')
        elif mletra[i] == chr(231):
            maux.append('K')
        elif mletra[i] == chr(245):
            maux.append('L')
        elif mletra[i] == chr(225):
            maux.append('M')
        elif mletra[i] == chr(237):
            maux.append('N')
        elif mletra[i] == chr(224):
            maux.append('O')
        elif mletra[i] == chr(208):
            maux.append('P')
        elif mletra[i] == chr(166):
            maux.append('Q')
        elif mletra[i] == chr(168):
            maux.append('R')
        elif mletra[i] == chr(172):
            maux.append('S')
        elif mletra[i] == chr(157):
            maux.append('T')
        elif mletra[i] == chr(140):
            maux.append('U')
        elif mletra[i] == chr(174):
            maux.append('W')
        elif mletra[i] == chr(20):
            maux.append('V')
        elif mletra[i] == chr(223):
            maux.append('X')
        elif mletra[i] == chr(239):
            maux.append('Y')
        elif mletra[i] == chr(235):
            maux.append('Z')
        elif mletra[i] == chr(251):
            maux.append('0')
        elif mletra[i] == chr(253):
            maux.append('1')
        elif mletra[i] == chr(252):
            maux.append('2')
        elif mletra[i] == chr(248):
            maux.append('3')
        elif mletra[i] == chr(216):
            maux.append('4')
        elif mletra[i] == chr(200):
            maux.append('5')
        elif mletra[i] == chr(136):
            maux.append('6')
        elif mletra[i] == chr(127):
            maux.append('7')
        elif mletra[i] == chr(21):
            maux.append('8')
        elif mletra[i] == chr(23):
            maux.append('9')
        elif mletra[i] == '0':
            maux.append(' ')
        elif mletra[i] == '1':
            maux.append('*')
        elif mletra[i] == '2':
            maux.append('-')
        elif mletra[i] == '3':
            maux.append('/')
        elif mletra[i] == '4':
            maux.append('.')
        elif mletra[i] == '5':
            maux.append(',')
        elif mletra[i] == 'A':
            maux.append('"')
        elif mletra[i] == '6':
            maux.append("'")
        elif mletra[i] == '7':
            maux.append('(')
        elif mletra[i] == '8':
            maux.append(')')
        elif mletra[i] == '9':
            maux.append('=')
        elif mletra[i] == 'B':
            maux.append('%')
        elif mletra[i] == 'C':
            maux.append('*')
        elif mletra[i] == 'D':
            maux.append('+')
        elif mletra[i] == 'E':
            maux.append('@')
        elif mletra[i] == 'F':
            maux.append(']')
        elif mletra[i] == 'G':
            maux.append('[')
        elif mletra[i] == 'I':
            maux.append('{')
        elif mletra[i] == 'J':
            maux.append('}')
        elif mletra[i] == 'K':
            maux.append('&')
        elif mletra[i] == 'L':
            maux.append('#')
        elif mletra[i] == 'M':
            maux.append('!')
        elif mletra[i] == 'N':
            maux.append(':')
        elif mletra[i] == 'O':
            maux.append(';')
        elif mletra[i] == 'P':
            maux.append('?')
        elif mletra[i] == 'Q':
            maux.append('|')
        elif mletra[i] == 'R':
            maux.append('\\')
        elif mletra[i] == 'S':
            maux.append('?')
        elif mletra[i] == '?':
            maux.append('?')
        elif mletra[i] == 'U':
            maux.append('?')
        elif mletra[i] == 'V':
            maux.append('?')
        elif mletra[i] == 'X':
            maux.append('?')
        elif mletra[i] == 'Y':
            maux.append('?')
        elif mletra[i] == 'Z':
            maux.append('?')
        elif mletra[i] == 'A':
            maux.append('?')
        elif mletra[i] == 'b':
            maux.append('?')
        elif mletra[i] == 'c':
            maux.append('?')
        elif mletra[i] == 'd':
            maux.append(None)
        else:
            maux.append('_')

    # print(maux)

    if len(mexp) == 0:
        msenha = mexp
    elif len(mexp) == 1:
        msenha = maux[1]
    else:
        msenha = maux[1] + maux[0]

    for i in range(2, len(maux)):
        msenha += maux[i]
    return msenha

# FUNCAO PARA CRIPTOGRAFA


def cripto(mexp):
    mletra = []
    maux = []
    msenha = ''
    mexp = mexp.upper()
    if len(mexp) > 10:
        print('Senha Invalida !!!')
        return

    for i in range(len(mexp)):
        if not mexp[i] == ' ':
            mletra.append(mexp[i])

    for i in range(len(mletra)):
        if mletra[i] == 'A':
                maux.append(chr(189))
        elif mletra[i] == 'B':
                maux.append(chr(184))
        elif mletra[i] == 'C':
                maux.append(chr(154))
        elif mletra[i] == 'D':
                maux.append(chr(181))
        elif mletra[i] == 'E':
                maux.append(chr(228))
        elif mletra[i] == 'F':
                maux.append(chr(230))
        elif mletra[i] == 'G':
                maux.append(chr(232))
        elif mletra[i] == 'H':
                maux.append(chr(218))
        elif mletra[i] == 'I':
                maux.append(chr(204))
        elif mletra[i] == 'J':
                maux.append(chr(236))
        elif mletra[i] == 'K':
                maux.append(chr(231))
        elif mletra[i] == 'L':
                maux.append(chr(245))
        elif mletra[i] == 'M':
                maux.append(chr(225))
        elif mletra[i] == 'N':
                maux.append(chr(237))
        elif mletra[i] == 'O':
                maux.append(chr(224))
        elif mletra[i] == 'P':
                maux.append(chr(208))
        elif mletra[i] == 'Q':
                maux.append(chr(166))
        elif mletra[i] == 'R':
                maux.append(chr(168))
        elif mletra[i] == 'S':
                maux.append(chr(172))
        elif mletra[i] == 'T':
                maux.append(chr(157))
        elif mletra[i] == 'U':
                maux.append(chr(140))
        elif mletra[i] == 'W':
                maux.append(chr(174))
        elif mletra[i] == 'V':
                maux.append(chr(20))
        elif mletra[i] == 'X':
                maux.append(chr(223))
        elif mletra[i] == 'Y':
                maux.append(chr(239))
        elif mletra[i] == 'Z':
                maux.append(chr(235))
        elif mletra[i] == '0':
                maux.append(chr(251))
        elif mletra[i] == '1':
                maux.append(chr(253))
        elif mletra[i] == '2':
                maux.append(chr(252))
        elif mletra[i] == '3':
                maux.append(chr(248))
        elif mletra[i] == '4':
                maux.append(chr(216))
        elif mletra[i] == '5':
                maux.append(chr(200))
        elif mletra[i] == '6':
                maux.append(chr(136))
        elif mletra[i] == '7':
                maux.append(chr(127))
        elif mletra[i] == '8':
                maux.append(chr(21))
        elif mletra[i] == '9':
                maux.append(chr(23))     
        elif mletra[i] == ' ':
                maux.append('0')     
        elif mletra[i] == '*':
                maux.append('1')     
        elif mletra[i] == '-':
                maux.append('2')     
        elif mletra[i] == '/':
                maux.append('3')     
        elif mletra[i] == '.':
                maux.append('4')     
        elif mletra[i] == ',':
                maux.append('5')     
        elif mletra[i] == '"':
                maux.append('A')     
        elif mletra[i] == "'":
                maux.append('6')     
        elif mletra[i] == '(':
                maux.append('7')     
        elif mletra[i] == ')':
                maux.append('8')     
        elif mletra[i] == '=':
                maux.append('9')     
        elif mletra[i] == '%':
                maux.append('B')     
        elif mletra[i] == '*':
                maux.append('C')     
        elif mletra[i] == '+':
                maux.append('D')     
        elif mletra[i] == '@':
                maux.append('E')     
        elif mletra[i] == ']':
                maux.append('F')     
        elif mletra[i] == '[':
                maux.append('G')     
        elif mletra[i] == '{':
                maux.append('I')     
        elif mletra[i] == '}':
                maux.append('J')     
        elif mletra[i] == '&':
                maux.append('K')     
        elif mletra[i] == '#':
                maux.append('L')     
        elif mletra[i] == '!':
                maux.append('M')     
        elif mletra[i] == ':':
                maux.append('N')     
        elif mletra[i] == ';':
                maux.append('O')     
        elif mletra[i] == '?':
                maux.append('P')     
        elif mletra[i] == '|':
                maux.append('Q')     
        elif mletra[i] == '\\':
                maux.append('R')     
        elif mletra[i] == '?':
                maux.append('S')     
        elif mletra[i] == '?':
                maux.append('T')     
        elif mletra[i] == '?':
                maux.append('U')     
        elif mletra[i] == '?':
                maux.append('V')     
        elif mletra[i] == '?':
                maux.append('X')     
        elif mletra[i] == '?':
                maux.append('Y')     
        elif mletra[i] == '?':
                maux.append('Z')     
        elif mletra[i] == '?':
                maux.append('a')     
        elif mletra[i] == '?':
                maux.append('b')     
        elif mletra[i] == '?':
                maux.append('c')     
        elif mletra[i] == NIL:
                maux.append('d')     
        else:
                maux.append('_')

    if len(mexp) == 0:
        msenha = ''
    elif len(mexp) == 1:
        msenha = maux[1]
    else:
        msenha = maux[1] + maux[0]
        for i in range(2, len(maux)):
            msenha += maux[i]
        return msenha


if __name__ == '__main__':
    # CONEXAO COM O BANCO DE DADOS FIREBIRD
    # lendo o arquivo sisconfig.ini
    # config = configparser.ConfigParser()
    # config.read('sisconfig.ini')
    # host = config.get('banco', 'host')
    # # Conecte-se ao banco de dados
    # hti_global.conexao_db = fdb.connect(dsn=host, user='SYSDBA', password='masterkey')
    # # Crie o hti_global.cursor
    # hti_global.cursor = hti_global.conexao_db.hti_global.cursor()
    # # listar_dados()
    nivel_acess = hti_global.geral_nivel_usuario
    mprg = 'SAC140'
    resposta = ver_nivel(mprg, 'INCLUSAO DE forNECEDOR/CONTA APAGAR', '15', nivel_acess, ' ', '  ')
    if not resposta:
        print('ok')

    # print(dcripto('ûüÈ'))