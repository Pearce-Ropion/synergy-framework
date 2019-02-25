def reportError(message, error=''):
    errorMsg = {
        'message': message,
        'error': str(error) if error is not None else None,
    }
    if error is None:
        print(message)
    else:
        print(message, error, sep='\n')
    return errorMsg

def isError(error):
    return 'error' in error
