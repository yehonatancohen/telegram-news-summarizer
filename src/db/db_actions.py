import sqlite3
from utils import logger
from sqlite3 import Error

def create_connection(db_file, timeout=10):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file, timeout=timeout)
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

def insert_multiple_channels(conn, table, data):
    """
    Insert multiple data into table
    :param conn: Connection object
    :param table: table name
    :param data: list of dictionaries of data to insert
    :return: last row id
    """
    
    sql_list = []

    for channel in data:
        if not channel.get('reliability'):
            channel['reliability'] = 1
        if not channel.get('name'):
            channel['name'] = 'undefined'
        
        # Create the keys, placeholders, and values for each channel
        keys = ', '.join(channel.keys())
        question_marks = ', '.join(list('?'*len(channel)))
        values = tuple(channel.values())
        
        # Create the SQL insert statement for the current channel
        sql = f'INSERT INTO {table} ({keys}) VALUES ({question_marks})'
        
        cur = conn.cursor()
        try:
            # Try to execute the SQL command for the current channel
            cur.execute(sql, values)
            logger.info(f"Data inserted successfully: {channel}")
        
        except sqlite3.IntegrityError as e:
            # Handle unique constraint error and continue with other channels
            if 'UNIQUE constraint failed' in str(e):
                logger.warning(f"Data already exists for channel: {channel}")
                continue  # Skip this channel and proceed with the next one
        
        except sqlite3.OperationalError as e:
            # Handle other operational errors that might affect the entire transaction
            logger.error(f"Error inserting data: {e}")
            conn.rollback()
            break  # Stop further processing if there's a critical operational error

    # Commit the transaction after processing all channels
    conn.commit()
    lastrowid = cur.lastrowid
    conn.close()
    return lastrowid

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
    except sqlite3.OperationalError as e:
        logger.error(f"Error inserting data: {e}")
        conn.rollback()

    conn.commit()
    lastrowid = cur.lastrowid
    conn.close()
    return lastrowid

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