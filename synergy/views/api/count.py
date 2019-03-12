from pyramid.view import view_config
from pyramid.response import Response

from ...database.members import get_count
from ...api.utils.response import responseSuccess, responseError, defaultResponse
from ...api.utils.reporter import reportError


def switch_action(type):
    options = ['all', 'groups', 'devices', 'channels']
    if type in options:
        return get_count

    return defaultResponse

@view_config(route_name='count', renderer='json', request_method='POST')
def count_handler(request):
    action = request.json_body

    if 'type' in action:
        actionType = action['type']
        callback = switch_action(actionType)

        if actionType == 'all':
            payload = {
                'groups': True,
                'devices': True,
                'channels': True,
            }

        else:
            payload = {
                actionType: True,
            }

        try:
            response = callback(payload)
            if 'error' not in response:
                return responseSuccess(response, actionType)
            else:
               return responseError(response['errors'], actionType, 400)
 
        except Exception as error:
            response = reportError('An error occured handing the count request', error)
            return responseError(response, actionType, 500)

    response = reportError('The count request was not formated correctly', None)
    return responseError(response, None, 400)    
    

