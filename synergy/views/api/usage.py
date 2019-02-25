from pyramid.view import view_config
from pyramid.response import Response

from ...api.utils.reporter import reportError
from ...api.utils.response import responseSuccess, responseError, defaultResponse


@view_config(route_name='usage', renderer='json', request_method='POST')
def usage_handler(request):
    action = request.json_body

    if 'type' in action and 'payload' in action:
        pass
        # Before (should be larger than After)
        # After (should be smaller than Before)
        # UUIDS (type) -> Get all UUIDs associated with this ID
        #  # If Group, get group members 
             # member is device, get all channels
           # If device, get all channels
        # 
        # Boolean
        # 
        #
        # actionType = action['type']
        # callback = switch_action(actionType)

        # try:
        #     response = callback(action['payload'])
        #     if 'error' not in response:
        #         return responseSuccess(response, actionType)
        #     else:
        #         return responseError(response, actionType, 400)

        # except Exception as error:
        #     response = reportError(
        #         'An error occured handling the usage request', error)
        #     return responseError(response, actionType, 500)

    response = reportError(
        'The usage request was not formatted correctly', None)
    return responseError(response, None, 400)
