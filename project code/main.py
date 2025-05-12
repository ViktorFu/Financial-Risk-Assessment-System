import sys
import random
from PyQt5.QtWidgets import QApplication, QMessageBox
from Client.models.database import init_database
from Client.controllers.admin_controller import AdminController
from Client.controllers.user_controller import UserController
from Client.controllers.risk_control_controller import RiskControlController
from Client.controllers.model_management_controller import ModelManagementController
from Client.controllers.credit_report_controller import CreditReportController
from Client.views.login_window import LoginWindow
from Client.views.user_info_window import UserInfoWindow
from Client.views.admin_window import AdminWindow

class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        # 初始化数据库
        try:
            init_database(csv_data_path='./CSV')
        except Exception as e:
            QMessageBox.critical(None, '数据库错误', f'数据库初始化失败: {str(e)}')
            sys.exit(1)
        
        # 初始化控制器
        self.admin_controller = AdminController()
        self.user_controller = UserController()
        self.risk_controller = RiskControlController()
        self.model_controller = ModelManagementController()
        self.credit_report_controller = CreditReportController()
        
        # 创建登录窗口
        self.login_window = LoginWindow(self.admin_controller)
        self.login_window.login_success.connect(self.on_login_success)
        self.login_window.show()

    def on_login_success(self, username, is_admin):
        # 更新控制器中的当前用户名
        self.user_controller.set_current_username(username)
        self.risk_controller.set_current_username(username)
        self.model_controller.set_current_username(username)
        self.credit_report_controller.set_current_username(username)
        
        if is_admin:
            self.admin_window = AdminWindow(
                username, 
                self.user_controller, 
                self.admin_controller,
                self.risk_controller,
                self.model_controller,
                self.credit_report_controller
            )
            self.admin_window.show()
        else:
            self.user_window = UserInfoWindow(username, self.user_controller)
            self.user_window.show()

if __name__ == '__main__':
    try:
        app = App(sys.argv)
        sys.exit(app.exec_())
    except Exception as e:
        QMessageBox.critical(None, '应用错误', f'应用发生错误: {str(e)}')
        sys.exit(1)