from pyramid.view import view_config
from pyramid.response import Response

from ...database.members import get_members
from ...api.utils.reporter import reportError
from ...api.utils.response import responseSuccess, responseError, defaultResponse


@view_config(route_name='members', renderer='json', request_method='POST')
def usage_handler(request):
    payload = request.json_body
    actionType = 'members'

    try:
        if 'members' not in payload or len(payload['members']) == 0:
            return responseSuccess([], actionType)

        accumulator = {
            'groups': [],
            'devices': [],
            'channels': [],
            'allChannels': [],
        }

        response = get_members(payload['members'], accumulator)
        if 'error' not in response:
            return responseSuccess(response, actionType)
        else:
            return responseError(response, actionType, 400)

    except Exception as error:
        response = reportError(
            'An error occured handling the members request', error)
        return responseError(response, actionType, 500)

    response = reportError(
        'The members request was not formatted correctly', None)
    return responseError(response, None, 400)
