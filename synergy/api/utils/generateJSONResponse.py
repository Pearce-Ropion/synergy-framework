from pyramid.response import Response

def generateJSONResponse(content, status, message = ''):
    response = Response(content_type='application/json')
    response.json_body = content
    response.status_code = status
    if status > 400:
        response.status = message
    return response
