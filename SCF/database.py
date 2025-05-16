import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent.parent / 'scf_database.db'

def create_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Tabla de usuarios
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL,
        unit TEXT,
        specialty TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Tabla para presupuesto aprobado (SCF-72)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS approved_budget (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        military_unit TEXT NOT NULL,
        specialty TEXT NOT NULL,
        date TEXT NOT NULL,
        details TEXT NOT NULL,
        approved_budget REAL NOT NULL,
        item_110101 REAL NOT NULL,
        item_110406 REAL NOT NULL,
        item_800000 REAL NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        created_by TEXT NOT NULL,
        FOREIGN KEY (created_by) REFERENCES users(username)
    )
    ''')
    
    # Tabla para presupuesto ejecutado (SCF-73)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS budget_execution (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        military_unit TEXT NOT NULL,
        specialty TEXT NOT NULL,
        directive_item TEXT NOT NULL,
        date TEXT NOT NULL,
        details TEXT NOT NULL,
        approved_budget REAL NOT NULL,
        executed_800440 REAL NOT NULL,
        executed_890441 REAL NOT NULL,
        balance REAL NOT NULL,
        execution_percentage REAL NOT NULL,
        expense_concept TEXT NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        created_by TEXT NOT NULL,
        FOREIGN KEY (created_by) REFERENCES users(username)
    )
    ''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Para acceder a las columnas por nombre
    return conn

# Crear tablas al importar el módulo
create_tables()