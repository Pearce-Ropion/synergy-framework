from pyramid.view import view_config
from pyramid.response import Response

from ..api.utils.reporter import reportError
from ..api.utils.response import responseSuccess, responseError, defaultResponse
from ..database.users import get_user


@view_config(route_name='login', renderer='json', request_method='POST')
def login_handler(request):
    action = request.json_body

    if 'type' in action and 'payload' in action:
        actionType = action['type']
        if actionType == 'login':

            try:
                response = get_user(action['payload'], False, True)
                print(response)
                if 'error' not in response:
                    return responseSuccess(response, actionType)
                else:
                    return responseError(response, actionType, 400)

            except Exception as error:
                response = reportError(
                    'An error occured handling the user request', error)
                return responseError(response, actionType, 500)

    response = reportError(
        'The login request was not formatted correctly', None)
    return responseError(response, None, 400)
