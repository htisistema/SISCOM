from PyQt6.QtWidgets import QApplication, QListWidget, QListWidgetItem, QVBoxLayout, QWidget

# Suponha que você tenha recuperado os dados do banco de dados Firebird
dados = [
    ("001", "Produto A", 10.99),
    ("002", "Produto", 15.99),
    ("003", "Produto C", 8.99),
    # ...
]

app = QApplication([])

# Criar o QListWidget
list_widget = QListWidget()

# Preencher o QListWidget com os dados do banco de dados
for cod_merc, mer, pr_venda in dados:
    item = QListWidgetItem(f"Código: {cod_merc}, Mercadoria: {mer}, Preço de Venda: {pr_venda}")
    list_widget.addItem(item)

# Configurar algumas propriedades do QListWidget
list_widget.setEditTriggers(QListWidget.EditTrigger.NoEditTriggers)
list_widget.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
list_widget.setSelectionBehavior(QListWidget.SelectionBehavior.SelectRows)

# Criar um layout para o widget principal
layout = QVBoxLayout()
layout.addWidget(list_widget)

# Criar o widget principal e definir o layout
widget = QWidget()
widget.setLayout(layout)
widget.show()

app.exec()
