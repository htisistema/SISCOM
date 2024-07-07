from datetime import datetime, timedelta

# Define a data de emissão
mdataemi = datetime.strptime("26/10/2023", "%d/%m/%Y")

# Define o prazo em dias
mprazo = 20

# Acrescenta o prazo à data de emissão
data_com_prazo = mdataemi + timedelta(days=mprazo)

# Exibe a nova data
print(data_com_prazo.strftime("%d/%m/%Y"))