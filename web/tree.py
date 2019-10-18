from collections import deque

class Tree():
    """ Класс для построения деревьев
        На вход кладем список объектов с обязательными полями id, parent_id, name

        На выходе получаем отсортированный список с подготовленными для вывода элементами
            [
                {
                    "obj": self.data[i], # объект
                    "left_tag": "", # html-код для отображения слева от строки
                    "right_tag": "", # html-код для отображения справа от строки
                    "level_value": 1, # уровень вложенности,
                    "level": [], # уровень вложенности,
                    "first_child": False, # первый дочерний элемент в ветке
                    "last_child": False, # последний дочерний элемент в ветке
                    "choices_tree_drawing": рисунок для selecta
                },
            ]
    """
    data = []
    tree = []

    _level = deque()

    def __init__(self, data):
        """ Заполняем и сортируем список словарей self.tree:
        """
        self.data = data
        if self.data and isinstance(self.data, list):
            if hasattr(self.data[0], "id") and hasattr(self.data[0], "parent_id"):
                self._make_tree()
            else:
                raise AttributeError("В объектах списка отсутствуют поля ID или PARENT_ID")

    def return_choises(self):
        """ Возвращаем список элементов для form.{name}.choices 
            для использования в селекте.
            С пустыми строками между элементами первого уровня
        """
        out = [('', " - НЕТ - ")]
        if self.tree:
            for row in self.tree:
                if not row['level_len']:
                    out.append(('', ''))
                out.append((str(row['obj'].id), row['choices_tree_drawing'] + row['obj'].name))
        return out

    def return_tree(self):
        """ Возвращаем отсортированный список
        """
        return self.tree

    def _make_tree(self, parent_id=0):
        has_child_flag = False
        for obj in self.data:
            # how to compare None and 0 (None == 0 = True)?
            if (obj.parent_id == parent_id) or (not obj.parent_id and not parent_id):
                has_child_flag = True
                first_child = False 
                last_child = False
                left_tag = "<li>"
                right_tag = "</li>"

                if parent_id:
                    first_child, last_child = self._siblings(obj.id, obj.parent_id)
                    self._level.append( last_child )
                
                if first_child:
                    left_tag = "<ul><li>"
                if last_child:
                    right_tag = "</li></ul>"

                self.tree.append({
                    "obj": obj,
                    "id": obj.id,
                    "left_tag": left_tag,
                    "right_tag": right_tag,
                    "first_child": first_child,
                    "last_child": last_child,
                    "level": self._level,
                    "level_len": len(self._level),
                    "choices_tree_drawing": self._draw_tree(),
                })
                self._make_tree(parent_id=obj.id)
                if parent_id:
                    self._level.pop()

    def _draw_tree(self):
        out = ''
        last_level_index = len(self._level)-1
        if last_level_index >= 0:
            for i in range(last_level_index):
                if self._level[i]:
                    out += '. '
                else:
                    out += '| '
            if self._level[last_level_index]:
                out += '+--'
            else:
                out += '|--'
        return out

    def _siblings(self, id, parent_id):
        first_child = None
        last_child = None
        first_child_flag = False
        last_child_flag = False
        for obj in self.data:
            if obj.parent_id == parent_id:
                if not first_child:
                    first_child = obj.id
                last_child = obj.id
        if first_child == id:
            first_child_flag = True
        if last_child == id:
            last_child_flag = True
        return first_child_flag, last_child_flag
