import traceback as tb


class MyDumbManager:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print("Произошла ошибка!")
            print(f"\tТип: {exc_type.__name__}")
            print(f"\tСообщение: {exc_value}")
            print("\tТрейсбэк:")
            tb.print_tb(traceback)
        return True


with MyDumbManager() as my_manager:
    raise ValueError("Generator damaged!")

print("За пределами контекста")
