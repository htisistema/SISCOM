import configparser
import customtkinter
import fdb
# from tkinter import messagebox
import tkinter as tk
# CONEXAO COM O BANCO DE DADOS FIREBIRD
# lendo o arquivo sisconfig.ini
config = configparser.ConfigParser()
config.read('sisconfig.ini')
host = config.get('banco', 'host')
# Conecte-se ao banco de dados
con = fdb.connect(dsn=host, user='SYSDBA', password='masterkey')
# Crie o cursor
cursor = con.cursor()

cursor.execute(f"SELECT max(cod_cli) FROM saccli ")
# Recupere o resultado
result = cursor.fetchone()
print(result)
mcod_cli = int(result[0] + 1)
print(mcod_cli)

# Função para cadastrar cliente
def cadastrar_cliente():
    if not cod_cli:
        tk.messagebox.showerror('Erro', 'O campo Código do Cliente é obrigatório.')
        return
    # cursor.execute(
    #     "INSERT INTO saccli (cod_cli, razao, nome, nascimento, endereco, bairro, cidade, uf, cep, email) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
    #     (cod_cli.get(), razao.get(), nome.get(), nascimento.get(), endereco.get(), bairro.get(), cidade.get(), uf.get(), cep.get(), email.get())
    # )
    cursor.execute("INSERT INTO saccli (cod_cli, razao, nome) VALUES (?, ?, ?)",(cod_cli.get(), razao.get(), nome.get()))

    con.commit()

# # LIMITE DE CARACTER NO GET
# def limit_input(action, new_input, max_length, entry):
#     if action == '1':  # inserção de caracteres
#         if len(entry.get()) >= int(max_length):
#                 return False
#         else:
#             return True
#     elif action == '0':  # exclusão de caracteres
#         return True

# Criação da janela principal
root = customtkinter.CTk()
root.title('Cadastro de Clientes')
root.focus()
root.iconbitmap("c:\helio\siachb\hti.ico")
largura_tela = root.winfo_screenwidth()
altura_tela = root.winfo_screenheight()
largura_janela = 900  # Defina a largura da sua janela de login
altura_janela = 700  # Defina a altura da sua janela de login
posicao_x = (largura_tela - largura_janela) / 2
posicao_y = (altura_tela - altura_janela) / 2
root.geometry("%dx%d+%d+%d" % (largura_janela, altura_janela, posicao_x, posicao_y))
# validate_cmd = root.register(limit_input)


# Criação dos widgets
label_titulo = customtkinter.CTkLabel(root, text='Cadastro de Cliente', font=('Arial', 20))

label_cod_cli = customtkinter.CTkLabel(root, text='Código do Cliente')
cod_cli = customtkinter.CTkEntry(root, placeholder_text='Código do Cliente', border_color='blue', width=100)

label_razao = customtkinter.CTkLabel(root, text='Razão Social')
razao = customtkinter.CTkEntry(root)

label_nome = customtkinter.CTkLabel(root, text='Nome')
nome = customtkinter.CTkEntry(root)

label_nascimento = customtkinter.CTkLabel(root, text='Data de Nascimento')
nascimento = customtkinter.CTkEntry(root)

label_endereco = customtkinter.CTkLabel(root, text='Endereço')
endereco = customtkinter.CTkEntry(root)

label_bairro = customtkinter.CTkLabel(root, text='Bairro')
bairro = customtkinter.CTkEntry(root)

label_cidade = customtkinter.CTkLabel(root, text='Cidade')
cidade = customtkinter.CTkEntry(root)

label_uf = customtkinter.CTkLabel(root, text='UF')
uf = customtkinter.CTkEntry(root)

label_cep = customtkinter.CTkLabel(root, text='CEP')
cep = customtkinter.CTkEntry(root)

label_email = customtkinter.CTkLabel(root, text='E-mail')
email = customtkinter.CTkEntry(root)


btn_cadastrar = customtkinter.CTkButton(root, text='Cadastrar', command=cadastrar_cliente)
btn_sair = customtkinter.CTkButton(root, text='Sair', command=root.quit)


# Inicialização dos campos de entrada
cod_cli.insert(0, mcod_cli)
razao.insert(0, ' ')
nome.insert(0, ' ')
nascimento.insert(0, ' ')
endereco.insert(0, ' ')
bairro.insert(0, ' ')
cidade.insert(0, ' ')
uf.insert(0, ' ')
cep.insert(0, ' ')
email.insert(0, ' ')



# Posicionamento dos widgets na tela
label_titulo.grid(row=0, column=0, columnspan=2, pady=20)

label_cod_cli.grid(row=1, column=0, padx=10, pady=5, sticky='s')
cod_cli.grid(row=1, column=1, padx=10, pady=5)

label_razao.grid(row=2, column=0, padx=10, pady=5, sticky='e')
razao.grid(row=2, column=1, padx=10, pady=5)

label_nome.grid(row=3, column=0, padx=10, pady=5, sticky='e')
nome.grid(row=3, column=1, padx=10, pady=5)

label_nascimento.grid(row=4, column=0, padx=10, pady=5, sticky='e')
nascimento.grid(row=4, column=1, padx=10, pady=5)

label_endereco.grid(row=5, column=0, padx=10, pady=5, sticky='e')
endereco.grid(row=5, column=1, padx=10, pady=5)

label_bairro.grid(row=6, column=0, padx=10, pady=5, sticky='e')
bairro.grid(row=6, column=1, padx=10, pady=5)

label_cidade.grid(row=7, column=0, padx=10, pady=5, sticky='e')
cidade.grid(row=7, column=1, padx=10, pady=5)

label_uf.grid(row=8, column=0, padx=10, pady=5, sticky='e')
uf.grid(row=8, column=1, padx=10, pady=5)

label_cep.grid(row=9, column=0, padx=10, pady=5, sticky='e')
cep.grid(row=9, column=1, padx=10, pady=5)

label_email.grid(row=10, column=0, padx=10, pady=5, sticky='e')
email.grid(row=10, column=1, padx=10, pady=5)


btn_cadastrar.grid(row=13, column=1, padx=10, pady=5)
btn_sair.grid(row=14, column=1, padx=10, pady=5)


root.mainloop()


