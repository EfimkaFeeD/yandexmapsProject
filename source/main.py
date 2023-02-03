import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from ui import Ui_MainWindow


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.search_button.clicked.connect(self.search)
        self.map_type = self.view_button.currentText()
        self.post_index = self.postId_box.isChecked()
        self.reset_button.clicked.connect(self.reset)
        self.view_button.currentTextChanged.connect(self.update_map_type)
        self.postId_box.clicked.connect(self.update_address)

    def search(self):
        self.address_label.setText(self.input_edit.text())

    def reset(self):
        pass

    def update_map_type(self):
        pass

    def update_address(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
