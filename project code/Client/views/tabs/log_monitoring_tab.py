from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                           QLineEdit, QPushButton, QFormLayout, QFrame,
                           QGroupBox, QMessageBox, QTableWidget, QTableWidgetItem,
                           QHeaderView, QComboBox, QSpinBox, QTabWidget, QDialog, QCheckBox, QDialogButtonBox,
                           QTextEdit, QDateEdit)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QColor

class LogMonitoringTab(QWidget):
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
            QLineEdit, QComboBox, QDateEdit {
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
            QLabel#statusLabel {
                color: #4aa3df;
                font-weight: bold;
                margin: 5px;
            }
            QTextEdit {
                border: 1px solid #e0e0e0;
                border-radius: 4px;
            }
            QCheckBox {
                margin: 5px;
            }
        """)
        
        main_layout = QVBoxLayout()
        
        # Upper section: Filter and operation area
        upper_section = QVBoxLayout()
        
        # Filter area
        filter_layout = QHBoxLayout()
        
        # Keyword search
        self.keyword_input = QLineEdit()
        self.keyword_input.setPlaceholderText("Filter search keyword")
        self.keyword_input.setFixedWidth(200)
        filter_layout.addWidget(self.keyword_input)
        
        # Log type
        filter_layout.addWidget(QLabel("Log type:"))
        self.log_type_combo = QComboBox()
        self.log_type_combo.addItems(["Please select", "Runtime logs", "Operation logs"])
        self.log_type_combo.setFixedWidth(120)
        filter_layout.addWidget(self.log_type_combo)
        
        
        # Add checkbox to enable date filter
        self.enable_date_filter = QCheckBox("Enable date filter")
        self.enable_date_filter.setChecked(True)  # Enabled by default
        self.enable_date_filter.stateChanged.connect(self.toggle_date_filter)
        filter_layout.addWidget(self.enable_date_filter)
        
        # Add date range filter
        self.date_filter_widget = QWidget()
        date_filter_layout = QHBoxLayout(self.date_filter_widget)
        date_filter_layout.setContentsMargins(0, 0, 0, 0)
        
        date_filter_layout.addWidget(QLabel("Start date:"))
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate().addDays(-30))  # Default shows last 30 days
        self.start_date.setDisplayFormat("yyyy-MM-dd")
        self.start_date.setFixedWidth(120)
        date_filter_layout.addWidget(self.start_date)
        
        date_filter_layout.addWidget(QLabel("End date:"))
        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate())  # Default shows today
        self.end_date.setDisplayFormat("yyyy-MM-dd")
        self.end_date.setFixedWidth(120)
        date_filter_layout.addWidget(self.end_date)
        
        filter_layout.addWidget(self.date_filter_widget)
        
        # Search button
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.load_logs)
        filter_layout.addWidget(self.search_button)
        filter_layout.addStretch()
        
        # Operation button area
        button_layout = QHBoxLayout()
        
        self.refresh_logs_button = QPushButton("Refresh logs")
        self.refresh_logs_button.clicked.connect(self.load_logs)
        
        self.mark_done_button = QPushButton("Mark as processed")
        self.mark_done_button.clicked.connect(self.mark_as_done)
        
        button_layout.addWidget(self.mark_done_button)
        button_layout.addWidget(self.refresh_logs_button)
        button_layout.addStretch()
        
        # Status info box
        status_frame = QFrame()
        status_frame.setObjectName("statusFrame")
        status_layout = QHBoxLayout()
        
        status_icon = QLabel("●")
        status_icon.setStyleSheet("color: #4aa3df;")
        status_layout.addWidget(status_icon)
        
        status_text = QLabel("Log monitoring service is online.")
        status_layout.addWidget(status_text)
        
        
        status_layout.addStretch()
        
        status_frame.setLayout(status_layout)
        
        upper_section.addLayout(filter_layout)
        upper_section.addLayout(button_layout)
        upper_section.addWidget(status_frame)
        
        # Middle section: Log table
        self.log_table = QTableWidget()
        self.log_table.setColumnCount(10)
        self.log_table.setHorizontalHeaderLabels([
            "", "Log ID", "Create time", "Operator", "Operation", "Error message", 
            "Exception info", "Is warning", "Is processed", "Warning type"
        ])
        self.log_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.log_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Fixed)
        self.log_table.setColumnWidth(0, 30)  # Checkbox column width
        self.log_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.log_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.log_table.verticalHeader().setVisible(False)
        
        # Set log selection event
        self.log_table.itemSelectionChanged.connect(self.on_log_selected)
        
        # Lower section: Log details area
        lower_section = QVBoxLayout()
        
        self.log_details = QTextEdit()
        self.log_details.setReadOnly(True)
        self.log_details.setMinimumHeight(150)
        self.log_details.setMaximumHeight(200)
        
        lower_section.addWidget(self.log_details)
        
        # Pagination control (keep original UI pagination style)
        pagination_layout = QHBoxLayout()
        pagination_layout.addStretch()
        
        self.prev_page_btn = QPushButton("<")
        self.page_1_btn = QPushButton("1")
        self.page_1_btn.setStyleSheet("background-color: #3e89fa; color: white;")
        self.page_2_btn = QPushButton("2")
        self.page_3_btn = QPushButton("3")
        self.next_page_btn = QPushButton(">")
        
        for btn in [self.prev_page_btn, self.page_1_btn, self.page_2_btn, self.page_3_btn, self.next_page_btn]:
            btn.setFixedSize(32, 32)
            if btn != self.page_1_btn:
                btn.setStyleSheet("background-color: white; color: #333; border: 1px solid #ddd;")
            pagination_layout.addWidget(btn)
        
        pagination_layout.addStretch()
        
        # Add all layouts to main layout
        main_layout.addLayout(upper_section)
        main_layout.addWidget(self.log_table)
        main_layout.addLayout(lower_section)
        main_layout.addLayout(pagination_layout)
        
        self.setLayout(main_layout)
        
        # Load log data
        self.load_logs()
    
    def toggle_date_filter(self, state):
        """Enable or disable date filter controls"""
        self.date_filter_widget.setEnabled(state == Qt.Checked)
        
        # Optional: Adjust UI visual feedback based on checkbox state
        if state == Qt.Checked:
            self.date_filter_widget.setStyleSheet("")
        else:
            self.date_filter_widget.setStyleSheet("color: #999999;")
    
    def load_logs(self):
        """Load log data"""
        self.log_table.setRowCount(0)
        
        # Get filter conditions
        keyword = self.keyword_input.text()
        log_type = self.log_type_combo.currentText()
        use_date_filter = self.enable_date_filter.isChecked()
        
        # Get date range (only used when date filter is enabled)
        start_date = None
        end_date = None
        
        if use_date_filter:
            start_date = self.start_date.date().toString("yyyy-MM-dd")
            end_date = self.end_date.date().toString("yyyy-MM-dd")
        
        # Get all logs from LogModel (this is currently the only available method)
        try:
            if hasattr(self.controller, 'get_all_logs'):
                logs = self.controller.get_all_logs()
            else:
                # If controller doesn't have this method, try to get directly from model
                from Client.models.log_model import LogModel
                logs = LogModel.get_all_logs()
                
            if logs:
                # Map model returned columns to UI expected structure
                # LogModel.get_all_logs() returns: [id, timestamp, username, action]
                
                # Filter by keyword
                if keyword:
                    logs = [log for log in logs if keyword.lower() in str(log).lower()]
                    
                # Filter by log type
                if log_type == "Runtime logs":
                    # Assume action field is at index 3
                    logs = [log for log in logs if any(op in str(log[3]).lower() for op in ["run", "start", "login", "system"])]
                elif log_type == "Operation logs":
                    logs = [log for log in logs if any(op in str(log[3]).lower() for op in ["modify", "delete", "add", "export"])]
                
                # Since model doesn't have is_done field, can't filter by processing status
                # If really need to filter by this, model needs to be updated to return this field
                
                # Filter by date range
                if use_date_filter:
                    filtered_logs = []
                    for log in logs:
                        # Assume timestamp is at index 1
                        timestamp_str = str(log[1]) if len(log) > 1 else ""
                        # Try to extract date part
                        if " " in timestamp_str:
                            log_date = timestamp_str.split(" ")[0]
                        else:
                            log_date = timestamp_str
                        
                        # Only keep logs within range
                        if start_date <= log_date <= end_date:
                            filtered_logs.append(log)
                    logs = filtered_logs
                    
                # Only show valid data  
                if logs and len(logs) > 0:
                    self.fill_logs_table(logs)
                    print(f"Loaded {len(logs)} logs")
                    return
                else:
                    print("No matching logs after filtering")
            else:
                print("No logs retrieved")
                
        except Exception as e:
            print(f"Error loading logs: {e}")
            import traceback
            traceback.print_exc()
    def _build_date_range_query(self, start_date, end_date, log_type=None, status=None, keyword=None):
        """Build SQL query with date range"""
        # Basic query
        sql = "SELECT * FROM logs WHERE 1=1"
        params = []
        
        # Add date range condition (if date filter is enabled)
        if start_date and end_date:
            sql += " AND create_time >= ? AND create_time < ?"
            params.extend([start_date, end_date])
        
        # Add log type condition
        if log_type and log_type != "Please select":
            if log_type == "Runtime logs":
                sql += " AND (operation LIKE '%run%' OR operation LIKE '%start%' OR operation LIKE '%login%' OR operation LIKE '%system%')"
            elif log_type == "Operation logs":
                sql += " AND (operation LIKE '%modify%' OR operation LIKE '%delete%' OR operation LIKE '%add%' OR operation LIKE '%export%')"
        
        # Add status condition
        if status and status != "Please select":
            if status == "Unprocessed":
                sql += " AND is_done = 0"
            elif status == "Processed":
                sql += " AND is_done = 1"
        
        # Add keyword condition
        if keyword:
            # Search keyword in multiple fields
            sql += " AND (log_id LIKE ? OR operator LIKE ? OR operation LIKE ? OR error_info LIKE ? OR exception_info LIKE ? OR warning_type LIKE ?)"
            keyword_param = f"%{keyword}%"
            params.extend([keyword_param] * 6)  # Add same parameter for 6 fields
        
        # Add sorting
        sql += " ORDER BY create_time DESC"
        
        return {"query": sql, "params": params}
    
    def _filter_logs_by_date(self, logs, start_date, end_date):
        """Filter logs by date range in memory"""
        # If date filter is not enabled, return all logs
        if not start_date or not end_date:
            return logs
            
        filtered_logs = []
        
        for log in logs:
            # Assume date field is at index 9 (according to table column order)
            try:
                log_date_str = str(log[2]) if len(log) > 2 else ""
                # Try to extract date part (assuming format is "YYYY-MM-DD HH:MM:SS")
                if " " in log_date_str:
                    log_date = log_date_str.split(" ")[0]
                else:
                    log_date = log_date_str
                
                # Check if date is within range
                if start_date <= log_date <= end_date:
                    filtered_logs.append(log)
            except Exception as e:
                print(f"Error filtering date: {e}")
                # If error occurs, keep this log
                filtered_logs.append(log)
        
        return filtered_logs

    def fill_logs_table(self, logs):
        """Fill table with actual log data"""
        self.log_table.setRowCount(0)  # Clear existing rows
        
        column_count = self.log_table.columnCount()
        
        # Define mapping - from model columns to UI columns
        # LogModel returns: [id, timestamp, username, action]
        # UI shows: ["", "Log ID", "Create time", "Operator", "Operation", "Error message", 
        #         "Exception info", "Is warning", "Is processed", "Warning type"]
        
        model_to_ui_map = {
            0: 1,  # id -> Log ID
            1: 2,  # timestamp -> Create time
            2: 3,  # username -> Operator
            3: 4,  # action -> Operation
        }
        
        for row_num, log in enumerate(logs):
            self.log_table.insertRow(row_num)
            
            # Add checkbox column
            checkbox = QTableWidgetItem()
            checkbox.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            checkbox.setCheckState(Qt.Unchecked)
            self.log_table.setItem(row_num, 0, checkbox)
            
            # Safe get function
            def safe_get(log, index, default=""):
                try:
                    if index < len(log):
                        return log[index]
                    return default
                except:
                    return default
            
            # Fill data columns
            for model_col, ui_col in model_to_ui_map.items():
                cell_data = safe_get(log, model_col)
                item = QTableWidgetItem(str(cell_data))
                item.setTextAlignment(Qt.AlignCenter)
                self.log_table.setItem(row_num, ui_col, item)
            
            # Fill blank columns since model doesn't have this data
            for col in range(5, column_count):
                if col == 7:  # Is warning - default shows "No"
                    item = QTableWidgetItem("No")
                    item.setBackground(QColor(248, 248, 248))
                    item.setForeground(QColor(108, 117, 125))
                elif col == 8:  # Is processed - default shows "No"
                    item = QTableWidgetItem("No")
                    item.setBackground(QColor(248, 248, 248))
                    item.setForeground(QColor(108, 117, 125))
                else:
                    item = QTableWidgetItem("")
                
                item.setTextAlignment(Qt.AlignCenter)
                self.log_table.setItem(row_num, col, item)

    def on_log_selected(self):
        """Handle log selection event, show details"""
        selected_rows = self.log_table.selectedItems()
        if not selected_rows:
            return

        row = selected_rows[0].row()
        
        # Get data displayed in table columns
        try:
            # Helper function to safely get text from table items
            def get_item_text(row, col, default=""):
                item = self.log_table.item(row, col)
                return item.text() if item else default
            
            log_id = get_item_text(row, 1)
            create_time = get_item_text(row, 2)
            operator = get_item_text(row, 3)
            operation = get_item_text(row, 4)
            error_info = get_item_text(row, 5, "None")
            exception_info = get_item_text(row, 6, "None")
            is_warning = get_item_text(row, 7, "No")
            is_done = get_item_text(row, 8, "No")
            warning_type = get_item_text(row, 9, "None")
            
            # Try to get details from model
            details_from_model = None
            if hasattr(self.controller, 'get_log_details'):
                details_from_model = self.controller.get_log_details(log_id)
            else:
                # Try to use model directly
                try:
                    from Client.models.log_model import LogModel
                    details_from_model = LogModel.get_log_details(log_id)
                except:
                    pass
            
            # Format detail text
            details = f"Log ID: {log_id}\n"
            details += f"Operator: {operator}\n"
            details += f"Operation: {operation}\n"
            details += f"Create time: {create_time}\n"
            
            if details_from_model:
                details += f"\nDetails:\n{details_from_model}\n"
            
            if error_info and error_info != "None":
                details += f"Error message: {error_info}\n"
            if exception_info and exception_info != "None":
                details += f"Exception info: {exception_info}\n"
            if warning_type and warning_type != "None":
                details += f"Warning type: {warning_type}\n"
            
            details += f"Is warning: {is_warning}\n"
            details += f"Is processed: {is_done}\n"
            
            self.log_details.setText(details)
        except Exception as e:
            print(f"Error displaying log details: {e}")
            self.log_details.setText("Unable to display log details.")
            import traceback
            traceback.print_exc()

    def mark_as_done(self):
        """Mark log as processed"""
        selected_rows = self.log_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, 'Warning', 'Please select a log first!')
            return
        
        row = selected_rows[0].row()
        
        # Check if log_id exists
        log_id_item = self.log_table.item(row, 1)
        if not log_id_item:
            QMessageBox.warning(self, 'Error', 'Failed to get log ID!')
            return
        
        log_id = log_id_item.text()
        
        # Add null check for the is_done item
        is_done_item = self.log_table.item(row, 8)  # Note: index changed to 8 to match table structure
        if not is_done_item:
            # If the item doesn't exist, assume it's not processed yet
            is_done = False
        else:
            is_done = is_done_item.text() == 'Yes'
        
        if is_done:
            QMessageBox.information(self, 'Info', 'This log has already been marked as processed!')
            return
        
        reply = QMessageBox.question(
            self, 'Confirm action',
            'Are you sure you want to mark this log as processed?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                # Note: LogModel currently doesn't provide a method to update log status
                # Only update in UI here, show success message
                
                QMessageBox.information(self, 'Info', 'Log has been marked as processed in the interface (Note: backend database not updated)')
                
                # Create a new item (if doesn't exist)
                if not is_done_item:
                    is_done_item = QTableWidgetItem('Yes')
                    self.log_table.setItem(row, 8, is_done_item)
                else:
                    is_done_item.setText('Yes')
                
                is_done_item.setBackground(QColor(240, 255, 240))
                is_done_item.setForeground(QColor(40, 167, 69))
                
                # Update log details
                self.on_log_selected()
                
            except Exception as e:
                print(f"Error marking log as processed: {e}")
                QMessageBox.warning(self, 'Error', f'Processing failed: {str(e)}')
                import traceback
                traceback.print_exc()