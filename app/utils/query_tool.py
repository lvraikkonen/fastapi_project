import os
import aiosqlite
import sqlite3


def get_table_names(db_conn):
    """Return a list of table names."""
    table_names = []
    tables = db_conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    for table in tables:
        table_names.append(table[0])
    return table_names


def get_column_names(db_conn, table_name):
    """Return a list of column names."""
    column_names = []
    columns = db_conn.execute(f"PRAGMA table_info('{table_name}');")
    for col in columns:
        column_names.append(col[1])
    return column_names


def get_database_info(db_conn):
    """Return a list of dicts containing the table name and columns for each table in the database."""
    table_dicts = []
    table_names = get_table_names(db_conn)
    for table_name in table_names:
        columns_names = get_column_names(db_conn, table_name)
        table_dicts.append({"table_name": table_name, "column_names": columns_names})
    return table_dicts


def get_database_info_str(db_conn):
    database_schema_dict = get_database_info(db_conn)
    database_schema_string = "\n".join(
        [
            f"Table: {table['table_name']}\nColumns: {', '.join(table['column_names'])}"
            for table in database_schema_dict
        ]
    )
    return database_schema_string


def ask_database(db_conn, query):
    """Function to query SQLite database with a provided SQL query."""
    try:
        results = str(db_conn.execute(query).fetchall())
    except Exception as e:
        results = f"query failed with error: {e}"
    return results
