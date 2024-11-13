import sys
import random
import json
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

class FrogParametersDialog(QDialog):
    def __init__(self, weight=1, max_jump_distance=200, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Параметры лягушки")
        
        layout = QVBoxLayout()
        
        # Вес лягушки
        weight_layout = QHBoxLayout()
        weight_label = QLabel("Вес лягушки:")
        self.weight_spinbox = QSpinBox()
        self.weight_spinbox.setRange(0, 10)
        self.weight_spinbox.setValue(weight)
        weight_layout.addWidget(weight_label)
        weight_layout.addWidget(self.weight_spinbox)
        layout.addLayout(weight_layout)
        
        # Максимальная дистанция прыжка
        jump_layout = QHBoxLayout()
        jump_label = QLabel("Макс. дистанция прыжка:")
        self.jump_spinbox = QSpinBox()
        self.jump_spinbox.setRange(100, 600)
        self.jump_spinbox.setValue(max_jump_distance)
        jump_layout.addWidget(jump_label)
        jump_layout.addWidget(self.jump_spinbox)
        layout.addLayout(jump_layout)
        
        # Кнопки
        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Отмена")
        
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def get_parameters(self):
        return {
            'weight': self.weight_spinbox.value(),
            'max_jump_distance': self.jump_spinbox.value()
        }

class Frog(QGraphicsEllipseItem):
    def __init__(self, x, y, weight, max_jump_distance, direction='right'):
        super().__init__(-10, -10, 20, 20)  # размеры лягушки
        self.setPos(QPointF(x, y))  # Начальная позиция лягушки
        self.weight = weight
        self.max_jump_distance = max_jump_distance
        self.setBrush(QBrush(QColor("red")))
        self.setZValue(10)
        self.direction = direction
        
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
        self.setFixedSize(1000, 600)
        self.scene = QGraphicsScene(0, 0, 800, 600)
        self.view = QGraphicsView(self.scene, self)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setGeometry(200, 0, 800, 600)
        self.view.setMouseTracking(False)
        self.view.wheelEvent = self.wheelEvent

        # Переменные для управления
        self.fall_speed = standrad.get("fall_speed")
        self.spawn_interval = standrad.get("spawn_interval")
        self.lily_weight_max = standrad.get("lily_weight_max")
        self.jump_update_interval = standrad.get("jump_update_interval")
        self.max_lilies = standrad.get("max_lilies")
        self.frog_weight = standrad.get("frog_weight")
        self.frog_jump_distance = standrad.get("frog_jump_distance")

        # Создание левой полоски для настроек параметров
        self.settings_panel = QWidget(self)
        self.settings_panel.setGeometry(0, 0, 200, 600)
        self.settings_layout = QVBoxLayout(self.settings_panel)

        # Добавление элементов настроек параметров в левую полоску
        self.add_settings_elements()

        self.pause_button = QPushButton("Пауза")
        self.pause_button.clicked.connect(self.toggle_pause)
        self.pause_button.setFixedSize(180, 50)
        self.settings_layout.addWidget(self.pause_button)

        self.add_frog_button = QPushButton("Добавить лягушку")
        self.add_frog_button.setCheckable(True)
        self.add_frog_button.clicked.connect(self.toggle_frog_adding_mode)
        self.add_frog_button.setFixedSize(180, 50)
        self.settings_layout.addWidget(self.add_frog_button)

        self.settings_layout.setAlignment(self.pause_button, Qt.AlignmentFlag.AlignTop)
        self.settings_layout.setAlignment(self.add_frog_button, Qt.AlignmentFlag.AlignTop)
        
        # Флаги
        self.is_paused = False
        self.is_adding_frog_mode = False

        # Cлед
        self.trail_length = 3
        self.lines = []

        # Берега
        self.left_shore = 0
        self.right_shore = self.scene.width()

        # Создание списка кувшинок и лягушек
        self.lilies = []
        self.previous_lily_pad = None

        # Первая лягушка
        self.frog = Frog(400, 300, weight=self.frog_weight, max_jump_distance=self.frog_jump_distance)
        self.scene.addItem(self.frog)
        self.frogs = [self.frog]

        self.view.mousePressEvent = self.handle_mouse_press

        # Таймеры
        self.timer_frog = QTimer()
        self.timer_frog.timeout.connect(self.update_frog_position)
        self.timer_frog.start(self.jump_update_interval)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_lily_pads_position)
        self.timer.start(10)

        self.spawn_timer = QTimer()
        self.spawn_timer.timeout.connect(self.spawn_lily_pads)
        self.spawn_timer.start(0)

    def toggle_frog_adding_mode(self, checked):
        self.is_adding_frog_mode = checked
        if checked:
            self.add_frog_button.setStyleSheet("""
                QPushButton {
                    background-color: lightgreen;
                    border: 2px solid green;
                }
            """)
        else:
            self.add_frog_button.setStyleSheet("")
    
    def find_lily_at_position(self, pos):
        for lily in self.lilies:
            distance = ((lily.pos().x() - pos.x())**2 + (lily.pos().y() - pos.y())**2)**0.5
            if distance < 30:  # Радиус кувшинки
                return lily
        return None
    
    def handle_mouse_press(self, event):
        scene_pos = self.view.mapToScene(event.pos())

        if self.is_adding_frog_mode:
            clicked_lily = self.find_lily_at_position(scene_pos)

            if clicked_lily:
                dialog = FrogParametersDialog(parent=self)

                if dialog.exec():
                    params = dialog.get_parameters()

                    new_frog = Frog(
                        scene_pos.x(), 
                        scene_pos.y(), 
                        weight=params['weight'], 
                        max_jump_distance=params['max_jump_distance']
                    )

                    self.scene.addItem(new_frog)
                    self.frogs.append(new_frog)

                self.add_frog_button.setChecked(False)
                self.toggle_frog_adding_mode(False)

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.timer_frog.stop()
            self.timer.stop()
            self.spawn_timer.stop()
            self.pause_button.setText("Продолжить")
        else:
            self.timer_frog.start(self.jump_update_interval)
            self.timer.start(10)
            self.spawn_timer.start(0)
            self.pause_button.setText("Пауза")

    def add_settings_elements(self):
        settings = [
            ("Скорость падения", self.fall_speed, self.update_fall_speed, (1, 3)),
            ("Интервал спавна", self.spawn_interval, self.update_spawn_interval, (100, 750)),
            ("Интервал обновления прыжка", self.jump_update_interval, self.update_jump_update_interval, (2, 250)),  
            ("Максимальное количество кувшинок", self.max_lilies, self.update_max_lilies, (1, 10)),
            ("Максимальный вес лилии", self.lily_weight_max, self.update_lily_weight_max, (1, 20))
        ]

        for label, initial_value, slot, (min_value, max_value) in settings:
            slider = QSlider(Qt.Orientation.Horizontal)
            slider.setRange(min_value, max_value)
            slider.setValue(initial_value)
            slider.valueChanged.connect(slot)

            self.settings_layout.addWidget(QLabel(label))
            self.settings_layout.addWidget(slider)

    def update_fall_speed(self, value):
        self.fall_speed = value

    def update_spawn_interval(self, value):
        self.spawn_interval = value

    def update_lily_weight_max(self, value):
        self.lily_weight_max = value

    def update_jump_update_interval(self, value):
        self.jump_update_interval = value
        self.timer_frog.start(self.jump_update_interval)

    def update_max_lilies(self, value):
        self.max_lilies = value

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
                x = random.randint(20, self.scene.width() - 20)  
                if all(abs(x - pos_x) > 40 for pos_x in positions):
                    positions.append(x)
                    break
            
            y = 0  # Начальное положение по оси Y (сверху)
            # Добавляем кувшинку в сцену с позицией (x, y)
            strength = random.randint(1, self.lily_weight_max)  # Случайная прочность
            lily = LilyPad(x, y, strength) 
            self.scene.addItem(lily)
            self.lilies.append(lily)

    def find_next_lily_pad(self, frog):
        possible_lilies = []
        current_pos = frog.pos()

        distance_to_left_shore = abs(current_pos.x() - self.left_shore)
        distance_to_right_shore = abs(current_pos.x() - self.right_shore)

        if frog.direction == 'right' and distance_to_right_shore <= frog.max_jump_distance:
            return QPointF(self.right_shore, current_pos.y())

        if frog.direction == 'left' and distance_to_left_shore <= frog.max_jump_distance:
            return QPointF(self.left_shore, current_pos.y())

        for lily in self.lilies:
            distance_x = abs(lily.pos().x() - current_pos.x())
            distance_y = abs(lily.pos().y() - current_pos.y())
            distance = (distance_x ** 2 + distance_y ** 2) ** 0.5

            if distance <= frog.max_jump_distance and distance > 20:
                possible_lilies.append(lily)

        if possible_lilies:
            if frog.direction == 'right':
                next_lily = max(possible_lilies, key=lambda l: l.pos().x())
            else:
                next_lily = min(possible_lilies, key=lambda l: l.pos().x())
            return next_lily.pos()
        
        return None
    
    def update_frog_position(self):
        if self.is_paused:
            return

        for frog in self.frogs:
            next_position = self.find_next_lily_pad(frog)

            if next_position:
                jumped_lily = None
                for lily in self.lilies:
                    if lily.pos() == next_position:
                        jumped_lily = lily
                        break
                    
                self.draw_path(frog.pos(), next_position)
                frog.crazy_jump(next_position)

                if self.previous_lily_pad:
                    if self.previous_lily_pad in self.lilies:
                        self.previous_lily_pad.strength -= frog.weight
                        if self.previous_lily_pad.strength <= 0:
                            self.scene.removeItem(self.previous_lily_pad)
                            self.lilies.remove(self.previous_lily_pad)

                self.previous_lily_pad = jumped_lily

            else:
                current_pos = frog.pos()
                self.draw_path(frog.pos(), current_pos)
                for lily in self.lilies:
                    if abs(lily.pos().x() - current_pos.x()) < 1:
                        frog.setPos(lily.pos().x(), lily.pos().y())
            
            if frog.direction == 'right' and frog.pos().x() >= self.right_shore:
                frog.direction = 'left'
            elif frog.direction == 'left' and frog.pos().x() <= self.left_shore:
                frog.direction = 'right'
    
    def draw_path(self, start_pos, end_pos):
        pen = QPen(QColor("blue"))
        pen.setWidth(1)
        line = self.scene.addLine(start_pos.x(), start_pos.y(), end_pos.x(), end_pos.y(), pen)
        self.lines.append(line)
    
        while len(self.lines) > self.trail_length * len(self.frogs):
            old_line = self.lines.pop(0)
            self.scene.removeItem(old_line)


if __name__ == '__main__':
    standrad = {
        "fall_speed" : 1,
        "spawn_interval" : 200,
        "lily_weight_max" : 1,
        "jump_update_interval" : 100,
        "max_lilies" : 7,
        "frog_weight" : 1,
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
