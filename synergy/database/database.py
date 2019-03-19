from uuid import uuid4 as uuidv4

import mysql.connector as mariadb

from ..api.utils.reporter import reportError

use_external = True
external_host = '24.130.208.33'
internal_host = '192.168.0.39'

config = {
    'user': 'synergy',
    'password': 'wonderland',
    'host': external_host if use_external else internal_host,
    'port': 3306,
    'database': 'synergy',
    'raise_on_warnings': True
}

def connectDB():
    try:
        conn = mariadb.connect(**config)
        cursor = conn.cursor(dictionary=True)
        conn.autocommit = True

        return conn, cursor

    except Exception as error:
        response = reportError(
            'SQL Error: Unable to connect to Synergy database', error)
        return response, None

    return None, None


def closeDB(conn, cursor):
    try:
        cursor.close()
        conn.close()

    except Exception as error:
        response = reportError(
            'SQL Error: Unable to close database connection', error)
        return response

    return
