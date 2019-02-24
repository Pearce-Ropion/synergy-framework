from uuid import uuid4 as uuidv4

from .database import connectDB, closeDB
from ..api.utils.reporter import reportError


def create_user(payload):
    conn, cursor = connectDB()

    try:

        user_exists = get_user(payload, True)

        if not user_exists:

            payload['userID'] = str(uuidv4())

            cols = list(payload.keys())
            vals = list(payload.values())
            placeholders = ', '.join(['%s'] * len(vals))
            formatted_cols = ', '.join(cols)

            query = ''' INSERT INTO users (%s) VALUES (%s) ''' % (
                formatted_cols, placeholders)

            try:
                cursor.execute(query, vals)
                closeDB(conn, cursor)
                return payload

            except Exception as error:
                responseError = reportError(
                    'SQL ERROR: An error occured creating a new user', error)
                closeDB(conn, cursor)
                return responseError

        else:
            responseError = reportError(
                'The user being created already exists', None)
            closeDB(conn, cursor)
            return responseError

    except Exception as error:
        responseError = reportError(
            'An error occured creating a new user', error)
        closeDB(conn, cursor)
        return responseError

    responseError = reportError('An error occured creating a new user', None)
    closeDB(conn, cursor)
    return responseError


def get_user(payload, ifExists = False):
    conn, cursor = connectDB()

    try:
        query = ''' SELECT * FROM users WHERE email = '%s' ''' % (
            payload['email'])
        cursor.execute(query)
        users = cursor.fetchall()

        if len(users) > 0 and ifExists:
            closeDB(conn, cursor)
            return True
        elif len(users) == 0 and ifExists:
            return False
        elif len(users) > 0:
            closeDB(conn, cursor)
            return users[0]
        else:
            responseError = reportError(
                'No users were found with email: {}'.format(payload['email']), None)
            closeDB(conn, cursor)
            return responseError

    except Exception as error:
        responseError = reportError(
            'SQL ERROR: An error occured getting user with email: {}'.format(payload['email']), error)
        closeDB(conn, cursor)
        return responseError

    responseError = reportError(
        'An error occured getting user with email: {}'.format(payload['email']), None)
    closeDB(conn, cursor)
    return responseError


def update_user(payload):
    conn, cursor = connectDB()

    try:
        cols = list(payload.keys())
        vals = list(payload.values())
        updates = []
        for i in range(len(vals)):
            updates.append("{} = '{}'".format(cols[i], vals[i]))
        updates = ', '.join(updates)

        query = ''' UPDATE users SET %s WHERE userID = '%s' ''' % (
            updates, payload['userID'])

        try:
            cursor.execute(query)
            closeDB(conn, cursor)
            return payload

        except Exception as error:
            responseError = reportError(
                'SQL ERROR: An error occured updating user with email: {}'.format(payload['email']), error)
            closeDB(conn, cursor)
            return responseError

    except Exception as error:
        responseError = reportError(
            'An error occured updating user with email: {}'.format(payload['email']), error)
        closeDB(conn, cursor)
        return responseError

    responseError = reportError(
        'An error occured updating user with email: {}'.format(payload['email']), None)
    closeDB(conn, cursor)
    return responseError


def delete_user(payload):
    conn, cursor = connectDB()

    try:
        query = ''' DELETE FROM users WHERE userID = '%s' ''' % (
            payload['userID'])
        cursor.execute(query)
        closeDB(conn, cursor)
        return {}

    except Exception as error:
        responseError = reportError(
            'SQL ERROR: An error occured deleting user with id: {}'.format(payload['userID']), error)
        closeDB(conn, cursor)
        return responseError

    responseError = reportError(
        'An error occured deleting user with id: {}'.format(payload['userID']), None)
    closeDB(conn, cursor)
    return responseError
