from pyramid.view import view_config
from pyramid.response import Response
from ...api.utils.generateJSONResponse import generateJSONResponse

def switch_action(type):
    actions = {
        'create': 'create1',
        'update': 'update1',
        'delete': 'delete1',
    }
    return actions.get(type, 'default1')

@view_config(route_name='user', renderer='json', request_method='POST')
def user_handler(request):
    action = request.json_body
    if 'type' in action and 'payload' in action:
        x = switch_action(action['type'])
        print(x)
        status = 200
    else:
        status = 400
    return generateJSONResponse('OK', status)
