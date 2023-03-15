class ValueNotExists(Exception):
    def __init__(self, message: str):
        super(ValueNotExists, self).__init__(f"Valor não existente {message}.")
