import string
import math
import random

class Row:
    def __init__(self, row_number):
        self.height = 1
        self.row_number = row_number

class Column:
    def __init__(self, column_number):
        self.width = 6
        self.column_number = column_number

        column_number += 1 
        digits = []
        while column_number > 0:
            digits.append(int(column_number % 26))
            column_number //= 27
        self.column_letter = "".join(string.ascii_uppercase[number_letter-1] for number_letter in reversed(digits))

    def column_header(self):
        if len(self.column_letter) <= self.width: 
            if self.width % 2 == len(self.column_letter) % 2: 
                return f"{' '*(math.floor((self.width-len(self.column_letter)))//2)}{self.column_letter}{' '*(math.floor((self.width-len(self.column_letter)))//2)}"
            else:
                return f"{' '*(math.floor((self.width-len(self.column_letter)))//2+1)}{self.column_letter}{' '*(math.floor((self.width-len(self.column_letter)))//2)}"
        else:
            return self.column_letter[0:self.width]