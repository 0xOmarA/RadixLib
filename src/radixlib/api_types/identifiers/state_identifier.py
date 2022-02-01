from radixlib.serializable import Serializable
import radixlib.utils as utils
from typing import Dict, Optional, Set, Any
from datetime import datetime
import dateparser
import json
import pytz


class StateIdentifier(Serializable):
    """ The implementation of an StateIdentifier """

    def __init__(
        self,
        version: Optional[int] = None,
        timestamp: Optional[datetime] = None,
        epoch: Optional[int] = None,
        round: Optional[int] = None
    ) -> None:
        """ Instantiates a new StateIdentifier from the state information

        Args:
            version (:obj:`int`, optional): An optional argument that defaults to None. If the 
                version is provided, the latest ledger state <= the given version is returned.
            timestamp (:obj:`datetime`, optional): An optional argument that defaults to None. If a 
                timestamp is provided, the latest ledger state <= the given timestamp is returned.
            epoch (:obj:`int`, optional): An optional argument that defaults to None. If an epoch is 
                provided, the ledger state at the given epoch <= the given round (else round 0) is 
                returned.
            round (:obj:`int`, optional): An optional argument that defaults to None. If a round is 
                provided, the ledger state at the given round <= the given round.

        Raises: 
            ValueError: Raised when invalid StateIdentifier arguments are given. StateIdentifiers
                are only valid in the cases below::

                #. All of the arguments are missing (creating no state identifier.)
                #. Only the state version is defined.
                #. Only the timestamp is defined.
                #. Only the epoch is defined.
                #. Only the epoch and round is defined.
        """

        # Checking the state identifier to ensure that it is a valid state identifier.
        # These checks are done due to: https://github.com/radixdlt/radixdlt-network-gateway/blob/c473fab883a53f8821842013336d0db5d2cb0258/src/GatewayAPI/Database/LedgerStateQuerier.cs#L251
        none_set: Set[None] = set([None])
        is_all_missing: bool = set([version, timestamp, epoch, round]) == none_set
        only_state_version: bool = version is not None and set([timestamp, epoch, round]) == none_set
        only_timestamp: bool = timestamp is not None and set([version, epoch, round]) == none_set
        only_epoch_given: bool = epoch is not None and set([timestamp, version, round]) == none_set
        epoch_and_round_given: bool = epoch is not None and round is not None and set([timestamp, version]) == none_set
        
        if [is_all_missing, only_state_version, only_timestamp, only_epoch_given, epoch_and_round_given].count(True) != 1:
            raise ValueError("The at_state_identifier was not either (A) missing (B) with only a state_version; (C) with only a Timestamp; (D) with only an Epoch; or (E) with only an Epoch and Round")

        # Setting the arguments to the variables 
        self.version: Optional[int] = version
        self.timestamp: Optional[datetime] = timestamp
        self.epoch: Optional[int] = epoch
        self.round: Optional[int] = round

    def __str__(self) -> str:
        """ Converts the object to a string """
        return f"""StateIdentifier({", ".join(map(lambda x: "%s=%s" % x, self.to_dict().items()))})"""

    def __repr__(self) -> str:
        """ Represents an object """
        return str(self)

    def __eq__(self, other: 'object') -> bool:
        """ Checks for equality between self and other """
        return self.to_dict() == other.to_dict() if isinstance(other, StateIdentifier) else False

    def to_dict(self) -> Dict[str, Any]:
        """" Converts the object to a dictionary """
        return utils.remove_none_values_recursively({
            "version": self.version,
            "timestamp": self.timestamp.astimezone(pytz.UTC).isoformat()[:23] + 'Z' if self.timestamp is not None else None,
            "epoch": self.epoch,
            "round": self.round,
        })

    def to_json_string(self) -> str:
        """ Converts the object to a JSON string """
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(
        cls,
        dictionary: Dict[str, Any]
    ) -> 'StateIdentifier':
        """ Creates a new instance of the StateIdentifier from a dictionary

        This method is used to load up an StateIdentifier from the dictionaries that are returned
        by the Gateway API.

        Args:
            dictionary (dict): A dictionary of the StateIdentifier obtained from the Gateway API.

        Returns:
            StateIdentifier: An StateIdentifier loaded with the data
        """

        return cls(
            version = dictionary['version'],
            timestamp = dateparser.parse(dictionary['timestamp']),
            epoch = dictionary['epoch'],
            round = dictionary['round'],
        )

    @classmethod
    def from_json_string(
        cls,
        json_string: str
    ) -> 'StateIdentifier':
        """ Creates a new instance of the StateIdentifier from a string

        This method is used to load up an StateIdentifier from the strings that are returned
        by the Gateway API.

        Args:
            json_string (str): The JSON serialzable strings returnd by the gateway API.

        Returns:
            StateIdentifier: An StateIdentifier loaded with the data
        """

        return cls.from_dict(json.loads(json_string))