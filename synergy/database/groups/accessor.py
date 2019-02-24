from uuid import uuid4 as uuidv4

from ..database import connectDB, closeDB
from ...api.utils.reporter import isError, reportError
from ..utils import listify

def set_group_name(payload):
    conn, cursor = connectDB()

    try:
        insert = listify(payload)
        query = ''' INSERT INTO groups (%s) VALUES (%s) ON DUPLICATE KEY UPDATE name='%s' ''' % (
            insert.columns, insert.placeholders, payload['name'])

        try:
            cursor.execute(query, insert.vals)
            closeDB(conn, cursor)
            return payload

        except Exception as error:
            responseError = reportError(
                'SQL Error: An error occured adding a group name', error)
            closeDB(conn, cursor)
            return responseError

    except Exception as error:
        responseError = reportError(
            'An error occured adding a group name', error)
        closeDB(conn, cursor)
        return responseError

    responseError = reportError(
        'An error occured adding a group name', None)
    closeDB(conn, cursor)
    return responseError


def add_groupie(payload):
    conn, cursor = connectDB()

    try:
        exists_query = ''' SELECT * FROM groupings WHERE groupID = '%s' AND uuid = '%s' ''' % (
            payload['groupID'], payload['uuid'])
        cursor.execute(exists_query)
        groupings = cursor.fetchall()

        if not len(groupings) > 0:
            try:
                insert = listify(payload)
                query = ''' INSERT INTO groupings (%s) VALUES (%s) ''' % (
                    insert.columns, insert.placeholders)

                try:
                    cursor.execute(query, insert.vals)
                    closeDB(conn, cursor)
                    return payload

                except Exception as error:
                    responseError = reportError(
                        'SQL Error: An error occured adding member to group', error)
                    closeDB(conn, cursor)
                    return responseError

            except Exception as error:
                responseError = reportError(
                    'An error occured adding member to group', error)
                closeDB(conn, cursor)
                return responseError
            
        else:
            responseError = reportError(
                'This uuid is already a member of this group', None)
            closeDB(conn, cursor)
            return responseError

    except Exception as error:
        responseError = reportError(
            'An error occured adding member to group', error)
        closeDB(conn, cursor)
        return responseError
    
    responseError = reportError(
        'An error occured adding member to group', None)
    closeDB(conn, cursor)
    return responseError


def remove_groupie(payload):
    conn, cursor = connectDB()

    try:
        query = ''' DELETE FROM groupings WHERE groupID = '%s' AND uuid = '%s' ''' % (
            payload['groupID'], payload['uuid'])

        try:
            cursor.execute(query)
            closeDB(conn, cursor)
            return payload

        except Exception as error:
            responseError = reportError(
                'SQL Error: An error occured removing member from group', error)
            closeDB(conn, cursor)
            return responseError

    except Exception as error:
        responseError = reportError(
            'An error occured removing member from group', error)
        closeDB(conn, cursor)
        return responseError

    responseError = reportError(
        'An error occured removing member from group', None)
    closeDB(conn, cursor)
    return responseError

def get_group_name(payload):
    conn, cursor = connectDB()

    try:
        query = ''' SELECT * FROM groups WHERE groupID = '%s' ''' % (
            payload['groupID'])
        cursor.execute(query)
        groups = cursor.fetchall()

        if len(groups) > 0:
            return groups[0]
        else:
            responseError = reportError(
                'No groups were found with the specified ID', None)
            closeDB(conn, cursor)
            return responseError

    except Exception as error:
        responseError = reportError(
            'SQL ERROR: An error occured getting the group with the specified ID', error)
        closeDB(conn, cursor)
        return responseError

    responseError = reportError(
        'An error occured getting the group with the specified ID', None)
    closeDB(conn, cursor)
    return responseError

def get_groupies(payload):
    conn, cursor = connectDB()

    try:
        query = ''' SELECT * FROM groupings WHERE groupID = '%s' ''' % (
            payload['groupID'])
        cursor.execute(query)
        members = cursor.fetchall()

        if len(members) > 0:
            return members
        else:
            responseError = reportError(
                'No group members were found for the specified group ID', None)
            closeDB(conn, cursor)
            return responseError

    except Exception as error:
        responseError = reportError(
            'SQL ERROR: An error occured getting group members with the specified ID', error)
        closeDB(conn, cursor)
        return responseError

    responseError = reportError(
        'An error occured getting group members with the specified ID', None)
    closeDB(conn, cursor)
    return responseError

    
def delete_grouping(payload):
    conn, cursor = connectDB()

    try:
        query = ''' DELETE FROM groups WHERE groupID = '%s' ''' % (
            payload['groupID'])

        try:
            cursor.execute(query)
            closeDB(conn, cursor)
            return {}

        except Exception as error:
            responseError = reportError(
                'SQL ERROR: An error occured deleting the group with the specified ID', error)
            closeDB(conn, cursor)
            return responseError

    except Exception as error:
        responseError = reportError(
            'An error occured deleting the group with the specified ID', error)
        closeDB(conn, cursor)
        return responseError

    responseError = reportError(
        'An error occured deleting the group with the specified ID', None)
    closeDB(conn, cursor)
    return responseError


def delete_groupies(payload):
    conn, cursor = connectDB()

    try:
        query = ''' DELETE FROM groupings WHERE groupID = '%s' ''' % (
            payload['groupID'])

        try:
            cursor.execute(query)
            closeDB(conn, cursor)
            return {}

        except Exception as error:
            responseError = reportError(
                'SQL ERROR: An error occured deleting the members of the group with the specified ID', error)
            closeDB(conn, cursor)
            return responseError

    except Exception as error:
        responseError = reportError(
            'An error occured deleting the members of the group with the specified ID', error)
        closeDB(conn, cursor)
        return responseError

    responseError = reportError(
        'An error occured deleting the members of the group with the specified ID', None)
    closeDB(conn, cursor)
    return responseError
