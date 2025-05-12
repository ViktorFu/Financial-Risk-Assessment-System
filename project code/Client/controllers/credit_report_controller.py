"""
Implementation of the new credit report controller
"""
from Client.models.credit_report_model import CreditReportModel
from Client.models.risk_control_model import LogMonitoringModel
import random

class CreditReportController:
    def __init__(self, current_username=None):
        self.current_username = current_username
    
    def set_current_username(self, username):
        self.current_username = username
    
    def get_all_reports(self):
        """Get all credit reports"""
        return CreditReportModel.get_all_reports()
    
    def get_report_by_id(self, report_id):
        """Get credit report by ID"""
        return CreditReportModel.get_report_by_id(report_id)
    
    def search_reports(self, name=None, phone=None, status=None):
        """Search credit reports"""
        return CreditReportModel.search_reports(name, phone, status)
    
    def add_report(self, rule_id, name, value, value_type, data_source, risk_domain, identification, status=1):
        """Add a new credit report"""
        if not self.current_username:
            return False
            
        # Generate a new log ID
        log_id = random.randint(1000, 9999)
        
        # Create a log entry
        LogMonitoringModel.add_log(
            log_id=log_id,
            operator=self.current_username,
            operation=f"Add credit report - {name}",
            is_warning=0,
            is_done=1,
            warning_type=""
        )
        
        # Add credit report
        return CreditReportModel.add_report(
            rule_id, name, value, value_type, status, data_source, risk_domain, identification
        )
    
    def update_report_status(self, report_id, status):
        """Update credit report status"""
        if not self.current_username:
            return False
            
        # Get report info
        report = CreditReportModel.get_report_by_id(report_id)
        if not report:
            return False
            
        # Generate a new log ID
        log_id = random.randint(1000, 9999)
        
        # Create a log entry
        LogMonitoringModel.add_log(
            log_id=log_id,
            operator=self.current_username,
            operation=f"Update credit report status - ID: {report_id}",
            is_warning=0,
            is_done=1,
            warning_type=""
        )
        
        # Update status
        return CreditReportModel.update_report_status(report_id, status)
    
    def delete_report(self, report_id):
        """Delete credit report"""
        if not self.current_username:
            return False
            
        # Get report info
        report = CreditReportModel.get_report_by_id(report_id)
        if not report:
            return False
            
        # Generate a new log ID
        log_id = random.randint(1000, 9999)
        
        # Create a log entry
        LogMonitoringModel.add_log(
            log_id=log_id,
            operator=self.current_username,
            operation=f"Delete credit report - ID: {report_id}",
            is_warning=0,
            is_done=1,
            warning_type=""
        )
        
        # Delete report
        return CreditReportModel.delete_report(report_id)
