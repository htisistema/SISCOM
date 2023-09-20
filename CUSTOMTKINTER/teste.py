import tkinter as tk

root = tk.Tk()

def limit_input(action, new_input, max_length, entry):
    if action == '1':  # inserção de caracteres
        if len(entry.get()) >= int(max_length):
                return False
        else:
            return True
    elif action == '0':  # exclusão de caracteres
        return True


entry1 = tk.Entry(root, validate="key")
entry1.config(validatecommand=(root.register(lambda action, new_input: limit_input(action, new_input, 5, entry1)), '%d', '%S'))
entry1.pack()





# validate_cmd = root.register(limit_input)
#
# cod_cli = tk.Entry(root)
# cod_cli = tk.Entry(root, validate="key", validatecommand=(validate_cmd, '%d', '%S', '5', cod_cli))
# cod_cli.pack()

# entry_cod_cli = tk.Entry(root, validate="key", validatecommand=(validate_cmd, '%d', '%S', '5'))
# entry_cod_cli.pack()
root.mainloop()
