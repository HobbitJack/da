from rowcol import Row, Column
from cell import Cell

import math
import string

class Spreadsheet:
    def __init__(self, total_rows: int, total_columns: int):
        self.cells = {(row,column):Cell(row, column) for row in range(total_rows) for column in range(total_columns)}
        self.content_cells: dict[tuple, Cell] = {}
        self.rows = [Row(row) for row in range(total_rows)]
        self.columns = [Column(column) for column in range(total_columns)]

