import sqlite3
from utils import logger
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        logger.error(e)
    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        logger.error(e)

def insert_data(conn, table, data):
    """
    Insert data into table
    :param conn: Connection object
    :param table: table name
    :param data: dictionary of data to insert
    :return: last row id
    """
    keys = ', '.join(data.keys())
    question_marks = ', '.join(list('?'*len(data)))
    values = tuple(data.values())
    
    sql = f'INSERT INTO {table} ({keys}) VALUES ({question_marks})'
    cur = conn.cursor()
    try:
        cur.execute(sql, values)
        logger.info(f"Data inserted successfully: {data}")
    except Error as e:
        if 'UNIQUE constraint failed' in str(e):
            logger.error(f"Data already exists in the database: {data}")
            return f"Data already exists in the database: {data}"
    conn.commit()
    return cur.lastrowid

def select_all(conn, table):
    """
    Query all rows in the table
    :param conn: the Connection object
    :param table: table name
    :return: list of rows
    """
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table}")
    
    rows = cur.fetchall()
    return rows