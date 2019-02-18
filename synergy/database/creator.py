from uuid import uuid4 as uuidv4
from database import set_group_name, add_groupie

def create_group(name, *ids):
    group_id = str(uuidv4())

    try:
        set_group_name(group_id, name)

        try:
            for i in range(len(ids)):
                add_groupie(group_id, ids[i])

        except Exception as error:
            print(''' Unable to add member groups to group: %s ''' % (name))
            print(error)

    except Exception as error:
        print(''' Unable to add group with name: %s ''' % (name))
        print(error)
