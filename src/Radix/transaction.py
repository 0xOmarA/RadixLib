from typing import List, Optional
from datetime import datetime
from .action import Action
from . import utils
import dateparser


class Transaction():
    """ A class which describtes a transaction on the Radix Ledger """

    def __init__(
       self, 
       fee: int,
       tx_id: str, 
       sent_at: str,
       actions: List[dict],
       message: Optional[str] = None
    ) -> None:
        """
        Instantiates a new Transaction object with the passed arguments

        # Arguments

        * `fee: int` - The fee paid in the transaction supplied in atto.
        * `tx_id: str` - A string of the transaction hash.
        * `sent_at: str` - A string of the time when the transaction was sent.
        * `actions: List[dict]` - A list of the action dictionaries.
        * `message: Optional[str]` - An optional string of the contained message.
        """
        self.__fee_in_xrd: float = utils.atto_to_xrd(fee)
        self.__tx_id: str = tx_id
        self.__sent_at: str = sent_at
        self.__sent_at_parsed: datetime = dateparser.parse(sent_at)
        self.__actions: List[Action] = list(map(lambda x: Action(**x), actions))
        self.__message: str = message

    def __str__(self) -> str:
        """ Represents this object as a string """
        return f"<Transaction tx_id=\"{self.tx_id}\">"

    def __repr__(self) -> str:
        """ Represents this object """
        return str(self)

    def __hash__(self) -> int:
        """ Returns an integer hash for the given transaction """
        return hash(self.tx_id)

    def __eq__(self, other: 'Transaction') -> bool:
        """ Compares self with other for equality """
        return False if not isinstance(other, Transaction) else self.tx_id == other.tx_id

    @property
    def fee(self) -> int:
        """ A getter method for the fee variable """ 
        return self.__fee

    @property
    def tx_id(self) -> str:
        """ A getter method for the tx_id variable """ 
        return self.__tx_id

    @property
    def sent_at(self) -> datetime:
        """ A getter method for the sent_at variable """ 
        return self.__sent_at_parsed

    @property
    def actions(self) -> List[Action]:
        """ A getter method for the actions variable """ 
        return self.__actions

    @property
    def message(self) -> Optional[str]:
        """ A getter method for the message variable """ 
        return self.__message

    def to_dict(self) -> dict:
        """ Represents this transaction object as a dictionary """
        return {key: value for key, value in {
            'fee': utils.xrd_to_atto(self.__fee_in_xrd),
            'txID': self.__tx_id,
            'sent_at': self.__sent_at,
            'actions': list(map(Action.to_dict, self.__actions)),
            'message': self.__message
        }.items() if value is not None}