import sys
from PySide6.QtCore import QStringListModel, QFile
from PySide6.QtWidgets import QApplication, QPushButton, QListView
from PySide6.QtUiTools import QUiLoader

UI_PATH = "main.ui"

class App:
    def __init__(self):
        loader = QUiLoader()
        f = QFile(UI_PATH); f.open(QFile.ReadOnly)
        self.window = loader.load(f); f.close()

        # 위젯 찾기 (QMainWindow 안의 centralwidget 하위에서 탐색)
        self.add_button = self.window.findChild(QPushButton, "Save_Button")
        self.list_view  = self.window.findChild(QListView,  "my_medicines")

        # 모델 연결 (안 하면 리스트뷰가 “비어 보임”)
        self.model = QStringListModel([])
        self.list_view.setModel(self.model)

        # 시그널 연결
        self.add_button.clicked.connect(self.add_item)
       

    def add_item(self):
        text = "mine"
        if not text:
            return
        items = self.model.stringList()
        items.append(text)
        self.model.setStringList(items)
 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = App()
    a.window.show()   # 포인트: window 자체를 show
    sys.exit(app.exec())
