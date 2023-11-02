import os
from spreadsheet import Spreadsheet

class App:
    def __init__(self):
        self.spreadsheet = Spreadsheet(10,2000)
        #               (row, column)
        self.top_left_cell=(0,0)
        self.current_cell=(0,0)

    def displaySpreadsheet(self):
        terminal_rows = os.get_terminal_size().lines
        terminal_columns = os.get_terminal_size().columns

        display_cell_columns = 0
        # 5 columns for row numbers and first cell boundary column
        total_columns = 5

        display_cell_rows = 0
        # 4 rows for formula bar, help bar, hotkey bar, first cell boundary row, and 1 more
        total_rows=5

        while display_cell_columns  + self.top_left_cell[1] + 1 < (len(self.spreadsheet.columns)) and total_columns < terminal_columns:

            if self.spreadsheet.columns[display_cell_columns+self.top_left_cell[1]].width <  terminal_columns - total_columns:
                total_columns += self.spreadsheet.columns[display_cell_columns+self.top_left_cell[1]].width + 1
                display_cell_columns += 1
            else: 
                break

        while display_cell_rows < len(self.spreadsheet.rows) and total_rows < terminal_rows:
            if self.spreadsheet.rows[display_cell_rows+self.top_left_cell[0]].height + 1<  terminal_rows - total_rows:
                total_rows += self.spreadsheet.rows[display_cell_rows+self.top_left_cell[0]].height + 1
                display_cell_rows += 1
            else:
                break
        
        display_string = "\n\n   ||"

        for column in self.spreadsheet.columns[self.top_left_cell[1]:self.top_left_cell[1]+display_cell_columns]:
            display_string += f"{column.column_header()}|"

        print(display_string)
        
if __name__=='__main__':
    app=App()
    app.displaySpreadsheet()
    exit

test='''
D3|=B3-BCorr(C3|
BCorr(Background) | Apply correction to background for subtraction fr-
   || A  |   B  |    C     |     D     |   E   |    F   |    G   |
---|+----+------+----------+-----------+       +        +        +
1  ||             Flux by Year         |                 Table-->|        
---|+----+------+----------+-----------+       +        +        +
2  ||Year  Flux  Background Unobs. Flux|[CHART] Too muc-         |
---|+    +      +          +           +       +        +        +
3  ||2012 4.5678    0.23759 ///////////|        This is          
---|+    +      +          +           +       +a merged+        +
4  ||2016 5.1637    0.23919            |         cell.        
---|+    +      +          +           +       +--------+--------+
5  ||2020 6.2374    0.24341            |       |  Model is good? |
---|+    +      +          +           +       +--------+--------+
6  ||2022 7.1234    0.24512            |       | chi^2    Good?  |
---|+----+------+----------+-----------+       +        +        +
7  |                                           |142.5654    No.  |
---|+    +      +          +           +       +--------+--------+
8  ||<- T                                                            
   ||able
---|+    +      +          +           +       +        +        +
   |                        This is a l                       
9  |                        arge cell w 
   |                        ith room!
---|+    +      +          +           +       +        +        +
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
    '''
#print(test)