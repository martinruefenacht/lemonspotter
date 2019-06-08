class Variable:
    def __init__(self, typeof, name, pointer_level=0):
        self.typeof = typeof
        self.name = name
        self.pointer_level = pointer_level
        
