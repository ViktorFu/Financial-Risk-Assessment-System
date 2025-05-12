from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                            QLineEdit, QPushButton, QRadioButton, QFormLayout,
                            QGroupBox, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal

class LoginWindow(QWidget):
    login_success = pyqtSignal(str, bool)

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.initUI()

    def initUI(self):
        self.setWindowTitle('User Management System - Login')
        self.setGeometry(300, 300, 350, 250)

        layout = QVBoxLayout()

        # Form layout
        form_layout = QFormLayout()

        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        form_layout.addRow('Username:', self.username_input)
        form_layout.addRow('Password:', self.password_input)

        # Radio button group
        role_group = QGroupBox("Login Type")
        role_layout = QHBoxLayout()

        self.user_radio = QRadioButton("Regular User")
        self.admin_radio = QRadioButton("Administrator")
        self.user_radio.setChecked(True)

        role_layout.addWidget(self.user_radio)
        role_layout.addWidget(self.admin_radio)
        role_group.setLayout(role_layout)

        # Login button
        self.login_button = QPushButton('Login')
        self.login_button.clicked.connect(self.login)

        layout.addLayout(form_layout)
        layout.addWidget(role_group)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        is_admin = self.admin_radio.isChecked()

        if not username or not password:
            QMessageBox.warning(self, 'Warning', 'Username and password cannot be empty!')
            return

        # Use controller to handle login
        result = self.controller.login(username, password, is_admin)
        if result:
            self.login_success.emit(username, is_admin)
            self.close()
