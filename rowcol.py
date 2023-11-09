import string
import math
import random


class Row:
    def __init__(self, row_number):
        self.height = 1
        self.row_number = row_number


class Column:
    # Procedure
    def __init__(self, column_number: int) -> None:
        self.width = 10
        self.column_number = column_number
        self.column_letter = ""

        column_number += 1
        digits = []
        while column_number > 0:
            digits.append(int(column_number % 26))
            column_number //= 27
        self.column_letter = "".join(
            string.ascii_uppercase[number_letter - 1]
            for number_letter in reversed(digits)
        )
        return

    # Function
    def column_header(self) -> str:
        if len(self.column_letter) < self.width:
            return f"{' ' * (((self.width - len(self.column_letter)) // 2) + ((self.width - len(self.column_letter)) % 2))}{self.column_letter}{' ' * ((self.width - len(self.column_letter)) // 2)}"
        return self.column_letter[0 : self.width]
