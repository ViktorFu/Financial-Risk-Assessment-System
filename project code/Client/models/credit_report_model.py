"""
Implementation of the credit report model
"""
from Client.models.database import get_connection, get_db_cursor, execute_query, execute_update
from datetime import date
import random
import logging

logger = logging.getLogger('credit_report')

class CreditReportModel:
    @staticmethod
    def get_all_reports():
        """Get all credit reports"""
        try:
            query = """
                SELECT 
                    id, rule_id, name, value, value_type, 
                    status, data_source, risk_domain, identification, create_time
                FROM credit_report
                ORDER BY create_time DESC
            """
            return execute_query(query)
        except Exception as e:
            logger.error(f"Failed to get credit reports: {str(e)}")
            return []
    
    @staticmethod
    def get_report_by_id(report_id):
        """Get credit report by ID"""
        try:
            query = """
                SELECT * FROM credit_report WHERE id = ?
            """
            results = execute_query(query, (report_id,))
            return results[0] if results else None
        except Exception as e:
            logger.error(f"Failed to get credit report by ID: {str(e)}")
            return None
    
    @staticmethod
    def search_reports(name=None, phone=None, status=None):
        """Search credit reports"""
        try:
            query = """
                SELECT 
                    id, rule_id, name, value, value_type, 
                    status, data_source, risk_domain, identification, create_time
                FROM credit_report
                WHERE 1=1
            """
            params = []
            
            if name:
                query += " AND name LIKE ?"
                params.append(f"%{name}%")
            
            if phone:
                query += " AND value LIKE ? AND value_type = 1"  # Assume value_type=1 means phone number
                params.append(f"%{phone}%")
            
            if status is not None:
                query += " AND status = ?"
                params.append(status)
                
            query += " ORDER BY create_time DESC"
            
            return execute_query(query, params)
        except Exception as e:
            logger.error(f"Failed to search credit reports: {str(e)}")
            return []
    
    @staticmethod
    def add_report(rule_id, name, value, value_type, status, data_source, risk_domain, identification):
        """Add a new credit report"""
        try:
            # Generate a random log_id
            log_id = random.randint(1000, 9999)
            
            query = """
                INSERT INTO credit_report (
                    rule_id, log_id, name, value, value_type, 
                    status, data_source, risk_domain, identification, create_time
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = (
                rule_id, log_id, name, value, value_type,
                status, data_source, risk_domain, identification, date.today()
            )
            
            success = execute_update(query, params) > 0
            logger.info(f"Add credit report {'succeeded' if success else 'failed'}")
            return success
        except Exception as e:
            logger.error(f"Failed to add credit report: {str(e)}")
            return False
    
    @staticmethod
    def update_report_status(report_id, status):
        """Update credit report status"""
        try:
            query = """
                UPDATE credit_report SET status = ? WHERE id = ?
            """
            return execute_update(query, (status, report_id)) > 0
        except Exception as e:
            logger.error(f"Failed to update credit report status: {str(e)}")
            return False
    
    @staticmethod
    def delete_report(report_id):
        """Delete credit report"""
        try:
            query = """
                DELETE FROM credit_report WHERE id = ?
            """
            return execute_update(query, (report_id,)) > 0
        except Exception as e:
            logger.error(f"Failed to delete credit report: {str(e)}")
            return False
