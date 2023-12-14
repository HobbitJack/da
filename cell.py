import math
import string
from cellformat import CellFormat
from typing import Any


class Cell:
    # Procedure
    def __init__(self, cell_column: int, cell_row: int) -> None:
        self.position = (cell_column, cell_row)
        self.content: list[str] = [""]
        self.formula = ""
        self.value: Any = ""
        self.type = ""
        self.slaves: list[Cell] = [self]
        self.master = self
        self.cell_format = CellFormat()
        self.width = 10
        self.height = 1

    # Function
    def columnLetter(self):
        column_number = self.position[0]
        if column_number == 0:
            return "A"
        digits = []
        while column_number:
            digits.append(int(column_number % 27))
            column_number //= 27
        return "".join(
            (string.ascii_uppercase[number_letter] for number_letter in digits)
        )

    # Function
    def __str__(self, use_long: bool = False):
        if not use_long:
            return f"{self.columnLetter()}{self.position[1] + 1}"
    
    #Function
    @staticmethod
    def parse_pos_from_str(parsestring: str) -> tuple[int, int]:
        parsestring = parsestring.upper()
        column_letter = ""
        row_number = ""
        char_index = 0
        while parsestring[char_index] in string.ascii_uppercase:
            column_letter += parsestring[char_index]

        column_number = 0
        for index, character in enumerate(column_letter):
            column_number += (len(column_letter) - index) * string.ascii_uppercase.index(character)
        return tuple[column_number + 1, row_number]