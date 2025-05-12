from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                           QLineEdit, QPushButton, QFormLayout, QFrame,
                           QGroupBox, QMessageBox, QTableWidget, QTableWidgetItem,
                           QHeaderView, QComboBox, QSpinBox, QTabWidget, QDialog, QCheckBox, 
                           QDialogButtonBox, QRadioButton, QTextEdit, QDoubleSpinBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette
import random


# Mock data
mock_data_RC = [
    ("RC0001", "16", "Phone", "1", "Loan", "Anti-cheat", "Blacklist", "Valid", "2022-04-23 23:12:00"),
    ("RC0002", "17", "Email", "2", "Credit Card", "Anti-fraud", "Blacklist", "Invalid", "2022-05-12 13:22:30"),
    ("RC0003", "18", "Phone", "1", "Loan", "Anti-attack", "Blacklist", "Invalid", "2022-10-31 08:22:24"),
    ("RC0004", "19", "Email", "2", "Credit Card", "Anti-fraud", "Blacklist", "Valid", "2022-07-23 22:12:28"),
    ("RC0005", "20", "Email", "4", "Loan", "Anti-fraud", "Blacklist", "Valid", "2022-10-31 23:12:00"),
    ("RC0006", "21", "Phone", "2", "Credit Card", "Anti-fraud", "Blacklist", "Valid", "2022-02-11 22:12:10"),
    ("RC0007", "22", "Email", "2", "Loan", "Anti-cheat", "Blacklist", "Invalid", "2022-10-21 13:23:10"),
    ("RC0008", "23", "Email", "1", "Loan", "Anti-cheat", "Blacklist", "Valid", "2022-05-21 09:12:02"),
    ("RC0009", "23", "Phone", "3", "Credit Card", "Anti-attack", "Blacklist", "Valid", "2022-04-11 10:12:01")
]


# 确保保留原来的mock数据
mock_data_RULES = [
    {"id": "RuleCode0011", "description": "Ant Pay score less than 500", "calls": 19, "status": "Disabled", "update_time": "2022-04-23 23:12:00"},
    {"id": "TradeCode0012", "description": "Average credit limit of credit card account", "calls": 2, "status": "Running", "update_time": "2022-05-12 13:22:30"},
    {"id": "RuleCode0013", "description": "JD Baitiao credit limit greater than 10000", "calls": 4, "status": "Running", "update_time": "2022-10-31 08:22:24"},
    {"id": "TradeCode0014", "description": "Credit card repayment overdue count greater than 5", "calls": 5, "status": "Disabled", "update_time": "2022-07-23 22:12:28"},
    {"id": "RuleCode0015", "description": "Whether there is a car loan record", "calls": 2, "status": "Running", "update_time": "2022-10-31 23:12:00"},
    {"id": "TradeCode0016", "description": "Repayment amount greater than 100,000 in last 6 months", "calls": 17, "status": "Running", "update_time": "2022-02-11 22:12:10"},
    {"id": "RuleCode0017", "description": "Repayment count greater than 60 in the past year", "calls": 1, "status": "Exception", "update_time": "2022-10-21 13:23:10"},
    {"id": "TradeCode0018", "description": "Credit card account cumulative overdue > 3", "calls": 1, "status": "Running", "update_time": "2022-05-21 09:12:02"},
    {"id": "RuleCode0019", "description": "Average usage limit of credit card over 6 months > 80%", "calls": 6, "status": "Running", "update_time": "2022-04-11 10:12:01"},
    {"id": "RuleCode0020", "description": "Credit score is lower than 600", "calls": 9, "status": "Disabled", "update_time": "2022-03-15 08:18:44"},
    {"id": "RuleCode0021", "description": "User has over 2 active loans", "calls": 3, "status": "Running", "update_time": "2022-06-01 14:28:05"},
    {"id": "RuleCode0022", "description": "Current overdue exceeds 30 days", "calls": 2, "status": "Running", "update_time": "2022-08-18 12:40:00"},
    {"id": "RuleCode0023", "description": "Customer has mortgage and car loan", "calls": 4, "status": "Disabled", "update_time": "2022-07-07 07:07:07"},
    {"id": "RuleCode0024", "description": "Debt ratio over 80%", "calls": 5, "status": "Running", "update_time": "2022-09-13 13:13:13"},
    {"id": "RuleCode0025", "description": "More than 3 credit inquiries in 1 month", "calls": 3, "status": "Exception", "update_time": "2022-05-20 20:20:20"}
]

class RiskControlTab(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        # 使用全局mock数据
        self.rules_data = mock_data_RULES

        self.initUI()

    def initUI(self):
        # Create subtabs
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { 
                border: 1px solid #e0e0e0;
                background: white; 
            }
            QTabWidget::tab-bar {
                left: 5px;
            }
            QTabBar::tab {
                background: #f8f8f8;
                border: 1px solid #e0e0e0;
                padding: 8px 12px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #3e89fa;
                color: white;
            }
        """)
        
        # Risk Control List Management tab
        self.name_list_tab = self.create_modern_name_list_tab()
        
        # Other tabs unchanged
        self.rules_tab = self.create_rules_tab()
        self.statistics_tab = self.create_statistics_tab()
        
        # 贷款评估页面
        self.loan_evaluation_tab = self.create_loan_evaluation_tab()
        
        # Add tabs
        self.tabs.addTab(self.name_list_tab, "Risk Control List Management")
        self.tabs.addTab(self.rules_tab, "Rules Management")
        self.tabs.addTab(self.statistics_tab, "Rule Statistics")
        self.tabs.addTab(self.loan_evaluation_tab, "Loan evaluation") # 新增
        
        # Main layout

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        

        # 确保显示数据
        self.display_rules_data(self.rules_data)

    def create_modern_name_list_tab(self):
        tab = QWidget()
        tab.setStyleSheet("""
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

        # Filter criteria
        filter_form = QHBoxLayout()

        # RCID filter
        filter_form.addWidget(QLabel("RCID:"))
        self.name_filter = QLineEdit()
        self.name_filter.setPlaceholderText("Please enter RCID")
        filter_form.addWidget(self.name_filter)

        # ID filter
        filter_form.addWidget(QLabel("ID:"))
        self.id_filter = QLineEdit()
        self.id_filter.setPlaceholderText("Please enter ID")
        filter_form.addWidget(self.id_filter)

        # Status filter
        filter_form.addWidget(QLabel("Status:"))
        self.status_filter = QComboBox()
        self.status_filter.addItems(["All", "Valid", "Invalid"])
        filter_form.addWidget(self.status_filter)

        # Type filter
        filter_form.addWidget(QLabel("Type:"))
        self.type_filter = QComboBox()
        self.type_filter.addItems(["All", "Phone", "Email"])
        filter_form.addWidget(self.type_filter)
        
        # Risk Domain filter
        filter_form.addWidget(QLabel("Risk Domain:"))
        self.risk_domain_filter = QComboBox()
        self.risk_domain_filter.addItems(["All", "Anti-cheat", "Anti-fraud", "Anti-attack"])
        filter_form.addWidget(self.risk_domain_filter)
        
        # Business Line filter
        filter_form.addWidget(QLabel("Business Line:"))
        self.stuff_filter = QComboBox()
        self.stuff_filter.addItems(["All", "Loan", "Credit Card"])
        filter_form.addWidget(self.stuff_filter)

        # Search button
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_name_list)

        # Reset button
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_name_filters)
        self.reset_button.setStyleSheet("""
            background-color: #6c757d;
            color: white;
        """)

        filter_layout.addLayout(filter_form)
        filter_layout.addWidget(self.search_button)
        filter_layout.addWidget(self.reset_button)
        filter_frame.setLayout(filter_layout)

        # Add filter frame to main layout
        layout.addWidget(filter_frame)

        # Action buttons area
        button_layout = QHBoxLayout()
        
        self.add_button = QPushButton("+ New")
        self.add_button.clicked.connect(lambda: self.add_name_list_entry())
        
        self.batch_button = QPushButton("Batch Import")
        
        self.more_button = QPushButton("More Actions ▼")
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.batch_button)
        button_layout.addWidget(self.more_button)
        button_layout.addStretch()
        
        # Status label
        status_label = QLabel("Name list cache filter is online")
        status_label.setObjectName("statusLabel")
        
        # Table
        self.name_list_table = QTableWidget()
        self.name_list_table.setColumnCount(11)
        self.name_list_table.setHorizontalHeaderLabels([
            "", "RCID", "ID", "Type", "Rule Hit-count", "Business Line",
            "Risk Domain", "Risk Tag", "Status", "List Creation Time", "Actions"
        ])
        self.name_list_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.name_list_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.name_list_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.name_list_table.verticalHeader().setVisible(False)
        self.load_name_list()
        
        layout.addLayout(button_layout)
        layout.addWidget(status_label)
        layout.addWidget(self.name_list_table)
        
        tab.setLayout(layout)
        return tab

    def search_risk_control(self):
        """搜索和过滤规则基于RuleID和Status"""
        # 获取过滤值
        rule_id_filter = self.rule_id_filter.text().strip().lower()
        status_filter = self.rule_status_filter.currentText()

        # 如果选择了"Please select"，则不进行状态过滤
        if status_filter == "Please select":
            status_filter = ""

        # 过滤规则数据
        filtered_data = []
        for rule in self.rules_data:
            rule_id = rule["id"].lower()
            status = rule["status"]

            # 应用过滤条件：rule_id部分匹配，status完全匹配
            if (not rule_id_filter or rule_id_filter in rule_id) and \
               (not status_filter or status_filter == status):
                filtered_data.append(rule)

        # 显示过滤后的结果
        self.display_rules_data(filtered_data)
        
        # 如果没有找到结果，显示提示
        if not filtered_data:
            QMessageBox.information(self, 'Search Results', 'No rules match the search criteria.')

    def reset_filters(self):
        """重置所有过滤器并显示所有规则"""
        # 清除过滤输入
        self.rule_id_filter.clear()
        self.rule_status_filter.setCurrentIndex(0)  # 重置为"Please select"
        
        # 重新加载所有规则数据
        self.display_rules_data(self.rules_data)

    def display_rules_data(self, data):
        """在表格中显示规则数据"""
        print(f"显示数据条数: {len(data)}")  # 调试日志
        
        # 先清空表格
        self.rules_table.setRowCount(0)
        
        # 对每条规则数据进行处理
        for row_idx, rule in enumerate(data):
            self.rules_table.insertRow(row_idx)

            # 添加复选框
            checkbox_widget = QWidget()
            checkbox_layout = QHBoxLayout(checkbox_widget)
            checkbox = QCheckBox()
            checkbox_layout.addWidget(checkbox)
            checkbox_layout.setAlignment(Qt.AlignCenter)
            checkbox_layout.setContentsMargins(0, 0, 0, 0)
            self.rules_table.setCellWidget(row_idx, 0, checkbox_widget)

            # 规则ID
            rule_id_item = QTableWidgetItem(rule["id"])
            rule_id_item.setTextAlignment(Qt.AlignCenter)
            self.rules_table.setItem(row_idx, 1, rule_id_item)

            # 规则描述
            desc_item = QTableWidgetItem(rule["description"])
            desc_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.rules_table.setItem(row_idx, 2, desc_item)

            # 服务调用次数
            calls_item = QTableWidgetItem(str(rule["calls"]))
            calls_item.setTextAlignment(Qt.AlignCenter)
            self.rules_table.setItem(row_idx, 3, calls_item)

            # 状态
            status_widget = QWidget()
            status_layout = QHBoxLayout(status_widget)
            status_layout.setContentsMargins(5, 0, 5, 0)
            status_layout.setSpacing(5)

            # 根据状态设置不同颜色的点
            status_dot = QLabel("●")
            if rule["status"] == "Running":
                status_dot.setStyleSheet("color: #36ce5e;")  # 绿色
            elif rule["status"] == "Disabled":
                status_dot.setStyleSheet("color: #9b9b9b;")  # 灰色
            else:  # Exception
                status_dot.setStyleSheet("color: #f43f5f;")  # 红色

            status_text = QLabel(rule["status"])
            status_layout.addWidget(status_dot)
            status_layout.addWidget(status_text)
            status_layout.addStretch()
            self.rules_table.setCellWidget(row_idx, 4, status_widget)

            # 更新时间
            time_item = QTableWidgetItem(rule["update_time"])
            time_item.setTextAlignment(Qt.AlignCenter)
            self.rules_table.setItem(row_idx, 5, time_item)

            # 操作按钮
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(5, 0, 5, 0)

            # 根据状态添加不同的按钮
            if rule["status"] == "Disabled":
                enable_btn = QPushButton("Enable")
                enable_btn.setStyleSheet("color: #4aa3df; background: transparent; border: none;")
                action_layout.addWidget(enable_btn)
            else:
                disable_btn = QPushButton("Disable")
                disable_btn.setStyleSheet("color: #4aa3df; background: transparent; border: none;")
                action_layout.addWidget(disable_btn)

            subscribe_btn = QPushButton("Subscribe to Alerts")
            subscribe_btn.setStyleSheet("color: #4aa3df; background: transparent; border: none;")
            action_layout.addWidget(subscribe_btn)

            action_layout.addStretch()
            action_widget.setLayout(action_layout)
            self.rules_table.setCellWidget(row_idx, 6, action_widget)

    def create_rules_tab(self):
        tab = QWidget()
        tab.setStyleSheet("""
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
            QPushButton#secondaryButton {
                background-color: white;
                color: #333;
                border: 1px solid #ddd;
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
        """)
        
        layout = QVBoxLayout()
        
        # 创建过滤区域
        filter_layout = QHBoxLayout()
        
        # RuleID过滤
        filter_layout.addWidget(QLabel("RuleID:"))
        self.rule_id_filter = QLineEdit()
        self.rule_id_filter.setPlaceholderText("Please enter Rule ID")
        self.rule_id_filter.setFixedWidth(180)
        filter_layout.addWidget(self.rule_id_filter)
        
        # 状态过滤
        filter_layout.addWidget(QLabel("Status:"))
        self.rule_status_filter = QComboBox()
        self.rule_status_filter.addItems(["Please select", "Disabled", "Running", "Exception"])
        self.rule_status_filter.setFixedWidth(120)
        filter_layout.addWidget(self.rule_status_filter)
        
        # 搜索按钮
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_risk_control)
        filter_layout.addWidget(self.search_button)

        # 重置按钮
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_filters)
        self.reset_button.setStyleSheet("""
            background-color: #ffffff;
            color: #3e89fa;
            border: 1px solid #3e89fa;
        """)
        filter_layout.addWidget(self.reset_button)
        
        filter_layout.addStretch()
        
        # 操作按钮区域
        button_layout = QHBoxLayout()
        
        self.add_rule_button = QPushButton("+ New")
        self.add_rule_button.clicked.connect(self.add_rule)
        
        self.batch_import_button = QPushButton("Batch Import")
        
        self.more_actions_button = QPushButton("More Actions ▼")
        
        button_layout.addWidget(self.add_rule_button)
        button_layout.addWidget(self.batch_import_button)
        button_layout.addWidget(self.more_actions_button)
        button_layout.addStretch()
        
        # 状态信息框
        status_frame = QFrame()
        status_frame.setObjectName("statusFrame")
        status_layout = QHBoxLayout()
        
        status_icon = QLabel("●")
        status_icon.setStyleSheet("color: #4aa3df;")
        status_layout.addWidget(status_icon)
        
        status_text = QLabel("Risk control rules filter status notification")
        status_layout.addWidget(status_text)
        
        clear_button = QPushButton("Clear")
        clear_button.setStyleSheet("color: #4aa3df; background: transparent; border: none;")
        status_layout.addStretch()
        status_layout.addWidget(clear_button)
        
        status_frame.setLayout(status_layout)
        
        # 规则表格
        self.rules_table = QTableWidget()
        self.rules_table.setColumnCount(7)
        self.rules_table.setHorizontalHeaderLabels([
            "", "Rule ID", "Description", "Service Call Count", "Status", "Updated Time", "Actions"
        ])
        self.rules_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.rules_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.rules_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.rules_table.verticalHeader().setVisible(False)
        
        # 分页区域
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
        
        for btn in [self.prev_page_btn, self.page_1_btn, self.page_2_btn, self.page_3_btn, 
                    self.page_4_btn, self.page_5_btn, self.page_6_btn, self.page_7_btn, 
                    self.page_8_btn, self.page_9_btn, self.next_page_btn]:
            btn.setFixedSize(32, 32)
            if btn != self.page_1_btn:
                btn.setStyleSheet("background-color: white; color: #333; border: 1px solid #ddd;")
            pagination_layout.addWidget(btn)
        
        pagination_layout.addStretch()
        
        # 添加所有组件到主布局
        layout.addLayout(filter_layout)
        layout.addSpacing(10)
        layout.addLayout(button_layout)
        layout.addSpacing(10)
        layout.addWidget(status_frame)
        layout.addWidget(self.rules_table)
        layout.addLayout(pagination_layout)
        
        tab.setLayout(layout)
        return tab
        
    
    def create_statistics_tab(self):
        tab = QWidget()
        tab.setStyleSheet("""
            QWidget {
                background-color: white;
                color: #333333;
                font-family: Arial, sans-serif;
            }
            QGroupBox {
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                margin-top: 1em;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: #3e89fa;
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
            QFrame#infoFrame {
                background-color: #f2f8fd;
                border-radius: 4px;
                border: 1px solid #d6e9f8;
                margin: 5px;
                padding: 10px;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Add title and info frame
        title_label = QLabel("Risk Control Rules Statistics")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        
        info_frame = QFrame()
        info_frame.setObjectName("infoFrame")
        info_layout = QHBoxLayout()
        
        info_icon = QLabel("●")
        info_icon.setStyleSheet("color: #4aa3df;")
        info_layout.addWidget(info_icon)
        
        info_text = QLabel("Risk control rule hit statistics data, showing the hit counts of each rule and categorized by business line.")
        info_layout.addWidget(info_text)
        info_layout.addStretch()
        
        info_frame.setLayout(info_layout)
        
        # Operation button area
        button_layout = QHBoxLayout()
        
        refresh_button = QPushButton('Refresh Statistics Data')
        refresh_button.clicked.connect(self.refresh_statistics)
        
        export_button = QPushButton('Export Statistics')
        export_button.clicked.connect(lambda: QMessageBox.information(self, "Notice", "Export function under development..."))
        
        button_layout.addWidget(refresh_button)
        button_layout.addWidget(export_button)
        button_layout.addStretch()
        
        # Rule hit count table
        hit_count_group = QGroupBox("Rule Hit Statistics")
        hit_count_layout = QVBoxLayout()
        
       
        self.hit_count_table = QTableWidget()
        self.hit_count_table.setColumnCount(3)
        self.hit_count_table.setHorizontalHeaderLabels(['Rule ID', 'Rule Name', 'Hit Count'])
        self.hit_count_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.hit_count_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.hit_count_table.setAlternatingRowColors(True)
        self.hit_count_table.setStyleSheet("alternate-background-color: #f9f9f9;")
        
        # Load hit count data
        self.load_hit_count()
        
        hit_count_layout.addWidget(self.hit_count_table)
        hit_count_group.setLayout(hit_count_layout)
        
        # Business line hit table
        business_hit_group = QGroupBox("Business Line Rule Hit Statistics")
        business_hit_layout = QVBoxLayout()
        
        self.business_hit_table = QTableWidget()
        self.business_hit_table.setColumnCount(3)
        self.business_hit_table.setHorizontalHeaderLabels(['Business Line', 'Rule Type', 'Hit Count'])
        self.business_hit_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.business_hit_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.business_hit_table.setAlternatingRowColors(True)
        self.business_hit_table.setStyleSheet("alternate-background-color: #f9f9f9;")
        
        # Load business hit data
        self.load_business_hit()
        
        business_hit_layout.addWidget(self.business_hit_table)
        business_hit_group.setLayout(business_hit_layout)
        
        # Add all components to main layout
        layout.addWidget(title_label)
        layout.addWidget(info_frame)
        layout.addLayout(button_layout)
        layout.addWidget(hit_count_group)
        layout.addWidget(business_hit_group)
        
        tab.setLayout(layout)
        return tab

    def create_loan_evaluation_tab(self):
        """创建贷款评估子页面"""
        tab = QWidget()
        tab.setStyleSheet("""
            QWidget {
                background-color: white;
                color: #333333;
                font-family: Arial, sans-serif;
            }
            QLabel {
                font-size: 13px;
                color: #333333;
            }
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
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
            QGroupBox {
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                margin-top: 1em;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: #3e89fa;
            }
        """)
        
        layout = QVBoxLayout()
        
        # 申请人信息表单区域
        applicant_group = QGroupBox("Applicant Basic Information")
        applicant_form = QFormLayout()
        
        self.applicant_name = QLineEdit()
        self.applicant_name.setPlaceholderText("Enter applicant's name")
        
        self.applicant_id = QLineEdit()
        self.applicant_id.setPlaceholderText("Enter ID number")
        
        self.applicant_phone = QLineEdit()
        self.applicant_phone.setPlaceholderText("Enter phone number")
        
        self.applicant_address = QLineEdit()
        self.applicant_address.setPlaceholderText("Enter address")
        
        applicant_form.addRow("Name:", self.applicant_name)
        applicant_form.addRow("ID Number:", self.applicant_id)
        applicant_form.addRow("Phone Number::", self.applicant_phone)
        applicant_form.addRow("Address:", self.applicant_address)
        
        applicant_group.setLayout(applicant_form)
        
        # 贷款信息表单区域
        loan_group = QGroupBox("Loan Information")
        loan_form = QFormLayout()
        
        self.loan_amount = QDoubleSpinBox()
        self.loan_amount.setRange(1000, 1000000)
        self.loan_amount.setValue(50000)
        self.loan_amount.setSingleStep(1000)
        self.loan_amount.setPrefix("¥ ")
        
        self.loan_term = QComboBox()
        self.loan_term.addItems(["6 months", "12 months", "24 months", "36 months", "60 months"])
        
        self.loan_purpose = QComboBox()
        self.loan_purpose.addItems(["Consumer Loan", "Housing Loan", "Auto Loan", "Education Loan", "Business Loan"])
        
        loan_form.addRow("Loan Amount:", self.loan_amount)
        loan_form.addRow("Loan Term:", self.loan_term)
        loan_form.addRow("Loan Purpose:", self.loan_purpose)
        
        loan_group.setLayout(loan_form)
        
        # 风控指标表单区域
        risk_group = QGroupBox("Risk Indicators")
        risk_form = QFormLayout()
        
        self.credit_score = QSpinBox()
        self.credit_score.setRange(300, 900)
        self.credit_score.setValue(700)
        self.credit_score.setSingleStep(1)
        
        self.overdue_count = QSpinBox()
        self.overdue_count.setRange(0, 100)
        self.overdue_count.setValue(0)
        
        self.max_overdue_days = QSpinBox()
        self.max_overdue_days.setRange(0, 1000)
        self.max_overdue_days.setValue(0)
        
        self.debt_ratio = QDoubleSpinBox()
        self.debt_ratio.setRange(0, 1)
        self.debt_ratio.setValue(0.3)
        self.debt_ratio.setSingleStep(0.01)
        self.debt_ratio.setDecimals(2)
        
        self.has_mortgage = QCheckBox("Yes")
        self.has_car_loan = QCheckBox("Yes")

        risk_form.addRow("Credit Score:", self.credit_score)
        risk_form.addRow("Historical Overdue Count:", self.overdue_count)
        risk_form.addRow("Max Overdue Days:", self.max_overdue_days)
        risk_form.addRow("Debt-to-Income Ratio:", self.debt_ratio)

        mortgage_layout = QHBoxLayout()
        mortgage_layout.addWidget(self.has_mortgage)
        mortgage_layout.addStretch()
        risk_form.addRow("Has Mortgage:", mortgage_layout)

        car_loan_layout = QHBoxLayout()
        car_loan_layout.addWidget(self.has_car_loan)
        car_loan_layout.addStretch()
        risk_form.addRow("Has Car Loan:", car_loan_layout)
        
        risk_group.setLayout(risk_form)
        
        # 操作按钮区域
        button_layout = QHBoxLayout()
        
        self.evaluate_button = QPushButton("Evaluate Application")
        self.evaluate_button.clicked.connect(self.evaluate_loan_application)

        self.reset_button = QPushButton("Reset")
        self.reset_button.setStyleSheet("""
            background-color: #6c757d;
            color: white;
        """)
        self.reset_button.clicked.connect(self.reset_loan_form)

        button_layout.addStretch()
        button_layout.addWidget(self.evaluate_button)
        button_layout.addWidget(self.reset_button)
        button_layout.addStretch()

        # Evaluation result section
        result_group = QGroupBox("Evaluation Result")
        result_layout = QVBoxLayout()
        
        # 总体结果显示
        self.result_frame = QFrame()
        self.result_frame.setStyleSheet("""
            QFrame {
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                background-color: #f8f9fa;
                padding: 10px;
            }
        """)
        result_frame_layout = QVBoxLayout()
        
        self.result_title = QLabel("Please complete the form and click Evaluate Application")
        self.result_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #3e89fa;")
        self.result_title.setAlignment(Qt.AlignCenter)
        
        self.result_score = QLabel("")
        self.result_score.setAlignment(Qt.AlignCenter)
        
        result_frame_layout.addWidget(self.result_title)
        result_frame_layout.addWidget(self.result_score)
        self.result_frame.setLayout(result_frame_layout)
        
        # Triggered rules list
        self.triggered_rules_label = QLabel("Triggered Risk Control Rules:")
        self.triggered_rules_label.setVisible(False)

        self.rules_table = QTableWidget()
        self.rules_table.setColumnCount(4)
        self.rules_table.setHorizontalHeaderLabels(["Rule ID", "Rule Name", "Rule Description", "Penalty"])
        self.rules_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.rules_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.rules_table.setAlternatingRowColors(True)
        self.rules_table.setVisible(False)
        
        result_layout.addWidget(self.result_frame)
        result_layout.addWidget(self.triggered_rules_label)
        result_layout.addWidget(self.rules_table)
        
        result_group.setLayout(result_layout)
        
        # 添加所有组件到主布局
        layout.addWidget(applicant_group)
        layout.addWidget(loan_group)
        layout.addWidget(risk_group)
        layout.addLayout(button_layout)
        layout.addWidget(result_group)
        
        tab.setLayout(layout)
        return tab

    def display_evaluation_result(self, result):
        """显示贷款评估结果"""
        if result["approved"]:
            self.result_title.setText("Application Approved")
            self.result_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #28a745;")
            self.result_frame.setStyleSheet("QFrame { border: 1px solid #28a745; border-radius: 4px; background-color: #d4edda; padding: 10px; }")
        else:
            self.result_title.setText("Application Rejected")
            self.result_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #dc3545;")
            self.result_frame.setStyleSheet("QFrame { border: 1px solid #dc3545; border-radius: 4px; background-color: #f8d7da; padding: 10px; }")

        self.result_score.setText(f"Risk Score: {result['score']}/100")    
        
        # 显示触发的规则
        triggered_rules = result.get("rule_results", [])
        
        if triggered_rules:
            self.triggered_rules_label.setVisible(True)
            self.rules_table.setVisible(True)
            self.rules_table.setRowCount(len(triggered_rules))
            
            for row, rule in enumerate(triggered_rules):
                self.rules_table.setItem(row, 0, QTableWidgetItem(rule["rule_id"]))
                self.rules_table.setItem(row, 1, QTableWidgetItem(rule["rule_name"]))
                self.rules_table.setItem(row, 2, QTableWidgetItem(rule["rule_expression"]))
                self.rules_table.setItem(row, 3, QTableWidgetItem(str(rule["penalty"])))
                
                # 为高扣分项添加红色背景
                if rule["penalty"] > 20:
                    for col in range(4):
                        self.rules_table.item(row, col).setBackground(QColor(255, 235, 235))
        else:
            self.triggered_rules_label.setVisible(False)
            self.rules_table.setVisible(False)

    def reset_loan_form(self):
        """Reset loan application form"""
        # 重置申请人信息
        self.applicant_name.clear()
        self.applicant_id.clear()
        self.applicant_phone.clear()
        self.applicant_address.clear()
        
        # 重置贷款信息
        self.loan_amount.setValue(50000)
        self.loan_term.setCurrentIndex(0)
        self.loan_purpose.setCurrentIndex(0)
        
        # 重置风控指标
        self.credit_score.setValue(700)
        self.overdue_count.setValue(0)
        self.max_overdue_days.setValue(0)
        self.debt_ratio.setValue(0.3)
        self.has_mortgage.setChecked(False)
        self.has_car_loan.setChecked(False)
        
        # 重置结果区域
        self.result_title.setText("Please complete the form and click Evaluate Application")
        self.result_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #3e89fa;")
        self.result_frame.setStyleSheet("QFrame { border: 1px solid #e0e0e0; border-radius: 4px; background-color: #f8f9fa; padding: 10px; }")
  
        self.result_score.setText("")
        self.triggered_rules_label.setVisible(False)
        self.rules_table.setVisible(False)

    def load_name_list(self):
        self.name_list_table.setRowCount(0)
        
        for row_num, data in enumerate(mock_data_RC):
            self.name_list_table.insertRow(row_num)
            
            # Add checkbox column
            self.name_list_table.setItem(row_num, 0, QTableWidgetItem(""))
            
            for col_num, cell_data in enumerate(data):
                item = QTableWidgetItem(cell_data)
                item.setTextAlignment(Qt.AlignCenter)
                
                # Status column
                if col_num == 7:
                    if cell_data == "Valid":
                        item.setBackground(QColor(240, 255, 240))
                        item.setForeground(QColor(40, 167, 69))
                    else:
                        item.setBackground(QColor(248, 248, 248))
                        item.setForeground(QColor(108, 117, 125))
                
                self.name_list_table.setItem(row_num, col_num + 1, item)
            
            # Add operations column - using plain text instead of buttons
            operations = QTableWidgetItem("Add to Whitelist  Add to Blacklist")
            operations.setForeground(QColor(0, 123, 255))
            operations.setTextAlignment(Qt.AlignCenter)
            self.name_list_table.setItem(row_num, 10, operations)

    def evaluate_loan_application(self):
        """处理按钮点击，提交数据并调用 controller 的风控方法"""
        applicant_data = {
            "name": self.applicant_name.text(),
            "id": self.applicant_id.text(),
            "phone": self.applicant_phone.text(),
            "address": self.applicant_address.text(),
            "loan_amount": self.loan_amount.value(),
            "loan_term": self.loan_term.currentText(),
            "loan_purpose": self.loan_purpose.currentText(),
            "credit_score": self.credit_score.value(),
            "overdue_count": self.overdue_count.value(),
            "max_overdue_days": self.max_overdue_days.value(),
            "debt_ratio": self.debt_ratio.value(),
            "has_mortgage": self.has_mortgage.isChecked(),
            "has_car_loan": self.has_car_loan.isChecked()
        }

        result = self.controller.evaluate_loan_application(applicant_data)
        self.display_evaluation_result(result)

    def load_hit_count(self):
        """Load rule hit count statistics"""
        self.hit_count_table.setRowCount(0)
        
        try:
            # Count the number of calls for RuleCode and TradeCode
            rule_code_count = 0
            trade_code_count = 0
            
            # Iterate through rule data to count the number and hit count for different types of rules
            for rule in mock_data_RULES:
                rule_id = rule["id"]
                rule_name = rule["description"]
                hit_count = rule["calls"]
                status = rule["status"]
                timestamp = rule["update_time"]

                # 处理包含"K"的字符串，例如"1.2K"
                if isinstance(hit_count, str) and 'K' in hit_count:
                    hit_count_value = float(hit_count.replace('K', '')) * 1000
                else:
                    hit_count_value = float(hit_count)

                    
                if rule_id.startswith("RuleCode"):
                    rule_code_count += hit_count_value
                elif rule_id.startswith("TradeCode"):
                    trade_code_count += hit_count_value
            
            # Add the statistics to the table
            self.hit_count_table.insertRow(0)
            self.hit_count_table.setItem(0, 0, QTableWidgetItem("RuleCode"))
            self.hit_count_table.setItem(0, 1, QTableWidgetItem("Business Rules"))
            self.hit_count_table.setItem(0, 2, QTableWidgetItem(str(int(rule_code_count))))
            
            self.hit_count_table.insertRow(1)
            self.hit_count_table.setItem(1, 0, QTableWidgetItem("TradeCode"))
            self.hit_count_table.setItem(1, 1, QTableWidgetItem("Transaction Rules"))
            self.hit_count_table.setItem(1, 2, QTableWidgetItem(str(int(trade_code_count))))
            
        except Exception as e:
            print(f"Error loading rule hit count statistics: {e}")

    def load_business_hit(self):
        """Load rule hit statistics by business line"""
        self.business_hit_table.setRowCount(0)
        
        try:
            # Create a dictionary for rule hit statistics by business line
            business_hits = {}
            
            # Iterate through data to count rule hits per business line
            for rc_id, user_id, channel, hit_count, business_line, rule_type, list_type, status, timestamp in mock_data_RC:
                if business_line not in business_hits:
                    business_hits[business_line] = {
                        "Anti-cheat": 0,
                        "Anti-fraud": 0,
                        "Anti-attack": 0,
                        "Total": 0
                    }
                
                # Accumulate hit counts
                hit_count_int = int(hit_count)
                if rule_type in business_hits[business_line]:
                    business_hits[business_line][rule_type] += hit_count_int
                business_hits[business_line]["Total"] += hit_count_int
            
            # Add the statistics to the table
            row_num = 0
            for business_line, rule_hits in business_hits.items():
                for rule_type, count in rule_hits.items():
                    # Include "Total" rows
                    self.business_hit_table.insertRow(row_num)
                    self.business_hit_table.setItem(row_num, 0, QTableWidgetItem(business_line))
                    self.business_hit_table.setItem(row_num, 1, QTableWidgetItem(rule_type))
                    self.business_hit_table.setItem(row_num, 2, QTableWidgetItem(str(count)))
                    row_num += 1
                
        except Exception as e:
            print(f"Error loading business line rule hit statistics: {e}")
    
    def refresh_statistics(self):
        self.load_hit_count()
        self.load_business_hit()
        QMessageBox.information(self, 'Success', 'Statistics refreshed!')
    
    def add_name_list_entry(self):
        # Create dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Name List Entry")
        dialog.setFixedWidth(400)
        
        # Form layout
        form_layout = QFormLayout()
        
        rule_id_input = QSpinBox()
        rule_id_input.setRange(1, 9999)
        
        risk_level_input = QSpinBox()
        risk_level_input.setRange(1, 5)
        
        list_type_combo = QComboBox()
        list_type_combo.addItems(['Blacklist', 'Whitelist', 'Greylist'])
        
        business_line_combo = QComboBox()
        business_line_combo.addItems(['Loan', 'Credit Card', 'Payment', 'Food Delivery', 'Bike Sharing', 'At Home', 'In Store'])
        
        risk_label_combo = QComboBox()
        risk_label_combo.addItems(['Fraud', 'Credit', 'Compliance', 'Operations'])
        
        risk_domain_combo = QComboBox()
        risk_domain_combo.addItems(['Personal', 'Corporate', 'Device', 'Other'])
        
        value_input = QLineEdit()
        value_input.setPlaceholderText('Phone number/ID/IP, etc.')
        
        value_type_combo = QComboBox()
        value_type_combo.addItems(['Phone Number', 'QQ Number', 'WeChat ID', 'Bank Card Number', 'IP Address', 'Device ID'])
        
        form_layout.addRow('Rule ID:', rule_id_input)
        form_layout.addRow('Risk Level:', risk_level_input)
        form_layout.addRow('List Type:', list_type_combo)
        form_layout.addRow('Business Line:', business_line_combo)
        form_layout.addRow('Risk Label:', risk_label_combo)
        form_layout.addRow('Risk Domain:', risk_domain_combo)
        form_layout.addRow('Value:', value_input)
        form_layout.addRow('Value Type:', value_type_combo)
        
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(button_box)
        
        dialog.setLayout(main_layout)
        
        # Show dialog
        if dialog.exec_() == QDialog.Accepted:
            rule_id = rule_id_input.value()
            risk_level = risk_level_input.value()
            list_type = list_type_combo.currentIndex() + 1
            business_line = business_line_combo.currentIndex() + 1
            risk_label = risk_label_combo.currentIndex() + 1
            risk_domain = risk_domain_combo.currentIndex() + 1
            value = value_input.text()
            value_type = value_type_combo.currentIndex() + 1
            
            if not value:
                QMessageBox.warning(self, 'Warning', 'Value cannot be empty!')
                return
            
            success = self.controller.add_name_list_entry(
                rule_id, risk_level, list_type, business_line,
                risk_label, risk_domain, value, value_type
            )
            
            if success:
                QMessageBox.information(self, 'Success', 'Name list entry added successfully!')
                self.load_name_list()
            else:
                QMessageBox.warning(self, 'Failure', 'Failed to add name list entry!')

    def delete_name_list_entry(self):
        selected_items = self.name_list_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, 'Warning', 'Please select a record to delete first!')
            return
        
        row = selected_items[0].row()
        entry_id = self.name_list_table.item(row, 1).text()
        value = self.name_list_table.item(row, 2).text()
        
        reply = QMessageBox.question(
            self, 'Confirm Deletion',
            f'Are you sure you want to delete the entry with value "{value}"?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success = self.controller.delete_name_list_entry(entry_id)
            
            if success:
                QMessageBox.information(self, 'Success', 'Record deleted successfully!')
                self.load_name_list()
            else:
                QMessageBox.warning(self, 'Failure', 'Failed to delete record!')
    
    def check_hit(self):
        value = self.name_filter.text()
        if not value:
            QMessageBox.warning(self, 'Warning', 'Please enter a value to check!')
            return
        
        value_type = self.type_filter.currentIndex()
        hits = self.controller.check_hit(value, value_type if value_type > 0 else None)
        
        if hits:
            hit_msg = "\n".join([f"Rule ID: {hit[2]}, Rule Name: {hit[3]}" for hit in hits])
            QMessageBox.information(self, 'Hit Rules', f'Value "{value}" hit the following rules:\n{hit_msg}')
        else:
            QMessageBox.information(self, 'No Hits', f'Value "{value}" did not hit any rules.')
    
    def add_rule(self):
        """Open dialog to add new rule"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Risk Control Rule")
        dialog.setMinimumSize(600, 500)
        
        dialog_layout = QVBoxLayout()
        
        # Rule scope selection
        scope_layout = QHBoxLayout()
        scope_label = QLabel("* Rule Scope:")
        scope_label.setStyleSheet("color: #333; font-size: 14px;")
        scope_layout.addWidget(scope_label)
        
        external_radio = QRadioButton("External")
        internal_radio = QRadioButton("Internal")
        internal_radio.setChecked(True)  # Default to Internal
        
        # Radio button style
        radio_style = """
            QRadioButton {
                spacing: 5px;
                color: #333;
                font-size: 14px;
            }
            QRadioButton::indicator {
                width: 20px;
                height: 20px;
                border-radius: 10px;
                border: 2px solid #ccc;
            }
            QRadioButton::indicator:checked {
                background-color: #3e89fa;
                border: 2px solid #3e89fa;
            }
        """
        external_radio.setStyleSheet(radio_style)
        internal_radio.setStyleSheet(radio_style)
        
        scope_layout.addWidget(external_radio)
        scope_layout.addWidget(internal_radio)
        scope_layout.addStretch()
        
        # Select service
        service_layout = QHBoxLayout()
        service_label = QLabel("* Select Service:")
        service_label.setStyleSheet("color: #333; font-size: 14px;")
        service_layout.addWidget(service_label)
        
        service_combo = QComboBox()
        service_combo.addItem("Please select")
        service_combo.addItems(["Loan", "Credit Card", "Payment", "Other Services"])
        service_combo.setMinimumWidth(350)
        service_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 5px;
                background: white;
                min-height: 30px;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #ddd;
                border-left-style: solid;
            }
        """)
        
        service_layout.addWidget(service_combo)
        service_layout.addStretch()
        
        # Rule description
        description_layout = QHBoxLayout()
        description_label = QLabel("Rule Description:")
        description_label.setStyleSheet("color: #333; font-size: 14px;")
        description_layout.addWidget(description_label)
        
        description_input = QLineEdit()
        description_input.setMinimumWidth(350)
        description_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 5px;
                min-height: 30px;
                            }
                        """)

        description_layout.addWidget(description_input)
        description_layout.addStretch()
        
        # Rule content
        content_label = QLabel("* Rule Content:")
        content_label.setStyleSheet("color: #333; font-size: 14px;")
        
       
        content_input = QTextEdit()
        content_input.setPlaceholderText("Please enter a valid rule expression")
        content_input.setMinimumHeight(200)
        content_input.setStyleSheet("""
            QTextEdit {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 5px;
            }
        """)
        
        # Character count
        char_count = QLabel("(0/9)")
        char_count.setStyleSheet("color: #999; font-size: 12px;")
        
        # Button area
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_button = QPushButton("Cancel")
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #333;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 8px 20px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
            }
        """)
        cancel_button.clicked.connect(dialog.reject)
        
        add_button = QPushButton("Add")
        add_button.setStyleSheet("""
            QPushButton {
                background-color: #3e89fa;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 20px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #2d7bf0;
            }
        """)
        
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(add_button)
        
        # Add all elements to dialog layout
        dialog_layout.addLayout(scope_layout)
        dialog_layout.addSpacing(15)
        dialog_layout.addLayout(service_layout)
        dialog_layout.addSpacing(15)
        dialog_layout.addLayout(description_layout)
        dialog_layout.addSpacing(15)
        dialog_layout.addWidget(content_label)
        dialog_layout.addWidget(content_input)
        dialog_layout.addWidget(char_count, 0, Qt.AlignRight)
        dialog_layout.addStretch()
        dialog_layout.addLayout(button_layout)
        
        dialog.setLayout(dialog_layout)
        
        # Update character count on text change
        def update_char_count():
            count = len(content_input.toPlainText())
            char_count.setText(f"({count}/9)")
        
        content_input.textChanged.connect(update_char_count)
        
        # Add button click handler
        def on_add_clicked():
            rule_name = description_input.text()
            rule_expression = content_input.toPlainText()
            is_external = external_radio.isChecked()
            
            if not rule_name and not rule_expression:
                QMessageBox.warning(dialog, 'Warning', 'Rule name and expression cannot be empty!')
                return
                
            if service_combo.currentIndex() == 0:
                QMessageBox.warning(dialog, 'Warning', 'Please select a service!')
                return
            
            success = self.controller.add_rule(rule_name, rule_expression, 1 if is_external else 0, "medium")
            
            if success:
                QMessageBox.information(dialog, 'Success', 'Rule added successfully!')
                dialog.accept()
                self.load_rules()
            else:
                QMessageBox.warning(dialog, 'Failure', 'Failed to add rule!')
        
        add_button.clicked.connect(on_add_clicked)
        
        # Show dialog
        dialog.exec_()
        
    def reset_name_filters(self):
        """Reset all name list filters"""
        self.name_filter.clear()
        self.id_filter.clear()
        self.status_filter.setCurrentIndex(0)
        self.type_filter.setCurrentIndex(0)
        self.risk_domain_filter.setCurrentIndex(0)
        self.stuff_filter.setCurrentIndex(0)
        
        # Reload all data
        self.load_name_list()

    def search_name_list(self):
        """Search name list based on filters"""
        # Get filter values
        name_filter = self.name_filter.text().strip()
        id_filter = self.id_filter.text().strip()
        status_filter = self.status_filter.currentText()
        type_filter = self.type_filter.currentText()
        risk_domain_filter = self.risk_domain_filter.currentText()
        stuff_filter = self.stuff_filter.currentText()
        
        # Apply filter logic
        filtered_data = []
        for item in mock_data_RC:  # Assume you have a list storing all name list data
            # Check each filter condition
            if name_filter and name_filter not in item[0]:
                continue
            
            if id_filter and id_filter != item[1]:
                continue
            
            if status_filter != "All" and status_filter != item[7]:
                continue
            
            if risk_domain_filter != "All" and risk_domain_filter != item[5]:
                continue
            
            if type_filter != "All" and type_filter != item[2]:
                continue
            
            if stuff_filter != "All" and stuff_filter != item[4]:
                continue
            
            # Passed all filters, add to results
            filtered_data.append(item)
        
        if filtered_data:
            self.fill_name_list_table(filtered_data)  # Assume you have a method to fill the table
        else:
            # No matching records
            self.name_list_table.setRowCount(0)
            QMessageBox.information(self, 'Notice', 'No records match the criteria!')

    def fill_name_list_table(self, data):
        """Fill name list table with data"""
        # Clear table
        self.name_list_table.setRowCount(0)
        
        # Fill table with data
        for row_num, row_data in enumerate(data):
            self.name_list_table.insertRow(row_num)
            
            # Add checkbox column (if needed)
            checkbox_item = QTableWidgetItem()
            checkbox_item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            checkbox_item.setCheckState(Qt.Unchecked)
            self.name_list_table.setItem(row_num, 0, checkbox_item)
            
            # Add other data
            for col_num, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                item.setTextAlignment(Qt.AlignCenter)
                
                # Style status column
                if col_num == 7:  # Status column
                    if cell_data == "Valid":
                        item.setBackground(QColor(240, 255, 240))
                        item.setForeground(QColor(40, 167, 69))
                    else:
                        item.setBackground(QColor(248, 248, 248))
                        item.setForeground(QColor(108, 117, 125))
                
                self.name_list_table.setItem(row_num, col_num + 1, item)  # +1 because first column is checkbox
            
            # Add operations column
            operations = QTableWidgetItem("Add to Whitelist  Add to Blacklist")
            operations.setForeground(QColor(0, 123, 255))
            operations.setTextAlignment(Qt.AlignCenter)
            self.name_list_table.setItem(row_num, 10, operations)