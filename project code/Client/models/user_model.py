from Client.models.database import get_connection

class UserModel:
    @staticmethod
    def authenticate(username, password):
        """Authenticate a user and return their admin status."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT is_admin FROM users WHERE username = ? AND password = ?",
                      (username, password))
        result = cursor.fetchone()
        conn.close()
        
        if result is None:
            return None
        return bool(result[0])
    
    @staticmethod
    def get_user_info(username):
        """Get user information by username."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT full_name, email, phone FROM users WHERE username = ?",
                      (username,))
        result = cursor.fetchone()
        conn.close()
        return result
    
    @staticmethod
    def get_all_users():
        """Get all users from the database."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, is_admin, full_name, email, phone FROM users")
        users = cursor.fetchall()
        conn.close()
        return users
    
    @staticmethod
    def add_user(username, password, is_admin, full_name, email, phone):
        """Add a new user to the database."""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, password, is_admin, full_name, email, phone) VALUES (?, ?, ?, ?, ?, ?)",
                (username, password, is_admin, full_name, email, phone)
            )
            conn.commit()
            success = True
        except sqlite3.IntegrityError:
            success = False
        conn.close()
        return success
    
    @staticmethod
    def update_user(user_id, username, password, is_admin, full_name, email, phone):
        """Update user information."""
        conn = get_connection()
        cursor = conn.cursor()
        
        # Get original username for logging
        cursor.execute("SELECT username FROM users WHERE id = ?", (user_id,))
        old_username = cursor.fetchone()[0]
        
        try:
            if password:
                cursor.execute(
                    "UPDATE users SET username = ?, password = ?, is_admin = ?, full_name = ?, email = ?, phone = ? WHERE id = ?",
                    (username, password, is_admin, full_name, email, phone, user_id)
                )
            else:
                cursor.execute(
                    "UPDATE users SET username = ?, is_admin = ?, full_name = ?, email = ?, phone = ? WHERE id = ?",
                    (username, is_admin, full_name, email, phone, user_id)
                )
            conn.commit()
            success = True
        except sqlite3.IntegrityError:
            success = False
        conn.close()
        return success, old_username
    
    @staticmethod
    def delete_user(user_id):
        """Delete a user from the database."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users WHERE id = ?", (user_id,))
        username = cursor.fetchone()[0]
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()
        return username