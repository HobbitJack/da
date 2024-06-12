class CellFormat:
    def __init__(self):
        # Procedure
        self.borders = {"up": False, "right": False, "down": False, "left": False}
        # Normal = 0, Money = 1, Scientific Notation = 2, Fix N = N+3
        self.number_type = 0
