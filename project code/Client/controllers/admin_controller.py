from Client.models.user_model import UserModel
from Client.models.log_model import LogModel

class AdminController:
    def __init__(self):
        pass
    
    def login(self, username, password, is_admin_login):
        """Handle login attempt and return success status."""
        user_type = UserModel.authenticate(username, password)
        
        if user_type is None:
            return False
        
        # Check permission
        if is_admin_login and not user_type:
            return False
        
        # Log login
        user_role = "Administrator" if is_admin_login else "Regular User"
        LogModel.add_log(username, 'Login', f'{user_role} logged into the system')
        
        return True
    
    def get_log_details(self, log_id):
        """Get details for a specific log."""
        return LogModel.get_log_details(log_id)
    
    def get_all_logs(self):
        """Get all logs."""
        return LogModel.get_all_logs()
