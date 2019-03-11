from pyramid.view import view_config
from pyramid.response import Response
from ...database.devices.devices import get_device, update_device, get_devices
import json

def switch_action(type):
    actions = {
        'get': get_device,
        'update': update_device,
        'multiplex' : get_devices,
    }
    return actions.get(type, defaultResponse)

@view_config(route_name='device', renderer='json', request_method='POST')
def device_handler(request):
    action = request.json_body

    if 'type' in action and 'payload' in action:
        actionType = action['type']
        callback = switch_action(actionType)

        try:
            response = callback(action['payload'])
            if 'error' not in response:
                return responseSuccess(response, actionType)
            else:
                return responseError(response['errors'], actionType, 400)

        except Exception as error:
            response = reportError(
                'An error occured handling the group request', error)
            return responseError(response, actionType, 500)

    response = reportError(
        'The group request was not formatted correctly', None)
    return responseError(response, None, 400)
