from abc import ABC, abstractclassmethod
from typing import Any

class ParserBase(ABC):
    """ An abstract base class which defines the functions needed for a parser """

    @abstractclassmethod
    def parse(cls, data: Any, data_type: str) -> Any:
        """ Routes the data parsing to the appropriate parsing function in this class.

        The purpose of this function is to route the data parsing to an appropriate parser function
        from within this class. The actual implementation of this parse function is up to the user;
        however, there are a few things that are recommended:

        #. The ``parse`` function should act as a router and only a router. It should not perform
            any parsing on it's own of any kind.
        #. The ``parse`` function should return the original data if no no parsing functions are 
            found in the module with the name in the `data_type`.
        """

    @abstractclassmethod
    def parse_get_gateway_info(cls, data: Any) -> Any:
        """ A function used for the parsing of the get_gateway_info API calls. """
    
    @abstractclassmethod
    def parse_derive_account_identifier(cls, data: Any) -> Any:
        """ A function used for the parsing of the derive_account_identifier API calls. """
    
    @abstractclassmethod
    def parse_get_account_balances(cls, data: Any) -> Any:
        """ A function used for the parsing of the get_account_balances API calls. """
    
    @abstractclassmethod
    def parse_get_stake_positions(cls, data: Any) -> Any:
        """ A function used for the parsing of the get_stake_positions API calls. """
    
    @abstractclassmethod
    def parse_get_unstake_positions(cls, data: Any) -> Any:
        """ A function used for the parsing of the get_unstake_positions API calls. """
    
    @abstractclassmethod
    def parse_get_account_transactions(cls, data: Any) -> Any:
        """ A function used for the parsing of the get_account_transactions API calls. """
    
    @abstractclassmethod
    def parse_get_native_token_info(cls, data: Any) -> Any:
        """ A function used for the parsing of the get_native_token_info API calls. """
    
    @abstractclassmethod
    def parse_get_token_info(cls, data: Any) -> Any:
        """ A function used for the parsing of the get_token_info API calls. """
    
    @abstractclassmethod
    def parse_derive_token_identifier(cls, data: Any) -> Any:
        """ A function used for the parsing of the derive_token_identifier API calls. """
    
    @abstractclassmethod
    def parse_get_validator(cls, data: Any) -> Any:
        """ A function used for the parsing of the get_validator API calls. """
    
    @abstractclassmethod
    def parse_get_validator_identifier(cls, data: Any) -> Any:
        """ A function used for the parsing of the get_validator_identifier API calls. """
    
    @abstractclassmethod
    def parse_get_validators(cls, data: Any) -> Any:
        """ A function used for the parsing of the get_validators API calls. """
    
    @abstractclassmethod
    def parse_get_transaction_rules(cls, data: Any) -> Any:
        """ A function used for the parsing of the get_transaction_rules API calls. """
    
    @abstractclassmethod
    def parse_build_transaction(cls, data: Any) -> Any:
        """ A function used for the parsing of the build_transaction API calls. """
    
    @abstractclassmethod
    def parse_finalize_transaction(cls, data: Any) -> Any:
        """ A function used for the parsing of the finalize_transaction API calls. """
    
    @abstractclassmethod
    def parse_submit_transaction(cls, data: Any) -> Any:
        """ A function used for the parsing of the submit_transaction API calls. """
    
    @abstractclassmethod
    def parse_transaction_status(cls, data: Any) -> Any:
        """ A function used for the parsing of the transaction_status API calls. """