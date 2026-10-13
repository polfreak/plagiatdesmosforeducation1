import math
import io
import base64
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import flet as ft

from entities import Formula
from formula_map import FormulaMap
from session_report import SessionReport
from ui_components import UIComponent


PASSWORD = "1234"


class CalculatorApp:
    def __init__(self, page):
        self.page = page
        self.report = SessionReport()
        self.formulas = FormulaMap()
        self.expression_field = UIComponent.text_field(
            "Функция y = f(x)", hint="Например: x**2"
        )
        self.password_field = UIComponent.text_field("Пароль", password=True)
        self.message = UIComponent.message()
        self.formula_list = ft.Column(spacing=5)
        self.chart = ft.Column(expand=True)
        self._add_examples()

    def _add_examples(self):
        examples = [

            ("Квадратичная", "x**2", "#1565C0"),
            ("Линейная", "2*x + 1", "#C62828"),
            ("Кубическая", "x**3", "#2E7D32"),
            ("Синус", "math.sin(x)", "#6A1B9A"),
            ("Косинус", "math.cos(x)", "#EF6C00"),
            ("Модуль", "abs(x)", "#00838F"),
            ("Корень", "math.sqrt(abs(x))", "#4E342E"),
            ("Обратная", "1/(x if abs(x) > 0.1 else 0.1)", "#455A64"),
            ("Экспонента", "math.exp(x/3)", "#AD1457"),
            ("Логарифм", "math.log(abs(x) + 1)", "#558B2F"),
    ]


        for name, expression, color in examples:
            self.formulas.add(Formula(name, expression, color))

    def build(self):
        self.page.title = "Графический калькулятор"
        self.page.window_width = 1000
        self.page.window_height = 750
        self.show_login()

    def show_login(self, _=None):
        self.page.controls.clear()
        self.password_field.value = ""
        self.message.value = ""
        self.page.add(
            ft.Container(
                content=ft.Column(
                    [
                        UIComponent.title("Вход в приложение"),
                        ft.Text("Введите пароль для продолжения."),
                        self.password_field,
                        UIComponent.button("Войти", self.login),
                        self.message,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15,
                ),
                padding=40,
                alignment=ft.Alignment.CENTER,
                expand=True,
            )
        )
        self.page.update()

    def login(self, _=None):
        if self.password_field.value == PASSWORD:
            self.report.log_login()
            self.show_calculator()
        else:
            self.message.value = "Неверный пароль."
            self.message.color = ft.Colors.RED
            self.page.update()

    def show_calculator(self):
        self.page.controls.clear()
        self.page.add(
            ft.Row(
                [
                    UIComponent.title("Графический калькулятор"),
                    ft.Container(expand=True),
                    UIComponent.button("Выйти", self.logout),
                ]
            ),
            UIComponent.divider(),
            ft.Row(
                [
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("Добавить функцию", weight=ft.FontWeight.BOLD),
                                self.expression_field,
                                UIComponent.button("Добавить график", self.add_formula),
                                UIComponent.button("Очистить графики", self.clear_formulas),
                                self.message,
                                UIComponent.divider(),
                                ft.Text("Функции", weight=ft.FontWeight.BOLD),
                                self.formula_list,
                            ],
                            scroll=ft.ScrollMode.AUTO,
                        ),
                        width=330,
                        padding=10,
                    ),
                    ft.VerticalDivider(),
                    ft.Container(content=self.chart, expand=True, padding=10),
                ],
                expand=True,
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
        )
        self.refresh_formula_list()
        self.draw_graphs()
        self.page.update()

    def add_formula(self, _=None):
        expression = (self.expression_field.value or "").strip()
        if not expression:
            self.message.value = "Введите выражение, например x**2."
            self.message.color = ft.Colors.RED
            self.page.update()
            return

        # Restrict evaluation to math functions and x.
        try:
            self._evaluate(expression, 1.0)
        except Exception as error:
            self.message.value = f"Не удалось прочитать формулу: {error}"
            self.message.color = ft.Colors.RED
            self.page.update()
            return

        number = len(self.formulas) + 1
        self.formulas.add(Formula(f"Функция {number}", expression, "#1565C0"))
        self.expression_field.value = ""
        self.message.value = "Функция добавлена."
        self.message.color = ft.Colors.GREEN
        self.refresh_formula_list()
        self.draw_graphs()
        self.page.update()

    @staticmethod
    def _evaluate(expression, x):
        allowed = {
            "x": x,
            "math": math,
            "abs": abs,
            "sqrt": math.sqrt,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "log": math.log,
            "exp": math.exp,
            "pi": math.pi,
            "e": math.e,
        }
        return eval(expression, {"__builtins__": {}}, allowed)

    def refresh_formula_list(self):
        self.formula_list.controls.clear()
        for index, formula in enumerate(self.formulas.formulas):
            self.formula_list.controls.append(
                ft.Row(
                    [
                        ft.Container(
                            width=12,
                            height=12,
                            bgcolor=formula.color,
                            border_radius=6,
                        ),
                        ft.Text(f"{formula.name}: {formula.expression}", expand=True),
                        ft.IconButton(
                            icon=ft.Icons.DELETE_OUTLINE,
                            tooltip="Удалить",
                            on_click=lambda e, item=formula: self.remove_formula(item),
                        ),
                    ]
                )
            )

    def remove_formula(self, formula):
        self.formulas.remove(formula)
        self.refresh_formula_list()
        self.draw_graphs()
        self.page.update()

    def clear_formulas(self, _=None):
        self.formulas.clear()
        self.refresh_formula_list()
        self.draw_graphs()
        self.page.update()

    def draw_graphs(self):
        fig, ax = plt.subplots(figsize=(8, 6))
        plotted = False

        for formula in self.formulas:
            xs, ys = [], []
            for step in range(401):
                x = -10 + step * 0.05
                try:
                    y = float(self._evaluate(formula.expression, x))
                    if not math.isfinite(y) or abs(y) >= 1000:
                        y = float("nan")
                except Exception:
                    y = float("nan")
                xs.append(x)
                ys.append(y)

            if any(math.isfinite(y) for y in ys):
                ax.plot(xs, ys, color=formula.color, linewidth=2,
                        label=formula.name)
                plotted = True

        self.chart.controls.clear()
        if not plotted:
            self.chart.controls.append(
                ft.Text("Нет данных для построения графика.")
            )
            plt.close(fig)
            self.page.update()
            return

        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        ax.axhline(0, color="gray", linewidth=0.8)
        ax.axvline(0, color="gray", linewidth=0.8)
        ax.grid(True, alpha=0.3)
        ax.legend(loc="upper right", fontsize=8)
        fig.tight_layout()

        buffer = io.BytesIO()
        fig.savefig(buffer, format="png", dpi=120)
        plt.close(fig)
        image_base64 = base64.b64encode(buffer.getvalue()).decode("ascii")
        self.chart.controls.append(
            ft.Image(src=f"data:image/png;base64,{image_base64}",
                     fit=ft.BoxFit.CONTAIN, expand=True)
        )
        self.page.update()

    def logout(self, _=None):
        self.report.log_logout()
        self.show_login()
