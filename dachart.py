import typing
import os

class daChart:
    def __init__(self, x_data: dict[str: list[typing.SupportsInt | typing.SupportsFloat]], y_data: dict[str: list[typing.SupportsInt | typing.SupportsFloat]], chart_type: str, title="Chart", x_axis_title="X", y_axis_title="Y", use_legend=True) -> None:
        self.x_data = x_data
        self.y_data = y_data
        if len(x_data) != len(y_data) and len(x_data) != 1:
            print
            raise 
        self.chart_type = chart_type
        self.title = title
        self.x_axis_title = x_axis_title
        self.y_axis_title = y_axis_title
        self.use_legend = use_legend
        self.scaling = "linear" #Or "logarithmic"

    # Function
    def get_terminal_size(self) -> tuple[int, int]:
        return (os.get_terminal_size().lines, os.get_terminal_size().columns)
    
    def display_chart(self):
        self.rows, self.columns = self.get_terminal_size()
        if self.rows < 20 or self.columns < 20:
            print("Terminal too small!")
            print("^S/M^S: Save Chart")
            print("Enter: Exit dachart")
        xmin = 0
        xmax = 0
        ymin = 0
        ymax = 0
        for dataset in self.x_data.keys():
            xmin = min(xmin, min(self.x_data[dataset]))
            xmax = max(xmax, max(self.x_data[dataset]))
            ymin = min(ymin, min(self.y_data[dataset]))
            ymax = max(ymax, max(self.y_data[dataset]))
        xdiff = xmax - xmin
        ydiff = ymax - ymin

def main() -> None:
    #chart = daChart({"Year" : [2012, 2016, 2020]}, {"Jack": [0.897608, 1.69525, 1.83220], "Nathalie": [0.81, 1.6, 1.7]}, "XYScatter", "Flux Comparison") #"Difference" : [0.0876083, 0.09525, 0.1322] })\
    #chart.display_chart()

    try:
        import msvcrt
        def get_next_keypress() -> bytes:
            try:
                while True:
                    if msvcrt.kbhit():
                        keypress = msvcrt.getch()
                        return keypress
            except KeyboardInterrupt:
                return "^C"
            
    except ImportError:
        print("Unix is not presently supported.")
        exit()

    while (keypress := get_next_keypress()) != bytes('\x04',"utf8"):
        print(keypress, end="hi")

if __name__ == "__main__":
    main()

"""
CHART(Title,Type,XSeries,[YSeries1,YSeries2,YSeries3,...YSeriesN])

    Warning: Scale may be off!
    CHART(A1,ScatterXY,BlockByCol(A2:D6))
    Various       Flux by Year
    8  |
    7.5|
    7  |                       @
    6.5|
    6  |                   @
    5.5|                               LEGEND
    5  |           @                   x: Flux
    4.5|   @                           o: Background
    4  |                               @: Unobs. Flux
    3.5|
    3  |
    2.5|
    2  |
    1.5|
    1  |
    0.5|
    0  +---o---+---o---+---o---o---+---
        2012    2016    2020    2024
                    Year
    Ret: Return to sheet | ^S: Save chart as bitmap | M^S: Save chart as text
"""