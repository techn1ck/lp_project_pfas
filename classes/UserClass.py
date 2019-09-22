import ZeroClass
import settings

class User(ZeroClass):

    id_name = 'id_user'
    table_name = settings.TABLE_PREFIX + 'users'

    data = {
        'id_user' : '',
        'name' : '',
        'surname' : '',
        'phone' : 0,
        'email' : '',
        'role' : 'user',
        
        'was_modified' : 0,
        'is_actual' : 1,
    }

    linked_tables_data = [
        {
            'table_name' : settings.TABLE_PREFIX + 'shared_acc_user',
            'data' : [],
        },
    ]


