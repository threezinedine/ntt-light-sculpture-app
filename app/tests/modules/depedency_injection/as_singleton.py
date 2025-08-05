from modules.dependency_injection.decorators import as_singleton


@as_singleton
class SingletonClass:
    count: int = 0

    def __new__(cls) -> "SingletonClass":
        cls.count += 1
        return super().__new__(cls)

    def print_count(self) -> None:
        print(f"TestSingletonClass count: {self.count}")
