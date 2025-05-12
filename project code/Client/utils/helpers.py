# Add these mappings to the existing helpers.py file

def format_phone(phone):
    """Format a phone number consistently."""
    # Just an example helper function
    if phone and len(phone) == 11:
        return f"{phone[:3]}-{phone[3:7]}-{phone[7:]}"
    return phone

# Risk control mappings for display
def get_risk_level_text(risk_level):
    """Get readable text for risk level."""
    risk_levels = {
        1: 'Low Risk',
        2: 'Medium-Low Risk',
        3: 'Medium Risk',
        4: 'Medium-High Risk',
        5: 'High Risk'
    }
    return risk_levels.get(risk_level, f'Unknown Risk ({risk_level})')

def get_business_line_text(business_line):
    """Get readable text for business line."""
    business_lines = {
        1: 'Loan',
        2: 'Credit Card',
        3: 'Payment',
        4: 'Investment'
    }
    return business_lines.get(business_line, f'Business Line {business_line}')

def get_list_type_text(list_type):
    """Get readable text for list type."""
    list_types = {
        1: 'Blacklist',
        2: 'Whitelist',
        3: 'Graylist'
    }
    return list_types.get(list_type, f'List Type {list_type}')

def get_risk_label_text(risk_label):
    """Get readable text for risk label."""
    risk_labels = {
        1: 'Fraud',
        2: 'Credit',
        3: 'Compliance',
        4: 'Operations'
    }
    return risk_labels.get(risk_label, f'Risk Label {risk_label}')
