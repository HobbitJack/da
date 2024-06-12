from rowcol import Row, Column
from cell import Cell

import mpmath
import daos
import string
from cell import Cell


class Spreadsheet:
    # Procedure
    def __init__(
        self,
        total_rows: int,
        total_columns: int,
        functions: dict[str, tuple[int, callable, str]],
    ) -> None:
        self.cells = {
            (column, row): Cell(column, row)
            for row in range(total_rows)
            for column in range(total_columns)
        }
        self.content_cells: dict[tuple, str] = {}
        self.rows = [Row(row) for row in range(total_rows)]
        self.columns = [Column(column) for column in range(total_columns)]
        self.daos_instance = daos.DAOS(functions)
        return

    # Procedure
    def evaluate_cell(self, cell: Cell) -> None:
        if cell.master is not cell:
            self.evaluate_cell(cell.master)
            cell.value = cell.master.value
            return

        if cell.formula.startswith("'") or cell.formula.startswith('"'):
            cell.value = cell.formula[1:]
            return

        if not cell.formula.startswith("="):
            try:
                cell.value = int(cell.formula)
                return
            except ValueError:
                try:
                    cell.value = mpmath.mpf(cell.formula)
                    return
                except ValueError:
                    cell.value = cell.formula
                    return

        else:
            try:
                self.daos_instance.reinit()
                self.daos_instance.evaluate_expression(cell.formula)
                cell.value = self.daos_instance.item_stack[-1]

                if (
                    isinstance(cell.value, mpmath.mpc)
                    and mpmath.re(cell.value) != 0
                    and mpmath.im(cell.value) == 0
                ):
                    cell.value = mpmath.re(cell.value)

                if isinstance(cell.value, mpmath.mpf) and (
                    int(cell.value) == cell.value
                ):
                    cell.value = int(self.daos_instance.item_stack[-1])

            except (KeyError, ArithmeticError, IndexError, ValueError) as e:
                cell.value = "##ERROR"


    # Function
    def generate_1D_cell_range(
        self,
        starting_position: tuple[int, int],
        number_of_cells: int,
        vertical=False,
        backwards=False,
    ) -> list[Cell]:
        return [
            self.cells[
                (
                    starting_position[0]
                    + ((i * 1 if not backwards else -1) if not vertical else 0),
                    starting_position[1]
                    + ((i * 1 if not backwards else -1) * vertical),
                )
            ]
            for i in range(number_of_cells)
        ]

    # Procedure
    def merge_cells(self, master: Cell, slaves: list[Cell]) -> None:
        master.slaves = slaves
        if master not in master.slaves:
            master.slaves.append(master)
        for slave in slaves:
            slave.master = master
        return

    # Procedure
    def set_cell_size(self, cell: Cell) -> None:
        all_columns = {cell.position[0] for cell in cell.slaves}
        all_rows = {cell.position[1] for cell in cell.slaves}
        cell.width = (
            sum((self.columns[column].width for column in all_columns))
            + len(all_columns)
            - 1
        )
        cell.height = (
            sum((self.rows[row].height for row in all_rows)) + len(all_rows) - 1
        )

    # Function
    def get_adjacent_cell(self, cell: Cell, direction: str) -> Cell | None:
        if direction == "up":
            if cell.position[1] == 0:
                return None
            return self.cells[cell.position[0], cell.position[1] - 1]

        if direction == "down":
            if cell.position[1] == len(self.rows) - 1:
                return None
            return self.cells[cell.position[0], cell.position[1] + 1]

        if direction == "left":
            if cell.position[0] == 0:
                return None
            return self.cells[cell.position[0] - 1, cell.position[1]]

        if direction == "right":
            if cell.position[0] == len(self.columns) - 1:
                return None
            return self.cells[cell.position[0] + 1, cell.position[1]]

        return None
