from radixlib.serializable import Serializable
from typing import Dict, Any, Union, List, Tuple, Set


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

def convert_to_dict_recursively(
    iterable: Union[Dict[Any, Any], List[Any], Tuple[Any], Set[Any]]
) -> Union[Dict[Any, Any], List[Any], Tuple[Any], Set[Any]]:
    """ Converts the individual items in an iterable to a dictionary if they're an instance of the
    Serializable class.

    This function recursively checks for Serializable objects in the iterable passed to it and 
    invokes the `to_dict` method on all of the objects that if finds which are Serializable. This 
    function is excuted on the objects which have been converted to a dictionary to ensure that 
    the entire dictionary is in a valid format.

    Args:
        iterable (Union[Dict[Any, Any], List[Any], Tuple[Any], Set[Any]]): An iterable which could 
            be a dictionary, list, tuple, or set to convert all of its Serializable objects into 
            their dictionary form.

    Returns:
        Union[Dict[Any, Any], List[Any], Tuple[Any], Set[Any]]: The iterable object reconstructed
            with all of the Serializable objects converted into a dictionary.
    
    """
    if isinstance(iterable, dict):
        new_dict: Dict[Any, Any] = {}
    
        for key, value in iterable.items():
            if isinstance(value, Serializable):
                new_dict[key] = convert_to_dict_recursively(value.to_dict())
            elif isinstance(value, (dict, list, tuple, set)):
                new_dict[key] = convert_to_dict_recursively(value) # type: ignore
            else:
                new_dict[key] = value

        return new_dict
    
    elif isinstance(iterable, (list, tuple, set)): # type: ignore
        new_list: List[Any] = []

        for item in iterable:
            if isinstance(item, Serializable):
                new_list.append(convert_to_dict_recursively(item.to_dict()))
            elif isinstance(item, (dict, list, tuple, set)):
                new_list.append(convert_to_dict_recursively(item)) # type: ignore
            else:
                new_list.append(item)

        return type(iterable)(new_list)
        
    else:
        raise NotImplementedError(
            f"No implementation for convert_to_dict_recursively available for: {type(iterable)}."
        )