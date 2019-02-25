from ..database import connectDB, closeDB

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
            print(
                ''' SQL Error: Unable to fetch device usages for device %s''' % (device_id))
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
