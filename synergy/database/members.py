from .devices.devices import get_device
from .devices.channels import get_channels

from ..api.utils.reporter import isError, reportError


def get_members(members, accumulator, channels=[]):
    try:
        if len(members) > 0:
            for member in members:
                if member['type'] == 'group':
                    # Defer import so as not to cause circular dependency importing
                    from .groups.accessor import get_groupies
                    result = get_groupies({
                        'groupID': member['uuid'],
                    }, channels)

                    if isError(result):
                        return result

                    accumulator['groups'].append(result)

                elif member['type'] == 'device':
                    result = get_device({
                        'deviceID':  member['uuid']
                    }, True, channels)

                    if isError(result):
                        return result

                    accumulator['devices'].append(result)

                elif member['type'] == 'channel':
                    result = get_channels({
                        'channelID': member['uuid']
                    })

                    if isError(result):
                        return result

                    accumulator['channels'].append(result)
                    channels.append(result)

            if len(accumulator['groups']) == 0 and len(accumulator['devices']) == 0 and len(accumulator['channels']) == 0:
                return members

            accumulator['allChannels'] = channels
            return accumulator

        else:
            responseError = reportError(
                'No members available to retrieve channels for', None)
            return responseError

    except Exception as error:
        responseError = reportError(
            'An error occured getting the members with the specified IDs', error)
        return responseError

    responseError = reportError('An error occured getting the members with the specified IDs', None)
    return responseError
