from PyQt6.QtCore import QDate
import hti_global as hg

# Suponha que hg.mdata_sis seja uma string no formato "YYYY-MM-DD"
mdata_sis_str = "2023-05-23"  # Exemplo de data em formato string
print(mdata_sis_str)
print(hg.mdata_sis)
mdata_sis = m_data_f.strftime("%Y/%m/%d")
# Converte a string para um objeto QDate
mdata_sis = QDate.fromString(hg.mdata_sis, "yyyy-MM-dd")
print(mdata_sis)
# Verifique se a conversão foi bem-sucedida
if not mdata_sis.isValid():
    raise ValueError(f"Data inválida: {hg.mdata_sis}")

# Adiciona os dias ao QDate
mdia = 10  # Exemplo de número de dias a adicionar
mdata_f = mdata_sis.addDays(mdia)
print(mdata_f)
# Imprime a nova data
print(mdata_f.toString("yyyy-MM-dd"))
