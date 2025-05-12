"""
Improve database.py by adding connection pooling and exception handling
"""
import sqlite3
import os
import csv  # Add missing csv import
import psycopg2  # Requires installation: pip install psycopg2-binary
from contextlib import contextmanager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='database.log')
logger = logging.getLogger('database')

# Configure database type: 'sqlite' or 'postgres'
DB_TYPE = 'sqlite'

# PostgreSQL connection parameters
PG_HOST = 'localhost'
PG_PORT = '5432'
PG_DB = 'risk_control'
PG_USER = 'postgres'
PG_PASSWORD = 'postgres'

# Global connection pool (simple implementation)
CONNECTION_POOL = []
MAX_POOL_SIZE = 5

def get_connection():
    """Create and return a database connection"""
    # Check connection pool
    if CONNECTION_POOL:
        return CONNECTION_POOL.pop()
    
    try:
        if DB_TYPE == 'sqlite':
            # SQLite connection
            db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'user_management.db')
            conn = sqlite3.connect(db_path)
            # Enable foreign key constraints
            conn.execute("PRAGMA foreign_keys = ON")
            return conn
        else:
            # PostgreSQL connection
            return psycopg2.connect(
                host=PG_HOST,
                port=PG_PORT,
                database=PG_DB,
                user=PG_USER,
                password=PG_PASSWORD
            )
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        raise

def release_connection(conn):
    """Return the connection to the connection pool"""
    if len(CONNECTION_POOL) < MAX_POOL_SIZE:
        CONNECTION_POOL.append(conn)
    else:
        conn.close()

@contextmanager
def get_db_cursor():
    """Context manager to get a database cursor and automatically handle connection closing"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.error(f"Database operation error: {str(e)}")
        raise
    finally:
        cursor.close()
        release_connection(conn)

def execute_query(query, params=None):
    """Execute a database query and return the result"""
    with get_db_cursor() as cursor:
        cursor.execute(query, params or ())
        return cursor.fetchall()

def execute_update(query, params=None):
    """Execute a database update operation"""
    with get_db_cursor() as cursor:
        cursor.execute(query, params or ())
        return cursor.rowcount
        
def load_csv_to_table(cursor, table_name, csv_path):
    """Load data from a CSV file into the specified table"""
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)
            
            # Generate placeholders
            placeholders = ','.join(['?'] * len(headers)) if DB_TYPE == 'sqlite' else \
                          ','.join(['%s'] * len(headers))
            
            # Build insert statement
            query = f"INSERT INTO {table_name} ({','.join(headers)}) VALUES ({placeholders})"
            
            # Bulk insert data
            batch = []
            for row in reader:
                # Handle empty values
                processed_row = [None if cell.strip() == '' else cell for cell in row]
                batch.append(processed_row)
                
                # Commit every 100 records
                if len(batch) >= 100:
                    cursor.executemany(query, batch)
                    batch = []
            
            # Commit remaining data
            if batch:
                cursor.executemany(query, batch)
            
            logger.info(f"Successfully imported {table_name} from {csv_path}")
    except Exception as e:
        logger.error(f"CSV import failed: {str(e)}")
        raise


def init_database(csv_data_path=None):  # Fix: add required parameter
    """Initialize the database and create tables (if not exist)"""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        if DB_TYPE == 'sqlite':
            # SQLite table definitions
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                is_admin INTEGER NOT NULL,
                full_name TEXT,
                email TEXT,
                phone TEXT
            )
            ''')

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                username TEXT NOT NULL,
                action TEXT NOT NULL,
                details TEXT
            )
            ''')

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS name_list (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rule_id INTEGER NOT NULL,
                log_id INTEGER NOT NULL,
                risk_level INTEGER NOT NULL,
                list_type INTEGER NOT NULL,
                business_line INTEGER NOT NULL,
                risk_label INTEGER NOT NULL,
                risk_domain INTEGER NOT NULL,
                value TEXT NOT NULL,
                value_type INTEGER NOT NULL,
                creator TEXT NOT NULL,
                create_time DATE NOT NULL
            )
            ''')
            
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS credit_report (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rule_id INTEGER NOT NULL,
                log_id INTEGER NOT NULL,
                status INTEGER NOT NULL,
                data_source TEXT NOT NULL,
                name TEXT NOT NULL,
                risk_domain INTEGER NOT NULL,
                value TEXT NOT NULL,
                value_type INTEGER NOT NULL,
                identification TEXT NOT NULL,
                create_time DATE NOT NULL
            )
            ''')
            
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS rule_management (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rule_id INTEGER NOT NULL,
                log_id INTEGER NOT NULL,
                rule_name TEXT NOT NULL,
                rule_expression TEXT NOT NULL,
                is_external INTEGER NOT NULL,
                priority TEXT,
                creator TEXT NOT NULL,
                create_time DATE NOT NULL
            )
            ''')
            
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS model_management (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                log_id INTEGER NOT NULL,
                model_name TEXT NOT NULL,
                model_file BLOB NOT NULL,
                model_version TEXT NOT NULL,
                environment TEXT NOT NULL,
                caller TEXT NOT NULL,
                approver TEXT NOT NULL,
                verified INTEGER NOT NULL,
                rollback INTEGER NOT NULL,
                create_time DATE NOT NULL
            )
            ''')
            
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS log_monitoring (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                log_id INTEGER NOT NULL,
                operator TEXT NOT NULL,
                operation TEXT NOT NULL,
                error_info TEXT,
                exception_info TEXT,
                is_warning INTEGER NOT NULL,
                is_done INTEGER NOT NULL,
                warning_type TEXT NOT NULL,
                create_time DATE NOT NULL
            )
            ''')
        else:
            # PostgreSQL table definitions
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                is_admin INTEGER NOT NULL,
                full_name TEXT,
                email TEXT,
                phone TEXT
            )
            ''')

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                username TEXT NOT NULL,
                action TEXT NOT NULL,
                details TEXT
            )
            ''')

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS name_list (
                id BIGSERIAL PRIMARY KEY,
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
            )
            ''')
            
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS credit_report (
                id BIGSERIAL PRIMARY KEY,
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
            )
            ''')
            
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS rule_management (
                id BIGSERIAL PRIMARY KEY,
                rule_id BIGINT NOT NULL,
                log_id BIGINT NOT NULL,
                rule_name VARCHAR(64) NOT NULL,
                rule_expression VARCHAR(256) NOT NULL,
                is_external INT NOT NULL,
                priority VARCHAR(64),
                creator VARCHAR(64) NOT NULL,
                create_time DATE NOT NULL
            )
            ''')
            
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS model_management (
                id BIGSERIAL PRIMARY KEY,
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
            )
            ''')
            
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS log_monitoring (
                id BIGSERIAL PRIMARY KEY,
                log_id BIGINT NOT NULL,
                operator VARCHAR(64) NOT NULL,
                operation VARCHAR(128) NOT NULL,
                error_info VARCHAR(256),
                exception_info VARCHAR(256),
                is_warning SMALLINT NOT NULL,
                is_done SMALLINT NOT NULL,
                warning_type VARCHAR(64) NOT NULL,
                create_time DATE NOT NULL
            )
            ''')

        # Add sample data (if not exist)
        if csv_data_path:  # Check if csv_data_path is provided
            cursor.execute("SELECT COUNT(*) FROM users")
            if cursor.fetchone()[0] == 0:
                # Load data from CSV files
                tables = {
                    'users': 'users.csv',
                    'logs': 'logs.csv',
                    'name_list': 'name_list.csv',
                    'log_monitoring': 'log_monitoring.csv',
                    'model_management': 'model_management.csv',
                    'rule_management': 'rule_management.csv',
                    'name_list': 'name_list.csv',
                    'credit_report': 'credit_report.csv',
                }

                for table, filename in tables.items():
                    csv_path = os.path.join(csv_data_path, filename)
                    if os.path.exists(csv_path):
                        load_csv_to_table(cursor, table, csv_path)
                    else:
                        logger.warning(f"CSV file {csv_path} does not exist, skipping initialization")

                conn.commit()
                logger.info("CSV data initialization completed")
        
        conn.commit()
        logger.info("Database initialization completed")
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        conn.rollback()
        raise
    finally:
        cursor.close()
        release_connection(conn)  # Use connection pool to release connection instead of closing directly
