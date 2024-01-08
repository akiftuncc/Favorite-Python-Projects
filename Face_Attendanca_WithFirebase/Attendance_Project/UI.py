import sys
import cv2
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QWidget,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QGridLayout,
    QTableWidget,
    QComboBox,
    QDesktopWidget
)
from PyQt5.QtGui import QPixmap, QImage, QColor
from PyQt5.QtCore import Qt, QTimer, QAbstractAnimation, QVariantAnimation
import numpy as np
import main
import asyncio
import EncodeGenerator
import AddDataToDatabase
import main



class LoginButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMinimumSize(60, 60)

        self.color1 = QColor(240, 53, 218)
        self.color2 = QColor(61, 217, 245)

        self._animation = QVariantAnimation(
            self,
            valueChanged=self._animate,
            startValue=0.00001,
            endValue=0.9999,
            duration=250
        )

    def _animate(self, value):
        qss = """
            font: 75 10pt "Microsoft YaHei UI";
            font-weight: bold;
            color: rgb(255, 255, 255);
            border-style: solid;
            border-radius:21px;
        """
        grad = "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {color1}, stop:{value} {color2}, stop: 1.0 {color1});".format(
            color1=self.color1.name(), color2=self.color2.name(), value=value
        )
        qss += grad
        self.setStyleSheet(qss)

    def enterEvent(self, event):
        self._animation.setDirection(QAbstractAnimation.Forward)
        self._animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._animation.setDirection(QAbstractAnimation.Backward)
        self._animation.start()
        super().enterEvent(event)


class VideoStream(QMainWindow):
    def __init__(self):
        super().__init__()

        self.video_height = 1700
        self.video_width = 1500
        self.setWindowTitle("Student Tracking System")


        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.login = LoginPage()

        self.video_label = QLabel(self)
        self.video_label.setAlignment(Qt.AlignCenter)

        self.textbox = QLineEdit(self)
        self.textbox.setReadOnly(True)
        self.textbox.setAlignment(Qt.AlignCenter)

        self.push_button = LoginButton('Add/Remove Person')
        self.push_button.setGeometry(10, 1200, 300, 50)

        self.cam_button = LoginButton('Open/Close Camera')  # button for camera control
        self.cam_button.clicked.connect(self.toggle_camera)

        self.push_button.clicked.connect(self.admin_page)

        self.setStyleSheet("""
                    QWidget {
                    background-color: #FFFFFF; /* Set window background color */
                    }
                    QLineEdit {
                    background-color: #00F8FF; /* Set textbox background color */
                    border: 2px solid #4CAF50; /* Set textbox border color and width */
                    border-radius: 5px; /* Set textbox border radius */
                    padding: 5px; /* Set padding inside the textbox */
                    selection-color: white; /* Set text selection color */
                    selection-background-color: #4CAF50; /* Set text selection background color */
                    font: 75 10pt "Microsoft YaHei UI";
                    font-weight: bold;
                    color: rgb(255, 255, 255);
                    border-style: solid;
                    border-radius:21px;
                    }
                    QLabel {
                    border: 2px solid #4CAF50; /* Set border color and width */
                    border-radius: 20px; /* Set border radius */
                    padding: 20px; /* Set padding inside the label */
                    background-color: #7B64FF; /* Set background color */

                    }
                """)
        #Yerleştirme############
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.push_button)
        button_layout.addWidget(self.cam_button)

        layout_center = QVBoxLayout(self.central_widget)
        layout_center.addWidget(self.video_label)
        layout_center.addWidget(self.textbox)
        layout_center.addLayout(button_layout)  # Add the horizontal button layout


        #self.cap = cv2.VideoCapture(cv2.CAP_DSHOW)
        self.is_camera_open = False  # Flag to track the camera state


        self.closed_camera_image_path = r'C:\Users\duruk\PycharmProjects\AI_Project\Depositphotos_122104490_S.png'
        self.closed_camera_image = cv2.imread(self.closed_camera_image_path)

        self.initUI()

    def initUI(self):
        self.resizeToDesktop()

    def resizeToDesktop(self):
        desktop = QDesktopWidget()
        screenRect = desktop.availableGeometry()

        self.setGeometry(screenRect)

    def admin_page(self):
        self.close()
        self.login.show()  # Assuming you have an LoginPage

    def toggle_camera(self):
        asyncio.run(main.main())


class AdminPage(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Student Tracking System")
        self.setGeometry(0, 0, 1000, 1000)
        self.video_height = 1300
        self.video_width = 1000
        self.number = 0

        #self.videostream = VideoStream()

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        # name-surname, number, started year, grade #############################################
        self.label_name = QLabel('<font size="4"> Name/Surname </font>')
        self.lineEdit_name = QLineEdit()
        self.lineEdit_name.setPlaceholderText('Please enter your name and surname')
        self.label_number = QLabel('<font size="4"> Student Number </font>')
        self.lineEdit_number = QLineEdit()
        self.lineEdit_number.setPlaceholderText('Please enter your number')
        self.label_year = QLabel('<font size="4"> Started year </font>')
        self.lineEdit_year = QLineEdit()
        self.lineEdit_year.setPlaceholderText('Please enter the year you started school')
        self.label_grade = QLabel('<font size="4"> Grade </font>')
        self.lineEdit_grade = QLineEdit()
        self.lineEdit_grade.setPlaceholderText('Please enter the your grade')
        ###########################################################################################
        


        # Buttons
        self.return_button = LoginButton("Return STS")
        self.return_button.clicked.connect(self.return_button_clicked)
        self.add_button = LoginButton("Add")
        self.add_button.clicked.connect(lambda: self.add_button_clicked())
        self.encode_button = LoginButton("Encode")
        self.encode_button.clicked.connect(self.encode_button_click)
        self.attendance_button = LoginButton("Attendance")
        self.attendance_button.clicked.connect(self.attendance_button_click)
        self.take_pic_button = LoginButton("Take Picture")
        self.take_pic_button.clicked.connect(self.take_pic_button_click)


        self.setStyleSheet("""
            background-color: #0000FF;
            QLineEdit {
                background-color: #0000FF; /* TextBox arka plan rengi */
                border: 2px solid #4CAF50; /* Kenarlık rengi ve genişliği */
                border-radius: 5px; /* Kenarlık köşe yuvarlatma */
                padding: 5px; /* İçerik kenarlık arasındaki boşluk */
                selection-color: white; /* Seçili metin rengi */
                selection-background-color: #4CAF50; /* Seçili metin arka plan rengi */
                font: 75 10pt "Microsoft YaHei UI"; /* Yazı tipi ve boyutu */
                font-weight: bold; /* Yazı kalınlığı */
                color: rgb(255, 255, 255); /* Yazı rengi */
                border-style: solid; /* Kenarlık stili */
                border-radius: 21px; /* Kenarlık köşe yuvarlatma */
            }

            """
                           )

        #self.video_label.setStyleSheet("""
        #QLabel {
        #border: 2px solid #4CAF50; /* Kenarlık rengi ve genişliği */
        #border-radius: 20px; /* Kenarlık köşe yuvarlatma */
        #padding: 20px; /* İçerik kenarlık arasındaki boşluk */
        #background-color: #7B64FF; /* Arka plan rengi */
        #        }
        #""")

        # Butonların stilini değiştirmek için QSS (Qt Style Sheet) kullanımı
        self.button_style = """
            QPushButton {
                background-color: #4CAF50; /* Yeşil arkaplan rengi */
                color: white; /* Beyaz metin rengi */
                border: 2px solid #4CAF50; /* Yeşil kenarlık */
                border-radius: 50px; /* Kenarlık köşe yuvarlatma */
                padding: 5px 10px; /* İçerik kenarlık arasındaki boşluk */
                font-weight : bold;
                font: 75 10pt "Microsoft YaHei UI";
                border-style: solid;
                border-radius:21px;
            }

            QPushButton:hover {
                background-color: #45A049; /* üzerine gelindiğinde rengi */
            }

            QPushButton:pressed {
                background-color: #3e8e41; /* Basıldığında rengi */
            }
        """

        # Stil bilgisini butonlara uygula
        #self.return_button.setStyleSheet(button_style)
        #self.add_button.setStyleSheet(button_style)
        #self.encode_button.setStyleSheet(button_style)
        #self.attendance_button.setStyleSheet(button_style)

        ######  Layout  ############################################
        '''
        self.layout = QGridLayout()
        self.layout.addWidget(self.label_name, 0, 0)
        self.layout.addWidget(self.lineEdit_name, 0, 1)
        self.layout.addWidget(self.label_number, 1, 0)
        self.layout.addWidget(self.lineEdit_number, 1, 1)
        self.layout.addWidget(self.label_year, 2, 0)
        self.layout.addWidget(self.lineEdit_year, 2, 1)
        self.layout.addWidget(self.label_grade, 3, 0)
        self.layout.addWidget(self.lineEdit_grade, 3, 1)

        self.ret_cam_buttons = QVBoxLayout()
        self.ret_cam_buttons.addWidget(self.return_button)
        self.ret_cam_buttons.addWidget(self.attendance_button)

        self.ad_update_buttons = QVBoxLayout()
        self.ad_update_buttons.addWidget(self.add_button)
        self.ad_update_buttons.addWidget(self.encode_button)

        self.buttons = QHBoxLayout()
        self.buttons.addLayout(self.ret_cam_buttons)
        self.buttons.addLayout(self.ad_update_buttons)

        self.down = QHBoxLayout()
        self.down.addLayout(self.buttons)
        self.down.addLayout(self.layout)

        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.addWidget(self.video_label)
        self.main_layout.addLayout(self.down)
        '''
        self.ret_cam_buttons = QVBoxLayout()
        self.ret_cam_buttons.addWidget(self.return_button)
        self.ret_cam_buttons.addWidget(self.attendance_button)

        self.ad_update_buttons = QVBoxLayout()
        self.ad_update_buttons.addWidget(self.add_button)
        self.ad_update_buttons.addWidget(self.encode_button)
        self.ad_update_buttons.addWidget(self.take_pic_button)

        self.buttons = QHBoxLayout()
        self.buttons.addLayout(self.ret_cam_buttons)
        self.buttons.addStretch()  # Add stretch to create space between the two button groups
        self.buttons.addLayout(self.ad_update_buttons)

        self.layout = QGridLayout()
        self.layout.addWidget(self.label_name, 0, 0)
        self.layout.addWidget(self.lineEdit_name, 0, 1)
        self.layout.addWidget(self.label_number, 1, 0)
        self.layout.addWidget(self.lineEdit_number, 1, 1)
        self.layout.addWidget(self.label_year, 2, 0)
        self.layout.addWidget(self.lineEdit_year, 2, 1)
        self.layout.addWidget(self.label_grade, 3, 0)
        self.layout.addWidget(self.lineEdit_grade, 3, 1)

        self.down = QVBoxLayout()
        self.down.addLayout(self.layout)
        self.down.addLayout(self.buttons)

        self.main_layout = QVBoxLayout(self.centralWidget())
        self.main_layout.addLayout(self.down)


        ###################################################################################
        

        self.initUI()

    def initUI(self):
        self.resizeToDesktop()

    def resizeToDesktop(self):
        desktop = QDesktopWidget()
        screenRect = desktop.availableGeometry()

        self.setGeometry(screenRect)

    def return_button_clicked(self):
        self.close()
        #self.videostream.show()

    def add_button_clicked(self):
        name = self.lineEdit_name.text()
        number = self.lineEdit_number.text()
        major = self.lineEdit_grade.text()
        year = self.lineEdit_year.text()
        print("ooo: ", name,number,major,year)
        AddDataToDatabase.data_creator(name, number, major, year)
        self.number = number
        
        

    def encode_button_click(self):
        EncodeGenerator.encode_event()

    def attendance_button_click(self):
        pass

    def take_pic_button_click(self):
        AddDataToDatabase.take_pic(self.number)


class LoginPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login Page')
        self.setGeometry(400, 400, 500, 500)

        self.stream = AdminPage()

        layout = QGridLayout()
        label_name = QLabel('<font size="4"> Username </font>')
        self.lineEdit_username = QLineEdit()
        self.lineEdit_username.setPlaceholderText('Please enter your username')
        layout.addWidget(label_name, 0, 0)
        layout.addWidget(self.lineEdit_username, 0, 1)

        label_password = QLabel('<font size="4"> Password </font>')
        self.lineEdit_password = QLineEdit()
        self.lineEdit_password.setPlaceholderText('Please enter your password')
        self.lineEdit_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(label_password, 1, 0)
        layout.addWidget(self.lineEdit_password, 1, 1)

        self.setStyleSheet("""
                    QWidget
                {
                    background - color:  # FFFFFF; /* Set window background color */
                    border: 2px solid #4CAF50; /* Set textbox border color and width */
                    border-radius: 5px; /* Set textbox border radius */
                    padding: 5px; /* Set padding inside the textbox */
                    selection-color: white; /* Set text selection color */
                    selection-background-color: #4CAF50; /* Set text selection background color */
                }
                    QLabel {
                            border: 2px solid #4CAF50; /* Set border color and width */
                            border-radius: 20px; /* Set border radius */
                            padding: 20px; /* Set padding inside the label */
                            background-color: #7B64FF; /* Set background color */
                            }
                    QLineEdit {
                                background-color: #0000FF; /* Set textbox background color */
                                border: 2px solid #4CAF50; /* Set textbox border color and width */
                                border-radius: 5px; /* Set textbox border radius */
                                padding: 5px; /* Set padding inside the textbox */
                                selection-color: white; /* Set text selection color */
                                selection-background-color: #4CAF50; /* Set text selection background color */
                                font: 75 10pt "Microsoft YaHei UI";
                                font-weight: bold;
                                color: rgb(255, 255, 255);
                                border-style: solid;
                                border-radius:21px;
                                }
                """)

        # Using LoginButton instead of QPushButton
        button_login = LoginButton('Login')
        button_login.clicked.connect(self.check_password)
        layout.addWidget(button_login, 2, 0, 1, 2)
        layout.setRowMinimumHeight(2, 75)

        self.setLayout(layout)

    def check_password(self):
        msg = QMessageBox()

        if self.lineEdit_username.text() == '' or self.lineEdit_password.text() == '':
            msg.setWindowTitle('Wrong Password')
            msg.setText("Fill Blanks")
            msg.exec_()

        elif self.lineEdit_username.text() == 'asd' and self.lineEdit_password.text() == 'asd':
            self.close()  # Close the login window upon successful login
            self.open_video_stream()
        else:
            msg.setText('Incorrect Username or Password')
            msg.exec_()

    def open_video_stream(self):
        self.stream.show()  # VideoStream is called. VideoStream is defined in __init__ method.


if __name__ == '__main__':
    app = QApplication(sys.argv)
    video_stream_window = VideoStream()
    video_stream_window.show()
    sys.exit(app.exec_())