from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QComboBox, QDateEdit, 
                            QTimeEdit, QCheckBox, QRadioButton, QTextEdit, 
                            QGroupBox, QFormLayout, QButtonGroup, QMessageBox)
from PyQt5.QtCore import Qt, QDate, QTime
from PyQt5.QtGui import QFont

class ModelCreationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Risk Control Model Creation")
        self.setMinimumSize(600, 650)
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                font-size: 14px;
                color: #333;
            }
            QComboBox, QDateEdit, QTimeEdit, QLineEdit, QTextEdit {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 8px;
                background: white;
                min-height: 20px;
            }
            QPushButton {
                border-radius: 4px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton#primaryButton {
                background-color: #3e89fa;
                color: white;
                border: none;
            }
            QPushButton#primaryButton:hover {
                background-color: #2d7bf0;
            }
            QPushButton#secondaryButton {
                background-color: white;
                color: #333;
                border: 1px solid #ddd;
            }
            QPushButton#secondaryButton:hover {
                background-color: #f5f5f5;
            }
            QCheckBox, QRadioButton {
                spacing: 8px;
            }
            QCheckBox::indicator, QRadioButton::indicator {
                width: 18px;
                height: 18px;
            }
            QRadioButton::indicator:checked {
                background-color: #3e89fa;
                border: 2px solid white;
                border-radius: 9px;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Model file selection
        model_form = QFormLayout()
        
        # Model file
        self.model_file_combo = QComboBox()
        self.model_file_combo.addItem("Please select")
        self.model_file_combo.addItems(["Risk Model A", "Risk Model B", "Risk Model C"])
        self.model_file_combo.setMinimumWidth(300)
        model_form.addRow(QLabel("Model File:"), self.model_file_combo)
        
        # Approver
        self.approver_combo = QComboBox()
        self.approver_combo.addItem("Please select")
        self.approver_combo.addItems(["Zhang San", "Li Si", "Wang Wu"])
        model_form.addRow(QLabel("Approver:"), self.approver_combo)
        
        # Valid time
        valid_time_layout = QHBoxLayout()
        
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setDisplayFormat("yyyy-MM-dd")
        
        valid_time_layout.addWidget(self.date_edit)
        valid_time_layout.addWidget(QLabel("-"))
        
        self.time_edit = QTimeEdit()
        self.time_edit.setTime(QTime.currentTime())
        self.time_edit.setDisplayFormat("hh:mm")
        valid_time_layout.addWidget(self.time_edit)
        
        model_form.addRow(QLabel("Valid Time:"), valid_time_layout)
        
        # Support inference
        self.inference_checkbox = QCheckBox()
        model_form.addRow(QLabel("Support Inference:"), self.inference_checkbox)
        
        # Runtime environment
        env_group = QGroupBox()
        env_layout = QVBoxLayout()
        
        self.python2_checkbox = QCheckBox("python2.0")
        self.python3_checkbox = QCheckBox("python3.0")
        
        env_layout.addWidget(self.python2_checkbox)
        env_layout.addWidget(self.python3_checkbox)
        
        env_group.setLayout(env_layout)
        model_form.addRow(QLabel("Runtime Environment:"), env_group)
        
        # Special resources
        resource_layout = QHBoxLayout()
        
        self.k8s_radio = QRadioButton("K8S Cluster")
        self.normal_radio = QRadioButton("General Cluster")
        
        resource_group = QButtonGroup(self)
        resource_group.addButton(self.k8s_radio)
        resource_group.addButton(self.normal_radio)
        
        resource_layout.addWidget(self.k8s_radio)
        resource_layout.addWidget(self.normal_radio)
        resource_layout.addStretch()
        
        model_form.addRow(QLabel("Special Resources:"), resource_layout)
        
        # Model notes
        self.notes_text = QTextEdit()
        self.notes_text.setPlaceholderText("Enter content here")
        self.notes_text.setMinimumHeight(100)
        model_form.addRow(QLabel("Model Notes:"), self.notes_text)
        
        # Add form to main layout
        layout.addLayout(model_form)
        layout.addStretch()
        
        # Bottom buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # Create button
        self.create_button = QPushButton("Create Now")
        self.create_button.setObjectName("primaryButton")
        self.create_button.setMinimumWidth(120)
        self.create_button.clicked.connect(self.on_create_clicked)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setObjectName("secondaryButton")
        self.cancel_button.setMinimumWidth(120)
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.create_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def get_model_data(self):
        """Get form data"""
        data = {
            "model_file": self.model_file_combo.currentText(),
            "approver": self.approver_combo.currentText(),
            "valid_date": self.date_edit.date().toString("yyyy-MM-dd"),
            "valid_time": self.time_edit.time().toString("hh:mm"),
            "support_inference": self.inference_checkbox.isChecked(),
            "python2": self.python2_checkbox.isChecked(),
            "python3": self.python3_checkbox.isChecked(),
            "k8s_cluster": self.k8s_radio.isChecked(),
            "normal_cluster": self.normal_radio.isChecked(),
            "notes": self.notes_text.toPlainText()
        }
        return data
    
    def show_success_dialog(self):
        """Show submission success dialog"""
        from Client.views.ModelApprovalSuccessDialog import ModelApprovalSuccessDialog
        
        model_data = self.get_model_data()
        
        valid_date = f"{model_data['valid_date']} ~ {model_data['valid_date']}"
        
        success_dialog = ModelApprovalSuccessDialog(
            model_id="M010012",
            responsible=model_data["approver"],
            valid_date=valid_date,
            parent=self
        )
        
        self.accept()
        success_dialog.exec_()

    def on_create_clicked(self):
        """Handle create now button click"""
        model_data = self.get_model_data()
        
        if model_data["model_file"] == "Please select" or model_data["approver"] == "Please select":
            QMessageBox.warning(self, 'Warning', 'Please select a model file and approver!')
            return
            
        if not model_data["python2"] and not model_data["python3"]:
            QMessageBox.warning(self, 'Warning', 'Please select at least one Python runtime environment!')
            return
            
        if not model_data["k8s_cluster"] and not model_data["normal_cluster"]:
            QMessageBox.warning(self, 'Warning', 'Please select a special resource type!')
            return
        
        self.show_success_dialog()
