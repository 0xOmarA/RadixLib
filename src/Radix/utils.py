from typing import Union


def xrd_to_atto(xrd_amount: Union[int, float, str]) -> int:
    """
    A method used to convert the supplied amount of XRD into the smallest unit
    of an XRD (called an Atto in Radix).

    # Arguments

    * `xrd_amount: xrd_amount: Union[int, float, str]` - An amount of XRD as a integer,
    float, or a string.

    # Returns

    * `int` - An integer of the amount of Atto corresponding to the XRD amount given.
    """

    return int(float(xrd_amount) * 10 ** 18)


def atto_to_xrd(atto_amount: Union[str, int]) -> float:
    """
    A method used to convert the smallest unit of an XRD (An Atto) into its equivalent
    value in XRD.

    # Arguments

    * `atto_amount: Union[str, int]` - An amount of Atto as an integer or a string. 

    # Returns

    `float` - A float of the amount of XRD corresponding to the Atto amount given.
    """

    return int(atto_amount) / (10 ** 18)
