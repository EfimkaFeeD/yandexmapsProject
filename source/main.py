import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from ui import Ui_MainWindow


map_api_server = "http://static-maps.yandex.ru/1.x/"
map_types = {'scheme': 'map', 'satellite': 'sat', 'hybrid': 'sat,skl'}


# Нахождение размеров топонима
def get_toponym_size(toponym):
    toponym_upper_corner, toponym_lower_corner = (toponym['boundedBy']['Envelope']['upperCorner']).split(' '), (
        toponym['boundedBy']['Envelope']['lowerCorner']).split(' ')
    toponym_longitude_size, toponym_lattitude_size = str(
        float(toponym_upper_corner[0]) - float(toponym_lower_corner[0])), str(
        float(toponym_upper_corner[1]) - float(toponym_lower_corner[1]))
    return [str(toponym_longitude_size), str(toponym_lattitude_size)]


# Основной класс приложения
class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.search_button.clicked.connect(self.search)
        self.reset_button.clicked.connect(self.reset)
        self.view_button.currentTextChanged.connect(self.update_map_type)
        self.postId_box.clicked.connect(self.update_address)
        self.address = None
        self.toponym_data = None

    # Поиск
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
        self.address = toponym['metaDataProperty']['GeocoderMetaData']['Address']
        self.update_address()
        toponym_coodrinates = toponym["Point"]["pos"]
        toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

        map_params = {
            "ll": ",".join([toponym_longitude, toponym_lattitude]),
            "spn": ",".join(get_toponym_size(toponym)),
            "size": "650,450",
            "l": map_types[self.view_button.currentText()]
        }
        self.toponym_data = map_params
        self.update_map()

    # Сброс поиска
    def reset(self):
        pass

    # Смена типа карты
    def update_map_type(self):
        if not self.toponym_data:
            return
        self.toponym_data['l'] = map_types[self.view_button.currentText()]
        self.update_map()

    def update_map(self):
        if not self.toponym_data:
            return
        print('got to map update')
        response = requests.get(map_api_server, params=self.toponym_data)
        pixmap = QPixmap()
        pixmap.loadFromData(response.content)
        self.map_image.setPixmap(pixmap)

    # Показ почтового индекса в адресе
    def update_address(self):
        if not self.address:
            return
        post_id = self.address['postal_code'] if 'postal_code' in self.address else ''
        if self.postId_box.isChecked():
            if post_id:
                self.address_label.setText(self.address['formatted'] + ', post code: ' + post_id)
            else:
                self.address_label.setText(self.address['formatted'] + ', post code: Can\'t determine')
        else:
            self.address_label.setText(self.address['formatted'])

    # Обработка событий клавиатуры
    def keyPressEvent(self, event):
        if not self.toponym_data:
            return
        # Зум: приближение
        if event.key() == Qt.Key_PageUp:
            spn = self.toponym_data['spn'].split(',')
            x = float(spn[0]) * 0.15
            y = float(spn[1]) * 0.15
            print('spn before:', spn)
            if float(spn[0]) > 0.0001 and float(spn[1]) > 0.0001:
                spn[0], spn[1] = str(float(spn[0]) - x), str(float(spn[1]) - y)
                print('spn after:', spn)
                self.toponym_data['spn'] = ','.join(spn)
                self.update_map()
        # Зум:  отдаление
        if event.key() == Qt.Key_PageDown:
            spn = self.toponym_data['spn'].split(',')
            x = float(spn[0]) * 0.15
            y = float(spn[1]) * 0.15
            print('spn before:', spn)
            if float(spn[0]) < 100 and float(spn[1]) < 70:
                spn[0], spn[1] = str(float(spn[0]) + x), str(float(spn[1]) + y)
                print('spn after:', spn)
                self.toponym_data['spn'] = ','.join(spn)
                self.update_map()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
