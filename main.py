import os.path
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QFileDialog, \
    QMessageBox, QFormLayout, QProgressBar
from PyQt5.QtCore import Qt, QTimer
from distutils.dir_util import copy_tree

LOCAL_INPUT_PATH = os.path.join(os.getcwd(), "input")


class ObjectDetectionLabeler(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Python Object Detection Auto Labeler")
        self.setGeometry(0, 0, 600, 200)
        self.center_on_screen()

        self.init_ui()

    def center_on_screen(self):
        screen_geometry = QApplication.desktop().availableGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

    def init_ui(self):
        # Giriş alanları ve butonlar
        self.image_path_input = QLineEdit(self)
        self.output_path_input = QLineEdit(self)
        self.max_angle_input = QLineEdit(self)
        self.rotate_angle_input = QLineEdit(self)

        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.start_process)

        # Progress Bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(0, 0, 300, 25)
        self.progress_bar.setAlignment(Qt.AlignCenter)

        # Giriş alanlarını düzenle
        form_layout = QFormLayout()
        form_layout.addRow("Input Image Path:", self.image_path_input)
        form_layout.addRow("Output Path:", self.output_path_input)
        form_layout.addRow("Max Angle:", self.max_angle_input)
        form_layout.addRow("Rotate Angle:", self.rotate_angle_input)

        # Ana düzen
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.start_button)
        main_layout.addWidget(self.progress_bar)

        self.setLayout(main_layout)

        # Timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer_value = 0

    def input_validator(self, input_image_path, output_path, max_angle, rotate_angle):
        if not os.path.exists(input_image_path):
            return False

        if not os.path.exists(output_path):
            return False

        if int(max_angle) < 0 or int(max_angle) > 360:
            return False

        if int(rotate_angle) < 0 or int(rotate_angle) > 360:
            return False

        return True

    def start_process(self):
        input_image_path = self.image_path_input.text()
        output_path = self.output_path_input.text()
        max_angle = self.max_angle_input.text()
        rotate_angle = self.rotate_angle_input.text()

        # validator
        if self.input_validator(input_image_path, output_path, max_angle, rotate_angle):
            from app.main import start_process

            # copy input directory to local input directory
            copy_tree(input_image_path, LOCAL_INPUT_PATH)

            start_process(LOCAL_INPUT_PATH, output_path, int(max_angle), int(rotate_angle))
            self.timer_value = 0
            self.timer.start(1000)

        # clear inside of input directory
        files_in_dir = os.listdir(LOCAL_INPUT_PATH)

        for file in files_in_dir:
            os.remove(f'{LOCAL_INPUT_PATH}/{file}')

    def update_progress(self):
        self.timer_value += 1
        self.progress_bar.setValue(int((self.timer_value / 60) * 100))

        if self.timer_value == 60:
            self.timer.stop()
            self.progress_bar.setValue(100)
            QMessageBox.information(self, "Info", "Object detection processing completed!")


if __name__ == '__main__':
    if not os.path.exists(LOCAL_INPUT_PATH):
        os.makedirs(LOCAL_INPUT_PATH)

    app = QApplication(sys.argv)
    window = ObjectDetectionLabeler()
    window.show()
    sys.exit(app.exec_())
