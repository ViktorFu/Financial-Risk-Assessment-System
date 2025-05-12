from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                           QLineEdit, QPushButton, QFormLayout, QFrame,
                           QGroupBox, QMessageBox, QTableWidget, QTableWidgetItem,
                           QHeaderView, QRadioButton, QButtonGroup, QComboBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont

class UserManagementTab(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.initUI()

    def initUI(self):
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                color: #333333;
                font-family: Arial, sans-serif;
            }
            QLabel {
                font-size: 13px;
                color: #333333;
            }
            QLineEdit {
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 5px;
                background: white;
                min-height: 25px;
            }
            QPushButton {
                background-color: #3e89fa;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2d7bf0;
            }
            QPushButton#secondaryButton {
                background-color: #f8f9fa;
                color: #333;
                border: 1px solid #ddd;
            }
            QPushButton#operationButton {
                background-color: #f8f9fa;
                color: #3e89fa;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 12px;
                min-width: 50px;
            }
            QPushButton#deleteButton {
                background-color: #f8d7da;
                color: #dc3545;
                border: 1px solid #f5c6cb;
            }
            QTableWidget {
                border: 1px solid #e0e0e0;
                gridline-color: #f0f0f0;
                selection-background-color: #e6f2ff;
                selection-color: #333333;
            }
            QHeaderView::section {
                background-color: #f8f8f8;
                color: #666666;
                padding: 5px;
                border: none;
                border-right: 1px solid #e0e0e0;
                border-bottom: 1px solid #e0e0e0;
            }
            QFrame#statusFrame {
                background-color: #f2f8fd;
                border-radius: 4px;
                border: 1px solid #d6e9f8;
                margin: 5px;
                padding: 10px;
            }
            QRadioButton {
                spacing: 5px;
            }
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
                border-radius: 9px;
                border: 2px solid #ccc;
            }
            QRadioButton::indicator:checked {
                background-color: #3e89fa;
                border: 2px solid white;
                border-radius: 9px;
            }
        """)

        layout = QVBoxLayout()
        
        # Filter area
        filter_layout = QHBoxLayout()
        
        # Username search
        self.username_search = QLineEdit()
        self.username_search.setPlaceholderText("Search username")
        self.username_search.setFixedWidth(200)
        filter_layout.addWidget(self.username_search)
        
        # Role filter
        filter_layout.addWidget(QLabel("Role:"))
        self.role_filter = QComboBox()
        self.role_filter.addItems(["All", "Admin", "Regular user"])
        self.role_filter.setFixedWidth(120)
        filter_layout.addWidget(self.role_filter)
        
        # Search button
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_users)  # Modified to call search_users method
        filter_layout.addWidget(self.search_button)
        
        # Reset button
        self.reset_button = QPushButton("Reset")
        self.reset_button.setObjectName("secondaryButton")
        self.reset_button.clicked.connect(self.reset_search)  # Added reset button
        filter_layout.addWidget(self.reset_button)
        
        filter_layout.addStretch()
        
        # Status info box
        self.status_frame = QFrame()
        self.status_frame.setObjectName("statusFrame")
        status_layout = QHBoxLayout()
        
        status_icon = QLabel("●")
        status_icon.setStyleSheet("color: #4aa3df;")
        status_layout.addWidget(status_icon)
        
        self.status_text = QLabel("User management system started, currently there are 0 users.")
        status_layout.addWidget(self.status_text)
        status_layout.addStretch()
        
        self.status_frame.setLayout(status_layout)
        
        # User table
        self.user_table = QTableWidget()
        self.user_table.setColumnCount(7)
        self.user_table.setHorizontalHeaderLabels(['ID', 'Username', 'Is Admin', 'Full Name', 'Email', 'Phone', 'Actions'])
        self.user_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.user_table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        self.user_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.user_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.user_table.setAlternatingRowColors(True)
        self.user_table.setStyleSheet("QTableWidget { alternate-background-color: #f9f9f9; }")

        # Create an empty row to display "No matching results"
        self.no_results_label = QLabel("No matching user records found")
        self.no_results_label.setAlignment(Qt.AlignCenter)
        self.no_results_label.setStyleSheet("color: #666; font-size: 14px; margin: 20px;")
        self.no_results_label.hide()  # Initially hidden

        # Load user data
        self.load_users()

        # Add/Edit user form area
        form_frame = QFrame()
        form_frame.setObjectName("statusFrame")
        form_layout = QVBoxLayout()
        
        # Form title
        form_title = QLabel("Add/Edit User")
        form_title.setStyleSheet("font-weight: bold; font-size: 14px; margin-bottom: 10px;")
        form_layout.addWidget(form_title)
        
        # Form content
        form_grid = QFormLayout()
        
        # ID
        self.user_id_input = QLineEdit()
        self.user_id_input.setReadOnly(True)
        self.user_id_input.setPlaceholderText('Leave blank when adding new user')
        form_grid.addRow("ID:", self.user_id_input)
        
        # Username
        self.new_username_input = QLineEdit()
        form_grid.addRow("Username:", self.new_username_input)
        
        # Password
        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.Password)
        form_grid.addRow("Password:", self.new_password_input)
        
        # Is Admin
        admin_widget = QWidget()
        admin_layout = QHBoxLayout(admin_widget)
        admin_layout.setContentsMargins(0, 0, 0, 0)
        
        self.is_admin_radio_group = QButtonGroup(self)
        self.admin_yes = QRadioButton("Yes")
        self.admin_no = QRadioButton("No")
        self.admin_no.setChecked(True)
        self.is_admin_radio_group.addButton(self.admin_yes)
        self.is_admin_radio_group.addButton(self.admin_no)
        
        admin_layout.addWidget(self.admin_yes)
        admin_layout.addWidget(self.admin_no)
        admin_layout.addStretch()
        
        form_grid.addRow("Is Admin:", admin_widget)
        
        # Full Name
        self.new_fullname_input = QLineEdit()
        form_grid.addRow("Full Name:", self.new_fullname_input)
        
        # Email
        self.new_email_input = QLineEdit()
        form_grid.addRow("Email:", self.new_email_input)
        
        # Phone
        self.new_phone_input = QLineEdit()
        form_grid.addRow("Phone:", self.new_phone_input)
        
        form_layout.addLayout(form_grid)
        
        # Form buttons
        button_layout = QHBoxLayout()
        
        self.add_button = QPushButton('Add')
        self.add_button.clicked.connect(self.add_user)
        
        self.update_button = QPushButton('Update')
        self.update_button.clicked.connect(self.update_user)
        
        self.delete_button = QPushButton('Delete')
        self.delete_button.setObjectName("deleteButton")
        self.delete_button.clicked.connect(self.delete_user)
        
        self.clear_button = QPushButton('Clear Form')
        self.clear_button.setObjectName("secondaryButton")
        self.clear_button.clicked.connect(self.clear_form)
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.clear_button)
        
        form_layout.addLayout(button_layout)
        form_frame.setLayout(form_layout)
        
        # Table selection event
        self.user_table.itemSelectionChanged.connect(self.on_user_selected)

        # Bottom pagination
        pagination_layout = QHBoxLayout()
        pagination_layout.addStretch()
        
        self.prev_page_btn = QPushButton("<")
        self.page_1_btn = QPushButton("1")
        self.page_1_btn.setStyleSheet("background-color: #3e89fa; color: white;")
        self.page_2_btn = QPushButton("2")
        
        for btn in [self.prev_page_btn, self.page_1_btn, self.page_2_btn]:
            btn.setFixedSize(32, 32)
            if btn != self.page_1_btn:
                btn.setStyleSheet("background-color: white; color: #333; border: 1px solid #ddd;")
            pagination_layout.addWidget(btn)
        
        pagination_layout.addStretch()

        # Add all widgets to main layout
        layout.addLayout(filter_layout)
        layout.addWidget(self.status_frame)
        layout.addWidget(self.user_table)
        layout.addWidget(self.no_results_label)  # Add no matching results label
        layout.addWidget(form_frame)
        layout.addLayout(pagination_layout)

        self.setLayout(layout)
        
        # Save all user data for filtering
        self.all_users = []

    def load_users(self):
        """Load all user data"""
        self.user_table.setRowCount(0)
        
        # Get actual data
        self.all_users = self.controller.get_all_users()
        
        # Update status bar display
        self.status_text.setText(f"User management system started, currently there are {len(self.all_users)} users.")
        
        # Display all users
        self.display_users(self.all_users)

    def display_users(self, users):
        """Display the user list in the table"""
        self.user_table.setRowCount(0)
        
        if not users:
            # Display no matching results
            self.user_table.hide()
            self.no_results_label.show()
            return
        
        # Has results, ensure table is shown, no matching label is hidden
        self.user_table.show()
        self.no_results_label.hide()
        
        for row_num, row_data in enumerate(users):
            self.user_table.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                if col_num == 2:  # is_admin column
                    data = 'Yes' if data else 'No'
                item = QTableWidgetItem(str(data))
                item.setTextAlignment(Qt.AlignCenter)
                
                # Set color for admin indicator
                if col_num == 2:  # is_admin column
                    if data == 'Yes':
                        item.setForeground(QColor(40, 167, 69))  # Green
                        item.setBackground(QColor(240, 255, 240))  # Light green background
                    else:
                        item.setForeground(QColor(108, 117, 125))  # Gray
                
                self.user_table.setItem(row_num, col_num, item)
            
            # Add action buttons
            operations_widget = QWidget()
            operations_layout = QHBoxLayout(operations_widget)
            operations_layout.setContentsMargins(0, 0, 0, 0)
            operations_layout.setSpacing(5)
            
            edit_btn = QPushButton("Edit")
            edit_btn.setObjectName("operationButton")
            edit_btn.clicked.connect(lambda checked, row=row_num: self.edit_user(row))
            
            delete_btn = QPushButton("Delete")
            delete_btn.setObjectName("deleteButton")
            delete_btn.clicked.connect(lambda checked, row=row_num: self.delete_user_from_table(row))
            
            operations_layout.addWidget(edit_btn)
            operations_layout.addWidget(delete_btn)
            operations_layout.addStretch()
            
            self.user_table.setCellWidget(row_num, 6, operations_widget)

    def search_users(self):
        """Filter users based on search criteria"""
        username_query = self.username_search.text().strip().lower()
        role_query = self.role_filter.currentText()
        
        # Filter results
        filtered_users = []
        
        for user in self.all_users:
            # Username match check
            username_match = True
            if username_query:
                username_match = username_query in str(user[1]).lower()
            
            # Role match check
            role_match = True
            if role_query != "All":
                is_admin = bool(user[2])  # Assuming user[2] stores boolean or 0/1
                role_match = (role_query == "Admin" and is_admin) or (role_query == "Regular user" and not is_admin)
            
            # Add only if both conditions are met
            if username_match and role_match:
                filtered_users.append(user)
        
        # Display filtered results
        self.display_users(filtered_users)
        
        # Update status bar with filtered results count
        if filtered_users:
            self.status_text.setText(f"Search results: Found {len(filtered_users)} matching users.")
        else:
            self.status_text.setText("Search results: No matching user records found.")

    def reset_search(self):
        """Reset search criteria and display all users"""
        self.username_search.clear()
        self.role_filter.setCurrentIndex(0)  # Set to "All"
        self.load_users()  # Reload all users

    def edit_user(self, row):
        """Edit user triggered from table edit button"""
        self.user_table.selectRow(row)
        self.on_user_selected()

    def delete_user_from_table(self, row):
        """Delete user triggered from table delete button"""
        self.user_table.selectRow(row)
        self.on_user_selected()
        self.delete_user()

    def on_user_selected(self):
        selected_rows = self.user_table.selectedItems()
        if not selected_rows:
            return

        row = selected_rows[0].row()
        user_id = self.user_table.item(row, 0).text()
        username = self.user_table.item(row, 1).text()
        is_admin = self.user_table.item(row, 2).text() == 'Yes'
        full_name = self.user_table.item(row, 3).text()
        email = self.user_table.item(row, 4).text()
        phone = self.user_table.item(row, 5).text()

        # Fill the form
        self.user_id_input.setText(user_id)
        self.new_username_input.setText(username)
        self.new_password_input.setText('')  # Don't show password for security
        self.admin_yes.setChecked(is_admin)
        self.admin_no.setChecked(not is_admin)
        self.new_fullname_input.setText(full_name)
        self.new_email_input.setText(email)
        self.new_phone_input.setText(phone)

    def add_user(self):
        username = self.new_username_input.text()
        password = self.new_password_input.text()
        is_admin = 1 if self.admin_yes.isChecked() else 0
        full_name = self.new_fullname_input.text()
        email = self.new_email_input.text()
        phone = self.new_phone_input.text()

        if not username or not password:
            QMessageBox.warning(self, 'Warning', 'Username and password cannot be empty!')
            return

        result = self.controller.add_user(username, password, is_admin, full_name, email, phone)
        
        if result:
            QMessageBox.information(self, 'Success', 'User added successfully!')
            self.clear_form()
            self.load_users()  # Refresh user list
            
            # If there are search criteria, refresh search results
            if self.username_search.text() or self.role_filter.currentText() != "All":
                self.search_users()
        else:
            QMessageBox.warning(self, 'Warning', 'Username already exists!')

    def update_user(self):
        user_id = self.user_id_input.text()
        if not user_id:
            QMessageBox.warning(self, 'Warning', 'Please select a user to update first!')
            return

        username = self.new_username_input.text()
        password = self.new_password_input.text()
        is_admin = 1 if self.admin_yes.isChecked() else 0
        full_name = self.new_fullname_input.text()
        email = self.new_email_input.text()
        phone = self.new_phone_input.text()

        if not username:
            QMessageBox.warning(self, 'Warning', 'Username cannot be empty!')
            return

        result = self.controller.update_user(user_id, username, password, is_admin, full_name, email, phone)
        
        if result:
            QMessageBox.information(self, 'Success', 'User information updated successfully!')
            self.clear_form()
            self.load_users()  # Refresh user list
            
            # If there are search criteria, refresh search results
            if self.username_search.text() or self.role_filter.currentText() != "All":
                self.search_users()
        else:
            QMessageBox.warning(self, 'Warning', 'Username already exists!')

    def delete_user(self):
        user_id = self.user_id_input.text()
        if not user_id:
            QMessageBox.warning(self, 'Warning', 'Please select a user to delete first!')
            return

        username = self.new_username_input.text()

        # Confirm deletion
        reply = QMessageBox.question(self, 'Confirm Deletion',
                                    f'Are you sure you want to delete user {username}? This action cannot be undone!',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.controller.delete_user(user_id)
            QMessageBox.information(self, 'Success', 'User deleted successfully!')
            self.clear_form()
            self.load_users()  # Refresh user list
            
            # If there are search criteria, refresh search results
            if self.username_search.text() or self.role_filter.currentText() != "All":
                self.search_users()

    def clear_form(self):
        self.user_id_input.clear()
        self.new_username_input.clear()
        self.new_password_input.clear()
        self.admin_no.setChecked(True)
        self.new_fullname_input.clear()
        self.new_email_input.clear()
        self.new_phone_input.clear()
        self.user_table.clearSelection()