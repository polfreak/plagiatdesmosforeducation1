from entities import Formula


class FormulaMap:

    def __init__(self):
        self._formulas = []

    @property
    def formulas(self):
        return self._formulas.copy()

    def add(self, formula):
        if not isinstance(formula, Formula):
            raise TypeError("Можно добавлять только объекты Formula.")
        self._formulas.append(formula)

    def remove(self, formula):
        if formula in self._formulas:
            self._formulas.remove(formula)

    def clear(self):
        self._formulas.clear()

    def __len__(self):
        return len(self._formulas)

    def __iter__(self):
        return iter(self._formulas)

    def __getitem__(self, index):
        return self._formulas[index]
