from abc import ABC, abstractmethod
from typing import Dict, Any

class Serializable(ABC):
    """ An abstrat implementation of a serializable class. """

    @abstractmethod
    def to_dict(self) -> Dict[Any, Any]:
        """ Converts the object to a dictionary """
        pass

    @abstractmethod
    def to_json_string(self) -> str:
        """ Converts the object to a JSON string """
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, dictionary: Dict[Any, Any]) -> object:
        """ Loads an object from a dictionary """
        pass

    @classmethod
    @abstractmethod
    def from_json_string(cls, json_string: str) -> object:
        """ Loads an object from a JSON string """
        pass