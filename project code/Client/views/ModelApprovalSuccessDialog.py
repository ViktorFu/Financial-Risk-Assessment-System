from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QFrame, QSpacerItem, QSizePolicy)
from PyQt5.QtGui import QPainter, QPen, QBrush, QPainterPath, QPixmap, QColor, QFont
from PyQt5.QtCore import Qt, QSize, QRect, QPoint

class ModelApprovalSuccessDialog(QDialog):
    def __init__(self, model_id="M010012", responsible="Qu Lili", valid_date="2022-08-11 ~ 202-09-11", parent=None):
        super().__init__(parent)
        self.model_id = model_id
        self.responsible = responsible
        self.valid_date = valid_date
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Model Submission Status")
        self.setMinimumSize(700, 500)
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                color: #333333;
            }
            QLabel#titleLabel {
                font-size: 24px;
                font-weight: bold;
                color: #333333;
            }
            QLabel#infoLabel {
                font-size: 14px;
                color: #666666;
            }
            QLabel#nameLabel {
                font-size: 13px;
                color: #999999;
            }
            QLabel#timeLabel {
                font-size: 13px;
                color: #999999;
            }
            QLabel#clickLabel {
                font-size: 13px;
                color: #3e89fa;
            }
            QPushButton {
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 14px;
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
                color: #333333;
                border: 1px solid #dddddd;
            }
            QPushButton#secondaryButton:hover {
                background-color: #f5f5f5;
            }
            QFrame#infoFrame {
                background-color: #f9f9f9;
                border-radius: 4px;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Top icon and title
        top_layout = QVBoxLayout()
        
        # Success icon
        icon_label = QLabel()
        # Create a green circle with white checkmark icon
        success_pixmap = self.create_success_icon(80)
        icon_label.setPixmap(success_pixmap)
        icon_label.setAlignment(Qt.AlignCenter)
        
        # Title text
        title_label = QLabel("Submission Successful")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignCenter)
        
        top_layout.addWidget(icon_label)
        top_layout.addWidget(title_label)
        top_layout.addSpacing(20)
        
        # Info box
        info_frame = QFrame()
        info_frame.setObjectName("infoFrame")
        info_layout = QVBoxLayout()
        
        # Project info
        project_info_layout = QHBoxLayout()
        
        id_label = QLabel(f"Project ID: {self.model_id}")
        id_label.setObjectName("infoLabel")
        
        responsible_label = QLabel(f"Responsible: {self.responsible}")
        responsible_label.setObjectName("infoLabel")
        
        date_label = QLabel(f"Valid Date: {self.valid_date}")
        date_label.setObjectName("infoLabel")
        
        project_info_layout.addWidget(id_label)
        project_info_layout.addStretch(1)
        project_info_layout.addWidget(responsible_label)
        project_info_layout.addStretch(1)
        project_info_layout.addWidget(date_label)
        
        # Progress bar
        progress_layout = QHBoxLayout()
        
        # Create progress points and connecting lines
        step1_active = self.create_progress_point(True, True)
        line1_active = self.create_progress_line(True)
        step2_active = self.create_progress_point(True, False)
        line2_inactive = self.create_progress_line(False)
        step3_inactive = self.create_progress_point(False, False)
        line3_inactive = self.create_progress_line(False)
        step4_inactive = self.create_progress_point(False, False)
        
        progress_layout.addWidget(step1_active)
        progress_layout.addWidget(line1_active, 1)
        progress_layout.addWidget(step2_active)
        progress_layout.addWidget(line2_inactive, 1)
        progress_layout.addWidget(step3_inactive)
        progress_layout.addWidget(line3_inactive, 1)
        progress_layout.addWidget(step4_inactive)
        
        # Progress labels
        progress_labels_layout = QHBoxLayout()
        
        step1_label = QLabel("Create Model")
        step1_label.setAlignment(Qt.AlignCenter)
        
        step2_label = QLabel("Consistency Check")
        step2_label.setAlignment(Qt.AlignCenter)
        
        step3_label = QLabel("Department Review")
        step3_label.setAlignment(Qt.AlignCenter)
        
        step4_label = QLabel("Complete")
        step4_label.setAlignment(Qt.AlignCenter)
        
        progress_labels_layout.addWidget(step1_label)
        progress_labels_layout.addStretch(1)
        progress_labels_layout.addWidget(step2_label)
        progress_labels_layout.addStretch(1)
        progress_labels_layout.addWidget(step3_label)
        progress_labels_layout.addStretch(1)
        progress_labels_layout.addWidget(step4_label)
        
        # Person names
        name_labels_layout = QHBoxLayout()
        
        name1_label = QLabel(self.responsible)
        name1_label.setObjectName("nameLabel")
        name1_label.setAlignment(Qt.AlignCenter)
        
        name2_label = QLabel("Zhou Maomao")
        name2_label.setObjectName("nameLabel")
        name2_label.setAlignment(Qt.AlignCenter)
        
        name_labels_layout.addWidget(name1_label)
        name_labels_layout.addStretch(1)
        name_labels_layout.addWidget(name2_label)
        name_labels_layout.addStretch(1)
        name_labels_layout.addWidget(QLabel(""))  # Empty placeholder
        name_labels_layout.addStretch(1)
        name_labels_layout.addWidget(QLabel(""))  # Empty placeholder
        
        # Time labels
        time_labels_layout = QHBoxLayout()
        
        time1_label = QLabel("2022-08-12 11:32")
        time1_label.setObjectName("timeLabel")
        time1_label.setAlignment(Qt.AlignCenter)
        
        time2_label = QLabel("Remind")
        time2_label.setObjectName("clickLabel")
        time2_label.setAlignment(Qt.AlignCenter)
        
        time_labels_layout.addWidget(time1_label)
        time_labels_layout.addStretch(1)
        time_labels_layout.addWidget(time2_label)
        time_labels_layout.addStretch(1)
        time_labels_layout.addWidget(QLabel(""))  # Empty placeholder
        time_labels_layout.addStretch(1)
        time_labels_layout.addWidget(QLabel(""))  # Empty placeholder
        
        # Add all components to info layout
        info_layout.addLayout(project_info_layout)
        info_layout.addSpacing(20)
        info_layout.addLayout(progress_layout)
        info_layout.addLayout(progress_labels_layout)
        info_layout.addLayout(name_labels_layout)
        info_layout.addLayout(time_labels_layout)
        
        info_frame.setLayout(info_layout)
        
        # Bottom buttons
        button_layout = QHBoxLayout()
        
        edit_button = QPushButton("Back to Edit")
        edit_button.setObjectName("primaryButton")
        edit_button.clicked.connect(self.reject)
        
        details_button = QPushButton("View Details")
        details_button.setObjectName("secondaryButton")
        
        print_button = QPushButton("Print")
        print_button.setObjectName("secondaryButton")
        
        button_layout.addWidget(edit_button)
        button_layout.addStretch()
        button_layout.addWidget(details_button)
        button_layout.addWidget(print_button)
        
        # Add all content to main layout
        layout.addLayout(top_layout)
        layout.addSpacing(30)
        layout.addWidget(info_frame)
        layout.addSpacing(30)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def create_success_icon(self, size):
        """Create success icon - white checkmark in green circle"""
        from PyQt5.QtGui import QPainter, QPen, QBrush, QPainterPath
        from PyQt5.QtCore import QSize, QRect, QPoint
        
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw green circle
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(60, 190, 60)))
        painter.drawEllipse(0, 0, size, size)
        
        # Draw white checkmark
        painter.setPen(QPen(Qt.white, size/10, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        
        # Checkmark path
        path = QPainterPath()
        path.moveTo(size*0.3, size*0.5)
        path.lineTo(size*0.45, size*0.65)
        path.lineTo(size*0.7, size*0.35)
        
        painter.drawPath(path)
        painter.end()
        
        return pixmap
    
    def create_progress_point(self, active, completed):
        """Create progress point"""
        point = QLabel()
        size = 16
        
        if active:
            color = QColor(62, 137, 250)  # Blue
        else:
            color = QColor(200, 200, 200)  # Gray
            
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw circle
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(color))
        painter.drawEllipse(0, 0, size, size)
        
        if completed:
            # Draw white checkmark to indicate completion
            painter.setPen(QPen(Qt.white, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(4, 8, 7, 11)
            painter.drawLine(7, 11, 12, 5)
            
        painter.end()
        
        point.setPixmap(pixmap)
        return point
    
    def create_progress_line(self, active):
        """Create progress line"""
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        
        if active:
            line.setStyleSheet("background-color: #3e89fa;")  # Blue
        else:
            line.setStyleSheet("background-color: #dddddd;")  # Gray
            
        line.setFixedHeight(2)
        return line