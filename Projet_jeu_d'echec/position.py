

class Position:

    def __init__(self, column, row):
        self._column = column
        self._row = row

    @property
    def column(self):
        return self._column

    @column.setter
    def column(self, value):
        self._column = value

    @property
    def row(self):
        return self._row

    @row.setter
    def row(self, value):
        self._row = value


    def col_index(self):
        return ord(self._column) - ord('a')


    def row_index(self):
        return self._row - 1


    def __str__(self):
        return f"{self._column}{self._row}"


    def __eq__(self, other):
        if not isinstance(other, Position):
            return False
        return self._column == other._column and self._row == other._row

    def __repr__(self):
        return f"Position('{self._column}', {self._row})"


    @staticmethod
    def from_indices(col_idx, row_idx):
        return Position(chr(ord('a') + col_idx), row_idx + 1)


    @staticmethod
    def is_valid_indices(col_idx, row_idx):
        return 0 <= col_idx <= 7 and 0 <= row_idx <= 7

