import logging
import re
from typing import Dict
from data import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


class TypeConverter:
    def __init__(self):
        self._typeMatchMap = {
            "int": "int",
            "long": "int",
            "short": "int",
            "char": "int",
            "u32": "int",
            "u64": "int",
            "u16": "int",
            "u8": "int",
            "i32": "int",
            "i64": "int",
            "i16": "int",
            "i8": "int",
            "float": "float",
            "f32": "float",
            "double": "float",
            "f64": "float",
            "bool": "bool",
            "b8": "bool",
            "string": "str",
            "void": "None",
        }

        self._typeMap: Dict[str, str] = {}  # type: ignore
        self._registeredTypes: Dict[str, str] = {}  # type: ignore

    @staticmethod
    def getRawTypeRegex(type: str) -> str:
        """
        Getting the raw type (the primitive type) regex pattern.
        """
        return f"^[\\s\\S:]*{type}[\\s\\S]*$"

    def convertType(self, type: str) -> str:
        """
        Convert the type from c++ header code into python type.
        """
        registeredTypeKeys = list(self._registeredTypes.keys())
        registeredTypeKeys.sort(key=len, reverse=True)

        for typeName, output in self._typeMap.items():
            if re.match(TypeConverter.getRawTypeRegex(typeName), type):
                return output

        # Try to match the type with the registered types.
        for typeName in registeredTypeKeys:
            if re.match(TypeConverter.getRawTypeRegex(typeName), type):
                return f'"{self._registeredTypes[typeName]}"'

        for typeName, output in self._typeMatchMap.items():
            if re.match(TypeConverter.getRawTypeRegex(typeName), type):
                return output

        logger.warning(f"Type {type} is not defined, using Any instead.")

        return "Any"

    def addType(self, type: str, output: str) -> None:
        self._registeredTypes[type] = output

    def addTypeMap(self, type: str, output: str) -> None:
        self._typeMap[type] = output
