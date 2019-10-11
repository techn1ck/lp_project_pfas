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
            self.make_tree()
        return self.out

    def make_tree(self, parent_id=0):
        for obj in self.data:
            # how to compare None and 0 (None == 0 = True)?
            if (obj.parent_id == parent_id) or (not obj.parent_id and not parent_id): 
                drawing = ''
                if parent_id:
                    self.level.append( self.last_sibling(obj.id, obj.parent_id) )
                    drawing = self.draw_tree()
                else:
                    self.out.append(('', ''))
                self.out.append((str(obj.id), drawing + obj.name))
                self.make_tree(obj.id)
                if parent_id:
                    self.level.pop()

    def draw_tree(self):
        out = ''
        l = len(self.level)
        for i, x in enumerate(self.level):
            if x and i == l-1: # last child last level
                out += '+--'
            elif not x and i == l-1: # not last child last level
                out += '|--'
            elif x:
                out += '. '
            elif not x:
                out += '| '
        return out
        
    def last_sibling(self, id, parent_id):
        last_child = 0
        for obj in self.data:
            if obj.parent_id == parent_id:
                last_child = obj.id
        if last_child == id:
            return True
