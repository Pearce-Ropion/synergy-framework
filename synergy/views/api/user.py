from pyramid.view import view_config
from pyramid.response import Response

from ...api.utils.reporter import reportError
from ...api.utils.response import responseSuccess, responseError, defaultResponse
from ...database.users import create_user, get_user, update_user, delete_user

def switch_action(type):
    actions = {
        'create': create_user,
        'update': update_user,
        'delete': delete_user,
        'get': get_user,
    }
    return actions.get(type, defaultResponse)

@view_config(route_name='user', renderer='json', request_method='POST')
def user_handler(request):
    action = request.json_body

    if 'type' in action and 'payload' in action:
        actionType = action['type']
        callback = switch_action(actionType)

        try:
            response = callback(action['payload'])
            if 'error' not in response:
                if 'password' in response:
                    response.pop('password', None)
                return responseSuccess(response, actionType)
            else:
                return responseError(response, actionType, 400)

        except Exception as error:
            response = reportError('An error occured handling the user request', error)
            return responseError(response, actionType, 500)

    response = reportError('The user request was not formatted correctly', None)
    return responseError(response, None, 400)
