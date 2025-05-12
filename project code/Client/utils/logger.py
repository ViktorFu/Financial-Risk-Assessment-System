from Client.models.log_model import LogModel

def log_action(username, action, details):
    """Helper function to log user actions."""
    LogModel.add_log(username, action, details)