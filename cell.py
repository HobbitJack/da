from format import CellFormat

class Cell:
    def __init__(self, cellRow: int, cellColumn: int):
        self.position = (cellRow, cellColumn)
        self.content = ""
        self.type = ""
        self.current_display_position=(-1,-1)
        self.merged: bool|Tuple[int, int] = False
        self.cell_format = CellFormat()
    
    def columnLetter(self):
        column_number = self.position[1]
        if column_number == 0:
            return "A"
        digits = []
        while column_number:
            digits.append(int(column_number % 27))
            column_number //= 27
        return "".join(string.ascii_uppercase[digits] for number_letter in digits)

    def __str__(self, use_long: bool):
        if not use_long:
            return f"{self.columnLetter()}{self.position[1]}"