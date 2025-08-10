from dataclasses import asdict
import json
from abc import ABC, abstractmethod
from dacite import from_dict
from utils.logger import logger


class StructBase(ABC):
    @abstractmethod
    def Update(self, other: "StructBase") -> None:
        """
        From loaded dataclass instance, this method will be used for modifying the value
            based on the loaded instance.

        This method will not affected the original instance address (id).

        Args:
            other: The loaded dataclass instance, this instance must be validated before
                calling this method.
        """
        raise NotImplementedError("Update method is not implemented")

    @abstractmethod
    def Compare(self, other: "StructBase") -> bool:
        """
        Used for testing purpose (easy for assertion).
        """
        raise NotImplementedError("Compare method is not implemented")

    def _Validate(self, loaded: "StructBase") -> bool:
        """
        The preprocess method where the loaded instance will be used before other operation.

        Args:
            loaded: The loaded dataclass instance, this instance can be modified in valid form.

        Returns:
            True if the loaded instance is valid, False otherwise.
        """
        return True

    def FromJson(self, jsonString: str) -> bool:
        """
        Quickly loading the instance with the content which is read from the json file.
        This method include the shema validation for protecting the data from the malicious input.

        Args:
            jsonString: The json string of the dataclass instance which is read from the file.

        Returns:
            True if the instance is loaded successfully, False otherwise.
        """
        try:
            loaded = from_dict(data_class=self.__class__, data=json.loads(jsonString))
        except Exception as e:
            logger.error(f"Failed to load {self.__class__.__name__} from json: {e}")
            return False

        if not self._Validate(loaded):
            return False

        self.Update(loaded)
        return True

    def ToJson(self) -> str:
        """
        Quickly convert to the json format for saving into the file.

        Returns:
            The json string of the dataclass instance.
        """
        return json.dumps(asdict(self), indent=4)  # type: ignore
