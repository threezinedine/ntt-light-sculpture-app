from abc import ABC, abstractmethod


class StructBase(ABC):
    @abstractmethod
    def Update(self, other: "StructBase") -> None:
        raise NotImplementedError("Update method is not implemented")

    @abstractmethod
    def Compare(self, other: "StructBase") -> bool:
        raise NotImplementedError("Compare method is not implemented")
