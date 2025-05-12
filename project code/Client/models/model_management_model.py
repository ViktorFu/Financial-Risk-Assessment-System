from Client.models.database import get_connection, get_db_cursor, execute_query, execute_update
from datetime import date
import logging

# Configure logger
logger = logging.getLogger('model_management')

class ModelManagementModel:
    @staticmethod
    def get_all_models():
        """Get all models"""
        try:
            query = """
                SELECT
                    id, model_name, model_version, environment,
                    caller, approver, verified, rollback, create_time
                FROM model_management
                ORDER BY create_time DESC
            """
            return execute_query(query)
        except Exception as e:
            logger.error(f"Failed to get all models: {str(e)}")
            return []
    
    @staticmethod
    def get_rollback_models():
        """Get models that have been rolled back"""
        try:
            query = """
                SELECT *
                FROM model_management
                WHERE rollback = 1
                ORDER BY create_time DESC
            """
            return execute_query(query)
        except Exception as e:
            logger.error(f"Failed to get rollback models: {str(e)}")
            return []
    
    @staticmethod
    def get_unverified_models():
        """Get unverified models"""
        try:
            query = """
                SELECT *
                FROM model_management
                WHERE verified = 0
                ORDER BY create_time DESC
            """
            return execute_query(query)
        except Exception as e:
            logger.error(f"Failed to get unverified models: {str(e)}")
            return []
    
    @staticmethod
    def get_model_errors():
        """Get model error records"""
        try:
            query = """
                SELECT
                    mm.id, mm.model_name, mm.model_version, mm.environment,
                    mm.approver, lm.error_info, lm.exception_info,
                    lm.create_time AS log_time
                FROM model_management mm
                JOIN log_monitoring lm ON mm.log_id = lm.log_id
                WHERE lm.is_warning = 1 
                   OR lm.error_info IS NOT NULL 
                   OR lm.exception_info IS NOT NULL
                ORDER BY log_time DESC
            """
            return execute_query(query)
        except Exception as e:
            logger.error(f"Failed to get model error records: {str(e)}")
            return []
    
    @staticmethod
    def add_model(log_id, model_name, model_file, model_version, environment,
                 caller, approver, verified=0, rollback=0):
        """Add new model"""
        try:
            query = """
                INSERT INTO model_management (
                    log_id, model_name, model_file, model_version, environment,
                    caller, approver, verified, rollback, create_time
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = (
                log_id, model_name, model_file, model_version, environment,
                caller, approver, verified, rollback, date.today()
            )
            
            success = execute_update(query, params) > 0
            logger.info(f"Add model {model_name} {'succeeded' if success else 'failed'}")
            return success
        except Exception as e:
            logger.error(f"Failed to add model: {str(e)}")
            return False
    
    @staticmethod
    def toggle_rollback(model_id, rollback_state):
        """Toggle model rollback state"""
        try:
            query = "UPDATE model_management SET rollback = ? WHERE id = ?"
            params = (1 if rollback_state else 0, model_id)
            
            success = execute_update(query, params) > 0
            action = "Set" if rollback_state else "Unset"
            logger.info(f"{action} model rollback (ID: {model_id}) {'succeeded' if success else 'failed'}")
            return success
        except Exception as e:
            logger.error(f"Failed to toggle model rollback state: {str(e)}")
            return False
    
    @staticmethod
    def toggle_verified(model_id, verified_state):
        """Toggle model verification state"""
        try:
            query = "UPDATE model_management SET verified = ? WHERE id = ?"
            params = (1 if verified_state else 0, model_id)
            
            success = execute_update(query, params) > 0
            action = "Verify" if verified_state else "Unverify"
            logger.info(f"{action} model (ID: {model_id}) {'succeeded' if success else 'failed'}")
            return success
        except Exception as e:
            logger.error(f"Failed to toggle model verification state: {str(e)}")
            return False
            
    @staticmethod
    def delete_model(model_id):
        """Delete model"""
        try:
            query = "DELETE FROM model_management WHERE id = ?"
            
            success = execute_update(query, (model_id,)) > 0
            logger.info(f"Delete model (ID: {model_id}) {'succeeded' if success else 'failed'}")
            return success
        except Exception as e:
            logger.error(f"Failed to delete model: {str(e)}")
            return False
            
    @staticmethod
    def search_models(model_name=None, environment=None, verified=None):
        """Search models"""
        try:
            query = """
                SELECT
                    id, model_name, model_version, environment,
                    caller, approver, verified, rollback, create_time
                FROM model_management
                WHERE 1=1
            """
            params = []
            
            if model_name:
                query += " AND model_name LIKE ?"
                params.append(f"%{model_name}%")
                
            if environment and environment != "All":
                query += " AND environment = ?"
                params.append(environment)
                
            if verified is not None:
                query += " AND verified = ?"
                params.append(verified)
                
            query += " ORDER BY create_time DESC"
            
            return execute_query(query, params)
        except Exception as e:
            logger.error(f"Failed to search models: {str(e)}")
            return []
