## type: ignore

from radixlib.identifiers.validator_identifier import ValiditorIdentifier
from radixlib.identifiers.account_identifier import AccountIdentifier
from radixlib.identifiers.network_identifier import Networkdentifier
from radixlib.identifiers.token_identifier import TokenIdentifier
from radixlib.identifiers.state_identifier import StateIdentifier

from typing import TypeVar as __TypeVar
Identifiers = __TypeVar(
    'Identifiers',
    AccountIdentifier,
    Networkdentifier,
    TokenIdentifier,
    ValiditorIdentifier,
    StateIdentifier
)