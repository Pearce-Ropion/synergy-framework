from pyramid.view import view_config
from pyramid.response import Response

from ...database.usages.usage import usage
from ...api.utils.reporter import reportError
from ...api.utils.response import responseSuccess, responseError, defaultResponse


@view_config(route_name='usage', renderer='json', request_method='POST')
def usage_handler(request):
    payload = request.json_body

    try:
        actionType = 'partial'
        if 'include' not in payload or len(payload['include']) == 0:
             actionType = 'all'

        response = usage(payload)
        if 'error' not in response:
            return responseSuccess(response, actionType)
        else:
            return responseError(response, actionType, 400)

    except Exception as error:
        response = reportError(
            'An error occured handling the usage request', error)
        return responseError(response, actionType, 500)

    response = reportError(
        'The usage request was not formatted correctly', None)
    return responseError(response, None, 400)
