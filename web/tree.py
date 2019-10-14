from collections import deque

class Tree():
    data = []
    out = []

    level = deque()

    def __init__(self, data):
        self.data = data

    def return_choises(self):
        self.out = [(str(0), " - НЕТ - ")]
        if self.data:
            self._make_tree()
        return self.out

    def _make_tree(self, parent_id=0):
        for obj in self.data:
            # how to compare None and 0 (None == 0 = True)?
            if (obj.parent_id == parent_id) or (not obj.parent_id and not parent_id): 
                drawing = ''
                if parent_id:
                    self.level.append( self._last_sibling(obj.id, obj.parent_id) )
                    drawing = self._draw_tree()
                else:
                    self.out.append(('', ''))
                self.out.append((str(obj.id), drawing + obj.name))
                self._make_tree(obj.id)
                if parent_id:
                    self.level.pop()

    def _draw_tree(self):
        out = ''
        last_level_index = len(self.level)-1
        for i in range(last_level_index):
            if self.level[i]:
                out += '. '
            else:
                out += '| '
        if self.level[last_level_index]:
           out += '+--'
        else:
            out += '|--'
        return out

    def _last_sibling(self, id, parent_id):
        last_child = None
        for obj in self.data:
            if obj.parent_id == parent_id:
                last_child = obj.id
        if last_child == id:
            return True
