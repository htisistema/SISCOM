from PyQt6.QtCore import QDate

# Suponha que hg.mdata_sis seja uma string no formato "YYYY-MM-DD"
mdata_sis_str = "2023-05-23"  # Exemplo de data em formato string

# Converte a string para um objeto QDate
mdata_sis = QDate.fromString(mdata_sis_str, "yyyy-MM-dd")

# Verifique se a conversão foi bem-sucedida
if not mdata_sis.isValid():
    raise ValueError(f"Data inválida: {mdata_sis_str}")

# Adiciona os dias ao QDate
mdia = 10  # Exemplo de número de dias a adicionar
mdata_f = mdata_sis.addDays(mdia)

# Imprime a nova data
print(mdata_f.toString("yyyy-MM-dd"))
