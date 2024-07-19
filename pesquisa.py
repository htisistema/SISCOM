import os
from PyQt6 import uic, QtWidgets, QtCore, QtGui
from hti_funcoes import conexao_banco
import hti_global as hg

# Variável global para armazenar os dados carregados do banco de dados
dados_lidos = []


# Função para carregar todos os dados do banco de dados na inicialização
def carregar_dados():
    global dados_lidos
    if hg.mtipo_temrinal == "L":
        valor_aprazo_calculado = "pr_venda * ((varejo / 100) + 1)"
    else:
        valor_aprazo_calculado = (
            "iif(pr_venda1 > 0, pr_venda1, pr_venda * ((varejo / 100) + 1))"
        )

    hg.conexao_cursor.execute(
        f"SELECT CAST(cod_merc as char(5)) as cod_merc, COALESCE(merc, ' ') as merc, "
        f"REPLACE(CAST(saldo_mer AS DECIMAL(12, 2)), '.', ',') as saldomer, "
        f"REPLACE(CAST(pr_venda AS DECIMAL(12, 2)), '.', ',') as prvenda, "
        f"REPLACE(CAST({valor_aprazo_calculado} AS DECIMAL(12, 2)), '.', ','), "
        f"COALESCE(unidade, ' '), "
        f"COALESCE(cod_barr, ' '), COALESCE(ref, ' ') FROM sacmerc "
        f"ORDER BY merc"
    )
    dados_lidos = hg.conexao_cursor.fetchall()
    hg.conexao_bd.commit()


# Função para pesquisar nos dados carregados
def pesquisa_prod():
    global dados_lidos
    nome_buscar = tela.pesquisa.text().strip().upper()
    print(nome_buscar[0:1], nome_buscar[1:])

    resultados = []

    if nome_buscar.startswith("*"):
        nome_buscar = nome_buscar[1:]
        resultados = [dado for dado in dados_lidos if nome_buscar in dado[1]]
    else:
        resultados = [dado for dado in dados_lidos if dado[1].startswith(nome_buscar)]

    # Atualize a interface do usuário com os dados filtrados
    listar_produto(resultados)


# Função para listar os produtos na interface do usuário
def listar_produto(resultados):
    tela.listView.clear()  # Limpa a listView (ou outro widget que você esteja usando)
    for resultado in resultados:
        item = QtWidgets.QListWidgetItem(f"{resultado[0]} - {resultado[1]}")
        tela.listView.addItem(item)


# Inicialize o aplicativo
app = QtWidgets.QApplication([])
app.setStyleSheet(hg.style_sheet)

tela = uic.loadUi(f"{hg.c_ui}\\menu.ui")
icon = QtGui.QIcon(f"{hg.c_imagem}\\htiico.ico")
tela.setWindowIcon(icon)

# Carregar dados na inicialização
conexao_banco()
carregar_dados()

# Conectar a função de pesquisa ao evento textChanged do campo de pesquisa
tela.pesquisa.textChanged.connect(pesquisa_prod)

# Mostrar a tela principal
tela.show()
app.exec()

# Fechar conexões e encerrar o aplicativo
hg.conexao_cursor.close()
tela.close()
hg.conexao_bd.close()
app.quit()
