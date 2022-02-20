from radixlib.api_types.identifiers import ValidatorIdentifier
from radixlib.serializable import Serializable
from typing import Dict, Any
import radixlib as radix
import json

class RegisterValidator(Serializable):
    """ Defines a RegisterValidator action. """

    def __init__(
        self,
        validator_address: str,
    ) -> None:
        """ Instantiates a new RegisterValidator action used for the creation of new tokens.

        Args:
            validator_address (str): The address of the validator to register to the network.

        Raises:
            ValueError: If the RRI given does not begin with XRD.
        """

        self.validator: ValidatorIdentifier = ValidatorIdentifier(validator_address)

    def to_dict(self) -> Dict[str, Any]:
        """" Converts the object to a dictionary """
        return radix.utils.remove_none_values_recursively(
            radix.utils.convert_to_dict_recursively({
                "type": "RegisterValidator",
                "validator": self.validator,
            })
        )

    def to_json_string(self) -> str:
        """ Converts the object to a JSON string """
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_dict(
        cls, 
        dictionary: Dict[Any, Any]
    ) -> 'RegisterValidator':
        """ Loads a RegisterValidator from a Gateway API response dictionary
        
        Args:
            dictionary (dict): The dictionary to load the object from

        Returns:
            RegisterValidator: A new RegisterValidator initalized from the dictionary
        
        Raises: 
            TypeError: Raised when the type of the action in the dictionary does not match
                the action name of the class
        """

        if dictionary.get('type') != "RegisterValidator":
            raise TypeError(f"Expected a dictionary with a type of RegisterValidator but got: {dictionary.get('type')}")

        return cls(
            validator_address = dictionary['validator']['address']
        )

    @classmethod
    def from_json_string(
        cls,
        json_string: str
    ) -> 'RegisterValidator':
        """ Loads a RegisterValidator from a Gateway API response JSON string. """
        return cls.from_dict(json.loads(json_string))