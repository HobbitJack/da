import random
import time
import os
import typing

import mpmath
from spreadsheet import Spreadsheet
from cell import Cell


class App:
    # Function
    def __init__(self):
        self.functions = self.read_functions()
        self.spreadsheet = Spreadsheet(100, 100, self.functions)
        #               (column, row)
        self.top_left_cell = (0, 0)
        self.current_cell = (2, 5)
        self.context = "Nav"

    def read_functions(self) -> dict[str, tuple[int, typing.Callable, str]]:
        functions = {}
        modules = []
        with open("config.txt", encoding="UTF-8") as file:
            for line in file:
                if line.startswith("- "):
                    modules.append(line.strip("- "))
                if line.startswith('"'):
                    functions[line.split(" || ")[0].strip('"')] = eval(
                        line.split(" || ")[1]
                    )
        return functions

    # Function
    def get_display_cell_rows(self) -> int:
        terminal_rows = os.get_terminal_size().lines
        # 5 rows for formula bar, help bar, column headers, first cell boundary row, context hotkey bar,
        text_rows = 7
        display_cell_rows = 0
        while (current_row := (display_cell_rows + self.top_left_cell[1])) < (
            len(self.spreadsheet.rows)
        ) and text_rows < terminal_rows:
            remaining_rows = terminal_rows - text_rows
            if self.spreadsheet.rows[current_row].height < remaining_rows:
                text_rows += self.spreadsheet.rows[current_row].height + 1
                display_cell_rows += 1
            else:
                break
        return display_cell_rows

    # Function
    def get_display_cell_columns(self) -> int:
        terminal_columns = os.get_terminal_size().columns
        # 4 columns for row numbers and first cell boundary row
        text_columns = 4
        display_cell_columns = 0
        while (current_column := (display_cell_columns + self.top_left_cell[0])) < (
            len(self.spreadsheet.columns)
        ) and text_columns < terminal_columns:
            remaining_columns = terminal_columns - text_columns
            if self.spreadsheet.columns[current_column].width < remaining_columns:
                text_columns += self.spreadsheet.columns[current_column].width + 1
                display_cell_columns += 1
            else:
                break
        return display_cell_columns

    # Procedure
    def display_UI(self) -> None:
        display_string = "\n\n   |"
        display_string += self.generate_spreadsheet()
        display_string += self.generate_shortcut_bar()
        print(display_string, end="", sep="")

    # Function
    def generate_spreadsheet(self) -> str:
        spreadsheet_string = ""
        display_cell_columns = self.get_display_cell_columns()
        display_cell_rows = self.get_display_cell_rows()

        spreadsheet_string += self.generate_columns_header(display_cell_columns)

        for row in range(display_cell_rows):
            spreadsheet_string += self.generate_cell_row(
                self.top_left_cell[1] + row, display_cell_columns
            )
            spreadsheet_string += (
                self.generate_row_boundary(row + 1, display_cell_columns) + "\n"
            )

        return spreadsheet_string

    # Function
    def generate_columns_header(self, display_cell_columns: int) -> str:
        header_string = ""
        for column in self.spreadsheet.columns[
            self.top_left_cell[1] : self.top_left_cell[1] + display_cell_columns
        ]:
            header_string += f"{column.column_header()}|"

        header_string += f"\n{self.generate_row_boundary(0, display_cell_columns)}\n"

        return header_string

    # Function
    def generate_cell_row(self, row_number: int, display_columns: int) -> str:
        row_text = ""
        row_height = self.spreadsheet.rows[row_number].height

        for cell_text_row in range(row_height):
            if cell_text_row == row_height - (mpmath.math2.ceil(row_height / 2)):
                row_text += f"{str(row_number + 1)[-3:]:3}"
            else:
                row_text += "   "

            row_text += self.get_horizontal_cell_boundary(0, row_number)

            for text_column, cell in enumerate(
                self.spreadsheet.generate_1D_cell_range(
                    (self.top_left_cell[0], row_number), display_columns
                )
            ):
                self.spreadsheet.evaluate_cell(cell)
                self.generate_cell_content(cell)
                if cell.master == cell:
                    row_text += cell.content[cell_text_row]
                row_text += self.get_horizontal_cell_boundary(
                    text_column + 1, row_number
                )

            row_text += "\n"

        return row_text

    # Function
    def get_horizontal_cell_boundary(self, columns: int, row_number: int) -> str:
        columns += self.top_left_cell[0]
        current_cell = self.spreadsheet.cells[columns, row_number]
        previous_cell = self.spreadsheet.get_adjacent_cell(current_cell, "left")

        if previous_cell:
            if current_cell in previous_cell.master.slaves:
                return ""

            if previous_cell.master.cell_format.borders["right"]:
                return "|"

            elif current_cell.master.cell_format.borders["left"]:
                return "|"

            return " "
        else:
            if current_cell.master.cell_format.borders["left"]:
                return "|"
            return " "

    # Function
    def generate_row_boundary(self, boundary_number: int, display_columns: int) -> str:
        boundary_string = "---+"
        row = self.top_left_cell[1] + boundary_number

        for column_to_display in range(
            self.top_left_cell[0], self.top_left_cell[0] + display_columns
        ):
            if (
                row >= 1
                and self.spreadsheet.cells[
                    (column_to_display, row - 1)
                ].master.cell_format.borders["down"]
                and self.spreadsheet.cells[(column_to_display, row)]
                not in self.spreadsheet.cells[
                    (column_to_display, row - 1)
                ].master.slaves
            ):
                boundary_string += (
                    "-" * self.spreadsheet.columns[column_to_display].width
                )
            elif self.spreadsheet.cells[
                (column_to_display, row)
            ].master.cell_format.borders["up"] and (
                (
                    self.spreadsheet.cells[(column_to_display, row - 1)]
                    not in self.spreadsheet.cells[
                        (column_to_display, row)
                    ].master.slaves
                )
                if row >= 1
                else True
            ):
                boundary_string += (
                    "-" * self.spreadsheet.columns[column_to_display].width
                )
            else:
                boundary_string += (
                    " " * self.spreadsheet.columns[column_to_display].width
                )
            boundary_string += "+"

        return boundary_string

    # Function
    def generate_shortcut_bar(self) -> str:
        context_shortcuts = []
        if self.context == "Nav":
            context_shortcuts = [
                "M-C: Give Spreadsheet Command",
                "Up/Down/Left/Right: Go Up/Down/Left/Right",
                "Ret: Edit Cell",
                "M-^Right/^Left: Increase/Decrease Column Width",
                "M-^Down/^Up: Increase/Decrease Row Height",
                "Shift+Up/Down/Left/Right: Highlight Cells",
                "^B: Apply Cell Borders",
            ]

        main_shortcuts = [
            "^D: Exit",
            "^S: Save",
            "^Q: Suspend",
            "^Z: Undo Last Action",
            "^Y: Redo Last Action",
        ]

        context_shortcuts_string = ""

        for shortcut in context_shortcuts:
            if (
                len(context_shortcuts_string) + 3 + len(shortcut)
                <= os.get_terminal_size().columns
            ):
                context_shortcuts_string += f"{shortcut} | "
            else:
                break
        context_shortcuts_string = context_shortcuts_string[:-3] + "\n"

        main_shortcuts_string = ""

        for shortcut in main_shortcuts:
            if (
                len(main_shortcuts_string) + 3 + len(shortcut)
                <= os.get_terminal_size().columns
            ):
                main_shortcuts_string += f"{shortcut} | "
            else:
                break
        main_shortcuts_string = main_shortcuts_string[:-3]

        return f"{context_shortcuts_string}{main_shortcuts_string}\n"

    # Procedure
    def generate_cell_content(self, cell: Cell) -> None:
        if cell.master is not cell:
            return
        self.spreadsheet.set_cell_size(cell)
        cell_width = cell.width
        cell_height = cell.height
        total_characters = cell_width * cell_height

        if isinstance(cell.value, mpmath.mpf) or isinstance(cell.value, int):
            value_string = (
                f"{' ' * (total_characters - len(str(cell.value)))}{cell.value}"
            )
        elif isinstance(cell.value, mpmath.mpc):
            if mpmath.re(cell.value) == 0:
                if total_characters >= len(f"{str(mpmath.im(cell.value))}i"):
                    value_string = f"{' ' * (total_characters - 1 - len(str(mpmath.im(cell.value))))}{mpmath.im(cell.value)}i"
                else:
                    value_string = f"{' ' * (1 if total_characters % 2 == 1 else 0)}{'' if mpmath.im(cell.value) >= 0 else '-'}{str(abs(mpmath.im(cell.value)))[0:(total_characters - (1 if mpmath.im(cell.value) >= 0 else 2))]}i"
            else:
                if total_characters >= len(str(cell.value)):
                    value_string = (
                        f"{' ' * (total_characters - len(str(cell.value)))}{cell.value}"
                    )
                else:
                    value_string = f"{' ' * (1 if total_characters % 2 == 1 and mpmath.re(cell.value) > 0 else 0)}{str(mpmath.re(cell.value))[0:(total_characters-2)//2 + (1 if mpmath.re(cell.value) < 0 else 0)]}{'+' if mpmath.im(cell.value) >= 0 else '-'}{str(abs(mpmath.im(cell.value)))[0:(total_characters-2)//2]}i"
        else:
            value_string = str(cell.value)

        cell_text_rows = ["" for i in range(cell_height)]

        if len(value_string) >= total_characters:
            for index, row in enumerate(cell_text_rows):
                cell_text_rows[index] = value_string[
                    cell_width * index : (cell_width * (index + 1))
                ]
            cell.content = cell_text_rows
        else:
            for i in range(total_characters):
                cell_text_rows[mpmath.math2.floor(i / cell_width)] += (
                    value_string[i] if i < len(value_string) else " "
                )

        # Text Centering
        if isinstance(cell.value, str):
            cell.content = [
                f"{' ' * ((cell_width - len(row.strip())) // 2 + ((cell_width - len(row.strip())) % 2))}{row.strip()}{' ' * ((cell_width - len(row.strip())) // 2)}"
                if len(cell.value) <= cell_width
                else row
                for row in cell_text_rows
            ]
            return

        cell.content = cell_text_rows


def setContent():
    app.spreadsheet.cells[(1, 1)].formula = "Quicklook Data"
    app.spreadsheet.cells[(1, 2)].formula = "Year"
    app.spreadsheet.cells[(2, 2)].formula = "ObsID"
    app.spreadsheet.cells[(3, 2)].formula = "FPMA Flux"
    app.spreadsheet.cells[(4, 2)].formula = "FPMB Flux"
    app.spreadsheet.cells[(5, 2)].formula = "Avg. Flux"
    app.spreadsheet.cells[(6, 2)].formula = "Ka Norm"
    app.spreadsheet.cells[(1, 3)].formula = "2012"
    app.spreadsheet.cells[(1, 4)].formula = "2012"
    app.spreadsheet.cells[(1, 5)].formula = "2012"
    app.spreadsheet.cells[(1, 6)].formula = "2016"
    app.spreadsheet.cells[(1, 7)].formula = "2020"
    app.spreadsheet.cells[(1, 8)].formula = "2022"
    app.spreadsheet.cells[(8, 1)].formula = "Henlo"
    app.spreadsheet.cells[(7, 9)].formula = "-arcsin(2)="
    app.spreadsheet.cells[(7, 10)].formula = "=-ASIN(2)"

    for key in app.spreadsheet.cells[(1, 1)].cell_format.borders.keys():
        app.spreadsheet.cells[(1, 1)].cell_format.borders[key] = "True"

    app.spreadsheet.columns[7].width = 11

    app.spreadsheet.merge_cells(
        app.spreadsheet.cells[(1, 1)], app.spreadsheet.generate_1D_cell_range((1, 1), 6)
    )


if __name__ == "__main__":
    app = App()
    i = 1
    while i:
        # app.spreadsheet.columns[random.randint(1,26)].width=random.randint(1,20)
        # app.spreadsheet.rows[random.randint(1,30)].height=random.randint(1,4)
        setContent()

        app.display_UI()
        time.sleep(1)
        # os.system("clear")
        i -= 1

test = """
E3|=C3-BCorr(D3|
BCorr(Background) | Apply correction to background for subtraction fr-
   | B  |   C  |    D     |     E     |   F   |    G   |    H   |
---+----+------+----------+-----------+       +        +        +
1  |          Flux by Year            |                 Table-->|        
---+----+------+----------+-----------+       +        +        +
2  |Year  Flux  Background Unobs. Flux|[CHART] Too muc-         |
---+    +      +          +           +       +        +        +
3  |2012 4.5678    0.23759 ///////////|                                   
---+    +      +          +           +       +        +        +
4  |2016 5.1637    0.23919            |                         
---+    +      +          +           +       +--------+--------+
5  |2020 6.2374    0.24341            |       |  Model is good? |
---+    +      +          +           +       +--------+--------+
6  |2022 7.1234    0.24512            |       | chi^2    Good?  |
---+----+------+----------+-----------+       +        +        +
7                                             |142.5654    No.  |
---+    +      +          +           +       +--------+--------+
8  |<- T                                                            
   |able
---+    +      +          +           +       +        +        +
                           This is a l                       
9                          arge cell w 
                           ith room!
---+    +      +          +           +       +        +        +
Ret: Input | ^Ret: Fill Down | M-Ret: Copy Down 
^D: Exit | ^S: Save | ^X: Suspend
----------------------------------------------------------------------

CHART(Title,Type,XSeries,[YSeries1,YSeries2,YSeries3,...YSeriesN])
CHART(A1,ScatterXY,BlockByCol(A2:D6))
Various       Flux by Year
  8|
7.5|
  7|                       @
6.5|
  6|                   @
5.5|                               LEGEND
  5|           @                   x: Flux
4.5|   @                           o: Background
  4|                               @: Unobs. Flux
3.5|
  3|
2.5|
  2|
1.5|
  1|
0.5|
  0+---o---+---o---+---o---o---+---
    2012    2016    2020    2024
                Year
Ret: Return to sheet | ^S: Save chart as bitmap | M^S: Save chart as text
    """
# print(test)
