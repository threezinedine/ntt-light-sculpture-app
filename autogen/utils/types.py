import re
from typing import Dict


class TypeConverter:
    def __init__(self):
        self._typeMatchMap = {
            f"int": "int",
            f"long": "int",
            f"short": "int",
            f"char": "int",
            f"float": "float",
            f"double": "float",
            f"bool": "bool",
            f"string": "str",
            f"void": "None",
        }

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

        for typeName in registeredTypeKeys:
            if re.match(TypeConverter.getRawTypeRegex(typeName), type):
                return self._registeredTypes[typeName]

        for typeName, output in self._typeMatchMap.items():
            if re.match(TypeConverter.getRawTypeRegex(typeName), type):
                return output
        return "Any"

    def addType(self, type: str, output: str) -> None:
        self._registeredTypes[type] = output
