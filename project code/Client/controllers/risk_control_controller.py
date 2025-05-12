from Client.models.risk_control_model import NameListModel, RuleModel, LogMonitoringModel
import random

class RiskControlController:
    def __init__(self, current_username=None):
        self.current_username = current_username
    
    def set_current_username(self, username):
        self.current_username = username
    
    def get_name_list_entries(self):
        """Get all entries from the name list."""
        return NameListModel.get_all_entries()
    
    def check_hit(self, value, value_type=None):
        """Check if a value hits any rule in the name list."""
        return NameListModel.check_hit(value, value_type)
    
    def add_name_list_entry(self, rule_id, risk_level, list_type, business_line, 
                           risk_label, risk_domain, value, value_type):
        """Add a new entry to the name list."""
        if not self.current_username:
            return False
            
        # Generate a new log ID
        log_id = random.randint(1000, 9999)
        
        # Create a log entry
        LogMonitoringModel.add_log(
            log_id=log_id,
            operator=self.current_username,
            operation="Add name list record",
            is_warning=0,
            is_done=1,
            warning_type=""
        )
        
        # Add the entry
        return NameListModel.add_entry(
            rule_id, log_id, risk_level, list_type, business_line,
            risk_label, risk_domain, value, value_type, self.current_username
        )
    
    def delete_name_list_entry(self, entry_id):
        """Delete an entry from the name list."""
        if not self.current_username:
            return False
            
        # Generate a new log ID
        log_id = random.randint(1000, 9999)
        
        # Create a log entry
        LogMonitoringModel.add_log(
            log_id=log_id,
            operator=self.current_username,
            operation="Delete name list record",
            is_warning=0,
            is_done=1,
            warning_type=""
        )
        
        # Delete the entry
        return NameListModel.delete_entry(entry_id)
    
    def get_all_rules(self):
        """Get all rules from rule management."""
        return RuleModel.get_all_rules()
    
    def get_rule_hit_count(self):
        """Get hit counts for each rule."""
        return RuleModel.get_rule_hit_count()
    
    def get_rule_hit_by_business(self):
        """Get hit counts by business line."""
        return RuleModel.get_rule_hit_by_business()
    
    def add_rule(self, rule_name, rule_expression, is_external=0, priority="medium"):
        """Add a new rule."""
        if not self.current_username:
            return False
            
        # Generate new IDs
        rule_id = random.randint(100, 999)
        log_id = random.randint(1000, 9999)
        
        # Create a log entry
        LogMonitoringModel.add_log(
            log_id=log_id,
            operator=self.current_username,
            operation="Create rule",
            is_warning=0,
            is_done=1,
            warning_type=""
        )
        
        # Add the rule
        return RuleModel.add_rule(
            rule_id, log_id, rule_name, rule_expression, 
            is_external, priority, self.current_username
        )
    
    def get_all_logs(self):
        """Get all logs."""
        return LogMonitoringModel.get_all_logs()
    
    def get_pending_warnings(self):
        """Get all pending warnings."""
        return LogMonitoringModel.get_pending_warnings()
    
    def mark_log_as_done(self, log_id):
        """Mark a log as done."""
        if not self.current_username:
            return False
            
        # Add a new log for this action
        new_log_id = random.randint(1000, 9999)
        LogMonitoringModel.add_log(
            log_id=new_log_id,
            operator=self.current_username,
            operation=f"Mark log {log_id} as done",
            is_warning=0,
            is_done=1,
            warning_type=""
        )
        
        # Mark the original log as done
        return LogMonitoringModel.mark_as_done(log_id)
    
    def get_log_by_type(self, log_type):
        """Get logs by type"""
        return LogMonitoringModel.get_log_by_type(log_type)
    
    # 在risk_control_controller.py中添加规则评估功能

   
    def _evaluate_rule(self, rule, applicant_data):
        """评估单个规则"""
        rule_id = rule[1]
        rule_expression = rule[4]
        
        # 这里简化了规则评估逻辑
        # 实际中可能需要规则引擎来解析和执行规则表达式
        triggered = False
        penalty = 0
        
        # 示例规则评估逻辑
        if "credit_score" in rule_expression and "credit_score" in applicant_data:
            if "< 500" in rule_expression and applicant_data["credit_score"] < 500:
                triggered = True
                penalty = 40
                
        if "overdue_count" in rule_expression and "overdue_count" in applicant_data:
            if "> 3" in rule_expression and applicant_data["overdue_count"] > 3:
                triggered = True
                penalty = 30
        
        return {"triggered": triggered, "penalty": penalty}
    

    # 在risk_control_controller.py中添加


    def _check_rule_triggered(self, rule_expression, applicant_data):
        """检查规则是否被触发"""
        try:
            # 确保数据类型正确
            credit_score = int(applicant_data["credit_score"])
            overdue_count = int(applicant_data["overdue_count"])
            max_overdue_days = int(applicant_data["max_overdue_days"])
            debt_ratio = float(applicant_data["debt_ratio"])
            loan_amount = float(applicant_data["loan_amount"].replace('¥', '').replace(',', '').strip()) if isinstance(applicant_data["loan_amount"], str) else float(applicant_data["loan_amount"])
            has_mortgage = bool(applicant_data["has_mortgage"])
            has_car_loan = bool(applicant_data["has_car_loan"])
            
            # 打印调试信息
            print(f"检查规则: {rule_expression}")
            print(f"申请人数据: 信用分={credit_score}, 逾期次数={overdue_count}, " 
                f"最长逾期天数={max_overdue_days}, 负债比={debt_ratio}, " 
                f"贷款金额={loan_amount}, 有房贷={has_mortgage}, 有车贷={has_car_loan}")
            
            # 信用分相关规则
            if "credit_score" in rule_expression.lower():
                if "< 550" in rule_expression and credit_score < 550:
                    print("触发高风险信用分规则")
                    return True, 50
                elif "< 600" in rule_expression and credit_score < 600:
                    print("触发中风险信用分规则")
                    return True, 30
                elif "< 650" in rule_expression and credit_score < 650:
                    print("触发低风险信用分规则")
                    return True, 20
            
            # 逾期相关规则
            if "overdue_count" in rule_expression.lower():
                if "> 5" in rule_expression and overdue_count > 5:
                    print("触发高风险逾期次数规则")
                    return True, 40
                elif "> 3" in rule_expression and overdue_count > 3:
                    print("触发中风险逾期次数规则")
                    return True, 25
                elif "> 0" in rule_expression and overdue_count > 0:
                    print("触发低风险逾期次数规则")
                    return True, 10
            
            # 最长逾期天数规则
            if "max_overdue_days" in rule_expression.lower():
                if "> 90" in rule_expression and max_overdue_days > 90:
                    print("触发高风险逾期天数规则")
                    return True, 45
                elif "> 60" in rule_expression and max_overdue_days > 60:
                    print("触发中风险逾期天数规则")
                    return True, 35
                elif "> 30" in rule_expression and max_overdue_days > 30:
                    print("触发低风险逾期天数规则")
                    return True, 20
            
            # 负债比规则
            if "debt_ratio" in rule_expression.lower():
                if "> 0.6" in rule_expression and debt_ratio > 0.6:
                    print("触发高风险负债比规则")
                    return True, 35
                elif "> 0.5" in rule_expression and debt_ratio > 0.5:
                    print("触发中风险负债比规则")
                    return True, 25
                elif "> 0.4" in rule_expression and debt_ratio > 0.4:
                    print("触发低风险负债比规则")
                    return True, 15
            
            # 多头借贷规则
            if "has_mortgage" in rule_expression.lower() and "has_car_loan" in rule_expression.lower():
                if has_mortgage and has_car_loan:
                    print("触发多头借贷规则")
                    return True, 15
            
            # 贷款金额规则
            if "loan_amount" in rule_expression.lower():
                if "> 500000" in rule_expression and loan_amount > 500000:
                    print("触发贷款金额规则")
                    return True, 10
        
        except Exception as e:
            print(f"规则评估错误: {str(e)}")
            import traceback
            traceback.print_exc()
        
        return False, 0
        
    # 删除所有其他的evaluate_loan_application方法，只保留这一个
    def evaluate_loan_application(self, applicant_data):
        """
        评估贷款申请
        
        Args:
            applicant_data (dict): 包含申请人信息和风控指标的字典
            
        Returns:
            dict: 包含评估结果的字典
        """
        print("\n========= 开始贷款评估 =========")
        print(f"申请人: {applicant_data['name']}")
        print(f"申请数据: {applicant_data}")
        
        if not self.current_username:
            return {"approved": False, "score": 0, "reason": "未授权的评估"}
        
        # 1. 获取所有活跃规则
        active_rules = self.get_active_rules()
        print(f"已加载 {len(active_rules)} 条规则")
        
        # 2. 初始化评分
        base_score = 100
        score = base_score
        rule_results = []
        
        # 3. 评估每条规则
        for rule in active_rules:
            rule_id = str(rule[1])
            rule_name = rule[3]
            rule_expression = rule[4]
            
            print(f"\n评估规则: {rule_name} ({rule_expression})")
            
            # 判断规则是否被触发
            is_triggered, penalty = self._check_rule_triggered(rule_expression, applicant_data)
            
            if is_triggered:
                print(f"规则触发! 扣除 {penalty} 分")
                score -= penalty
                rule_results.append({
                    "rule_id": rule_id,
                    "rule_name": rule_name,
                    "rule_expression": rule_expression,
                    "penalty": penalty
                })
        
        # 4. 确定最终评估结果
        approved = score >= 60
        print(f"\n最终评分: {score}/100")
        print(f"决定: {'通过' if approved else '拒绝'}")
        print("========= 评估结束 =========\n")
        
        # 5. 记录评估结果
        log_id = random.randint(1000, 9999)
        LogMonitoringModel.add_log(
            log_id=log_id,
            operator=self.current_username,
            operation=f"贷款评估 - 申请人: {applicant_data['name']}",
            error_info="" if approved else "拒绝贷款",
            exception_info="",
            is_warning=0 if approved else 1,
            is_done=1,
            warning_type="" if approved else "风控评分过低"
        )
        
        # 6. 如果拒绝，添加到名单
        if not approved:
            for rule_result in rule_results:
                try:
                    # 选择一个合适的rule_id用于记录
                    trigger_rule_id = int(rule_result["rule_id"])
                    
                    # 添加到名单
                    self.add_name_list_entry(
                        rule_id=trigger_rule_id,
                        risk_level=5,  # 高风险
                        list_type=1,   # 名单类型(1=黑名单)
                        business_line=1 if applicant_data['loan_purpose'] == 'Consumer Loan' else 2,
                        risk_label=1,  # 风险标签
                        risk_domain=1,  # 风险领域
                        value=str(applicant_data['id']),  # 身份证号
                        value_type=1   # 身份证类型
                    )
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    print(f"添加名单失败: {str(e)}")
        
        # 7. 返回评估结果
        return {
            "approved": approved,
            "score": score,
            "rule_results": rule_results,
        }

    # 添加缺失的get_active_rules方法
    def get_active_rules(self):
        """获取所有活跃的风控规则"""
        try:
            # 在这里，我们从数据库获取所有规则
            # 实际环境中你可能需要添加条件过滤已禁用的规则
            rules = RuleModel.get_all_rules()
            


            # 创建信用分规则
            self.add_rule("信用分低于550", "credit_score < 550", 0, "high")
            self.add_rule("信用分低于600", "credit_score < 600", 0, "medium")
            self.add_rule("信用分低于650", "credit_score < 650", 0, "low")
                
            # 创建逾期次数规则
            self.add_rule("逾期次数超过5次", "overdue_count > 5", 0, "high")
            self.add_rule("逾期次数超过3次", "overdue_count > 3", 0, "medium")
            self.add_rule("有逾期记录", "overdue_count > 0", 0, "low")
            
             # 创建逾期天数规则
            self.add_rule("最长逾期天数超过90天", "max_overdue_days > 90", 0, "high")
            self.add_rule("最长逾期天数超过60天", "max_overdue_days > 60", 0, "medium")
            self.add_rule("最长逾期天数超过30天", "max_overdue_days > 30", 0, "low")
                
            # 创建负债比规则
            self.add_rule("负债收入比超过0.6", "debt_ratio > 0.6", 0, "high")
            self.add_rule("负债收入比超过0.5", "debt_ratio > 0.5", 0, "medium")
            self.add_rule("负债收入比超过0.4", "debt_ratio > 0.4", 0, "low")
                
            # 创建多头借贷规则
            self.add_rule("同时有房贷和车贷", "has_mortgage and has_car_loan", 0, "medium")
                
            # 创建贷款金额规则
            self.add_rule("贷款金额超过50万", "loan_amount > 500000", 0, "low")
                
            # 重新获取规则
            rules = RuleModel.get_all_rules()
            
            return rules
        except Exception as e:
            print(f"获取活跃规则失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return []

    def _record_loan_application(self, applicant_data):
        """记录贷款申请"""
        # 实际实现中连接到数据库记录申请信息
        # 这里简化为返回一个随机ID
        return random.randint(100000, 999999)

    def _record_rule_match(self, loan_app_id, rule_id, rule_name, rule_expression, penalty):
        """记录规则匹配结果"""
        # 实际实现中将匹配结果写入数据库
        pass

    def _update_loan_application(self, loan_app_id, score, approved):
        """更新贷款申请状态"""
        # 实际实现中更新数据库中的申请状态
        pass

    def _add_to_risk_control_list(self, applicant_data, rule_results):
        """将拒绝的申请添加到风控名单"""
        for rule_result in rule_results:
            if rule_result["penalty"] >= 30:  # 只记录高扣分的规则
                try:
                    # 添加到风控名单
                    self.add_name_list_entry(
                        rule_id=int(rule_result["rule_id"]),
                        risk_level=5,  # 高风险
                        list_type=1,   # 黑名单
                        business_line=1 if applicant_data['loan_purpose'] == 'Consumer Loan' else 2,
                        risk_label=1,  # 风险标签
                        risk_domain=1,  # 风险领域
                        value=applicant_data['id'],  # 身份证号
                        value_type=1   # 身份证类型
                    )
                except Exception as e:
                    print(f"添加风控名单失败: {str(e)}")