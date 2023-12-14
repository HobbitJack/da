import cell

class CellRange:
    def __init__(self, first_cell: str, last_cell: str) -> None:
        self.first_cell = first_cell = cell.Cell.parse_pos_from_str(first_cell)
        self.last_cell = cell.Cell.parse_pos_from_str(last_cell)

    @staticmethod
    def parse_from_str(parsestring: str) -> CellRange:
        reached_split = False
        first_cell_str: str = ""
        last_cell_str: str = ""
        for character in parsestring:
            if character == ":":
                reached_split = True
                continue

            if not reached_split:
                first_cell_str += character
            else:
                last_cell_str += character

        return CellRange(first_cell_str, last_cell_str)