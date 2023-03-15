class ValueNotExists(Exception):
    def __init__(self):
        super(ValueNotExists, self).__init__("Valor não existente na em gramáticas.")
