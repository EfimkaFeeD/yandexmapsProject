import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap
from ui import Ui_MainWindow


def get_toponym_size(toponym):
    toponym_upper_corner, toponym_lower_corner = (toponym['boundedBy']['Envelope']['upperCorner']).split(' '), (
        toponym['boundedBy']['Envelope']['lowerCorner']).split(' ')
    toponym_longitude_size, toponym_lattitude_size = str(
        float(toponym_upper_corner[0]) - float(toponym_lower_corner[0])), str(
        float(toponym_upper_corner[1]) - float(toponym_lower_corner[1]))
    return [str(toponym_longitude_size), str(toponym_lattitude_size)]


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
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": self.input_edit.text(),
            "format": "json"}

        response = requests.get(geocoder_api_server, params=geocoder_params)

        if not response:
            print('Error')
            return

        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]
        address = toponym['metaDataProperty']['GeocoderMetaData']['Address']['formatted']
        self.address_label.setText(address)
        toponym_coodrinates = toponym["Point"]["pos"]
        toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

        map_params = {
            "ll": ",".join([toponym_longitude, toponym_lattitude]),
            "spn": ",".join(get_toponym_size(toponym)),
            "l": "map"
        }

        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)

        pixmap = QPixmap()
        pixmap.loadFromData(response.content)
        self.map_image.setPixmap(pixmap)

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
