from ..database import connectDB, closeDB

from ...api.utils.reporter import reportError

def usage(payload):
    conn, cursor = connectDB()

    try:
        is_cumulative = False
        include_where_clause = False
        is_inital_param = True
        after_clause = ''
        before_clause = ''

        if 'include' not in payload or len(payload['include']) == 0:
            is_cumulative = True
        if 'after' in payload:
            # Any time after the given value (inclusive)
            after_clause = ' AND time >= {}'.format(payload['after'])
            include_where_clause = True
            if is_inital_param:
                after_clause = after_clause[3:]
                is_inital_param = False
        if 'before' in payload:
            # Any time before the give value (inclusive)
            before_clause = ' AND time <= {}'.format(payload['before'])
            include_where_clause = True
            if is_inital_param:
                before_clause = before_clause[4:]
                is_inital_param = False

        try:
            if is_cumulative:
                where_clause = ' WHERE' if include_where_clause else ''
                query = ''' SELECT * FROM usages%s%s%s ''' % (where_clause, after_clause, before_clause)

                try:
                    cursor.execute(query)
                    currents = cursor.fetchall()
                    print(currents)

                    if len(currents):
                        payload['currents'] = currents
                    else:
                        payload['currents'] = []
                    
                    return payload

                except Exception as error:
                    responseError = reportError(
                        'SQL ERROR: An error occured fetching the available currents', error)
                    closeDB(conn, cursor)
                    return responseError

            else:
                for channel in payload['include']:
                    channel_num = 'ch' + str(channel['position'])
                    query = ''' SELECT %s FROM usages WHERE deviceID = '%s'%s%s ''' % (
                        channel_num, channel['deviceID'], after_clause, before_clause)

                    try:
                        cursor.execute(query)
                        current = cursor.fetchall()

                        if len(current):
                            # Since we are only getting a single column we can assume type safety of current[0][channel_num]
                            channel['current'] = current[0][channel_num]
                        else:
                            channel['current'] = None

                    except Exception as error:
                        responseError = reportError(
                            'SQL ERROR: An error occured fetching current with the specified ID', error)
                        closeDB(conn, cursor)
                        return responseError
                
                return payload['include']

        except Exception as error:
            responseError = reportError(
                'An error occured fetching the specified currents', error)
            closeDB(conn, cursor)
            return responseError

    except Exception as error:
        responseError = reportError(
            'An error occured resolving the parameters of the query', error)
        closeDB(conn, cursor)
        return responseError

    responseError = reportError(
        'An error occured resolving the parameters of the query', None)
    closeDB(conn, cursor)
    return responseError
