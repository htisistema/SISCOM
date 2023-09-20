import configparser
from PyQt6 import QtWidgets

geral_cod_usuario = '999'
geral_nivel_usuario = '15 '
VERSAO_ANTIGA = 'v23.04.13'
m_autorizado = False
config = configparser.ConfigParser()
config.read('sisconfig.ini')
c_imagem = config.get('caminho_imagem', 'caminho_img')
c_ui = config.get('caminho_ui', 'caminho_ui')
mtipo_temrinal = config.get('tipo_terminal', 'tipo_term')
mtp_tela = config.get('tipo_tela', 'tp_tela')
host = config.get('banco', 'host')
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
    border-radius: 8px;
}
QLabel {
    border-radius: 8px;
    font: 800 10pt "Arial";
    border-color: rgb(162, 162, 162);
    background-color: rgb(164, 185, 255);
    border-style: Outset;
    border-width: 2px;
}
QLineEdit {
    border-radius: 8px;
    font: 800 10pt "Arial";
    background-color: rgb(255, 255, 255);
    border-color: rgb(132, 168, 163);
    border-style: Outset;
    border-width: 2px;

}
QDateEdit {
    border-radius: 8px;
    font: 800 10pt "Arial";
    background-color: rgb(255, 255, 255);
    border-color: rgb(132, 168, 163);
    border-style: Outset;
    border-width: 2px;

}

QPushButton {
    font: 800 10pt "Arial";
    background-color: rgb(164, 185, 255);
    border-color: rgb(132, 168, 163);
    border-style: Outset;
    border-width: 2px;
    border-radius: 8px;
}
QPushButton:pressed {
    background-color: rgb(255, 255, 255);
    border-color: blue;
    border-style: Outset;
    border-width: 2px;
    border-radius: 8px;
}

QComboBox {
    border-radius: 8px;
    font: 800 10pt "Arial";
    background-color: rgb(255, 255, 255);
    border-color: rgb(132, 168, 163);
    border-style: Outset;
    border-width: 2px;
}
QRadioButton {
    border-radius: 8px;
    font: 800 10pt "Arial";
    border-color: rgb(162, 162, 162);
    background-color: rgb(164, 185, 255);
    border-style: Outset;
    border-width: 2px;

}
QDoubleSpinBox {
    border-radius: 8px;
    font: 800 10pt "Arial";
    background-color: rgb(255, 255, 255);
    border-color: rgb(132, 168, 163);
    border-style: Outset;
    border-width: 2px;
}
QMainWindow {
    border-radius: 8px;
    font: 800 10pt "Arial";
    border-color: rgb(162, 162, 162);
    background-color: rgb(190, 216, 255);
    border-style: Outset;
    border-width: 2px;
}
QGroupBox {
    border-radius: 8px;
    font: 800 10pt "Arial";
    border-color: rgb(162, 162, 162);
    background-color: rgb(190, 216, 255);
    border-style: Outset;
    border-width: 2px;
}
MainWindow {
    border-radius: 8px;
    font: 800 10pt "Arial";
    border-color: rgb(162, 162, 162);
    background-color: rgb(190, 216, 255);
    border-style: Outset;
    border-width: 2px;
}

QTableWidget {
    border-radius: 8px;
    font: 800 10pt "Arial";
    background-color: rgb(255, 255, 255);
    border-color: rgb(132, 168, 163);
    border-style: Outset;
    border-width: 2px;
}

"""

if __name__ == '__main__':
    conexao_cursor.close()
    conexao_bd.close()

