from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                           QLineEdit, QPushButton, QFormLayout, QFrame,
                           QGroupBox, QMessageBox, QTableWidget, QTableWidgetItem,
                           QHeaderView, QComboBox, QFileDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
import os

class ModelManagementTab(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.model_file_data = None
        self.model_file_name = ""
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
            QLineEdit, QComboBox {
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
                min-width: 60px;
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
            QLabel#statusLabel {
                color: #4aa3df;
                font-weight: bold;
                margin: 5px;
            }
        """)
        
        # Create main layout
        layout = QVBoxLayout()
        
        # Create tabs
        self.tab_layout = QHBoxLayout()
        self.model_tab_btn = QPushButton("Model Management")
        self.model_tab_btn.setStyleSheet("""
            background-color: white;
            color: #333;
            border: none;
            border-bottom: 2px solid #3e89fa;
            border-radius: 0;
            padding: 10px 15px;
            font-weight: bold;
        """)
        
        self.error_tab_btn = QPushButton("Model Errors")
        self.error_tab_btn.setStyleSheet("""
            background-color: white;
            color: #333;
            border: none;
            border-bottom: 1px solid #e0e0e0;
            border-radius: 0;
            padding: 10px 15px;
        """)
        
        self.error_tab_btn.clicked.connect(self.show_error_tab)
        self.model_tab_btn.clicked.connect(self.show_model_tab)
        
        self.tab_layout.addWidget(self.model_tab_btn)
        self.tab_layout.addWidget(self.error_tab_btn)
        self.tab_layout.addStretch()
        
        # Filter area
        filter_layout = QHBoxLayout()
        
        # Model name search
        self.model_name_search = QLineEdit()
        self.model_name_search.setPlaceholderText("Search model name")
        self.model_name_search.setFixedWidth(200)
        filter_layout.addWidget(self.model_name_search)
        
        # Environment filter
        filter_layout.addWidget(QLabel("Environment:"))
        self.env_filter = QComboBox()
        self.env_filter.addItems(["All", "development", "testing", "production"])
        self.env_filter.setFixedWidth(150)
        filter_layout.addWidget(self.env_filter)
        
        # Verification status filter
        filter_layout.addWidget(QLabel("Status:"))
        self.status_filter = QComboBox()
        self.status_filter.addItems(["All", "Verified", "Unverified"])
        self.status_filter.setFixedWidth(150)
        filter_layout.addWidget(self.status_filter)
        
        # Search button
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.load_models)
        
        # Reset button
        self.reset_button = QPushButton("Reset")
        self.reset_button.setObjectName("secondaryButton")
        self.reset_button.clicked.connect(self.reset_filters)
        
        filter_layout.addWidget(self.search_button)
        filter_layout.addWidget(self.reset_button)
        filter_layout.addStretch()
        
        # Status info frame
        status_frame = QFrame()
        status_frame.setObjectName("statusFrame")
        status_layout = QHBoxLayout()
        
        status_icon = QLabel("●")
        status_icon.setStyleSheet("color: #4aa3df;")
        status_layout.addWidget(status_icon)
        
        status_text = QLabel("Model management system started. There are 3 models.")
        status_layout.addWidget(status_text)
        status_layout.addStretch()
        
        status_frame.setLayout(status_layout)
        
        # Model table
        self.model_table = QTableWidget()
        self.model_table.setColumnCount(10)  # Add one column for action buttons
        self.model_table.setHorizontalHeaderLabels([
            'ID', 'Model Name', 'Version', 'Environment', 'Caller', 'Approver',
            'Verified', 'Rolled Back', 'Created At', 'Actions'
        ])
        self.model_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.model_table.horizontalHeader().setSectionResizeMode(9, QHeaderView.ResizeToContents)  # Actions column auto-size
        self.model_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.model_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.model_table.setAlternatingRowColors(True)
        self.model_table.setStyleSheet("QTableWidget { alternate-background-color: #f9f9f9; }")
        
        # Load model data
        self.load_models()
        
        # Add model area
        add_model_frame = QFrame()
        add_model_frame.setObjectName("statusFrame")
        add_layout = QVBoxLayout()
        
        # Add model title
        add_title = QLabel("Add Model")
        add_title.setStyleSheet("font-weight: bold; font-size: 14px; margin-bottom: 10px;")
        add_layout.addWidget(add_title)
        
        # Add model form
        form_layout = QFormLayout()
        
        # Model name
        self.model_name_input = QLineEdit()
        form_layout.addRow("Model Name:", self.model_name_input)
        
        # Version
        self.model_version_input = QLineEdit()
        self.model_version_input.setPlaceholderText("e.g.: 1.0.0")
        form_layout.addRow("Version:", self.model_version_input)
        
        # Environment
        self.environment_combo = QComboBox()
        self.environment_combo.addItems(['development', 'testing', 'production'])
        form_layout.addRow("Environment:", self.environment_combo)
        
        # Approver
        self.approver_input = QLineEdit()
        form_layout.addRow("Approver:", self.approver_input)
        
        # Model file
        file_layout = QHBoxLayout()
        self.file_path_label = QLabel("No file selected")
        self.file_select_button = QPushButton("Select Model File")
        self.file_select_button.setObjectName("secondaryButton")
        self.file_select_button.clicked.connect(self.select_model_file)
        
        file_layout.addWidget(self.file_path_label)
        file_layout.addWidget(self.file_select_button)
        
        form_layout.addRow("Model File:", file_layout)
        
        add_layout.addLayout(form_layout)
        
        # Add model button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.add_model_button = QPushButton("+ New")
        self.add_model_button.clicked.connect(self.add_model)
        
        button_layout.addWidget(self.add_model_button)
        add_layout.addLayout(button_layout)
        
        add_model_frame.setLayout(add_layout)
        
        # Model operation buttons
        operation_layout = QHBoxLayout()
        
        self.verify_button = QPushButton('Mark as Verified')
        self.verify_button.setObjectName("operationButton")
        self.verify_button.clicked.connect(self.toggle_verified)
        
        self.rollback_button = QPushButton('Rollback Model')
        self.rollback_button.setObjectName("operationButton")
        self.rollback_button.clicked.connect(self.toggle_rollback)
        
        self.refresh_button = QPushButton('Refresh')
        self.refresh_button.setObjectName("operationButton")
        self.refresh_button.clicked.connect(self.load_models)
        
        operation_layout.addWidget(self.verify_button)
        operation_layout.addWidget(self.rollback_button)
        operation_layout.addWidget(self.refresh_button)
        operation_layout.addStretch()
        
        # Pagination at bottom
        pagination_layout = QHBoxLayout()
        pagination_layout.addStretch()
        
        self.prev_page_btn = QPushButton("<")
        self.page_1_btn = QPushButton("1")
        self.page_1_btn.setStyleSheet("background-color: #3e89fa; color: white;")
        
        for btn in [self.prev_page_btn, self.page_1_btn]:
            btn.setFixedSize(32, 32)
            if btn != self.page_1_btn:
                btn.setStyleSheet("background-color: white; color: #333; border: 1px solid #ddd;")
            pagination_layout.addWidget(btn)
        
        pagination_layout.addStretch()
        
        # Error table (hidden by default)
        self.error_table = QTableWidget()
        self.error_table.setColumnCount(8)
        self.error_table.setHorizontalHeaderLabels([
            'ID', 'Model Name', 'Version', 'Environment', 'Approver',
            'Error Message', 'Exception', 'Log Time'
        ])
        self.error_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.error_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.error_table.setVisible(False)
        
        # Add widgets to main layout
        layout.addLayout(self.tab_layout)
        layout.addLayout(filter_layout)
        layout.addWidget(status_frame)
        layout.addWidget(self.model_table)
        layout.addWidget(self.error_table)
        layout.addLayout(operation_layout)
        layout.addWidget(add_model_frame)
        layout.addLayout(pagination_layout)
        
        self.setLayout(layout)
    
    def show_model_tab(self):
        """Switch to model management tab"""
        self.model_tab_btn.setStyleSheet("""
            background-color: white;
            color: #333;
            border: none;
            border-bottom: 2px solid #3e89fa;
            border-radius: 0;
            padding: 10px 15px;
            font-weight: bold;
        """)
        self.error_tab_btn.setStyleSheet("""
            background-color: white;
            color: #333;
            border: none;
            border-bottom: 1px solid #e0e0e0;
            border-radius: 0;
            padding: 10px 15px;
        """)
        self.model_table.setVisible(True)
        self.error_table.setVisible(False)
    
    def show_error_tab(self):
        """Switch to model errors tab"""
        self.error_tab_btn.setStyleSheet("""
            background-color: white;
            color: #333;
            border: none;
            border-bottom: 2px solid #3e89fa;
            border-radius: 0;
            padding: 10px 15px;
            font-weight: bold;
        """)
        self.model_tab_btn.setStyleSheet("""
            background-color: white;
            color: #333;
            border: none;
            border-bottom: 1px solid #e0e0e0;
            border-radius: 0;
            padding: 10px 15px;
        """)
        self.model_table.setVisible(False)
        self.error_table.setVisible(True)
        self.load_model_errors()
    
    def reset_filters(self):
        """Reset filters"""
        self.model_name_search.clear()
        self.env_filter.setCurrentIndex(0)
        self.status_filter.setCurrentIndex(0)
        self.load_models()
    
    def load_models(self):
        """Load model data"""
        self.model_table.setRowCount(0)
        
        # Get filter criteria
        model_name = self.model_name_search.text()
        env = self.env_filter.currentText()
        status = self.status_filter.currentText()
        
        # Fetch models
        if status == "Verified":
            models = [m for m in self.controller.get_all_models() if m[6] == 1]
        elif status == "Unverified":
            models = [m for m in self.controller.get_all_models() if m[6] == 0]
        else:
            models = self.controller.get_all_models()
        
        # Apply environment filter
        if env != "All":
            models = [m for m in models if m[3] == env]
        
        # Apply name filter
        if model_name:
            models = [m for m in models if model_name.lower() in m[1].lower()]
        
        for row_num, model in enumerate(models):
            self.model_table.insertRow(row_num)
            for col_num, data in enumerate(model):
                # Handle yes/no columns
                if col_num in [6, 7]:  # Verified, Rolled Back
                    data = 'Yes' if data else 'No'
                
                item = QTableWidgetItem(str(data))
                item.setTextAlignment(Qt.AlignCenter)
                
                # Style verification and rollback status
                if col_num == 6:  # Verified column
                    if data == 'Yes':
                        item.setBackground(QColor(240, 255, 240))
                        item.setForeground(QColor(40, 167, 69))
                    else:
                        item.setForeground(QColor(108, 117, 125))
                
                if col_num == 7:  # Rolled Back column
                    if data == 'Yes':
                        item.setBackground(QColor(255, 243, 205))
                        item.setForeground(QColor(176, 132, 0))
                
                self.model_table.setItem(row_num, col_num, item)
            
            # Add action buttons
            operations_widget = QWidget()
            operations_layout = QHBoxLayout(operations_widget)
            operations_layout.setContentsMargins(0, 0, 0, 0)
            operations_layout.setSpacing(5)
            
            is_verified = self.model_table.item(row_num, 6).text() == 'Yes'
            is_rollback = self.model_table.item(row_num, 7).text() == 'Yes'
            
            if is_verified:
                verify_btn = QPushButton("Unverify")
            else:
                verify_btn = QPushButton("Verify")
            verify_btn.setObjectName("operationButton")
            verify_btn.clicked.connect(lambda checked, row=row_num: self.toggle_verified_row(row))
            
            if is_rollback:
                rollback_btn = QPushButton("Cancel Rollback")
            else:
                rollback_btn = QPushButton("Rollback")
            rollback_btn.setObjectName("operationButton")
            rollback_btn.clicked.connect(lambda checked, row=row_num: self.toggle_rollback_row(row))
            
            operations_layout.addWidget(verify_btn)
            operations_layout.addWidget(rollback_btn)
            operations_layout.addStretch()
            
            self.model_table.setCellWidget(row_num, 9, operations_widget)

    def load_model_errors(self):
        """Load model error data"""
        self.error_table.setRowCount(0)
        
        # Fetch actual data
        errors = self.controller.get_model_errors()
        
        # Use mock data if none
        if not errors or len(errors) == 0:
            mock_data = [
                (1, "Risk Control Decision Model", "1.0.0", "development", "Li Si", "Model load failed", "NullPointerException", "2025-04-02"),
                (2, "Credit Rating Model", "0.9.5", "development", "Sun Ba", "Input data format error", "ValueError", "2025-04-05")
            ]
            errors = mock_data
        
        for row_num, error in enumerate(errors):
            self.error_table.insertRow(row_num)
            for col_num, data in enumerate(error):
                item = QTableWidgetItem(str(data if data is not None else ""))
                item.setTextAlignment(Qt.AlignCenter)
                
                # Style error and exception columns
                if col_num == 5:  # Error Message
                    item.setForeground(QColor(220, 53, 69))
                if col_num == 6:  # Exception
                    item.setForeground(QColor(176, 132, 0))
                
                self.error_table.setItem(row_num, col_num, item)
    
    def select_model_file(self):
        """Select model file"""
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select Model File", "", "All Files (*)")
        
        if file_path:
            # Read file as binary
            try:
                with open(file_path, 'rb') as file:
                    self.model_file_data = file.read()
                self.model_file_name = os.path.basename(file_path)
                self.file_path_label.setText(self.model_file_name)
            except Exception as e:
                QMessageBox.warning(self, 'Error', f'Failed to read file: {str(e)}')
                self.model_file_data = None
                self.model_file_name = ""
                self.file_path_label.setText('No file selected')
    
    def add_model(self):
        """Add new model"""
        model_name = self.model_name_input.text()
        model_version = self.model_version_input.text()
        environment = self.environment_combo.currentText()
        approver = self.approver_input.text()
        
        if not model_name or not model_version or not approver:
            QMessageBox.warning(self, 'Warning', 'Model name, version, and approver cannot be empty!')
            return
            
        if not self.model_file_data:
            QMessageBox.warning(self, 'Warning', 'Please select a model file!')
            return
        
        success = self.controller.add_model(
            model_name, self.model_file_data, model_version, 
            environment, approver
        )
        
        if success:
            QMessageBox.information(self, 'Success', 'Model added successfully!')
            self.model_name_input.clear()
            self.model_version_input.clear()
            self.approver_input.clear()
            self.model_file_data = None
            self.model_file_name = ""
            self.file_path_label.setText('No file selected')
            self.load_models()
        else:
            QMessageBox.warning(self, 'Error', 'Failed to add model!')
    
    def toggle_verified(self):
        """Toggle verification status of selected model"""
        selected_items = self.model_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, 'Warning', 'Please select a model first!')
            return
        
        row = selected_items[0].row()
        self.toggle_verified_row(row)
    
    def toggle_verified_row(self, row):
        """Toggle verification status of specified model row"""
        model_id = self.model_table.item(row, 0).text()
        current_state = self.model_table.item(row, 6).text() == 'Yes'
        
        # Set to opposite state
        new_state = not current_state
        action = "mark as verified" if new_state else "mark as unverified"
        
        reply = QMessageBox.question(
            self, 'Confirm Action',
            f'Are you sure you want to {action} this model?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success = self.controller.toggle_verified(model_id, new_state)
            
            if success:
                QMessageBox.information(self, 'Success', f'Model {action}!')
                self.load_models()
            else:
                QMessageBox.warning(self, 'Error', 'Operation failed!')
    
    def toggle_rollback(self):
        """Toggle rollback status of selected model"""
        selected_items = self.model_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, 'Warning', 'Please select a model first!')
            return
        
        row = selected_items[0].row()
        self.toggle_rollback_row(row)
    
    def toggle_rollback_row(self, row):
        """Toggle rollback status of specified model row"""
        model_id = self.model_table.item(row, 0).text()
        current_state = self.model_table.item(row, 7).text() == 'Yes'
        
        # Set to opposite state
        new_state = not current_state
        action = "rollback" if new_state else "cancel rollback"
        
        reply = QMessageBox.question(
            self, 'Confirm Action',
            f'Are you sure you want to {action} this model?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success = self.controller.toggle_rollback(model_id, new_state)
            
            if success:
                QMessageBox.information(self, 'Success', f'Model {action}!')
                self.load_models()
            else:
                QMessageBox.warning(self, 'Error', 'Operation failed!')
