import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
            client_id INT NOT NULL,
            file_id TEXT NOT NULL
            );
"""
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())
    

    def add_client(self, client_id: int, file_id: str):
        sql = "INSERT INTO Users (client_id, file_id) VALUES (?, ?)"
        self.execute(sql, parameters=(client_id, file_id,), commit=True)
    
    def select_file_id(self, client_id: int):
        sql = "SELECT file_id FROM Users WHERE client_id = ?"
        result = self.execute(sql, parameters=(client_id,), fetchone=True)
        if result is None:
            return None
        return result[0]