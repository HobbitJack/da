class CellFormat:
    def __init__(self):
        # Procedure
        self.borders = {"up": False, "right": False, "down": False, "left": False}
        # Normal = 0, Money = 1, Scientific Notation = 2, Fix N = N+3
        self.number_type = 0
        # white = 0, black = 1, red = 2, blue = 3, green = 4, cyan = 5, magenta = 6, yellow = 7
        self.text_color = 0
        self.background_color = 1
