import sys
import random
import json
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

class Frog(QGraphicsEllipseItem):
    def __init__(self, x, y, weight, max_jump_distance):
        super().__init__(-10, -10, 20, 20)  # размеры лягушки
        self.setPos(QPointF(x, y))  # Начальная позиция лягушки
        self.weight = weight
        self.max_jump_distance = max_jump_distance
        self.setBrush(QBrush(QColor("red")))
        self.setZValue(10)

    def crazy_jump(self, where):
        self.setPos(where.x(), where.y())  # Устанавливаем как x, так и y

class LilyPad(QGraphicsEllipseItem):
    def __init__(self, x, y, strength):
        super().__init__(-15, -15, 30, 30)  # размеры кувшинки
        self.setPos(x, y)  # Устанавливаем координаты (x, y)
        self.strength = strength
        self.setBrush(QBrush(QColor("green")))

    def fall(self, speed):
        # Смещаем кувшинку вниз на `speed` пикселей
        current_pos = self.pos()
        self.setPos(current_pos.x(), current_pos.y() + speed)
    
    def getPos(self):
        return self.pos()

class MainWindow(QMainWindow):
    def __init__(self, standrad):
        super().__init__()
        self.setFixedSize(1000, 600)  # Установка фиксированного размера окна 1000x600
        self.scene = QGraphicsScene(0, 0, 800, 600)  # Создание сцены 800x600
        self.view = QGraphicsView(self.scene, self)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setGeometry(200, 0, 800, 600)  # Установка геометрии QGraphicsView

        # Переменные для управления
        self.trail_length = standrad.get("trail_length")
        self.fall_speed = standrad.get("fall_speed")
        self.spawn_interval = standrad.get("spawn_interval")
        self.lily_weight_max = standrad.get("lily_weight_max")
        self.jump_update_interval = standrad.get("jump_update_interval")
        self.lily_pad_fall_update_interval = standrad.get("lily_pad_fall_update_interval")
        self.max_lilies = standrad.get("max_lilies")
        self.frog_weight = standrad.get("frog_weight")
        self.frog_jump_distance = standrad.get("frog_jump_distance")

        # Создание левой полоски для настроек параметров
        self.settings_panel = QWidget(self)
        self.settings_panel.setGeometry(0, 0, 200, 600)
        self.settings_layout = QVBoxLayout(self.settings_panel)

        # Добавление элементов настроек параметров в левую полоску
        self.fall_speed_slider = QSlider(Qt.Orientation.Horizontal)
        self.fall_speed_slider.setRange(1, 8)
        self.fall_speed_slider.setValue(self.fall_speed)
        self.fall_speed_slider.valueChanged.connect(self.update_fall_speed)
        self.settings_layout.addWidget(QLabel("Скорость падения"))
        self.settings_layout.addWidget(self.fall_speed_slider)

        self.spawn_interval_slider = QSlider(Qt.Orientation.Horizontal)
        self.spawn_interval_slider.setRange(100, 750)
        self.spawn_interval_slider.setValue(self.spawn_interval)
        self.spawn_interval_slider.valueChanged.connect(self.update_spawn_interval)
        self.settings_layout.addWidget(QLabel("Интервал спавна"))
        self.settings_layout.addWidget(self.spawn_interval_slider)

        self.lily_weight_max_slider = QSlider(Qt.Orientation.Horizontal)
        self.lily_weight_max_slider.setRange(1, 20)
        self.lily_weight_max_slider.setValue(self.lily_weight_max)
        self.lily_weight_max_slider.valueChanged.connect(self.update_lily_weight_max)
        self.settings_layout.addWidget(QLabel("Максимальный вес кувшинки"))
        self.settings_layout.addWidget(self.lily_weight_max_slider)

        self.jump_update_interval_slider = QSlider(Qt.Orientation.Horizontal)
        self.jump_update_interval_slider.setRange(2, 1000)
        self.jump_update_interval_slider.setValue(self.jump_update_interval)
        self.jump_update_interval_slider.valueChanged.connect(self.update_jump_update_interval)
        self.settings_layout.addWidget(QLabel("Интервал обновления прыжка"))
        self.settings_layout.addWidget(self.jump_update_interval_slider)

        self.lily_pad_fall_update_interval_slider = QSlider(Qt.Orientation.Horizontal)
        self.lily_pad_fall_update_interval_slider.setRange(1, 20)
        self.lily_pad_fall_update_interval_slider.setValue(self.lily_pad_fall_update_interval)
        self.lily_pad_fall_update_interval_slider.valueChanged.connect(self.update_lily_pad_fall_update_interval)
        self.settings_layout.addWidget(QLabel("Интервал обновления падения кувшинки"))
        self.settings_layout.addWidget(self.lily_pad_fall_update_interval_slider)

        self.max_lilies_slider = QSlider(Qt.Orientation.Horizontal)
        self.max_lilies_slider.setRange(1, 10)
        self.max_lilies_slider.setValue(self.max_lilies)
        self.max_lilies_slider.valueChanged.connect(self.update_max_lilies)
        self.settings_layout.addWidget(QLabel("Максимальное количество кувшинок"))
        self.settings_layout.addWidget(self.max_lilies_slider)

        self.frog_weight_slider = QSlider(Qt.Orientation.Horizontal)
        self.frog_weight_slider.setRange(0, 20)
        self.frog_weight_slider.setValue(self.frog_weight)
        self.frog_weight_slider.valueChanged.connect(self.update_frog_weight)
        self.settings_layout.addWidget(QLabel("Вес лягушки"))
        self.settings_layout.addWidget(self.frog_weight_slider)

        self.frog_jump_distance_slider = QSlider(Qt.Orientation.Horizontal)
        self.frog_jump_distance_slider.setRange(100, 500)
        self.frog_jump_distance_slider.setValue(self.frog_jump_distance)
        self.frog_jump_distance_slider.valueChanged.connect(self.update_frog_jump_distance)
        self.settings_layout.addWidget(QLabel("Максимальное расстояние прыжка лягушки"))
        self.settings_layout.addWidget(self.frog_jump_distance_slider)

        self.trail_length_slider = QSlider(Qt.Orientation.Horizontal)
        self.trail_length_slider.setRange(0, 20)
        self.trail_length_slider.setValue(self.trail_length)
        self.trail_length_slider.valueChanged.connect(self.update_trail_length)
        self.settings_layout.addWidget(QLabel("Длина следа"))
        self.settings_layout.addWidget(self.trail_length_slider)

        # Cлед
        self.lines = []

        # Берега
        self.left_shore = 0
        self.right_shore = self.scene.width()
        self.current_shore = 'left'

        # Логика движения
        self.direction = 'right'  # Лягушка начинает с левого берега

        # Создание списка кувшинок
        self.lilies = []

        # Текущая кувшинка
        self.previous_lily_pad = None

        # Лягушка
        self.frog = Frog(400, 300, weight=self.frog_weight, max_jump_distance=self.frog_jump_distance)
        self.scene.addItem(self.frog)

        # Таймеры
        self.timer_frog = QTimer()
        self.timer_frog.timeout.connect(self.update_frog_position)
        self.timer_frog.start(self.jump_update_interval)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_lily_pads_position)
        self.timer.start(self.lily_pad_fall_update_interval)

        self.spawn_timer = QTimer()
        self.spawn_timer.timeout.connect(self.spawn_lily_pads)
        self.spawn_timer.start(0)

    #апдейты
    def update_trail_length(self, value):
        self.trail_length = value
    
    def update_fall_speed(self, value):
        self.fall_speed = value

    def update_spawn_interval(self, value):
        self.spawn_interval = value

    def update_lily_weight_max(self, value):
        self.lily_weight_max = value

    def update_jump_update_interval(self, value):
        self.jump_update_interval = value
        self.timer_frog.start(self.jump_update_interval)

    def update_lily_pad_fall_update_interval(self, value):
        self.lily_pad_fall_update_interval = value
        self.timer.start(self.lily_pad_fall_update_interval)

    def update_max_lilies(self, value):
        self.max_lilies = value

    def update_frog_weight(self, value):
        self.frog.weight = value

    def update_frog_jump_distance(self, value):
        self.frog_jump_distance = value
        self.frog.max_jump_distance = value

    def update_lily_pads_position(self):
        for lily in self.lilies:
            lily.fall(self.fall_speed)
            if lily.pos().y() > self.scene.height():
                self.scene.removeItem(lily)
                self.lilies.remove(lily)

    def spawn_lily_pads(self):
        self.spawn_timer.start(random.randint(self.spawn_interval-100, self.spawn_interval+100))
        # Случайное количество кувшинок от 1 до n
        number_of_lilies = random.randint(1, self.max_lilies)
        positions = []  # Список для хранения позиций, чтобы избежать пересечения

        for _ in range(number_of_lilies):
            # Случайное положение по оси X, с проверкой на расстояние между кувшинками
            while True:
                x = random.randint(int(self.frog_jump_distance // 4), int(self.scene.width() - self.frog_jump_distance // 4))  
                if all(abs(x - pos_x) > 40 for pos_x in positions):  # 40 пикселей - минимальное расстояние
                    positions.append(x)
                    break
            
            y = 0  # Начальное положение по оси Y (сверху)
            # Добавляем кувшинку в сцену с позицией (x, y)
            strength = random.randint(1, self.lily_weight_max)  # Случайная прочность
            lily = LilyPad(x, y, strength) 
            self.scene.addItem(lily)
            self.lilies.append(lily)

    def find_next_lily_pad(self):
        possible_lilies = []
        current_pos = self.frog.pos()

        # Определяем расстояние до левого и правого берегов
        distance_to_left_shore = abs(current_pos.x() - self.left_shore)
        distance_to_right_shore = abs(current_pos.x() - self.right_shore)

        # Проверка на возможность прыжка на берег
        if self.direction == 'right' and distance_to_right_shore <= self.frog.max_jump_distance:
            return QPointF(self.right_shore, current_pos.y())  # Повернуть в сторону правого берега

        if self.direction == 'left' and distance_to_left_shore <= self.frog.max_jump_distance:
            return QPointF(self.left_shore, current_pos.y())  # Повернуть в сторону левого берега

        # Обычный поиск кувшинок
        for lily in self.lilies:
            distance_x = abs(lily.pos().x() - current_pos.x())
            distance_y = abs(lily.pos().y() - current_pos.y())
            distance = (distance_x ** 2 + distance_y ** 2) ** 0.5

            if distance <= self.frog.max_jump_distance and distance > 20:
                possible_lilies.append(lily)

        if possible_lilies:
            if self.direction == 'right':
                next_lily = max(possible_lilies, key=lambda l: l.pos().x())  # Ближайшая вправо
            else:
                next_lily = min(possible_lilies, key=lambda l: l.pos().x())  # Ближайшая влево

            return next_lily.pos()
        
        return None


    def update_frog_position(self):
        next_position = self.find_next_lily_pad()
        if next_position:
            # Найти кувшинку, c которой прыгнула лягушка
            jumped_lily = None
            for lily in self.lilies:
                if lily.pos() == next_position:
                    jumped_lily = lily
                    break
            
            # Прыжок на следующую кувшинку
            self.draw_path(self.frog.pos(), next_position)
            self.frog.crazy_jump(next_position)

            # Если лягушка прыгнула с предыдущей кувшинки, снижаем её прочность
            if self.previous_lily_pad:
                if self.previous_lily_pad in self.lilies:  # Проверяем, что кувшинка всё ещё в списке
                    self.previous_lily_pad.strength -= self.frog.weight  # Уменьшаем прочность на вес лягушки
                    if self.previous_lily_pad.strength <= 0:
                        # Если прочность кувшинки достигла нуля, удаляем её из сцены
                        self.scene.removeItem(self.previous_lily_pad)
                        self.lilies.remove(self.previous_lily_pad)

            self.previous_lily_pad = jumped_lily

        else:
            # Если нет доступных кувшинок для прыжка, лягушка следует за кувшинкой вниз
            current_pos = self.frog.pos()
            self.draw_path(self.frog.pos(), current_pos)
            for lily in self.lilies:
                if abs(lily.pos().x() - current_pos.x()) < 1:  # Если лягушка находится на кувшинке
                    # Следуем за кувшинкой вниз
                    self.frog.setPos(lily.pos().x(), lily.pos().y())


        # Проверка, достигла ли лягушка берега, чтобы сменить направление
        if self.direction == 'right' and self.frog.pos().x() >= self.right_shore:
            self.direction = 'left'  # Лягушка меняет направление на левое
        elif self.direction == 'left' and self.frog.pos().x() <= self.left_shore:
            self.direction = 'right'  # Лягушка меняет направление на правое
        
    def draw_path(self, start_pos, end_pos):
        pen = QPen(QColor("blue"))
        pen.setWidth(1)
        line = self.scene.addLine(start_pos.x(), start_pos.y(), end_pos.x(), end_pos.y(), pen)
        self.lines.append(line)

        if len(self.lines) > self.trail_length:
            while len(self.lines) > self.trail_length:
                old_line = self.lines.pop(0)
                self.scene.removeItem(old_line)


if __name__ == '__main__':
    standrad = {
        "trail_length": 2,
        "fall_speed" : 2,
        "spawn_interval" : 500,
        "lily_weight_max" : 5,
        "jump_update_interval" : 100,
        "lily_pad_fall_update_interval" : 20,
        "max_lilies" : 7,
        "frog_weight" : 5,
        "frog_jump_distance" : 200
    }
    try:
        with open('test.json') as f:
            inpJson = json.loads(f.read())
        standrad.update(inpJson)
    except FileNotFoundError:
        pass
    app = QApplication(sys.argv)
    window = MainWindow(standrad)
    window.show()
    sys.exit(app.exec())
