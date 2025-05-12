from Client.models.database import get_connection, get_db_cursor, execute_query, execute_update
import random
from datetime import date
import logging

# Configure logger
logger = logging.getLogger('risk_control')

class NameListModel:
    @staticmethod
    def get_all_entries():
        """Get all entries from the name list"""
        try:
            query = """
                SELECT nl.id, nl.value, nl.rule_id, nl.risk_level, nl.business_line, nl.create_time, 
                       rm.rule_name, rm.rule_expression
                FROM name_list nl
                JOIN rule_management rm ON nl.rule_id = rm.rule_id
            """
            return execute_query(query)
        except Exception as e:
            logger.error(f"Failed to get all name list entries: {str(e)}")
            return []
    
    @staticmethod
    def check_hit(value, value_type=None):
        """Check if the value hits any rule"""
        try:
            query = """
                SELECT nl.id, nl.value, nl.rule_id, rm.rule_name, rm.rule_expression
                FROM name_list nl
                JOIN rule_management rm ON nl.rule_id = rm.rule_id
                WHERE nl.value = ?
            """
            params = [value]
            
            if value_type is not None:
                query += " AND nl.value_type = ?"
                params.append(value_type)
                
            return execute_query(query, params)
        except Exception as e:
            logger.error(f"Failed to check hit: {str(e)}")
            return []
    
    @staticmethod
    def add_entry(rule_id, log_id, risk_level, list_type, business_line, 
                 risk_label, risk_domain, value, value_type, creator):
        """Add new entry to the name list"""
        try:
            query = """
                INSERT INTO name_list (
                    rule_id, log_id, risk_level, list_type, business_line,
                    risk_label, risk_domain, value, value_type, creator, create_time
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = (
                rule_id, log_id, risk_level, list_type, business_line,
                risk_label, risk_domain, value, value_type, creator, date.today()
            )
            
            success = execute_update(query, params) > 0
            logger.info(f"Add name list entry {value} {'succeeded' if success else 'failed'}")
            return success
        except Exception as e:
            logger.error(f"Failed to add name list entry: {str(e)}")
            return False
    
    @staticmethod
    def delete_entry(entry_id):
        """Delete name list entry"""
        try:
            query = "DELETE FROM name_list WHERE id = ?"
            
            success = execute_update(query, (entry_id,)) > 0
            logger.info(f"Delete name list entry (ID: {entry_id}) {'succeeded' if success else 'failed'}")
            return success
        except Exception as e:
            logger.error(f"Failed to delete name list entry: {str(e)}")
            return False
            
    @staticmethod
    def search_entries(value=None, business_line=None, risk_domain=None, 
                      risk_label=None, status=None, value_type=None):
        """Search name list entries"""
        try:
            query = """
                SELECT nl.id, nl.value, nl.rule_id, nl.risk_level, nl.business_line, nl.create_time, 
                       rm.rule_name, rm.rule_expression
                FROM name_list nl
                JOIN rule_management rm ON nl.rule_id = rm.rule_id
                WHERE 1=1
            """
            params = []
            
            if value:
                query += " AND nl.value LIKE ?"
                params.append(f"%{value}%")
                
            if business_line and business_line != "请选择":
                query += " AND nl.business_line = ?"
                params.append(business_line)
                
            if risk_domain and risk_domain != "请选择":
                query += " AND nl.risk_domain = ?"
                params.append(risk_domain)
                
            if risk_label and risk_label != "请选择":
                query += " AND nl.risk_label = ?"
                params.append(risk_label)
                
            if value_type and value_type != "请选择":
                query += " AND nl.value_type = ?"
                params.append(value_type)
                
            query += " ORDER BY nl.create_time DESC"
            
            return execute_query(query, params)
        except Exception as e:
            logger.error(f"Failed to search name list entries: {str(e)}")
            return []


class RuleModel:
    @staticmethod
    def get_all_rules():
        """Get all rules"""
        try:
            query = """
                SELECT id, rule_id, log_id, rule_name, rule_expression, 
                       is_external, priority, creator, create_time
                FROM rule_management
            """
            return execute_query(query)
        except Exception as e:
            logger.error(f"Failed to get all rules: {str(e)}")
            return []
    
    # 在risk_control_model.py的RuleModel类中添加

    @staticmethod
    def get_active_rules():
        """获取所有活跃规则"""
        try:
            query = """
                SELECT id, rule_id, log_id, rule_name, rule_expression, 
                    is_external, priority, creator, create_time
                FROM rule_management
                ORDER BY priority DESC, create_time DESC
            """
            return execute_query(query)
        except Exception as e:
            logger.error(f"Failed to get active rules: {str(e)}")
            return []

    @staticmethod
    def get_rule_hit_count():
        """Get hit count per rule"""
        try:
            query = """
                SELECT 
                    nl.rule_id,
                    rm.rule_name,
                    COUNT(*) AS hit_count
                FROM name_list nl
                JOIN rule_management rm ON nl.rule_id = rm.rule_id
                GROUP BY nl.rule_id, rm.rule_name
                ORDER BY hit_count DESC
            """
            return execute_query(query)
        except Exception as e:
            logger.error(f"Failed to get rule hit count: {str(e)}")
            return []
    
    @staticmethod
    def get_rule_hit_by_business():
        """Get rule hit count by business line"""
        try:
            query = """
                SELECT 
                    nl.business_line,
                    nl.rule_id,
                    rm.rule_name,
                    COUNT(*) AS hit_count
                FROM name_list nl
                JOIN rule_management rm ON nl.rule_id = rm.rule_id
                GROUP BY nl.business_line, nl.rule_id, rm.rule_name
                ORDER BY hit_count DESC
            """
            return execute_query(query)
        except Exception as e:
            logger.error(f"Failed to get rule hit count by business: {str(e)}")
            return []
    
    @staticmethod
    def add_rule(rule_id, log_id, rule_name, rule_expression, is_external, priority, creator):
        """Add new rule"""
        try:
            query = """
                INSERT INTO rule_management (
                    rule_id, log_id, rule_name, rule_expression,
                    is_external, priority, creator, create_time
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = (
                rule_id, log_id, rule_name, rule_expression,
                is_external, priority, creator, date.today()
            )
            
            success = execute_update(query, params) > 0
            logger.info(f"Add rule {rule_name} {'succeeded' if success else 'failed'}")
            return success
        except Exception as e:
            logger.error(f"Failed to add rule: {str(e)}")
            return False
            
    @staticmethod
    def update_rule(rule_id, rule_name, rule_expression, is_external, priority):
        """Update rule"""
        try:
            query = """
                UPDATE rule_management 
                SET rule_name = ?, rule_expression = ?, is_external = ?, priority = ?
                WHERE rule_id = ?
            """
            params = (rule_name, rule_expression, is_external, priority, rule_id)
            
            success = execute_update(query, params) > 0
            logger.info(f"Update rule (ID: {rule_id}) {'succeeded' if success else 'failed'}")
            return success
        except Exception as e:
            logger.error(f"Failed to update rule: {str(e)}")
            return False
            
    @staticmethod
    def delete_rule(rule_id):
        """Delete rule"""
        try:
            query = "DELETE FROM rule_management WHERE rule_id = ?"
            
            success = execute_update(query, (rule_id,)) > 0
            logger.info(f"Delete rule (ID: {rule_id}) {'succeeded' if success else 'failed'}")
            return success
        except Exception as e:
            logger.error(f"Failed to delete rule: {str(e)}")
            return False
            
    @staticmethod
    def search_rules(rule_id=None, rule_name=None, status=None):
        """Search rules"""
        try:
            query = """
                SELECT id, rule_id, log_id, rule_name, rule_expression, 
                       is_external, priority, creator, create_time
                FROM rule_management
                WHERE 1=1
            """
            params = []
            
            if rule_id:
                query += " AND rule_id = ?"
                params.append(rule_id)
                
            if rule_name:
                query += " AND rule_name LIKE ?"
                params.append(f"%{rule_name}%")
                
            query += " ORDER BY create_time DESC"
            
            return execute_query(query, params)
        except Exception as e:
            logger.error(f"Failed to search rules: {str(e)}")
            return []


class LogMonitoringModel:
    @staticmethod
    def get_all_logs():
        """Get all logs"""
        try:
            query = """
                SELECT id, log_id, operator, operation, error_info, exception_info,
                       is_warning, is_done, warning_type, create_time
                FROM log_monitoring
                ORDER BY create_time DESC
            """
            return execute_query(query)
        except Exception as e:
            logger.error(f"Failed to get all logs: {str(e)}")
            return []
    
    @staticmethod
    def get_pending_warnings():
        """Get pending warning logs"""
        try:
            query = """
                SELECT *
                FROM log_monitoring
                WHERE is_done = 0
                  AND (
                    is_warning = 1
                    OR error_info IS NOT NULL
                    OR exception_info IS NOT NULL
                  )
                ORDER BY create_time DESC
            """
            return execute_query(query)
        except Exception as e:
            logger.error(f"Failed to get pending warnings: {str(e)}")
            return []
    
    @staticmethod
    def add_log(log_id, operator, operation, error_info="", exception_info="", 
               is_warning=0, is_done=0, warning_type=""):
        """Add log entry"""
        try:
            query = """
                INSERT INTO log_monitoring (
                    log_id, operator, operation, error_info, exception_info,
                    is_warning, is_done, warning_type, create_time
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = (
                log_id, operator, operation, error_info, exception_info,
                is_warning, is_done, warning_type, date.today()
            )
            
            success = execute_update(query, params) > 0
            logger.info(f"Add log {operation} {'succeeded' if success else 'failed'}")
            return success
        except Exception as e:
            logger.error(f"Failed to add log: {str(e)}")
            return False
    
    @staticmethod
    def mark_as_done(log_id):
        """Mark log as done"""
        try:
            query = "UPDATE log_monitoring SET is_done = 1 WHERE log_id = ?"
            
            success = execute_update(query, (log_id,)) > 0
            logger.info(f"Mark log as done (ID: {log_id}) {'succeeded' if success else 'failed'}")
            return success
        except Exception as e:
            logger.error(f"Failed to mark log as done: {str(e)}")
            return False
    
    @staticmethod
    def get_log_by_type(log_type):
        """Get logs by type"""
        try:
            query = "SELECT * FROM log_monitoring WHERE 1=1"
            
            if log_type == "运行日志":
                query += " AND operation LIKE '%运行%'"
            elif log_type == "操作日志":
                query += " AND operation NOT LIKE '%运行%'"
                
            return execute_query(query)
        except Exception as e:
            logger.error(f"Failed to get logs by type: {str(e)}")
            return []
            
    @staticmethod
    def delete_log(log_id):
        """Delete log"""
        try:
            query = "DELETE FROM log_monitoring WHERE log_id = ?"
            
            success = execute_update(query, (log_id,)) > 0
            logger.info(f"Delete log (ID: {log_id}) {'succeeded' if success else 'failed'}")
            return success
        except Exception as e:
            logger.error(f"Failed to delete log: {str(e)}")
            return False
            
    @staticmethod
    def search_logs(keyword=None, log_type=None, is_done=None):
        """Search logs"""
        try:
            query = """
                SELECT id, log_id, operator, operation, error_info, exception_info,
                       is_warning, is_done, warning_type, create_time
                FROM log_monitoring
                WHERE 1=1
            """
            params = []
            
            if keyword:
                query += " AND (operation LIKE ? OR operator LIKE ? OR error_info LIKE ?)"
                keyword_param = f"%{keyword}%"
                params.extend([keyword_param, keyword_param, keyword_param])
                
            if log_type == "运行日志":
                query += " AND operation LIKE '%运行%'"
            elif log_type == "操作日志":
                query += " AND operation NOT LIKE '%运行%'"
                
            if is_done is not None:
                query += " AND is_done = ?"
                params.append(is_done)
                
            query += " ORDER BY create_time DESC"
            
            return execute_query(query, params)
        except Exception as e:
            logger.error(f"Failed to search logs: {str(e)}")
            return []
