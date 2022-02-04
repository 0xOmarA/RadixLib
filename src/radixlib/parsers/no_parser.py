from typing import Callable, Optional, Any
from radixlib.parsers.base_parser import ParserBase

class NoParser(ParserBase):
    """ Defines a parser which performs no parsing of the data whatsoever.

    This class defines a parser which does not perform parsing over any of the data at all. While 
    this class might seem somewhat redundant, it acually makes the implementation of partial parsers 
    a lot more simple. To create a partial parser all tha you would need to do is to inherit from 
    this class and then define the parsing functions that you would like.
    """

    @classmethod
    def parse(
        cls,
        data: Any,
        data_type: str
    ) -> Any:
        """ Routes the parsing of the data to the appropriate parsing function from within the class

        This function acts as a router which tires to find the appropriate parsing function within 
        the class to parse the data. If no parser is implemented for this data type, then the 
        original data is returned without any parsing.

        Args:
            data (Any): Data of any type to pass to the parser function
            data_type (str): Type of the data or the origin of the data

        Returns:
            Any: The parsed data
        """

        # Getting the parsing function for this data type from the attributes of the class
        function_name: str = f'parse_{data_type}'
        parsing_function: Optional[Callable[..., Any]] = getattr(cls, function_name, None)

        # We try calling the parsing function with the data that we have. If the parsing function 
        # works, then we return the parsed data. However, if a TypeError or NotImplementedError is
        # raised, then we return the original data
        try:
            parsed_data: Any = parsing_function(data) # type: ignore
            return parsed_data if parsed_data is not None else data
        except (TypeError, NotImplementedError):
            return data

    @classmethod
    def parse_get_gateway_info(cls, data: Any) -> Any:
        """ A function used for the parsing of the get_gateway_info API calls. """
        raise NotImplementedError("No implementation for get_gateway_info")

    @classmethod
    def parse_derive_account_identifier(cls, data: Any) -> Any:
        """ A function used for the parsing of the derive_account_identifier API calls. """
        raise NotImplementedError("No implementation for derive_account_identifier")

    @classmethod
    def parse_get_account_balances(cls, data: Any) -> Any:
        """ A function used for the parsing of the get_account_balances API calls. """
        raise NotImplementedError("No implementation for get_account_balances")

    @classmethod
    def parse_get_stake_positions(cls, data: Any) -> Any:
        """ A function used for the parsing of the get_stake_positions API calls. """
        raise NotImplementedError("No implementation for get_stake_positions")

    @classmethod
    def parse_get_unstake_positions(cls, data: Any) -> Any:
        """ A function used for the parsing of the get_unstake_positions API calls. """
        raise NotImplementedError("No implementation for get_unstake_positions")

    @classmethod
    def parse_get_account_transactions(cls, data: Any) -> Any:
        """ A function used for the parsing of the get_account_transactions API calls. """
        raise NotImplementedError("No implementation for get_account_transactions")

    @classmethod
    def parse_get_native_token_info(cls, data: Any) -> Any:
        """ A function used for the parsing of the get_native_token_info API calls. """
        raise NotImplementedError("No implementation for get_native_token_info")

    @classmethod
    def parse_get_token_info(cls, data: Any) -> Any:
        """ A function used for the parsing of the get_token_info API calls. """
        raise NotImplementedError("No implementation for get_token_info")

    @classmethod
    def parse_derive_token_identifier(cls, data: Any) -> Any:
        """ A function used for the parsing of the derive_token_identifier API calls. """
        raise NotImplementedError("No implementation for derive_token_identifier")

    @classmethod
    def parse_get_validator(cls, data: Any) -> Any:
        """ A function used for the parsing of the get_validator API calls. """
        raise NotImplementedError("No implementation for get_validator")

    @classmethod
    def parse_get_validator_identifier(cls, data: Any) -> Any:
        """ A function used for the parsing of the get_validator_identifier API calls. """
        raise NotImplementedError("No implementation for get_validator_identifier")

    @classmethod
    def parse_get_validators(cls, data: Any) -> Any:
        """ A function used for the parsing of the get_validators API calls. """
        raise NotImplementedError("No implementation for get_validators")

    @classmethod
    def parse_get_transaction_rules(cls, data: Any) -> Any:
        """ A function used for the parsing of the get_transaction_rules API calls. """
        raise NotImplementedError("No implementation for get_transaction_rules")

    @classmethod
    def parse_build_transaction(cls, data: Any) -> Any:
        """ A function used for the parsing of the build_transaction API calls. """
        raise NotImplementedError("No implementation for build_transaction")

    @classmethod
    def parse_finalize_transaction(cls, data: Any) -> Any:
        """ A function used for the parsing of the finalize_transaction API calls. """
        raise NotImplementedError("No implementation for finalize_transaction")

    @classmethod
    def parse_submit_transaction(cls, data: Any) -> Any:
        """ A function used for the parsing of the submit_transaction API calls. """
        raise NotImplementedError("No implementation for submit_transaction")

    @classmethod
    def parse_transaction_status(cls, data: Any) -> Any:
            """ A function used for the parsing of the transaction_status API calls. """
            raise NotImplementedError("No implementation for transaction_status")
