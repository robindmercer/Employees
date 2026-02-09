"""
Database connection and operations module
Handles all database interactions with proper connection management
"""
import mysql.connector
from mysql.connector import Error
from config import app_config
import logging

logger = logging.getLogger(__name__)


class Database:
    """Database connection manager"""
    
    def __init__(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(
                host=app_config.MYSQL_HOST,
                user=app_config.MYSQL_USER,
                password=app_config.MYSQL_PASSWORD,
                database=app_config.MYSQL_DB
            )
            if self.connection.is_connected():
                logger.info("Database connection established")
        except Error as e:
            logger.error(f"Error connecting to database: {e}")
            raise
    
    def get_connection(self):
        """Get active connection, reconnect if needed"""
        try:
            if self.connection and self.connection.is_connected():
                return self.connection
            else:
                self.connect()
                return self.connection
        except Error as e:
            logger.error(f"Connection error: {e}")
            raise
    
    def execute_query(self, query, params=None):
        """Execute SELECT query"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=False)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Error as e:
            logger.error(f"Query execution error: {e}")
            return None
    
    def execute_update(self, query, params=None):
        """Execute INSERT, UPDATE, DELETE query"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            logger.info(f"Query executed successfully. Rows affected: {cursor.rowcount}")
            cursor.close()
            return cursor.rowcount
        except Error as e:
            conn.rollback()
            logger.error(f"Update execution error: {e}")
            raise
    
    def close(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("Database connection closed")


# Global database instance
db = Database()
