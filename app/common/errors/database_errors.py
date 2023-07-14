class ItemNotFoundError(Exception):
    """An item not found Error Exception"""

    def __init__(self, message, table, key, value):
        super().__init__()
        self.message = message
        self.table = table
        self.key = key
        self.value = value

    def __str__(self):
        return f"ERROR: {self.message}. Item: Key {self.key}=={self.value} in table {self.table}."
