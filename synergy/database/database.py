import mysql.connector as mariadb
import config
from uuid import uuid4 as uuidv4


def connectDB():
    try:
        conn = mariadb.connect(
            user=config.user,
            password=config.password,
            database=config.database
        )
        cursor = conn.cursor
        conn.autocommit = True

        return conn, cursor

    except Exception as error:
        print('SQL Error: Unable to connect to MySQL database')
        print(error)
        return None


def closeDB(conn, cursor):
    try:
        cursor.close()
        conn.close()

    except Exception as error:
        print('SQL Error: Unable to close connection to MySQL database')
        print(error)


def total_usage():
    conn, cursor = connectDB()

    try:
        col_list = ['time', 'ch1', 'ch2', 'ch3', 'ch4', 'ch5',
                    'ch6', 'ch7', 'ch8', 'ch9', 'ch10', 'ch11', 'ch12']
        query_columns = ', '.join(col_list)
        query = ''' SELECT (%s) FROM usages ''' % (query_columns)

        try:
            cursor.execute(query)
            result = cursor.fetchall()
            closeDB(conn, cursor)
            return result

        except Exception as error:
            print(''' SQL Error: Unable to fetch total usage statistics''')
            print(error)
            closeDB(conn, cursor)
            return None

    except Exception as error:
        print('Error generating query for total usage statistics')
        print(error)
        closeDB(conn, cursor)
        return None

    closeDB(conn, cursor)
    return None


def device_usage(device_id):
    conn, cursor = connectDB()

    try:
        col_list = ['time', 'ch1', 'ch2', 'ch3', 'ch4', 'ch5',
                    'ch6', 'ch7', 'ch8', 'ch9', 'ch10', 'ch11', 'ch12']
        query_columns = ', '.join(col_list)
        query = ''' SELECT (%s) FROM usages WHERE deviceID = (%s) ''' % (
            query_columns, device_id)

        try:
            cursor.execute(query)
            result = cursor.fetchall()
            closeDB(conn, cursor)
            return result

        except Exception as error:
            print(''' SQL Error: Unable to fetch device usages for device %s''' %(device_id))
            print(error)
            closeDB(conn, cursor)
            return None

    except Exception as error:
        print('Error generating query for device usage selection')
        print(error)
        closeDB(conn, cursor)
        return None

    closeDB(conn, cursor)
    return None


def ch_usage(ch_id):
    conn, cursor = connectDB()

    try:
        device_from_channel_query = ''' SELECT deviceID FROM channels WHERE channelID = (%s) ''' % (
            ch_id)
        cursor.execute(device_from_channel_query)

        try:
            device_id = cursor.fetchall()
            channel_column_position_query = ''' SELECT * FROM devices WHERE deviceID = (%s) ''' % (
                device_id)
            cursor.execute(channel_column_position_query)

            try:
                all_chs = cursor.fetchall()
                channel_idx = all_chs.index(ch_id)
                col = "ch" + str(channel_idx - 2)

                channel_usage_query = ''' SELECT (%s) FROM usages WHERE deviceID = (%s) ''' % (
                    col, device_id)
                cursor.execute(channel_usage_query)
                result = cursor.fetchall()

                closeDB(conn, cursor)
                return result

            except Exception as error:
                print(
                    ''' SQL Error: Unable to get usage data for channel %s''' % (ch_id))
                print(error)
                closeDB(conn, cursor)
                return None

        except Exception as error:
            print(
                ''' SQL Error: Unable to get channel ID position for channel %s''' % (ch_id))
            print(error)
            closeDB(conn, cursor)
            return None

    except Exception as error:
        print(''' SQL Error: Unable to get device ID for channel %s''' % (ch_id))
        print(error)
        closeDB(conn, cursor)
        return None

    closeDB(conn, cursor)
    return None


def get_ch_name(ch_id):
    conn, cursor = connectDB()

    try:
        query = ''' SELECT name FROM channels WHERE channelID = (%s) ''' % (
            ch_id)

        try:
            cursor.execute(query)
            name = cursor.fetchall()
            closeDB(conn, cursor)
            return name[0]

        except Exception as error:
            print(''' SQL Error: Unable to get channel name for channel %s''' % (ch_id))
            print(error)
            closeDB(conn, cursor)
            return None

    except Exception as error:
        print('Error generating query for channel name selection')
        print(error)
        closeDB(conn, cursor)
        return None

    closeDB(conn, cursor)
    return None


def get_device_name(device_id):
    conn, cursor = connectDB()

    try:
        query = ''' SELECT name FROM devices WHERE deviceID = (%s) ''' % (
            device_id)

        try:
            cursor.execute(query)
            name = cursor.fetchall()
            closeDB(conn, cursor)
            return name[0]

        except Exception as error:
            print(''' SQL Error: Unable to feetch device name for device ''' %
                  (device_id))
            print(error)
            closeDB(conn, cursor)
            return None

    except Exception as error:
        print('Error generating query for device name selection')
        print(error)
        closeDB(conn, cursor)
        return None

    closeDB(conn, cursor)
    return None


def set_ch_name(device_id, ch_id, name):
    conn, cursor = connectDB()

    try:
        cols = ['deviceID', 'channelID', 'name']
        vals = [device_id, ch_id, name]
        query_placeholders = ', '.join(['%s'] * len(vals))
        query_columns = ', '.join(cols)
        insert_query = ''' INSERT INTO channels (%s) VALUES (%s) ON DUPLICATE KEY UPDATE name=(%s)''' % (
            query_columns, query_placeholders, name)

        try:
            cursor.execute(insert_query, vals)

        except Exception as error:
            print(''' SQL Error: Unable to insert new channel name for channel %s on device %s ''' % (
                device_id, ch_id))
            print(error)
            closeDB(conn, cursor)

    except Exception as error:
        print('Error generating query for channel name insertion')
        print(error)
        closeDB(conn, cursor)

    closeDB(conn, cursor)


def set_device_name(device_id, name):
    conn, cursor = connectDB()

    try:
        cols = ['deviceID', 'name']
        vals = [device_id, name]
        query_placeholders = ', '.join(['%s'] * len(vals))
        query_columns = ', '.join(cols)
        insert_query = ''' INSERT INTO devices (%s) VALUES (%s) ON DUPLICATE KEY UPDATE name=(%s)''' % (
            query_columns, query_placeholders, name)

        try:
            cursor.execute(insert_query, vals)

        except Exception as error:
            print(''' SQL Error: Unable to set device name for device %s''' %
                  (device_id))
            print(error)
            closeDB(conn, cursor)

    except Exception as error:
        print('Error generating query for device name insertion')
        print(error)
        closeDB(conn, cursor)

    closeDB(conn, cursor)


def set_group_name(group_id, name):
    conn, cursor = connectDB()

    try:
        cols = ['groupID', 'name']
        vals = [group_id, name]
        query_placeholders = ', '.join(['%s'] * len(vals))
        query_columns = ', '.join(cols)
        insert_query = ''' INSERT INTO groups (%s) VALUES (%s) ON DUPLICATE KEY UPDATE name=(%s)''' % (
            query_columns, query_placeholders, name)

        try:
            cursor.execute(insert_query, vals)

        except Exception as error:
            print(''' SQL Error: Unable to set group name for group %s''' %
                  (group_id))
            print(error)
            closeDB(conn, cursor)

    except Exception as error:
        print('Error generating query for group name insertion')
        print(error)
        closeDB(conn, cursor)

    closeDB(conn, cursor)


def get_groupies(group_id):
    conn, cursor = connectDB()

    try:
        query = ''' SELECT * FROM groupings WHERE groupID = (%s) ''' % (
            group_id)

        try:
            cursor.execute(query)
            groupies = cursor.fetchall()
            closeDB(conn, cursor)
            return groupies

        except Exception as error:
            print(
                ''' SQL Error: Unable to fetch group members for group %s''' % (group_id))
            print(error)
            closeDB(conn, cursor)
            return None

    except Exception as error:
        print('Error generating query for group member selection')
        print(error)
        closeDB(conn, cursor)
        return None

    closeDB(conn, cursor)
    return None


def add_groupie(group_id, uuid):
    conn, cursor = connectDB()

    try:
        cols = ['groupId', 'uuid']
        vals = [group_id, uuid]
        query_placeholders = ', '.join(['%s'] * len(vals))
        query_columns = ', '.join(cols)
        query = ''' INSERT INTO groupings (%s) VALUES (%s) ''' % (
            query_columns, query_placeholders)

        try:
            cursor.execute(query, vals)

        except Exception as error:
            print(''' SQL Error: Unable to insert item %s into group with id = %s''' % (
                uuid, group_id))
            print(error)
            closeDB(conn, cursor)

    except Exception as error:
        print('Error generating query for group member insertion')
        print(error)
        closeDB(conn, cursor)

    closeDB(conn, cursor)


def create_group(name, *ids):
    group_id = str(uuidv4())

    try:
        set_group_name(group_id, name)

        try:
            for i in range(len(ids)):
                add_groupie(group_id, ids[i])

        except Exception as error:
            print(''' Unable to add member groups to group: %s ''' % (name))
            print(error)

    except Exception as error:
        print(''' Unable to add group with name: %s ''' % (name))
        print(error)
