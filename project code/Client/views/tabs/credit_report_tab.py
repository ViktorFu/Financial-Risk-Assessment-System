from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                           QLineEdit, QPushButton, QFormLayout, QFrame,
                           QGroupBox, QMessageBox, QTableWidget, QTableWidgetItem,
                           QHeaderView, QComboBox, QSpinBox, QTabWidget, QDialog,
                           QDialogButtonBox, QCheckBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
import random
from Client.utils.helpers import get_risk_level_text, get_business_line_text

class CreditReportTab(QWidget):
    def __init__(self, controller=None):
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
            QFrame#filterFrame {
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
        
        layout = QVBoxLayout()
        
        # Create filter frame
        filter_frame = QFrame()
        filter_frame.setObjectName("filterFrame")
        filter_layout = QHBoxLayout()
        
        # Filter conditions
        filter_form = QHBoxLayout()
        
        # ID Filter
        filter_form.addWidget(QLabel("ID:"))
        self.id_filter = QLineEdit()
        self.id_filter.setPlaceholderText("Please enter ID")
        filter_form.addWidget(self.id_filter)
        
        # ReportID Filter
        filter_form.addWidget(QLabel("ReportID:"))
        self.report_id_filter = QLineEdit()
        self.report_id_filter.setPlaceholderText("Please enter ReportID")
        filter_form.addWidget(self.report_id_filter)
        
        # Name Filter
        filter_form.addWidget(QLabel("Name:"))
        self.name_filter = QLineEdit()
        self.name_filter.setPlaceholderText("Please enter name")
        filter_form.addWidget(self.name_filter)
        
        # Status Filter
        filter_form.addWidget(QLabel("Status:"))
        self.status_filter = QComboBox()
        self.status_filter.addItems(["All", "Valid", "Invalid"])
        filter_form.addWidget(self.status_filter)
        
        # Source Filter
        filter_form.addWidget(QLabel("Source:"))
        self.source_filter = QLineEdit()
        self.source_filter.setPlaceholderText("Please enter source")
        filter_form.addWidget(self.source_filter)
        
        # Search button
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_credit_reports)
        
        # Reset button
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_filters)
        self.reset_button.setStyleSheet("""
            background-color: #6c757d;
            color: white;
        """)
        
        filter_layout.addLayout(filter_form)
        filter_layout.addWidget(self.search_button)
        filter_layout.addWidget(self.reset_button)
        filter_frame.setLayout(filter_layout)
        
        # Operation buttons area
        button_layout = QHBoxLayout()
        
        self.add_button = QPushButton("+ New")
        self.add_button.clicked.connect(self.add_credit_report)
        
        self.batch_button = QPushButton("Batch Import")
        self.batch_button.clicked.connect(self.batch_import)
        
        self.more_button = QPushButton("More Actions ▼")
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.batch_button)
        button_layout.addWidget(self.more_button)
        button_layout.addStretch()
        
        # Status label
        status_label = QLabel("Credit report historical variables have been cached.")
        status_label.setObjectName("statusLabel")
        
        # Table
        self.report_table = QTableWidget()
        self.report_table.setColumnCount(11)
        self.report_table.setHorizontalHeaderLabels([
            "", "ID", "ReportID", "Name", "ComAddress", "HomeAddress", 
            "Hit-count", "Format", "Status", "CreateTime", "Source"
        ])
        self.report_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.report_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.report_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.report_table.verticalHeader().setVisible(False)
        
        # Load data
        self.load_credit_reports()
        
        # Bottom pagination
        pagination_layout = QHBoxLayout()
        pagination_layout.addStretch()
        
        self.prev_page_btn = QPushButton("<")
        self.page_1_btn = QPushButton("1")
        self.page_1_btn.setStyleSheet("background-color: #3e89fa; color: white;")
        self.page_2_btn = QPushButton("2")
        self.page_3_btn = QPushButton("3")
        self.page_4_btn = QPushButton("4")
        self.page_5_btn = QPushButton("5")
        self.page_6_btn = QPushButton("6")
        self.page_7_btn = QPushButton("7")
        self.page_8_btn = QPushButton("8")
        self.page_9_btn = QPushButton("9")
        self.next_page_btn = QPushButton(">")
        
        pagination_layout.addWidget(self.prev_page_btn)
        pagination_layout.addWidget(self.page_1_btn)
        pagination_layout.addWidget(self.page_2_btn)
        pagination_layout.addWidget(self.page_3_btn)
        pagination_layout.addWidget(self.page_4_btn)
        pagination_layout.addWidget(self.page_5_btn)
        pagination_layout.addWidget(self.page_6_btn)
        pagination_layout.addWidget(self.page_7_btn)
        pagination_layout.addWidget(self.page_8_btn)
        pagination_layout.addWidget(self.page_9_btn)
        pagination_layout.addWidget(self.next_page_btn)
        pagination_layout.addStretch()
        
        # Add all elements to the main layout
        layout.addWidget(filter_frame)
        layout.addLayout(button_layout)
        layout.addWidget(status_label)
        layout.addWidget(self.report_table)
        layout.addLayout(pagination_layout)
        
        self.setLayout(layout)
        
        # Store original data for filtering
        self.all_reports = []
    
    def reset_filters(self):
        """Reset all filter conditions"""
        self.id_filter.clear()
        self.report_id_filter.clear()
        self.name_filter.clear()
        self.status_filter.setCurrentIndex(0)
        self.source_filter.clear()
        
        # Reload all data
        self.load_credit_reports()
    
    def load_credit_reports(self):
        """Load credit report data"""
        self.report_table.setRowCount(0)
        
        # Try to get data from the controller
        try:
            if self.controller and hasattr(self.controller, 'get_all_reports'):
                reports = self.controller.get_all_reports()
                
                if reports and len(reports) > 0:
                    self.all_reports = reports
                    self.fill_report_table(reports)
                    return
        except Exception as e:
            print(f"Error loading credit reports: {e}")
        
        # If there is no appropriate controller or data, use mock data
        self.load_mock_data()
    
    def load_mock_data(self):
        """Load mock data"""
        # Mock data
        mock_data = [
            ("16","CR0011", "User16", "Beijing Haidian", "Beijing Haidian", "13", "XML", "Valid", "2022-04-23 23:12:00", "People's Bank of China"),
            ("17","CR0012", "User17", "Beijing Haidian", "Beijing Haidian", "72", "JSON", "Invalid", "2022-05-12 13:22:30", "People's Bank of China"),
            ("18","CR0013", "User18", "Beijing Haidian", "Beijing Haidian", "67", "JSON", "Valid", "2022-10-31 08:22:24", "People's Bank of China"),
            ("19","CR0014", "User19", "Beijing Haidian", "Beijing Haidian", "67", "XML", "Invalid", "2022-07-23 22:12:28", "People's Bank of China"),
            ("20","CR0015", "User20", "Beijing Haidian", "Beijing Haidian", "12", "JSON", "Invalid", "2022-10-31 23:12:00", "Agricultural Bank of China"),
            ("21","CR0016", "User21", "Beijing Haidian", "Beijing Haidian", "100", "JSON", "Valid", "2022-02-11 22:12:10", "China Construction Bank"),
            ("22","CR0017", "User22", "Beijing Haidian", "Beijing Haidian", "163", "XML", "Valid", "2022-10-21 13:23:10", "Bank of China"),
            ("23","CR0018", "User23", "Beijing Haidian", "Beijing Haidian", "12", "JSON", "Valid", "2022-05-21 09:12:02", "Industrial and Commercial Bank of China"),
            ("24","CR0019", "User24", "Beijing Haidian", "Beijing Haidian", "21", "JSON", "Valid", "2022-04-11 10:12:01", "China Merchants Bank")
        ]
        
        # Store original data for filtering
        self.all_reports = mock_data
        
        for row_num, data in enumerate(mock_data):
            self.report_table.insertRow(row_num)
            
            # Add checkbox column
            checkbox_item = QTableWidgetItem()
            checkbox_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            checkbox_item.setCheckState(Qt.Unchecked)
            self.report_table.setItem(row_num, 0, checkbox_item)
            
            for col_num, cell_data in enumerate(data):
                item = QTableWidgetItem(cell_data)
                item.setTextAlignment(Qt.AlignCenter)
                
                # Set style for status column
                if col_num == 7:  # Status column
                    if cell_data == "Valid":
                        item.setBackground(QColor(240, 255, 240))
                        item.setForeground(QColor(40, 167, 69))
                    else:
                        item.setBackground(QColor(248, 248, 248))
                        item.setForeground(QColor(108, 117, 125))
                
                self.report_table.setItem(row_num, col_num + 1, item)
    
    def fill_report_table(self, reports):
        """Fill the table with actual data"""
        self.report_table.setRowCount(0)
        
        for row_num, report in enumerate(reports):
            self.report_table.insertRow(row_num)
            
            # Add checkbox column
            checkbox_item = QTableWidgetItem()
            checkbox_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            checkbox_item.setCheckState(Qt.Unchecked)
            self.report_table.setItem(row_num, 0, checkbox_item)
            # If it is mock data
            for col_num, cell_data in enumerate(report):
                item = QTableWidgetItem(cell_data)
                item.setTextAlignment(Qt.AlignCenter)
                
                # Set style for status column
                if col_num == 7:  # Status column
                    if cell_data == "Valid":
                        item.setBackground(QColor(240, 255, 240))
                        item.setForeground(QColor(40, 167, 69))
                    else:
                        item.setBackground(QColor(248, 248, 248))
                        item.setForeground(QColor(108, 117, 125))
                
                self.report_table.setItem(row_num, col_num + 1, item)
    
    def search_credit_reports(self):
        """Search credit reports based on filter conditions"""
        # Get filter conditions
        id_filter = self.id_filter.text().strip()
        report_id_filter = self.report_id_filter.text().strip()
        name_filter = self.name_filter.text().strip()
        status_filter = self.status_filter.currentText()
        source_filter = self.source_filter.text().strip()
        
        # Use mock data for filtering
        if not self.all_reports:
            self.load_mock_data()
        
        # Apply filtering logic
        filtered_data = []
        for report in self.all_reports:
            # Check each filter condition
            if id_filter and id_filter != report[0]:
                continue
                
            if report_id_filter and report_id_filter.upper() not in report[1].upper():
                continue
                
            if name_filter and name_filter not in report[2]:
                continue
                
            if status_filter != "All" and status_filter != report[7]:
                continue
                
            if source_filter and source_filter not in report[9]:
                continue
                
            # Passed all filter conditions, add to results
            filtered_data.append(report)
        
        if filtered_data:
            self.fill_report_table(filtered_data)
        else:
            # No matching records
            self.report_table.setRowCount(0)
            QMessageBox.information(self, 'Notice', 'No records match the criteria!')
    
    def add_credit_report(self):
        """Add new credit report"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Credit Report")
        dialog.setFixedWidth(400)
        
        # Form layout
        form_layout = QFormLayout()
        
        # ID
        id_input = QLineEdit()
        
        # ReportID
        report_id_input = QLineEdit()
        
        # Name
        name_input = QLineEdit()
        
        # Company Address
        com_address_input = QLineEdit()
        com_address_input.setText("Beijing Haidian")
        
        # Home Address
        home_address_input = QLineEdit()
        home_address_input.setText("Beijing Haidian")
        
        # Hit Count
        hit_count_input = QSpinBox()
        hit_count_input.setRange(1, 999)
        hit_count_input.setValue(10)
        
        # Format
        format_input = QComboBox()
        format_input.addItems(['JSON', 'XML'])
        
        # Status
        status_input = QComboBox()
        status_input.addItems(['Valid', 'Invalid'])
        
        # Creation Time (read-only, auto-generated)
        create_time_input = QLineEdit()
        create_time_input.setText("2022-04-13 12:00:00")
        create_time_input.setEnabled(False)
        
        # Source
        source_input = QComboBox()
        source_input.addItems(['People\'s Bank of China', 'Agricultural Bank of China', 'China Construction Bank', 'Bank of China', 'Industrial and Commercial Bank of China', 'China Merchants Bank'])
        source_input.setEditable(True)
        
        form_layout.addRow('ID:', id_input)
        form_layout.addRow('ReportID:', report_id_input)
        form_layout.addRow('Name:', name_input)
        form_layout.addRow('Company Address:', com_address_input)
        form_layout.addRow('Home Address:', home_address_input)
        form_layout.addRow('Hit Count:', hit_count_input)
        form_layout.addRow('Format:', format_input)
        form_layout.addRow('Status:', status_input)
        form_layout.addRow('Creation Time:', create_time_input)
        form_layout.addRow('Source:', source_input)
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(button_box)
        
        dialog.setLayout(main_layout)
        
        # Display dialog
        if dialog.exec_() == QDialog.Accepted:
            # Get form data
            id_val = id_input.text()
            report_id = report_id_input.text()
            name = name_input.text()
            com_address = com_address_input.text()
            home_address = home_address_input.text()
            hit_count = str(hit_count_input.value())
            format_val = format_input.currentText()
            status = status_input.currentText()
            create_time = create_time_input.text()
            source = source_input.currentText()
            
            if not id_val or not report_id or not name:
                QMessageBox.warning(self, 'Warning', 'ID, ReportID, and Name cannot be empty!')
                return
            
            # Add to table
            if self.controller:
                # Use controller to add report
                pass
            else:
                # Add to mock data
                new_report = (
                    id_val, report_id, name, com_address, home_address,
                    hit_count, format_val, status, create_time, source
                )
                self.all_reports.append(new_report)
                
                # Update table
                row_num = self.report_table.rowCount()
                self.report_table.insertRow(row_num)
                
                # Add checkbox
                checkbox_item = QTableWidgetItem()
                checkbox_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                checkbox_item.setCheckState(Qt.Unchecked)
                self.report_table.setItem(row_num, 0, checkbox_item)
                
                # Add other data
                for col_num, cell_data in enumerate(new_report):
                    item = QTableWidgetItem(cell_data)
                    item.setTextAlignment(Qt.AlignCenter)
                    
                    # Set style for status column
                    if col_num == 7:  # Status column
                        if cell_data == "Valid":
                            item.setBackground(QColor(240, 255, 240))
                            item.setForeground(QColor(40, 167, 69))
                        else:
                            item.setBackground(QColor(248, 248, 248))
                            item.setForeground(QColor(108, 117, 125))
                    
                    self.report_table.setItem(row_num, col_num + 1, item)
                
                QMessageBox.information(self, 'Success', 'Credit report added successfully!')
    
    def batch_import(self):
        """Batch import credit reports"""
        QMessageBox.information(self, 'Feature Notice', 'Batch import functionality is under development...')
