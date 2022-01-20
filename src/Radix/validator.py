from typing import List, Optional, Union
from datetime import datetime
from .action import Action
from . import utils
import dateparser


class Validator():
    """ A class which describtes a Validator on the Radix Ledger """

    def __init__(
        self, 
        total_delegated_stake: Union[str, int],
        uptime_percentage: Union[str, float, int],
        proposals_missed: int,
        address: str,
        info_url: str,
        owner_delegation: Union[str, int],
        name: str,
        validator_fee: Union[str, float, int],
        registered: bool,
        owner_address: str,
        is_external_stake_accepted: bool,
        proposals_completed: Union[str, int],
    ) -> None:
        """
        Instantiates a new Validator object with the passed arguments

        # Arguments

        * `total_delegated_stake: Union[str, int]` - The total amount of the stake delegated to this 
        validator.
        * `uptime_percentage: Union[str, float, int]` - The percentage of uptime. This is a number between
        0 and 100.
        * `proposals_missed: int` - The number of proposals which were missed by this validator.
        * `address: str` - A string of the address to this validator.
        * `info_url: str` - A string of the URL containing the information of the validator.
        * `owner_delegation: Union[str, int]` - The amount of Atto which the owner of the pool has delegated
        to the pool.
        * `name: str` - The name of the stake pool.
        * `validator_fee: Union[str, float, int]` - The fee which is taken by the validator.
        * `registered: bool` - A boolean which defines whether this node is registered as a validator or not.
        * `owner_address: str` - A string of the address of the owner.
        * `is_external_stake_accepted: bool` - A boolean which defines whether this validator is accepting 
        staking or not.
        * `proposals_completed: Union[str, int]` - A number which defines the number of proposals that the
        validator has completed

        """
        self.__total_delegated_stake: Union[str, int] = int(total_delegated_stake)
        self.__uptime_percentage: Union[str, float, int] = float(uptime_percentage)
        self.__proposals_missed: int = proposals_missed
        self.__address: str = address
        self.__info_url: str = info_url
        self.__owner_delegation: Union[str, int] = int(owner_delegation)
        self.__name: str = name
        self.__validator_fee: Union[str, float, int] = float(validator_fee)
        self.__registered: bool = registered
        self.__owner_address: str = owner_address
        self.__is_external_stake_accepted: bool = is_external_stake_accepted
        self.__proposals_completed: Union[str, int] = int(proposals_completed)

    def __str__(self) -> str:
        """ Represents this object as a string """
        return f"<Validator address=\"{self.address}\">"

    def __repr__(self) -> str:
        """ Represents this object """
        return str(self)

    def __hash__(self) -> int:
        """ Returns an integer hash for the given transaction """
        return hash(self.address)

    def __eq__(self, other: 'Validator') -> bool:
        """ Compares self with other for equality """
        return False if not isinstance(other, Validator) else self.address == other.address

    @property
    def total_delegated_stake(self) -> int:
        """ A getter method for the total_delegated_stake property """
        return self.__total_delegated_stake

    @property
    def uptime_percentage(self) -> float:
        """ A getter method for the uptime_percentage property """
        return self.__uptime_percentage

    @property
    def proposals_missed(self) -> int:
        """ A getter method for the proposals_missed property """
        return self.__proposals_missed

    @property
    def address(self) -> str:
        """ A getter method for the address property """
        return self.__address

    @property
    def info_url(self) -> str:
        """ A getter method for the info_url property """
        return self.__info_url

    @property
    def owner_delegation(self) -> int:
        """ A getter method for the owner_delegation property """
        return self.__owner_delegation

    @property
    def name(self) -> str:
        """ A getter method for the name property """
        return self.__name

    @property
    def validator_fee(self) -> float:
        """ A getter method for the validator_fee property """
        return self.__validator_fee

    @property
    def registered(self) -> bool:
        """ A getter method for the registered property """
        return self.__registered

    @property
    def owner_address(self) -> str:
        """ A getter method for the owner_address property """
        return self.__owner_address

    @property
    def is_external_stake_accepted(self) -> bool:
        """ A getter method for the is_external_stake_accepted property """
        return self.__is_external_stake_accepted

    @property
    def proposals_completed(self) -> int:
        """ A getter method for the proposals_completed property """
        return self.__proposals_completed

    def to_dict(self) -> dict:
        """ Represents this validator object as a dictionary """
        return {key: value for key, value in {
            'totalDelegatedStake': str(self.__total_delegated_stake),
            'uptimePercentage': str(self.__uptime_percentage),
            'proposalsMissed': self.__proposals_missed,
            'address': self.__address,
            'infoURL': self.__info_url,
            'ownerDelegation': str(self.__owner_delegation),
            'name': self.__name,
            'validatorFee': str(self.__validator_fee),
            'registered': self.__registered,
            'ownerAddress': self.__owner_address,
            'isExternalStakeAccepted': self.__is_external_stake_accepted,
            'proposalsCompleted': self.__proposals_completed,
        }.items() if value is not None}