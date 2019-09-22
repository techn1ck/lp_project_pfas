class ZeroClass():
    """
    Родительский класс для объектов

    Реализует основные методы методы
    - __init__
    - get - получение объекта по id
    - save - сохранение объекта в БД
    - delete - удаление объекта
    - get_list - получение списка объектов для вывода в шаблоне

    Так же через этот класс будет унифицированна работа с историей изменений

    Переменные:
    
    id_value = 0 - id объекта
    id_name = '' - названия поля primary key в таблице
    table_name = '' - название таблицы в БД
    data = {} - словарь - {'название поля в таблице' : 'значение'}
    linked_tables_data = [] - список словарей для реализации связей с другими объектами. СТРУКТУРА НЕ ОКОНЧАТЕЛЬНАЯ
    """

    id_value = 0
    id_name = ''
    table_name = ''
    data = {}
    linked_tables_data = []


    def __init__(self, id_value=0):
        """
        В классах-потомках должны быть переназначены переменные id_name, table_name, data
        Если передан id объекта, загружаю данные из базы
        """
        if not id_name:
            raise ValueError
        
        if not table_name:
            raise ValueError

        if not data:
            raise ValueError
              
        self.id_value = abs(int(value))
        if self.id_value:
            self.get(self.id_value)



    def get(self, id_value=0):
        pass


    def save(self):
        pass


    def delete(self):
        pass


    def get_list(self, params={}):
        pass
