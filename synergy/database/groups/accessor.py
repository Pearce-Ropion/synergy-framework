from uuid import uuid4 as uuidv4

from ..database import connectDB, closeDB
from ..members import get_members
from ..devices.devices import get_device
from ..devices.channels import get_channels
from ..utils import listify

from ...api.utils.reporter import isError, reportError


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
        # check if this group to group member combination already exists
        exists_query = ''' SELECT * FROM groupings WHERE groupID = '%s' AND uuid = '%s' ''' % (
            payload['groupID'], payload['uuid'])
        cursor.execute(exists_query)
        groupings = cursor.fetchall()

        if len(groupings) == 0:
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


def get_groupies(payload, channels = []):
    conn, cursor = connectDB()

    try:
        group = get_group_name(payload)

        if isError(group):
            closeDB(conn, cursor)
            return group

    except Exception as error:
        responseError = reportError('An error occured retrieving the group name with the specified ID: {}'.format(payload['groupID']), error)
        closeDB(conn, cursor)
        return responseError


    try:
        query = ''' SELECT * FROM groupings WHERE groupID = '%s' ''' % (
            payload['groupID'])
        cursor.execute(query)
        members = cursor.fetchall()

        accumulator = {
            'groupID': group['groupID'],
            'name': group['name'],
            'groups': [],
            'devices': [],
            'channels': [],
            'allChannels': [],
        }

        result = get_members(members, accumulator, channels)

        if isError(result):
            closeDB(conn, cursor)
            return result
        else:
            return accumulator

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


def multiplex_groups(payload):
    conn, cursor = connectDB()

    try:
        query = ''' SELECT groupID FROM groups ORDER BY name ASC LIMIT %s, %s''' % (
            payload['offset'], payload['count'])

        cursor.execute(query)
        groupIDs = cursor.fetchall()
        closeDB(conn, cursor)

        try:

            result = []
            errors = []

            for groupID in groupIDs:
                group = get_groupies(groupID)
                if isError(group):
                    errors.append(group)
                else:
                    result.append(group)

            if len(errors) > 0:
                return {
                    'error': True,
                    'errors': errors,
                }

            return result

        except Exception as error:
            responseError = reportError(
                'An error occured retrieving group members', error)
            return responseError

    except Exception as error:
        responseError = reportError(
            'An error occured retrieving groups', error)
        closeDB(conn, cursor)
        return responseError

    responseError = reportError(
        'An error occured retrieving groups', None)
    closeDB(conn, cursor)
    return responseError
