import re


def remove_none_values_recursively(dictionary: dict) -> dict:
    """
    Recursively removes the key value pairs where the value is None. 

    # Arguments

    * `dictionary: dict` - The dictionary to remove the `None` key value pairs from

    # Returns

    `dict` - A dicionary of with the `None` key value pairs removed.
    """

    return {
        key: remove_none_values_recursively(value) if isinstance(value, dict) else value
        for key, value in dictionary.items()
        if value is not None
    }


def camel_case_to_snake_case(string: str) -> str:
    """
    This method is used to transform a camel_case_string into snake case.
    
    # Arguments
    
    * `string: str` - A string in camelCase which we want to convert to snake_case.
    
    # Returns
    
    * `str` - The string in snake_case.
    """

    string: str = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', string).lower()