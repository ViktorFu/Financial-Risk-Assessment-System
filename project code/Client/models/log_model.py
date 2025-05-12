from Client.models.database import get_connection

class LogModel:
    @staticmethod
    def add_log(username, action, details):
        """Add a new log entry."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO logs (username, action, details) VALUES (?, ?, ?)",
                      (username, action, details))
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_all_logs():
        """Get all logs from the database."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, timestamp, username, action FROM logs ORDER BY timestamp DESC")
        logs = cursor.fetchall()
        conn.close()
        return logs
    
    @staticmethod
    def get_log_details(log_id):
        """Get details for a specific log entry."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT details FROM logs WHERE id = ?", (log_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else ""