from abc import ABC, abstractmethod


class Entity(ABC):

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Имя не должно быть пустым.")
        self._name = value.strip()

    @abstractmethod
    def info(self):
        pass

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r})"

    def __eq__(self, other):
        return isinstance(other, Entity) and self.name == other.name


class Formula(Entity):
    def __init__(self, name, expression, color="#1565C0"):
        super().__init__(name)
        self._expression = expression
        self._color = color

    @property
    def expression(self):
        return self._expression

    @expression.setter
    def expression(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Формула не должна быть пустой.")
        self._expression = value.strip()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    def info(self):
        return f"{self.name}: y = {self.expression}"

    def __len__(self):
        return len(self.expression)

    def __lt__(self, other):
        if not isinstance(other, Formula):
            return NotImplemented
        return self.name < other.name

    def __str__(self):
        return f"{self.name}: y = {self.expression}"

    def __repr__(self):
        return (
            f"Formula(name={self.name!r}, expression={self.expression!r}, "
            f"color={self.color!r})"
        )
