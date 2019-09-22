import ZeroClass
import settings

class User(ZeroClass):

    id_name = 'id_operation'
    table_name = settings.TABLE_PREFIX + 'users'

    data = {
        'id_operation' : 0,
        'id_cat' : 0,
        'id_account' : 0,
        'id_shared_operation' : 0,
        'id_future_operation' : 0,
        'id_parent_operation' : 0,
 
        'name' : '',
        'comment' : '',
 
        'has_child' : 0,
        'was_modified' : 0,
        'is_actual' : 1,
    }

    linked_tables_data = [
        {
            'table_name' : settings.TABLE_PREFIX + 'operation_tag',
            'data' : [],
        },
    ]


