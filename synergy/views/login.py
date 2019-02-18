from pyramid.view import view_config
from pyramid.response import Response

@view_config(route_name='login', renderer='json', request_method='POST')
def login_handler(request):
    response = Response(content_type='application/json')
    response.json_body = request.json_body
    return response
