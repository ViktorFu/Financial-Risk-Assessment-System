from Client.models.user_model import UserModel
from Client.models.log_model import LogModel

class UserController:
    def __init__(self, current_username=None):
        self.current_username = current_username

    def set_current_username(self, username):
        self.current_username = username
    
    def get_user_info(self, username):
        return UserModel.get_user_info(username)
    
    def get_all_users(self):
        return UserModel.get_all_users()
    
    def add_user(self, username, password, is_admin, full_name, email, phone):
        success = UserModel.add_user(username, password, is_admin, full_name, email, phone)
        if success and self.current_username:
            LogModel.add_log(self.current_username, '创建用户', f'创建了用户: {username}')
        return success
    
    def update_user(self, user_id, username, password, is_admin, full_name, email, phone):
        success, old_username = UserModel.update_user(user_id, username, password, is_admin, full_name, email, phone)
        if success and self.current_username:
            LogModel.add_log(self.current_username, '更新用户', f'更新了用户信息: {old_username} -> {username}')
        return success
    
    def delete_user(self, user_id):
        username = UserModel.delete_user(user_id)
        if self.current_username:
            LogModel.add_log(self.current_username, '删除用户', f'删除了用户: {username}')
        return True