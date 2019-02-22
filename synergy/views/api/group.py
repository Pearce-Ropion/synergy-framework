from pyramid.view import view_config
from pyramid.response import Response
import json

@view_config(route_name='group', renderer='json', request_method='POST')
def login_handler(request):
    response = Response(content_type='application/json')
    response.json_body = json.dumps(request.json_body)
    return response
