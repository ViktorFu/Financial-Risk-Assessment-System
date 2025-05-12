--创建 name_list 名单系统表
CREATE TABLE name_list (
    id BIGINT PRIMARY KEY,
    rule_id BIGINT NOT NULL,
    log_id BIGINT NOT NULL,
    risk_level INT NOT NULL,
    list_type INT NOT NULL,
    business_line SMALLINT NOT NULL,
    risk_label SMALLINT NOT NULL,
    risk_domain SMALLINT NOT NULL,
    value VARCHAR(256) NOT NULL,
    value_type INT NOT NULL,
    creator VARCHAR(32) NOT NULL,
    create_time DATE NOT NULL
);
--创建 credit_report 征信报告表
CREATE TABLE credit_report (
    id BIGINT PRIMARY KEY,
    rule_id BIGINT NOT NULL,
    log_id BIGINT NOT NULL,
    status SMALLINT NOT NULL,
    data_source VARCHAR(128) NOT NULL,
    name VARCHAR(64) NOT NULL,
    risk_domain SMALLINT NOT NULL,
    value VARCHAR(256) NOT NULL,
    value_type INT NOT NULL,
    identification VARCHAR(64) NOT NULL,
    create_time DATE NOT NULL
);
--创建 rule_management 风控规则表
CREATE TABLE rule_management (
    id BIGINT PRIMARY KEY,
    rule_id BIGINT NOT NULL,
    log_id BIGINT NOT NULL,
    rule_name VARCHAR(64) NOT NULL,
    rule_expression VARCHAR(256) NOT NULL,
    is_external INT NOT NULL,
    priority VARCHAR(64),
    creator VARCHAR(64) NOT NULL,
    create_time DATE NOT NULL
);
--创建 model_management 模型管理表
CREATE TABLE model_management (
    id BIGINT PRIMARY KEY,
    log_id BIGINT NOT NULL,
    model_name VARCHAR(16) NOT NULL,
    model_file BYTEA NOT NULL,
    model_version VARCHAR(16) NOT NULL,
    environment VARCHAR(16) NOT NULL,
    caller VARCHAR(256) NOT NULL,
    approver VARCHAR(64) NOT NULL,
    verified SMALLINT NOT NULL,
    rollback SMALLINT NOT NULL,
    create_time DATE NOT NULL
);
--创建 log_monitoring 日志监控表
CREATE TABLE log_monitoring (
    id BIGINT PRIMARY KEY,
    log_id BIGINT NOT NULL,
    operator VARCHAR(64) NOT NULL,
    operation VARCHAR(128) NOT NULL,
    error_info VARCHAR(256) NOT NULL,
    exception_info VARCHAR(256) NOT NULL,
    is_warning SMALLINT NOT NULL,
    is_done SMALLINT NOT NULL,
    warning_type VARCHAR(64) NOT NULL,
    create_time DATE NOT NULL
);
-- 贷款申请表
CREATE TABLE loan_applications (
    id BIGINT PRIMARY KEY,
    applicant_name VARCHAR(64) NOT NULL,
    applicant_id VARCHAR(18) NOT NULL,  -- 身份证号
    phone VARCHAR(11) NOT NULL,
    address VARCHAR(256),
    loan_amount DECIMAL(12,2) NOT NULL,
    loan_term VARCHAR(16) NOT NULL,
    loan_purpose VARCHAR(32) NOT NULL,
    credit_score INT NOT NULL,
    overdue_count INT NOT NULL,
    max_overdue_days INT NOT NULL,
    debt_ratio DECIMAL(5,2) NOT NULL,
    has_mortgage SMALLINT NOT NULL,
    has_car_loan SMALLINT NOT NULL,
    risk_score INT,
    status VARCHAR(16) NOT NULL, -- 'Pending', 'Approved', 'Rejected'
    decision_time TIMESTAMP,
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    operator VARCHAR(64)
);

-- 贷款风控评估详情表
CREATE TABLE loan_risk_evaluations (
    id BIGINT PRIMARY KEY,
    loan_application_id BIGINT NOT NULL,
    rule_id BIGINT NOT NULL,
    rule_name VARCHAR(128) NOT NULL,
    rule_expression VARCHAR(256) NOT NULL,
    penalty INT NOT NULL,
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (loan_application_id) REFERENCES loan_applications(id)
);
--如果要判断某个用户是否在名单中命中了风控规则（比如在 name_list 表中某条记录满足对应规则）
--查询某用户是否命中规则（命中名单）
SELECT nl.id, nl.value, nl.rule_id, rm.rule_name, rm.rule_expression
FROM name_list nl
JOIN rule_management rm ON nl.rule_id = rm.rule_id
WHERE rm.rule_id = 1;
--WHERE rm.rule_id = 2;
--WHERE rm.rule_id = 3;
--WHERE rm.rule_id = 4;

--因为风控系统在运行过程中会生成大量日志，我们现在要找出日志中未处理的异常
--找出还没处理的（is_done = 0），异常的（is_warning = 1 或有 error/exception 信息），包含报错或异常信息的
SELECT *
FROM log_monitoring
WHERE is_done = 0
  AND (
    is_warning = 1
    OR error_info IS NOT NULL
    OR exception_info IS NOT NULL
  );
--统计各风控规则的命中次数（命中排行榜）
--1.想知道每个规则被命中多少次
SELECT 
    nl.rule_id,
    rm.rule_name,
    COUNT(*) AS hit_count
FROM name_list nl
JOIN rule_management rm ON nl.rule_id = rm.rule_id
GROUP BY nl.rule_id, rm.rule_name
ORDER BY hit_count DESC;
--2.按业务线和规则维度统计命中次数，就是哪个规则最近异常频率高
SELECT 
    nl.business_line,
    nl.rule_id,
    rm.rule_name,
    COUNT(*) AS hit_count
FROM name_list nl
JOIN rule_management rm ON nl.rule_id = rm.rule_id
GROUP BY nl.business_line, nl.rule_id, rm.rule_name
ORDER BY hit_count DESC;
--3.近 7 天内命中次数最多的规则
SELECT 
    nl.rule_id,
    rm.rule_name,
    COUNT(*) AS hit_count
FROM name_list nl
JOIN rule_management rm ON nl.rule_id = rm.rule_id
WHERE nl.create_time >= CURRENT_DATE - INTERVAL '7 days'--我们的示例数据里没有七天内的，可以改成800测试用
GROUP BY nl.rule_id, rm.rule_name
ORDER BY hit_count DESC;
--查看模型运行状态 + 审批记录 + 异常追踪
--因为希望了解风控模型的模型运行日志/谁调用的？在哪个环境？/是否验证通过？是否发生回滚？/是否产生了异常日志？
--1.查看所有模型运行记录
SELECT
    id AS model_id,
    model_name,
    model_version,
    environment,
    caller,
    approver,
    verified,
    rollback,
    create_time
FROM model_management
ORDER BY create_time DESC;
--2.查看回滚过的模型
SELECT *
FROM model_management
WHERE rollback = 1;
--3.查看验证失败或未验证的模型
SELECT *
FROM model_management
WHERE verified = 0;
--4.联合日志表，查看模型运行是否产生异常（通过 log_id）
SELECT
    mm.model_name,
    mm.model_version,
    mm.environment,
    mm.approver,
    lm.error_info,
    lm.exception_info,
    lm.create_time AS log_time
FROM model_management mm
JOIN log_monitoring lm ON mm.log_id = lm.log_id
WHERE lm.is_warning = 1 OR lm.error_info IS NOT NULL OR lm.exception_info IS NOT NULL;
--模拟新增规则 + 自动生成日志
--假如你是风控工程师，要插入一条新规则
INSERT INTO rule_management (
    id, rule_id, log_id, rule_name, rule_expression,
    is_external, priority, creator, create_time
) VALUES (
    6, 6, 111, '规则6', 'value > 100',
    0, 'high', 'admin', '2025-04-08'
);
--假如你想记录一条日志，标记“规则创建成功”或“失败”
INSERT INTO log_monitoring (
    id, log_id, operator, operation, error_info, exception_info,
    create_time, is_warning, is_done, warning_type
) VALUES (
    11, 111, 'admin', 'INSERT',
    'Error: syntax fail', 'Exception: invalid rule expression',
    '2025-04-08', 1, 0, '规则注册失败'
);
--检查规则是否插入
SELECT * FROM rule_management WHERE rule_id = 6;
--检查日志是否入库
SELECT * FROM log_monitoring WHERE log_id = 111;