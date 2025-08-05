from modules.dependency_injection.decorators import as_transition


@as_transition
class TransitionClass:
    count: int = 0

    def __new__(cls) -> "TransitionClass":
        cls.count += 1
        return super().__new__(cls)
