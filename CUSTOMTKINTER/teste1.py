# def limit_input(action, new_input, max_length):
#     if action == '1':  # inserção de caracteres
#         if len(entry.get()) >= int(max_length):
#             return False
#         else:
#             return True
#     elif action == '0':  # exclusão de caracteres
#         return True
#
# validate_cmd = root.register(limit_input)
#
# entry = tk.Entry(root, validate="key", validatecommand=(validate_cmd, '%d', '%S', '10'))
# entry.pack()


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
#
# entry1 = tk.Entry(root)
# validate_cmd = root.register(lambda action, new_input: limit_input(action, new_input, 5, entry1))
# entry1.config(validate="key", validatecommand=(validate_cmd, '%d', '%S'))
# entry1.pack()
#
entry1 = tk.Entry(root, validate="key")
entry1.config(validatecommand=(root.register(lambda action, new_input: limit_input(action, new_input, 5, entry1)), '%d', '%S'))
entry1.pack()

entry2 = tk.Entry(root, validate="key")
entry2.config(validatecommand=(root.register(lambda action, new_input: limit_input(action, new_input, 10, entry2)), '%d', '%S'))
entry2.pack()








root.mainloop()
