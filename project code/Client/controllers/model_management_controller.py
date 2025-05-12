from Client.models.model_management_model import ModelManagementModel
from Client.models.risk_control_model import LogMonitoringModel
import random

class ModelManagementController:
    def __init__(self, current_username=None):
        self.current_username = current_username
    
    def set_current_username(self, username):
        self.current_username = username
    
    def get_all_models(self):
        """Get all models."""
        return ModelManagementModel.get_all_models()
    
    def get_rollback_models(self):
        """Get models that have been rolled back."""
        return ModelManagementModel.get_rollback_models()
    
    def get_unverified_models(self):
        """Get unverified models."""
        return ModelManagementModel.get_unverified_models()
    
    def get_model_errors(self):
        """Get models with errors."""
        return ModelManagementModel.get_model_errors()
    
    def add_model(self, model_name, model_file, model_version, environment, approver):
        """Add a new model."""
        if not self.current_username:
            return False
            
        # Generate a new log ID
        log_id = random.randint(1000, 9999)
        
        # Create a log entry
        LogMonitoringModel.add_log(
            log_id=log_id,
            operator=self.current_username,
            operation=f"Add model {model_name} {model_version}",
            is_warning=0,
            is_done=1,
            warning_type=""
        )
        
        # Add the model
        return ModelManagementModel.add_model(
            log_id, model_name, model_file, model_version, environment,
            self.current_username, approver
        )
    
    def toggle_rollback(self, model_id, rollback_state):
        """Toggle the rollback state of a model."""
        if not self.current_username:
            return False
            
        # Generate a new log ID
        log_id = random.randint(1000, 9999)
        
        # Create a log entry
        action = "Rollback" if rollback_state else "Cancel rollback"
        LogMonitoringModel.add_log(
            log_id=log_id,
            operator=self.current_username,
            operation=f"{action} model ID: {model_id}",
            is_warning=0,
            is_done=1,
            warning_type=""
        )
        
        # Toggle rollback state
        return ModelManagementModel.toggle_rollback(model_id, rollback_state)
    
    def toggle_verified(self, model_id, verified_state):
        """Toggle the verified state of a model."""
        if not self.current_username:
            return False
            
        # Generate a new log ID
        log_id = random.randint(1000, 9999)
        
        # Create a log entry
        action = "Verified" if verified_state else "Unverified"
        LogMonitoringModel.add_log(
            log_id=log_id,
            operator=self.current_username,
            operation=f"{action} model ID: {model_id}",
            is_warning=0,
            is_done=1,
            warning_type=""
        )
        
        # Toggle verified state
        return ModelManagementModel.toggle_verified(model_id, verified_state)
