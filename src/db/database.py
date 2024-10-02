
from .db_actions import create_connection, create_table, insert_data, select_all, insert_multiple_channels

def init_channels():
    database = r"channels.db"

    sql_create_channels_table = """ CREATE TABLE IF NOT EXISTS channels (
                                            id text PRIMARY KEY,
                                            name text NOT NULL,
                                            reliability integer
                                        ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # Check if the table already exists
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='channels';")
        if cursor.fetchone() is None:
            # create channels table
            create_table(conn, sql_create_channels_table)
        else:
            print("Table 'channels' already exists.")
    else:
        print("Error! cannot create the database connection.")

def add_telegram_channel(channel_id, name, reliability):
    """
    Add a new telegram channel to the channels table
    :param conn: Connection object
    :param channel_id: id of the channel
    :param name: name of the channel
    :param reliability: reliability level of the channel
    :return: last row id
    """

    conn = create_connection(r"channels.db", timeout=10)

    lastrowid = insert_data(conn, 'channels', {'id': channel_id, 'name': name, 'reliability': reliability})

    return lastrowid

def add_multiple_telegram_channels(channels):
    """
    Add multiple telegram channels to the channels table
    :param conn: Connection object
    :param channels: list of dictionaries of channels
    :return: last row id
    """

    conn = create_connection(r"channels.db", timeout=10)

    lastrowid = insert_multiple_channels(conn, 'channels', channels)

    return lastrowid

def get_telegram_channels():
    """
    Query all rows in the channels table
    :param conn: the Connection object
    :return: list of rows
    """

    conn = create_connection(r"channels.db")

    rows = select_all(conn, 'channels')
    channels = []
    for row in rows:
        channel = {
            'id': row[0],
            'name': row[1],
            'reliability': row[2]
        }
        channels.append(channel)

    return channels