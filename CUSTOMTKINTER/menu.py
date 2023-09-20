import tkinter as tk

# import customtkinter as ctk

# def arquivo():
#     pass

def funcao1():
    print("Opção 1")

def funcao2():
    print("Opção 2")

def funcao3():
    print("Opção 3")



def movimento():
    # Coloque as ações a serem executadas ao selecionar a opção "Movimento" aqui
    pass

def consulta():
    # Coloque as ações a serem executadas ao selecionar a opção "Consulta" aqui
    pass

def relatorio():
    # Coloque as ações a serem executadas ao selecionar a opção "Relatório" aqui
    pass

def utilitario():
    # Coloque as ações a serem executadas ao selecionar a opção "Utilitário" aqui
    pass

def sair():
    quit()


def criar_menu():
    root = tk.Tk()
    root.title("Menu Principal")
    root.focus()
    root.iconbitmap("c:\helio\siachb\hti.ico")
    # root.geometry("400x300")
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    largura_janela = 900  # Defina a largura da sua janela de login
    altura_janela = 800  # Defina a altura da sua janela de login
    posicao_x = (largura_tela - largura_janela) / 2
    posicao_y = (altura_tela - altura_janela) / 2
    root.geometry("%dx%d+%d+%d" % (largura_janela, altura_janela, posicao_x, posicao_y))
    menu = tk.Menu(root)
    arquivo = tk.Menu(menu)
    # menu.add_command(label="Arquivo", command=arquivo)
    arquivo.add_command(label="Opção 1", command=funcao1)
    arquivo.add_command(label="Opção 2", command=funcao2)
    arquivo.add_command(label="Opção 3", command=funcao3)
    menu.add_cascade(label="Arquivo", menu=arquivo)
    menu.add_command(label="Movimento", command=movimento)
    menu.add_command(label="Consulta", command=consulta)
    menu.add_command(label="Relatório", command=relatorio)
    menu.add_command(label="Utilitário", command=utilitario)
    menu.add_command(label="Sair", command=sair)
    root.config(menu=menu)
    root.mainloop()

if __name__ == '__main__':
     criar_menu()
