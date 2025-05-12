from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                            QFormLayout, QGroupBox, QMessageBox)

class UserInfoWindow(QWidget):
    def __init__(self, username, controller):
        super().__init__()
        self.username = username
        self.controller = controller
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f'User Info - {self.username}')
        self.setGeometry(300, 300, 400, 300)

        layout = QVBoxLayout()

        # Load user information
        user_info = self.controller.get_user_info(self.username)
        
        if user_info:
            full_name, email, phone = user_info

            form = QFormLayout()
            form.addRow('Username:', QLabel(self.username))
            form.addRow('Full Name:', QLabel(full_name))
            form.addRow('Email:', QLabel(email))
            form.addRow('Phone:', QLabel(phone))

            info_group = QGroupBox("Personal Information")
            info_group.setLayout(form)
            layout.addWidget(info_group)

            # Logout button
            self.logout_button = QPushButton('Log Out')
            self.logout_button.clicked.connect(self.close)
            layout.addWidget(self.logout_button)

            self.setLayout(layout)
        else:
            QMessageBox.critical(self, 'Error', 'Failed to load user information!')
            self.close()
