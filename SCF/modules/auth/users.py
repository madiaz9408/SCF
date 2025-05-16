import sqlite3
from database import get_db_connection

def create_default_admin():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
            ("admin", "admin123", "administrador")
        )
        conn.commit()
    except sqlite3.Error:
        pass
    finally:
        conn.close()

def get_user_permissions(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT role FROM users WHERE id = ?", (user_id,))
    role = cursor.fetchone()[0]
    conn.close()
    
    # Permisos básicos según rol
    if role == "administrador":
        return {"all": True}
    else:
        return {
            "view_reports": True,
            "edit_own_data": True
        }