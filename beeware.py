# Para criar uma tela de login em uma aplicação móvel utilizando o Beeware e acessando o Firebird com uma tabela que
# contém o ID e senha dos usuários, você pode utilizar a biblioteca FDB para se conectar ao banco de dados.
# A seguir, está um exemplo de código para criar uma tela de login com campos de entrada de usuário e senha:

import fdb
import toga
from toga_react_native import (
    TogaApp as App,
    Box,
    Button,
    Label,
    TextInput,
)
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class LoginWindow(App):
    def __init__(self):
        super().__init__()
        self.connection = None

    def startup(self):
        # Cria a janela de login
        self.main_window = toga.MainWindow(title=self.name)

        # Cria os campos de entrada de usuário e senha
        self.usuario_input = TextInput(placeholder='Usuário')
        self.senha_input = TextInput(placeholder='Senha', secure=True)

        # Cria um botão para realizar o login
        self.botao_login = Button('Login', on_press=self.realiza_login)

        # Adiciona os campos e o botão a uma caixa vertical
        caixa = Box(
            children=[
                Label('Entre com seu usuário e senha:'),
                self.usuario_input,
                self.senha_input,
                self.botao_login,
            ],
            style=Pack(direction=COLUMN, padding=20),
        )

        # Adiciona a caixa à janela
        self.main_window.content = caixa

        # Exibe a janela
        self.main_window.show()

    def realiza_login(self, widget):
        # Recupera o usuário e senha informados nos campos de entrada
        usuario = self.usuario_input.value
        senha = self.senha_input.value

        # Realiza a conexão com o banco de dados Firebird
        try:
            self.connection = fdb.connect(
                host='localhost',
                database='/path/to/database.fdb',
                user='username',
                password='password',
            )
        except fdb.Error as e:
            self.main_window.error_dialog('Erro', 'Não foi possível conectar ao banco de dados: ' + str(e))
            return

        # Realiza a consulta ao banco de dados para verificar as credenciais de login
        cursor = self.connection.cursor()
        cursor.execute("SELECT id FROM tabela_usuarios WHERE id = ? AND senha = ?", (usuario, senha))
        resultado = cursor.fetchone()

        # Verifica se a consulta retornou um resultado válido
        if resultado:
            self.main_window.info_dialog('Login', 'Login realizado com sucesso.')
        else:
            self.main_window.error_dialog('Login', 'Usuário ou senha inválidos.')


def main():
    return LoginWindow()


if __name__ == '__main__':
    main().main_loop()





# CRIAR AS MESAS

import toga
from toga_react_native import (
    TogaApp as App,
    Button,
    ScrollView,
    Stack,
    Text,
)
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class MesaWindow(App):
    def startup(self):
        # Cria a janela de escolha de mesa
        self.main_window = toga.MainWindow(title=self.name)

        # Define o número total de mesas
        self.total_mesas = 50

        # Cria um botão para cada mesa
        self.botoes_mesas = []
        for mesa in range(1, self.total_mesas + 1):
            self.botoes_mesas.append(Button(str(mesa), on_press=self.seleciona_mesa))

        # Adiciona os botões a uma pilha
        stack = Stack(
            children=self.botoes_mesas,
            style=Pack(direction=ROW, padding=20),
        )

        # Adiciona a pilha a uma rolagem
        scroll_view = ScrollView(
            content=stack,
        )

        # Adiciona a rolagem à janela
        self.main_window.content = scroll_view

        # Exibe a janela
        self.main_window.show()

    def seleciona_mesa(self, widget):
        # Recupera o número da mesa selecionada
        mesa_selecionada = int(widget.children[0].value)

        # Realiza alguma ação com a mesa selecionada (ex: abrir um novo pedido)

        # Exibe uma mensagem de sucesso
        self.main_window.info_dialog('Escolha de mesa', f'Mesa {mesa_selecionada} selecionada com sucesso.')


def main():
    return MesaWindow('Escolha de Mesa')


if __name__ == '__main__':
    main().main_loop()
