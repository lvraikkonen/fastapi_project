import os
import aiosqlite
import sqlite3
from typing import List, Dict, Any


def get_table_names(db_conn: sqlite3.Connection) -> List[str]:
    """Return a list of table names."""
    table_names = []
    tables = db_conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    for table in tables:
        table_names.append(table[0])
    return table_names


def get_column_names(db_conn: sqlite3.Connection, table_name: str) -> List[str]:
    """Return a list of column names."""
    column_names = []
    columns = db_conn.execute(f"PRAGMA table_info('{table_name}');")
    for col in columns:
        column_names.append(col[1])
    return column_names


def get_database_info(db_conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    """Return a list of dicts containing the table name and columns for each table in the database."""
    table_dicts = []
    table_names = get_table_names(db_conn)
    for table_name in table_names:
        column_names = get_column_names(db_conn, table_name)
        table_dicts.append({"table_name": table_name, "column_names": column_names})
    return table_dicts


def get_database_info_str(db_conn: sqlite3.Connection) -> str:
    """Return a string representation of the database schema."""
    database_schema_dict = get_database_info(db_conn)
    database_schema_string = "\n".join(
        [
            f"Table: {table['table_name']}\nColumns: {', '.join(table['column_names'])}"
            for table in database_schema_dict
        ]
    )
    return database_schema_string


def ask_database(db_conn: sqlite3.Connection, query: str) -> str:
    """Function to query SQLite database with a provided SQL query."""
    try:
        results = str(db_conn.execute(query).fetchall())
    except Exception as e:
        results = f"query failed with error: {e}"
    return results


async def get_table_names_async(db_conn: aiosqlite.Connection) -> List[str]:
    """Return a list of table names."""
    table_names = []
    async with db_conn.execute("SELECT name FROM sqlite_master WHERE type='table';") as cursor:
        async for row in cursor:
            table_names.append(row[0])
    return table_names


async def get_column_names_async(db_conn: aiosqlite.Connection, table_name: str) -> List[str]:
    """Return a list of column names."""
    column_names = []
    async with db_conn.execute(f"PRAGMA table_info('{table_name}');") as cursor:
        async for row in cursor:
            column_names.append(row[1])
    return column_names


async def get_database_info_async(db_conn: aiosqlite.Connection) -> List[Dict[str, Any]]:
    """Return a list of dicts containing the table name and columns for each table in the database."""
    table_dicts = []
    table_names = await get_table_names_async(db_conn)
    for table_name in table_names:
        column_names = await get_column_names_async(db_conn, table_name)
        table_dicts.append({"table_name": table_name, "column_names": column_names})
    return table_dicts


async def get_database_info_str_async(db_conn: aiosqlite.Connection) -> str:
    """Return a string representation of the database schema."""
    database_schema_dict = await get_database_info_async(db_conn)
    database_schema_string = "\n".join(
        [
            f"Table: {table['table_name']}\nColumns: {', '.join(table['column_names'])}"
            for table in database_schema_dict
        ]
    )
    return database_schema_string


async def ask_database_async(db_conn: aiosqlite.Connection, query: str) -> str:
    """Function to query SQLite database with a provided SQL query."""
    try:
        async with db_conn.execute(query) as cursor:
            results = await cursor.fetchall()
        return str(results)
    except Exception as e:
        return f"query failed with error: {e}"
