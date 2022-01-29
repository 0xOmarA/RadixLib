from radixlib.serializable import Serializable
from typing import Dict, Any


def remove_none_values_recursively(dictionary: Dict[Any, Any]) -> Dict[Any, Any]:
    """ Recursively removes the key value pairs where the value is None. 

    This is a recursive function which tries to find key value pairs where the value is None and 
    then remove these pairs from the dictionary. 

    Args:
        dictionary (dict): The dictionary to remove the None values from.

    Returns:
        dict: A dictionary with the None value pairs removed.
    """

    return {
        key: remove_none_values_recursively(value) if isinstance(value, dict) else value # type: ignore
        for key, value in dictionary.items()
        if value is not None
    }

def convert_to_dict_recursively(dictionary: Dict[Any, Any]) -> Dict[Any, Any]:
    """ Converts the dictionary passed to it to a dictionary if it has Serializable objects.

    This function recursively checks for Serializable objects in the dictionary passed to it and 
    invokes the `to_dict` method on all of the objects that if finds which are Serializable. This 
    function is excuted on the objects which have been converted to a dictionary to ensure that 
    the entire dictionary is in a valid format.

    Args:
        dictionary (dict): The dictionary to look for the Serializable objects in and to convert to 
            dict.

    Returns:
        dict: A dictionary with the .to_dict method invoked on all of the Serializable objects.
    
    """
    new_dict: Dict[Any, Any] = {}
    
    for key, value in dictionary.items():
        if isinstance(value, Serializable):
            new_dict[key] = convert_to_dict_recursively(value.to_dict())
        elif isinstance(value, dict):
            new_dict[key] = convert_to_dict_recursively(value) # type: ignore
        else:
            new_dict[key] = value

    return new_dict