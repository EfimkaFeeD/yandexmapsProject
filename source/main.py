import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from ui import Ui_MainWindow


map_api_server = "http://static-maps.yandex.ru/1.x/"
map_types = {'scheme': 'map', 'satellite': 'sat', 'hybrid': 'sat,skl'}

MAP_SIZE = (650, 450)


# Нахождение размеров топонима
def get_toponym_size(toponym):
    toponym_upper_corner, toponym_lower_corner = (toponym['boundedBy']['Envelope']['upperCorner']).split(
        ' '), (toponym['boundedBy']['Envelope']['lowerCorner']).split(' ')
    toponym_longitude_size, toponym_latitude_size = str(
        float(toponym_upper_corner[0]) - float(toponym_lower_corner[0])), str(
        float(toponym_upper_corner[1]) - float(toponym_lower_corner[1]))
    return [str(toponym_longitude_size), str(toponym_latitude_size)]


# Основной класс приложения
class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        super().setupUi(self)
        self.setFixedSize(1280, 720)
        self.setWindowTitle('YandexMapsApp')
        self.setWindowIcon(QIcon('icon.png'))
        self.setStyleSheet("background-color: rgb(54, 73, 78)")
        self.search_button.setStyleSheet(
            "border-radius:20;background-color: rgb(149, 173, 182);color: white")
        self.reset_button.setStyleSheet(
            "border-radius:20;background-color: rgb(149, 173, 182);color: white")
        self.input_edit.setStyleSheet(
            "border-radius:20;background-color: rgb(149, 173, 182);color: white")
        self.address_label.setStyleSheet(
            "border-radius:20;background-color: rgb(149, 173, 182);color: white")
        self.input_label.setStyleSheet("color: white")
        self.postId_box.setStyleSheet("color: white")
        self.status_textedit.setStyleSheet(
            "border-radius:20;background-color: rgb(149, 173, 182);color: white")
        self.search_button.clicked.connect(self.search)
        self.reset_button.clicked.connect(self.reset)
        self.view_button.currentTextChanged.connect(self.update_map_type)
        self.postId_box.clicked.connect(self.update_address)
        self.address = None
        self.toponym_data = None
        self.status_text = []

    # Поиск
    def search(self):
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": self.input_edit.text(),
            "format": "json"}

        response = requests.get(geocoder_api_server, params=geocoder_params)

        json_response = response.json()

        try:
            if not json_response["response"]["GeoObjectCollection"]:
                self.error('empty api response')
                return
        except KeyError as error:
            self.error(error)
            return

        try:
            toponym = json_response["response"]["GeoObjectCollection"][
                "featureMember"][0]["GeoObject"]
        except IndexError as error:
            self.error(error)
            return
        self.address = toponym['metaDataProperty']['GeocoderMetaData']['Address']
        self.update_address()
        toponym_coordinates = toponym["Point"]["pos"]
        toponym_longitude, toponym_latitude = toponym_coordinates.split(" ")

        map_params = {
            "ll": ",".join([toponym_longitude, toponym_latitude]),
            "spn": ",".join(get_toponym_size(toponym)),
            "size": ','.join(map(str, MAP_SIZE)),
            "l": map_types[self.view_button.currentText()],
            "pt": f'{",".join([toponym_longitude, toponym_latitude])},comma'
        }
        self.toponym_data = map_params
        self.update_map()

    # Сброс поиска
    def reset(self):
        self.map_image.setPixmap(QPixmap())
        self.address_label.setText('')
        self.address = None
        self.toponym_data = None

    # Смена типа карты
    def update_map_type(self):
        if not self.toponym_data:
            return
        self.toponym_data['l'] = map_types[self.view_button.currentText()]
        self.update_map()

    # Обновление изображения карты
    def update_map(self):
        if not self.toponym_data:
            return
        self.status_text.append('Map updated')
        self.status_textedit.setText('\n'.join(self.status_text))
        self.status_text = []
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
                self.address_label.setText(
                    self.address['formatted'] + ', post code: ' + post_id)
            else:
                self.address_label.setText(
                    self.address['formatted'] +
                    ', post code: Can\'t determine')
        else:
            self.address_label.setText(self.address['formatted'])

    # Обработка событий клавиатуры
    def keyPressEvent(self, event):
        if not self.toponym_data:
            return
        # Зум: приближение
        if event.key() == Qt.Key_PageUp:
            spn = self.toponym_data['spn'].split(',')
            x = float(spn[0]) * 0.3
            y = float(spn[1]) * 0.3
            self.status_text.append('Spn before: ' + ' '.join(spn))
            if float(spn[0]) - x > 0.0001 and float(spn[1]) - y > 0.0001:
                spn[0], spn[1] = str(float(spn[0]) - x), str(float(spn[1]) - y)
                self.status_text.append('Spn after: ' + ' '.join(spn))
                self.toponym_data['spn'] = ','.join(spn)
                self.update_map()
        # Зум: отдаление
        if event.key() == Qt.Key_PageDown:
            spn = self.toponym_data['spn'].split(',')
            x = float(spn[0]) * 0.3
            y = float(spn[1]) * 0.3
            self.status_text.append('Spn before: ' + ' '.join(spn))
            if float(spn[0]) - x < 125 and float(spn[1]) - y < 75:
                spn[0], spn[1] = str(float(spn[0]) + x), str(float(spn[1]) + y)
                self.status_text.append('Spn after: ' + ' '.join(spn))
                self.toponym_data['spn'] = ','.join(spn)
                self.update_map()
        # Передвижения центра карты выше
        if event.key() in [Qt.Key_W, 1062]:
            ll = self.toponym_data['ll'].split(',')
            self.status_text.append('Ll before: ' + ' '.join(ll))
            spn = self.toponym_data['spn'].split(',')
            y = float(spn[1]) * 0.85
            self.status_text.append('y: ' + str(y))
            if float(ll[1]) + y < 75:
                ll[1] = str(float(ll[1]) + y)
                self.status_text.append('Ll after: ' + ' '.join(ll))
                self.status_text.append('Spn: ' + ' '.join(spn))
                self.toponym_data['ll'] = ','.join(ll)
                self.update_map()
        # Передвижение центра карты ниже
        if event.key() in [Qt.Key_S, 1067]:
            ll = self.toponym_data['ll'].split(',')
            self.status_text.append('Ll before: ' + ' '.join(ll))
            spn = self.toponym_data['spn'].split(',')
            y = float(spn[1]) * 0.85
            self.status_text.append('y: ' + str(y))
            if float(ll[1]) - y > -75:
                ll[1] = str(float(ll[1]) - y)
                self.status_text.append('Ll after: ' + ' '.join(ll))
                self.status_text.append('Spn: ' + ' '.join(spn))
                self.toponym_data['ll'] = ','.join(ll)
                self.update_map()
        # Передвижение центра карты правее
        if event.key() in [Qt.Key_D, 1042]:
            ll = self.toponym_data['ll'].split(',')
            self.status_text.append('Ll before: ' + ' '.join(ll))
            spn = self.toponym_data['spn'].split(',')
            x = float(spn[0]) * 0.85
            self.status_text.append('x: ' + str(x))
            if float(ll[0]) + x < 180:
                ll[0] = str(float(ll[0]) + x)
                self.status_text.append('Ll after: ' + ' '.join(ll))
                self.status_text.append('Spn: ' + ' '.join(spn))
                self.toponym_data['ll'] = ','.join(ll)
                self.update_map()
        # Передвижение центра карты левее
        if event.key() in [Qt.Key_A, 1060]:
            ll = self.toponym_data['ll'].split(',')
            self.status_text.append('Ll before: ' + ' '.join(ll))
            spn = self.toponym_data['spn'].split(',')
            x = float(spn[0]) * 0.85
            self.status_text.append('x: ' + str(x))
            if float(ll[0]) - x > -180:
                ll[0] = str(float(ll[0]) - x)
                self.status_text.append('Ll after: ' + ' '.join(ll))
                self.status_text.append('Spn: ' + ' '.join(spn))
                self.toponym_data['ll'] = ','.join(ll)
                self.update_map()

    # Обработка событий мыши для установки меток
    def mousePressEvent(self, event):
        if not self.toponym_data:
            return
        spn = tuple(map(float, self.toponym_data['spn'].split(',')))
        ll = tuple(map(float, self.toponym_data['ll'].split(',')))
        self.status_text.append('Old coords: ' + ' '.join(map(str, ll)))
        absolute_pos = event.pos().x(), event.pos().y()
        shift = self.map_image.x() + self.map_image.width() // 2 - MAP_SIZE[0] // 2,\
            self.map_image.y() + self.map_image.height() // 2 - MAP_SIZE[1] // 2
        relative_pos = absolute_pos[0] - shift[0], absolute_pos[1] - shift[1]
        if not (
                0 <= relative_pos[0] <= MAP_SIZE[0]) or not (
                0 <= relative_pos[1] <= MAP_SIZE[1]):
            return
        center_delta = relative_pos[0] - \
            MAP_SIZE[0] // 2, relative_pos[1] - MAP_SIZE[1] // 2
        spn_shift = spn[0] / MAP_SIZE[0], spn[1] / MAP_SIZE[1]
        degree_shift = center_delta[0] * \
            spn_shift[0], -center_delta[1] * spn_shift[1]
        cord = ll[0] + degree_shift[0], ll[1] + degree_shift[1]
        self.status_text.append('New coords: ' + ' '.join(map(str, cord)))
        self.toponym_data['pt'] = ','.join(map(str, cord)) + ',comma'
        self.update_map()

    # Ошибка в получении запроса
    def error(self, error):
        self.status_text.append('ERROR')
        self.status_text.append(str(error))
        self.status_textedit.setText('\n'.join(self.status_text))
        self.status_text = []
        self.reset()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
