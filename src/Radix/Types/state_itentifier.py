from typing import Optional, Set
from datetime import datetime
from .. import utils
import pytz


class StateIdentifier():
    """ Used to describe a previous period in the state of the blockchain """

    def __init__(
        self,
        version: Optional[int] = None,
        timestamp: Optional[datetime] = None,
        epoch: Optional[int] = None,
        round: Optional[int] = None
    ) -> None:
        """
        Initalizes a new StateIdentifier using the passed arguments

        # Argument

        * `version: Optional[int]` - If the version is provided, the latest ledger state <= the 
        given version is returned.
        * `timestamp: Optional[datetime]` - If a timestamp is provided, the latest ledger state <= 
        the given timestamp is returned.
        * `epoch: Optional[int]` - If an epoch is provided, the ledger state at the given epoch <= 
        the given round (else round 0) is returned.
        * `round: Optional[int]` - If an round is provided, the ledger state at the given round <= 
        the given round.

        # Raises

        * `ValueError` - Raised when the object is initalized in an incorrect way. 
        """
        
        # Setting the arguments to the variables 
        self.__version: Optional[int] = version
        self.__timestamp: Optional[datetime] = timestamp
        self.__epoch: Optional[int] = epoch
        self.__round: Optional[int] = round

        # Checking the state identifier to ensure that it is a valid state identifier.
        # These checks are done due to: https://github.com/radixdlt/radixdlt-network-gateway/blob/c473fab883a53f8821842013336d0db5d2cb0258/src/GatewayAPI/Database/LedgerStateQuerier.cs#L251
        none_set: Set[None] = set([None])
        is_all_missing: bool = set([self.version, self.timestamp, self.epoch, self.round]) == none_set
        only_state_version: bool = self.version is not None and set([self.timestamp, self.epoch, self.round]) == none_set
        only_timestamp: bool = self.timestamp is not None and set([self.version, self.epoch, self.round]) == none_set
        only_epoch_given: bool = self.epoch is not None and set([self.timestamp, self.version, self.round]) == none_set
        epoch_and_round_given: bool = self.epoch is not None and self.round is not None and set([self.timestamp, self.version]) == none_set
        
        if [is_all_missing, only_state_version, only_timestamp, only_epoch_given, epoch_and_round_given].count(True) != 1:
            raise ValueError("The at_state_identifier was not either (A) missing (B) with only a state_version; (C) with only a Timestamp; (D) with only an Epoch; or (E) with only an Epoch and Round")

    @property
    def version(self) -> int:
        """ A getter method for the version """
        return self.__version

    @property
    def timestamp(self) -> datetime:
        """ A getter method for the timestamp """
        return self.__timestamp

    @property
    def epoch(self) -> int:
        """ A getter method for the epoch """
        return self.__epoch

    @property
    def round(self) -> int:
        """ A getter method for the round """
        return self.__round

    def to_dict(self) -> dict:
        """ Converts the StateIdentifier to a dictionary and removed the None pairs """
        return utils.remove_none_values_recursively({
            "version": self.version,
            "timestamp": self.timestamp.astimezone(pytz.UTC).isoformat().replace('+00:00', 'Z'),
            "epoch": self.epoch,
            "round": self.round,
        })