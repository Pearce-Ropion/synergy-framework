from pyramid.view import view_config
from pyramid.response import Response

from ...database.groups.caller import create_group, get_group, update_group, delete_group
from ...api.utils.response import responseSuccess, responseError, defaultResponse
from ...api.utils.reporter import reportError


def switch_action(type):
    actions = {
        'create': create_group,
        'get': get_group,
        'update': update_group,
        'delete': delete_group,
    }
    return actions.get(type, defaultResponse)

@view_config(route_name='group', renderer='json', request_method='POST')
def group_handler(request):
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
                'An error occured handling the user request', error)
            return responseError(response, actionType, 500)

    response = reportError(
        'The group request was not formatted correctly', None)
    return responseError(response, None, 400)
