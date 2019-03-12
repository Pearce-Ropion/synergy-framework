from uuid import uuid4 as uuidv4

from ..database import connectDB, closeDB
from ...api.utils.reporter import isError, reportError
from ..utils import listify


def get_channels(payload, isDeviceQuery = False):
    conn, cursor = connectDB()

    key = 'deviceID' if isDeviceQuery else 'channelID'

    try:
        query = ''' SELECT * FROM channels WHERE %s = '%s' ''' % (
            key, payload[key])
        cursor.execute(query)
        channels = cursor.fetchall()

        if len(channels) > 0:
            if isDeviceQuery:
                return channels
            else:
                # Channel IDs should be unique so len(channels) === 1
                return channels[0]
        else:
            if isDeviceQuery:
                responseError = reportError(
                    'No channels were found for the device with the specified ID: {}'.format(payload[key]), None)
            else:
                responseError = reportError(
                    'No channel was found with the specified ID: {}'.format(payload[key]), None)
            closeDB(conn, cursor)
            return responseError

    except Exception as error:
        responseError = reportError(
            'An error occured getting the channels with the specified ID', error)
        closeDB(conn, cursor)
        return responseError

    responseError = reportError(
        'An error occured getting the channels with the specified ID', None)
    closeDB(conn, cursor)
    return responseError

def update_channel(payload):
    conn, cursor = connectDB()

    try:
        query = ''' UPDATE channels SET name = '%s' WHERE channelID = '%s' ''' % (
            payload['name'], payload['channelID'])
        cursor.execute(query)
        closeDB(conn, cursor)
        return payload

    except Exception as error:
        responseError = reportError(
            'SQL ERROR: An error occured updating the name of the channel with the specified ID: {}'.format(payload['channelID']), error)
        closeDB(conn, cursor)
        return responseError

    responseError = reportError(
        'An error occured updating the name of the channel with the specified ID: {}'.format(payload['channelID']), None)
    closeDB(conn, cursor)
    return responseError


def multiplex_channels(payload):
    conn, cursor = connectDB()

    try:
        query = ''' SELECT * FROM channels ORDER BY name ASC LIMIT %s, %s''' % (
            payload['offset'], payload['count'])
        
        cursor.execute(query)
        channels = cursor.fetchall()
        closeDB(conn, cursor)

        return channels

    except Exception as error:
        responseError = reportError(
            'An error occurred while retrieving channels', error)
        closeDB(conn, cursor)
        return responseError

    responseError = reportError(
        'An error occurred retrieving channels', None)
    closeDB(conn, cursor)
    return responseError

