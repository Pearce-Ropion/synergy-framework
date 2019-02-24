from pyramid.response import Response

from .reporter import reportError

def defaultResponse(*payload):
    return reportError('Invalid action type', None)


def JSONResponse(content, status):
    response = Response(content_type='application/json')
    response.json_body = content
    response.status = status
    return response


def responseSuccess(payload, type):
    response = {
        'type': type,
        'valid': True,
        'payload': payload,
    }
    return JSONResponse(response, 200)


def responseError(errors, type, status):
    response = {
        'type': type,
        'valid': False,
        'errors': errors,
    }
    return JSONResponse(response, status)
