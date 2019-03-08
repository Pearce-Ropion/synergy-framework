from uuid import uuid4 as uuidv4

from ...api.utils.reporter import isError, reportError
from .accessor import set_group_name, add_groupie, remove_groupie, get_group_name, get_groupies, delete_grouping, delete_groupies

def create_group(payload):
    group_id = str(uuidv4())

    errors = []
    response = {}

    try:
        result = set_group_name({
            'groupID': group_id,
            'name': payload['name'],
        })

        if isError(result):
            errors.append(result)
        else:
            response = result

    except Exception as error:
        errors.append(reportError(
            'An error occured creating a group with name: {}'.format(payload['name']), error))

    if 'members' in payload and isinstance(payload['members'], list):
        try:
            members = payload['members']
            if len(members) > 0:
                response['members'] = []

            for i in range(len(members)):
                result = add_groupie({
                    'groupID': group_id,
                    'uuid': members[i]['uuid'],
                    'type': members[i]['type'],
                })

                if isError(result):
                    errors.append(result)
                else:
                    response['members'].append(result)

        except Exception as error:
            errors.append(reportError(
                'An error occured adding members to group with name: {}'.format(payload['name']), error))

    if len(errors) > 0:
        return {
            'error': True,
            'errors': errors,
        }

    return response


def get_group(payload):
    errors = []
    response = {}
    channels = []

    try:
        result = get_groupies(payload, channels)

        if isError(result):
            errors.append(result)
        else:
            response['members'] = result

    except Exception as error:
        errors.append(reportError(
            'An error occured retrieving the group members with the specified ID: {}'.format(payload['groupID']), error))

    if len(errors) > 0:
        return {
            'error': True,
            'errors': errors,
        }
    
    return response


def update_group(payload):
    errors = []
    response = {}
    isModified = False

    if 'name' in payload:
        try:
            
            result = set_group_name({
                'groupID': payload['groupID'],
                'name': payload['name'],
            })

            if isError(result):
                errors.append(result)
            else:
                isModified = True
                response = result

        except Exception as error:
            errors.append(reportError(
                'An error occured setting the name of the group with the specified ID: {}'.format(payload['groupID']), error))
    
    if 'add' in payload:
        try:
            members = payload['add']
            if len(members) > 0:
                response['added'] = []

            for i in range(len(members)):
                result = add_groupie({
                    'groupID': payload['groupID'],
                    'uuid': members[i]['uuid'],
                    'type': members[i]['type'],
                })

                if isError(result):
                    errors.append(result)
                else:
                    isModified = True
                    response['added'].append(result)


        except Exception as error:
            errors.append(reportError(
                'An error occured adding new members to the group with the specified ID: {}'.format(payload['groupID']), error))

    if 'remove' in payload:
        try:

            if len(payload['remove']) > 0:
                response['removed'] = []

            for i in range(len(payload['remove'])):
                result = remove_groupie({
                    'groupID': payload['groupID'],
                    'uuid': payload['remove'][i],
                })

                if isError(result):
                    errors.append(result)
                else:
                    isModified = True
                    response['removed'].append(result)

        except Exception as error:
            errors.append(reportError(
                'An error occured removing members from the group with the specified ID: {}'.format(payload['groupID']), error))

    if isModified:
        try:

            result = get_group({
                'groupID': payload['groupID'],
            })

            if isError(result):
                errors.append(result)
            else:
                response = {
                    'result': result,
                    'log': response,
                }
        
        except Exception as error:
            errors.append(reportError(
                'An error occured retreiving the updated group with the specified ID: {}'.format(payload['groupID']), error))

    if len(errors) > 0:
        return {
            'error': True,
            'errors': errors,
        }

    return response


def delete_group(payload):
    errors = []
    response = {}

    try:
        result = delete_grouping(payload)

        if isError(result):
            errors.append(result)
        else:
            response = result

        try:
            result = delete_groupies(payload)

            if isError(result):
                errors.append(result)
            else:
                response = result

        except Exception as error:
            errors.append(reportError(
                'An error occured deleting the group with the specified ID: {}'.format(payload['groupID']), error))

    except Exception as error:
        errors.append(reportError(
            'An error occured deleting the group with the specified ID: {}'.format(payload['groupID']), error))

    if len(errors) > 0:
        return {
            'error': True,
            'errors': errors,
        }

    return response


def all_groups(payload):
    # Payload is empty object
    errors = []
    response = {}

    try:
        result = get_groups(payload)

        if isError(result):
            errors.append(result)
        else:
            response = result

    except Exception as error:
        errors.append(reportError(
            'An error occured deleting the group with the specified ID: {}'.format(payload['groupID']), error))

    if len(errors) > 0:
        return {
            'error': True,
            'errors': errors,
        }

    return response

    
