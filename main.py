from calculator_app import CalculatorApp


def main(page):
    app = CalculatorApp(page)
    app.build()


if __name__ == "__main__":
    import flet as ft
    ft.run(main)
