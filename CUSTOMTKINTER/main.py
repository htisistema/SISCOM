import fdb
import customtkinter
from PIL import Image
import configparser
from tkinter import messagebox
# import menu
from menu import criar_menu

# light
customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('dark-blue')

# import tkinter as tk

# Crie a janela
login_window = customtkinter.CTk()
login_window.iconbitmap("c:\helio\siachb\hti.ico")
login_window.title("Login")
largura_tela = login_window.winfo_screenwidth()
altura_tela = login_window.winfo_screenheight()
largura_janela = 300 # Defina a largura da sua janela de login
altura_janela = 400 # Defina a altura da sua janela de login
posicao_x = (largura_tela - largura_janela) / 2
posicao_y = (altura_tela - altura_janela) / 2
login_window.geometry("%dx%d+%d+%d" % (largura_janela, altura_janela, posicao_x, posicao_y))

# Impede a redimensionamento da janela
# login_window.resizable(False, False)


# img = PhotoImage(file="c:\helio\siachb\htilogo.jpg")
my_image = customtkinter.CTkImage(light_image=Image.open("c:\helio\siachb\htifirma1.jpg"),
                                  dark_image=Image.open("c:\helio\siachb\htifirma1.jpg"),
                                  size=(90, 90))

button = customtkinter.CTkLabel(login_window, image=my_image,width=120,height=25)
button.pack(padx=10, pady=10)

# Crie o campo de entrada de usuário
user_label = customtkinter.CTkLabel(login_window, text="Usuário:")
user_label.pack(padx=5, pady=5)

user_entry = customtkinter.CTkEntry(login_window, placeholder_text='Seu codigo')
user_entry.pack(padx=5, pady=5)
user_entry.focus()

# Crie o campo de entrada de senha
password_label = customtkinter.CTkLabel(login_window, text="Senha:")
password_label.pack(padx=5, pady=5)

password_entry = customtkinter.CTkEntry(login_window, show="*", placeholder_text='Sua Senha')
password_entry.pack(padx=5, pady=5)

def login():
    # lendo o arquivo sisconfig.ini
    config = configparser.ConfigParser()
    config.read('sisconfig.ini')
    host = config.get('banco', 'host')

    # Conecte-se ao banco de dados
    con = fdb.connect(dsn=host, user='SYSDBA', password='masterkey')
    # Crie o cursor
    cursor = con.cursor()
    # Execute a consulta
    cursor.execute(f"SELECT * FROM insopera WHERE scod_op='{user_entry.get()}' and plug='{password_entry.get()}'")
    # Recupere o resultado
    result = cursor.fetchone()
    # print(result[0])
    # Feche a conexão
    con.close()

    # Verifique se o resultado é válido
    if result is None:
        messagebox.showerror("Erro de login", "Usuário ou senha incorretos!")
    else:
        # messagebox.showinfo("Bem-vindo", "Login bem sucedido!")
        login_window.destroy()
        criar_menu()


# Crie o botão de login
login_button = customtkinter.CTkButton(login_window, text="Login", command=login)
login_button.pack(padx=10, pady=10)

# Inicie o loop principal da janela
login_window.mainloop()

if __name__ == '__main__':
     login().run()
