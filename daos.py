import typing
import mpmath


class DAOS:
    # Procedure
    def __init__(self, functions: dict[str, tuple[int, typing.Callable, str]]) -> None:
        self.operation_stack: list[str] = []
        self.item_stack: typing.Any = []
        self.current_item = ""

        self.variables = {"E": mpmath.e, "PI": mpmath.pi, "i": mpmath.mpc("0","1")}
        self.operation_arguments = {
            "=": 0,
            "+": 2,
            "-": 2,
            "*": 2,
            "/": 2,
            "^": 2,
            "NEG": 1,
            "_": 1,
            "I": 1
        }
        self.operation_priorities = {
            "=": 5,
            "(": 5,
            "+": 4,
            "-": 4,
            "*": 3,
            "/": 3,
            "I": 3,
            "NEG": 1,
            "_": 3,
            "^": 2,
        }
        self.functions: dict[str, typing.callable] = {}
        for function in functions:
            self.functions[function] = functions[function][1]
            self.operation_arguments[function] = functions[function][0]
            self.operation_priorities[function] = 1
        return

    # Function
    def evaluate_operation(self, arguments, operation) -> typing.Any:
        if operation == "_" or operation == "NEG":
            return -1 * arguments[0]

        elif operation == "+":
            return arguments[0] + arguments[1]

        elif operation == "-":
            return arguments[0] - arguments[1]

        elif operation == "*":
            return arguments[0] * arguments[1]

        elif operation == "/":
            return arguments[0] / arguments[1]

        elif operation == "^":
            return arguments[0] ** arguments[1]

        elif operation == "I":
            return arguments[0] * self.variables["i"]

        elif operation in self.functions:
            return self.functions[operation](arguments)

        else:
            raise ArithmeticError

    # Procedure
    def reinit(self) -> None:
        self.operation_stack = []
        self.item_stack = []
        self.current_item = ""
        return

    # Procedure
    def evaluate_expression(self, expression) -> None:
        expression = expression[1:]
        expression += "="
        for index, character in enumerate(expression):
            if character == "-":
                if self.current_item == "":
                    self.operation_stack.append("NEG")
                    continue

            if character == "i" or character == "j" or character == "I" or character == "J":
                if self.current_item == "" or self.current_item.isnumeric() or self.current_item in self.variables:
                    if self.current_item != "":
                        self.evaluate_current_item()
                        self.operation_stack.append("I")
                        self.evaluate_last_operation()
                        self.current_item = ""
                    else:
                        self.item_stack.append(self.variables["i"])
                    continue
                else:
                    self.current_item += "i"
                    self.current_item = self.current_item.strip()
                    continue

            elif character in self.operation_arguments:
                self.evaluate_current_item()
                while (
                    len(self.operation_stack) >= 1
                    and self.operation_priorities[self.operation_stack[-1]]
                    <= self.operation_priorities[character]
                ):
                    self.evaluate_last_operation()
                self.operation_stack.append(character)

            elif character == "(":
                self.evaluate_current_item()
                self.operation_stack.append("(")

            elif character == ")":
                self.evaluate_current_item()
                while self.operation_stack[-1] != "(":
                    self.evaluate_last_operation()
                self.operation_stack.pop()

            elif character == ",":
                self.evaluate_current_item()
                while self.operation_stack[-1] != "(":
                    self.evaluate_last_operation()
            else:
                self.current_item += character
                self.current_item = self.current_item.strip()

        return

    # Procedure
    def evaluate_last_operation(self) -> None:
        arguments = [
            self.item_stack[i]
            for i in range(
                len(self.item_stack)
                - self.operation_arguments[self.operation_stack[-1]],
                len(self.item_stack),
            )
        ]
        for _ in arguments:
            self.item_stack.pop()
        if answer := self.evaluate_operation(arguments, self.operation_stack[-1]):
            self.item_stack.append(answer)
        self.operation_stack.pop()
        return

    # Procedure
    def evaluate_current_item(self) -> None:
        if self.current_item:
            if self.current_item.upper() not in self.operation_arguments:
                self.item_stack.append(
                    self.variables[self.current_item]
                    if self.current_item in self.variables.keys()
                    else mpmath.mpf(self.current_item)
                )
            else:
                self.operation_stack.append(self.current_item.upper())
        self.current_item = ""
        return


if __name__ == "__main__":
    daos_instance = DAOS(
        {
            "SIN": (1, lambda arguments: mpmath.sin(arguments[0]), ""),
            "ASIN": (1, lambda arguments: mpmath.asin(arguments[0]), ""),
            "COS": (1, lambda arguments: mpmath.cos(arguments[0]), ""),
            "TAN": (1, lambda arguments: mpmath.tan(arguments[0]), ""),
            "SQRT": (1, lambda arguments: mpmath.sqrt(arguments[0]), ""),
            "LN": (1, lambda arguments: mpmath.ln(arguments[0]), ""),
            "EXP": (1, lambda arguments: mpmath.exp(arguments[0]), ""),
            "RAD": (1, lambda arguments: arguments[0] * mpmath.pi / 180, ""),
            "DEG": (1, lambda arguments: arguments[0] * 180 / mpmath.pi, ""),
            "NLOG": (
                2,
                lambda arguments: mpmath.ln(arguments[0]) / mpmath.ln(arguments[1]),
                "NLOG(X, BASE) -- Returns the base-BASE logarithm of X",
            ),
        }
    )
    expression = "="
    expression += input("=")

    daos_instance.evaluate_expression(expression)

    print(daos_instance.item_stack[-1])
