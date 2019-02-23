from pyramid.response import Response

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


def responseError(error, type, status):
    response = {
        'type': type,
        'valid': False,
        'error': error,
    }
    return JSONResponse(response, status)


def reportError(message, error=''):
    errorMsg = {
        'message': message,
        'error': str(error) if error is not None else None,
    }

    print(errorMsg)
    return errorMsg
