from PyQt6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene

app = QApplication([])
view = QGraphicsView()
scene = QGraphicsScene()
view.setScene(scene)
view.show()
app.exec()
