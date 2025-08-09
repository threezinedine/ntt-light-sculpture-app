from dataclasses import asdict
import json
from abc import ABC, abstractmethod
from dacite import from_dict
from utils.logger import logger


class StructBase(ABC):
    @abstractmethod
    def Update(self, other: "StructBase") -> None:
        raise NotImplementedError("Update method is not implemented")

    @abstractmethod
    def Compare(self, other: "StructBase") -> bool:
        raise NotImplementedError("Compare method is not implemented")

    def FromJson(self, jsonString: str) -> bool:
        try:
            loaded = from_dict(data_class=self.__class__, data=json.loads(jsonString))
        except Exception as e:
            logger.error(f"Failed to load {self.__class__.__name__} from json: {e}")
            return False

        self.Update(loaded)
        return True

    def ToJson(self) -> str:
        return json.dumps(asdict(self))  # type: ignore
