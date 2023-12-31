import configparser
from PyQt6 import QtWidgets

VERSAO = 'v23.04.13'
SISTEMA = '.: SISCOM :. Sistema Automacao Comercial'
SIT_TIP = 'SISCOM'
HTISISTEMA = '.: HTI Sistemas Ltda :.'
CNPJ_HTI = '24494200000106'
INSC_MUNCI = '066728339'
RAZAO_HTI = 'M. EDUARDA B. B. CINTRA'
END_HTI = 'Rua Cicero Monteiro'
MNUM_HTI = '1040'
COMP_HTI = ''
BAIRRO_HTI = 'Centro'
CIDADE_HTI = 'Tacaimbo'
UF_HTI = 'PE'
CEP_HTI = '55140000'
FONE_HTI = '993127894'


geral_cod_usuario = '999'
geral_nivel_usuario = '15 '
mcodempresa = '001'
VERSAO_ANTIGA = 'v23.04.13'
m_autorizado = False
config = configparser.ConfigParser()
config.read('sisconfig.ini')
c_usuario = config.get('caminho_usuario', 'caminho_usuario')
c_cliente = config.get('caminho_cliente', 'caminho_cliente')
c_produto = config.get('caminho_produto', 'caminho_produto')
c_imagem = config.get('caminho_imagem', 'caminho_img')
c_ui = config.get('caminho_ui', 'caminho_ui')
mtipo_temrinal = config.get('tipo_terminal', 'tipo_term')
mtp_tela = config.get('tipo_tela', 'tp_tela')
host = config.get('banco', 'host')
nome_computador = config.get('terminal', 'nome_terminal')
conexao_bd = ' '
conexao_cursor = ' '
estados = ['AC - ACRE', 'AL - ALAGOAS', 'AP - AMAPA', 'AM - AMAZONAS', 'BA - BAHIA', 'CE - CEARA',
           'DF - DISTRITO FEDERAL', 'ES - ESPIRITO SANTOS', 'EX - EXTERIOR', 'GO - GOIAS',
           'MA - MARANHAO', 'MS - MATO GROSSO SUL', 'MT - MATO GROSS', 'MG - MINAS GERAIS',
           'PA - PARA', 'PB - PARAIBA', 'PE - PERNAMBUCO', 'PI - PIAUI', 'PR - PARANA',
           'RJ - RIO DE JANEIRO', 'RN - RIO GRANDE DO NORTE', 'RS - RIO GRANDE DO SUL',
           'RR - RORAIMA', 'RO - RONDONIA', 'SC - SANTA CATARINA', 'SE - SERGIPE',
           'SP - SAO PAULO', 'TO - TOCANTINS']


# Crie uma classe para a folha de estilo CSS
style_sheet = """
QWidget {
    border-radius: 4px;
}
QLabel {
    font: 700 10pt "Segoe UI";
    border-color: rgb(162, 162, 162);
    background-color: rgb(164, 185, 255);
    border-style: Outset;
    border-width: 2px;
    border-radius: 4px;
}
QLineEdit {
    font: 700 12pt "Segoe UI";
    background-color: rgb(255, 255, 255);
    border-color: rgb(132, 168, 163);
    border-style: Outset;
    border-width: 2px;
    border-radius: 4px;

}
QDateEdit {
    font: 700 12pt "Segoe UI";
    background-color: rgb(255, 255, 255);
    border-color: rgb(132, 168, 163);
    border-style: Outset;
    border-width: 2px;
    border-radius: 4px;

}

QPushButton {
    font: 700 12pt "Segoe UI";
    background-color: rgb(164, 185, 255);
    border-color: rgb(132, 168, 163);
    border-style: Outset;
    border-width: 2px;
    border-radius: 4px;
}
QPushButton:pressed {
    background-color: rgb(255, 255, 255);
    border-color: blue;
    border-style: Outset;
    border-width: 2px;
    border-radius: 4px;
}

QComboBox {
    font: 700 12pt "Segoe UI";
    background-color: rgb(255, 255, 255);
    border-color: rgb(132, 168, 163);
    border-style: Outset;
    border-width: 2px;
    border-radius: 4px;
}
QRadioButton {
    font: 700 12pt "Segoe UI";
    border-color: rgb(162, 162, 162);
    background-color: rgb(164, 185, 255);
    border-style: Outset;
    border-width: 2px;
    border-radius: 4px;

}
QDoubleSpinBox {
    font: 700 12pt "Segoe UI";
    background-color: rgb(255, 255, 255);
    border-color: rgb(132, 168, 163);
    border-style: Outset;
    border-width: 2px;
    border-radius: 4px;
}
QMainWindow {
    font: 700 12pt "Segoe UI";
    border-color: rgb(162, 162, 162);
    background-color: rgb(190, 216, 255);
    border-style: Outset;
    border-width: 2px;
    border-radius: 4px;
}
QGroupBox {
    font: 700 12pt "Segoe UI";
    border-color: rgb(162, 162, 162);
    background-color: rgb(190, 216, 255);
    border-style: Outset;
    border-width: 2px;
    border-radius: 4px;
}
MainWindow {
    font: 700 12pt "Segoe UI";
    border-color: rgb(162, 162, 162);
    background-color: rgb(190, 216, 255);
    border-style: Outset;
    border-width: 2px;
    border-radius: 4px;
}

QTableWidget {
    font: 700 12pt "Segoe UI";
    background-color: rgb(255, 255, 255);
    border-color: rgb(132, 168, 163);
    border-style: Outset;
    border-width: 2px;
    border-radius: 4px;
}

"""

if __name__ == '__main__':
    conexao_cursor.close()
    conexao_bd.close()

