from datetime import datetime


class SessionReport:
    def __init__(self, file_name="report.txt"):
        self.file_name = file_name
        self.login_time = None

    @staticmethod
    def current_time():
        return datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    def log_login(self):
        self.login_time = self.current_time()
        with open(self.file_name, "a", encoding="utf-8") as file:
            file.write(f"Вход: {self.login_time}\n")

    def log_logout(self):
        logout_time = self.current_time()
        with open(self.file_name, "a", encoding="utf-8") as file:
            file.write(f"Выход: {logout_time}\n")
            file.write("-" * 30 + "\n")
