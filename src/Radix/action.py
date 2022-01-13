from typing import Union
from enum import Enum
import json


class ActionType(Enum):
    """ An enum which defines the type of actions """
    Other = "Other"
    TokenTransfer = "TokenTransfer"
    StakeTokens = "StakeTokens"
    UnstakeTokens = "UnstakeTokens"
    BurnTokens = "BurnTokens"
    MintTokens = "MintTokens"
    RegisterValidator = "RegisterValidator"
    UnregisterValidator = "UnregisterValidator"
    UpdateValidatorMetadata = "UpdateValidatorMetadata"
    UpdateValidatorFee = "UpdateValidatorFee"
    UpdateValidatorOwner = "UpdateValidatorOwner"
    UpdateAllowDelegationFlag = "UpdateAllowDelegationFlag"
    CreateFixedSupplyToken = "CreateFixedSupplyToken"
    CreateMutableSupplyToken = "CreateMutableSupplyToken"

    def __str__(self) -> str:
        """ Converts the enum to a string """
        return self.value


class Action():
    """ 
    A class which acts as a wrapper for Radix Actions. Built with references to the 
    following GitHub pages:

    * https://github.com/radixdlt/radixdlt/tree/1.0.6/radixdlt-java/radixdlt-java/src/main/java/com/radixdlt/client/lib/api/action
    * https://github.com/radixdlt/radixdlt/blob/5f63817be7a2f3dda54c3fa12a29d041f7b58ff9/radixdlt-java/radixdlt-java/src/main/java/com/radixdlt/client/lib/api/ActionType.java
    """

    def __init__(
        self,
        type: Union[ActionType, str],
        **kwargs: dict
    ) -> None:
        """ 
        Creates a new action object with the keyword arguments provided. 

        # Arguments

        * `kwargs: dict` - A dictionary of keyword arguments which will make up the final
        action dict.

        # Raises

        * `ValueError` - If the `type` argument passed is neither an `ActionType` or a stirng
        """

        # Ensure that the type passed is an ActionType or a string
        if not isinstance(type, ActionType) and not isinstance(type, str):
            raise ValueError(f"The passed `type` argument is neither an ActionType nor a string.")

        # Since 'from' is a reserved keyword in Python, we can not use 'from' in the kwargs.
        # Therefore, wherever there was a 'from' it was replaced with a 'from_address'. We now
        # need to replace them.
        self.__data: dict = {
            key.replace('from_address', 'from').replace('to_address', 'to'): value
            for key, value in kwargs.items()
        }

        self.__data['type'] = str(type)

    @property
    def data(self) -> dict:
        return self.__data

    def __str__(self) -> str:
        """ Converts this object to a string """
        return json.dumps(self.__data)

    def to_dict(self) -> dict:
        """ Converts this object to a dictionary """
        return json.loads(str(self))

    @classmethod
    def new_other_action(cls) -> 'Action':
        """
        Creates a new action of the type 'Other'

        # Returns

        * `Action` - An action object of this other action.
        """

        return cls(
            type = 'other'
        )

    @classmethod
    def new_token_transfer_action(
        cls,
        from_address: str,
        to_address: str,
        amount: int,
        rri: str,
    ) -> 'Action':
        """ 
        Creates a new action of the type "TokenTransfer"

        # Arguments

        * `from_address: str` - A string of the address which will be sending the tokens.
        * `to_address: str` - A string of the address which will be getting the tokens.
        * `amount: int` - An integer of the amount of tokens to send. As an example, if we want to
        send 10 XRD we would specify an amount of 10000000000000000000.
        * `rri: str` - The Radix Resource Identifier (RRI) of the token which we will be sending.

        # Returns

        * `Action` - An action object of this token transfer action.
        """

        return cls(
            type=ActionType.TokenTransfer,
            from_address=from_address,
            to_address=to_address,
            amount=amount,
            rri=rri,
        )

    @classmethod
    def new_stake_action(
        cls,
        from_address: str,
        validator: str,
        amount: int
    ) -> 'Action':
        """
        Creates a new action of the type "StakeTokens"

        # Arguments

        * `from_address: str` - A string of the address which will be staking their tokens.
        * `validator: str` - A string of the validator's address which the tokens will be staked to.
        * `amount: str` - An integer of the amount of XRD to be staked. As an example, if I wish to stake
        10 XRD, then the amount would be 10000000000000000000.

        # Returns

        * `Action` - An action object of this XRD staking.
        """

        return cls(
            type=ActionType.StakeTokens,
            from_address=from_address,
            validator=validator,
            amount=amount,
        )

    @classmethod
    def new_unstake_action(
        cls,
        from_address: str,
        validator: str,
        amount: int
    ) -> 'Action':
        """
        Creates a new action of the type "UnstakeTokens"

        # Arguments

        * `from_address: str` - A string of the address which will be unstaking their tokens.
        * `validator: str` - A string of the validator's address which the tokens will be unstaked from.
        * `amount: str` - An integer of the amount of XRD to be unstaked. As an example, if I wish to unstake
        10 XRD, then the amount would be 10000000000000000000.

        # Returns

        * `Action` - An action object of this XRD unstaking.
        """

        return cls(
            type=ActionType.UnstakeTokens,
            from_address=from_address,
            validator=validator,
            amount=amount,
        )

    @classmethod
    def new_token_burn_action(
        cls,
        from_address: str,
        amount: int,
        rri: str
    ) -> 'Action':
        """
        Creates a new action of the type "BurnTokens"

        # Arguments

        * `from_address: str` - A string of the address which we wish to burn the tokens from.
        * `amount: int` - An integer of the amount of tokens which we wish to burn.
        * `rri: str` - A string of the Radix Resource Identifier (RRI) of the token which we will be burning. 

        # Returns

        * `Action` - An action object of this burn.
        """

        return cls(
            type=ActionType.BurnTokens,
            from_address=from_address,
            amount=amount,
            rri=rri,
        )

    @classmethod
    def new_token_mint_action(
        cls,
        to_address: str,
        amount: int,
        rri: str
    ) -> 'Action':
        """
        Creates a new action of the type "MintTokens"

        # Arguments

        * `to_address: str` - A string of the address which we wish to mint the tokens to.
        * `amount: int` - An integer of the amount of tokens which we wish to mint.
        * `rri: str` - A string of the Radix Resource Identifier (RRI) of the token which we will be minting. 

        # Returns

        * `Action` - An action object of this burn.
        """

        return cls(
            type=ActionType.MintTokens,
            to_address=to_address,
            amount=amount,
            rri=rri,
        )

    @classmethod
    def new_register_validator_action(
        cls,
        validator: str,
        name: str,
        url: str,
    ) -> 'Action':
        """
        Creates a new action of the type "RegisterValidator"

        # Arguments

        * `validator: str` - The address of the validator which we wish to register.
        * `name: str` - The name of the validator.
        * `url: str` - The URL to use to query this validator.

        # Returns

        * `Action` - An action object of this validator registration.
        """

        return cls(
            type=ActionType.RegisterValidator,
            validator=validator,
            name=name,
            url=url,
        )

    @classmethod
    def new_unregister_validator_action(
        cls,
        delegate: str,
        name: str,
        url: str,
    ) -> 'Action':
        """
        Creates a new action of the type "UnregisterValidator"

        # Arguments

        * `validator: str` - The address of the validator which we wish to unregister.
        * `name: str` - The name of the validator.
        * `url: str` - The URL to use to query this validator.

        # Returns

        * `Action` - An action object of this validator unregistration.
        """

        return cls(
            type=ActionType.UnregisterValidator,
            delegate=delegate,
            name=name,
            url=url,
        )

    @classmethod
    def new_update_validator_metadata_action(
        cls,
        delegate: str,
        name: str,
        url: str,
    ) -> 'Action':
        """
        Creates a new action of the type "UpdateValidatorMetadata"

        # Arguments

        * `validator: str` - The address of the validator which we wish to update.
        * `name: str` - The name of the validator.
        * `url: str` - The URL to use to query this validator.

        # Returns

        * `Action` - An action object of this validator metadata update.
        """

        return cls(
            type=ActionType.UpdateValidatorMetadata,
            delegate=delegate,
            name=name,
            url=url,
        )

    @classmethod
    def new_update_validator_fee_action(
        cls,
        validator: str,
        validator_fee: int,
    ) -> 'Action':
        """
        Creates a new action of the type "UpdateValidatorFee"

        # Arguments

        * `validator: str` - The address of the validator which we wish to update the fees for.
        * `validator_fee: int` - The fee which is asociated with this validator

        # Returns

        * `Action` - An action object of this validator fee update.
        """

        return cls(
            type=ActionType.UpdateValidatorFee,
            validator=validator,
            validatorFee=validator_fee,
        )

    @classmethod
    def new_update_validator_owner_action(
        cls,
        validator: str,
        to_address: str,
    ) -> 'Action':
        """
        Creates a new action of the type "UpdateValidatorOwner"

        # Arguments

        * `validator: str` - A string of the validator's address which we wish to update the owner for.
        * `to_address: str` - A string of the address which we want to transfer the ownership to.

        # Returns

        * `Action` - An action object of this validator owner update
        """

        return cls(
            type=ActionType.UpdateValidatorOwner,
            validator=validator,
            to_address=to_address,
        )

    @classmethod
    def new_update_validator_allow_delegation_flag_action(
        cls,
        validator: str,
        allow_delegation: bool,
    ) -> 'Action':
        """
        Creates a new action of the type "UpdateAllowDelegationFlag"

        # Arguments

        * `validator: str` - A string of the validator address that we wish to update the delegation flag for.
        * `allow_delegation: bool` - A boolean of whether delegation to this pool is allowed or not.

        # Returns

        * `Action` - An action object of this validator delegation flag update.
        """

        return cls(
            type=ActionType.UpdateAllowDelegationFlag,
            validator=validator,
            allowDelegation=allow_delegation
        )

    @classmethod
    def new_create_fixed_token_action(
        cls,
        to_address: str,
        public_key_of_signer: str,
        symbol: str,
        name: str,
        description: str,
        icon_url: str,
        token_url: str,
        supply: str,
    ) -> 'Action':
        """
        Creates a new action of the type "CreateFixedSupplyToken"

        # Arguments

        * `to_address: str` - A string of the address which the tokens will be created and minted
        to.
        * `public_key_of_signer: str` - A string of the public key of the signer. In most of the 
        cases, this is the public key of the `to_address` or whoever will sign the transaction.
        * `symbol: str` - A string of the symbol that the token will have.
        * `name: str` - A string of the name of the token.
        * `description: str` - A string of the description of the token.
        * `icon_url: str` - A string of the URL of the token icon.
        * `token_url`: str - A string of the URL for the token. Could be the website for the token.
        * `supply: str` - A string of the total supply of the token.

        # Returns

        * `Action` - An action object of this new token
        """

        return cls(
            type=ActionType.CreateFixedSupplyToken,
            to_address=to_address,
            publicKeyOfSigner=public_key_of_signer,
            symbol=symbol,
            name=name,
            description=description,
            iconUrl=icon_url,
            tokenUrl=token_url,
            supply=supply,
        )

    @classmethod
    def new_create_mutable_token_action(
        cls,
        public_key_of_signer: str,
        symbol: str,
        name: str,
        description: str,
        icon_url: str,
        token_url: str,
    ) -> 'Action':
        """
        Creates a new action of the type "CreateMutableSupplyToken"

        # Arguments

        * `public_key_of_signer: str` - A string of the public key of the signer. In most of the 
        cases, this is the public key of the `to_address` or whoever will sign the transaction.
        * `symbol: str` - A string of the symbol that the token will have.
        * `name: str` - A string of the name of the token.
        * `description: str` - A string of the description of the token.
        * `icon_url: str` - A string of the URL of the token icon.
        * `token_url`: str - A string of the URL for the token. Could be the website for the token.

        # Returns

        * `Action` - An action object of this new token
        """
        return cls(
            type=ActionType.CreateMutableSupplyToken,
            publicKeyOfSigner=public_key_of_signer,
            symbol=symbol,
            name=name,
            description=description,
            iconUrl=icon_url,
            tokenUrl=token_url,
        )
