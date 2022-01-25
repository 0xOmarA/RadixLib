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