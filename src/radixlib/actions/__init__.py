# type: ignore

# the imports for all of the actions
from radixlib.actions.create_token_definition import CreateTokenDefinition
from radixlib.actions.unregister_validator import UnregisterValidator
from radixlib.actions.register_validator import RegisterValidator
from radixlib.actions.transfer_tokens import TransferTokens
from radixlib.actions.unstake_tokens import UnstakeTokens
from radixlib.actions.stake_tokens import StakeTokens
from radixlib.actions.mint_tokens import MintTokens
from radixlib.actions.burn_tokens import BurnTokens

# Creating an action type
from typing import Union as __Union
ActionType = __Union[
    CreateTokenDefinition,
    UnregisterValidator,
    RegisterValidator,
    TransferTokens,
    UnstakeTokens,
    StakeTokens,
    MintTokens,
    BurnTokens
]