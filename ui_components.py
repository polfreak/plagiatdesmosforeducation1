import flet as ft


class UIComponent:

    @staticmethod
    def title(text):
        return ft.Text(text, size=25, weight=ft.FontWeight.BOLD)

    @staticmethod
    def button(text, on_click, icon=None):
        return ft.Button(
            content=text,
            on_click=on_click,
            icon=icon
        )

    @staticmethod
    def text_field(label, password=False, hint=None):
        return ft.TextField(
            label=label,
            password=password,
            can_reveal_password=password,
            hint_text=hint,
        )

    @staticmethod
    def message(text="", color=None):
        return ft.Text(text, color=color)

    @staticmethod
    def divider():
        return ft.Divider()
