from PyQt5.QtWidgets import QMainWindow, QTabWidget
from Client.views.tabs.user_management_tab import UserManagementTab
from Client.views.tabs.log_monitoring_tab import LogMonitoringTab
from Client.views.tabs.risk_control_tab import RiskControlTab
from Client.views.tabs.model_management_tab import ModelManagementTab
from Client.views.tabs.credit_report_tab import CreditReportTab

class AdminWindow(QMainWindow):
    def __init__(self, username, user_controller, log_controller, risk_controller=None, model_controller=None, credit_report_controller=None):
        super().__init__()
        self.username = username
        self.user_controller = user_controller
        self.log_controller = log_controller
        self.risk_controller = risk_controller
        self.model_controller = model_controller
        self.credit_report_controller = credit_report_controller  # New
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f'Admin Control Panel - {self.username}')
        self.setGeometry(100, 100, 900, 700)

        # Create tab widget
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)

        # Create tab contents
        self.user_management_tab = UserManagementTab(self.user_controller)
        self.logs_tab = LogMonitoringTab(self.log_controller)
        
        # Add risk control and model management tabs (if controllers are provided)
        if self.risk_controller:
            self.risk_control_tab = RiskControlTab(self.risk_controller)
            self.credit_report_tab = CreditReportTab(self.risk_controller)  # Using risk_controller
        
        if self.model_controller:
            self.model_management_tab = ModelManagementTab(self.model_controller)

        # Add tabs to tab container
        self.tabs.addTab(self.user_management_tab, "User Management")
        
        if self.model_controller:
            self.tabs.addTab(self.model_management_tab, "Model Management")
        
        if self.risk_controller:
            self.tabs.addTab(self.credit_report_tab, "Credit Report Management")
            self.tabs.addTab(self.risk_control_tab, "Risk Control List Management")

        self.tabs.addTab(self.logs_tab, "System Logs")

        self.setCentralWidget(self.tabs)
