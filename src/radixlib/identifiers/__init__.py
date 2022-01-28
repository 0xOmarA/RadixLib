## type: ignore

from radixlib.identifiers.validator_identifier import ValidatorIdentifier
from radixlib.identifiers.account_identifier import AccountIdentifier
from radixlib.identifiers.network_identifier import NetworkIdentifier
from radixlib.identifiers.token_identifier import TokenIdentifier
from radixlib.identifiers.state_identifier import StateIdentifier

from typing import TypeVar as __TypeVar
Identifiers = __TypeVar(
    'Identifiers',
    AccountIdentifier,
    NetworkIdentifier,
    TokenIdentifier,
    ValidatorIdentifier,
    StateIdentifier
)