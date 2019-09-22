import ZeroClass
import settings

class User(ZeroClass):

    id_name = 'id_tag'
    table_name = settings.TABLE_PREFIX + 'tag'

    data = {
        'id_tag' : 0,
        'id_user' : 0,
        'name' : '',
        
        'was_modified' : 0,
        'is_actual' : 1,
    }

    linked_tables_data = [
        {
            'table_name' : settings.TABLE_PREFIX + 'bot_template_tag',
            'data' : [],
        },
    ]

