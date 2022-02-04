from radixlib.network import Network
from radixlib.actions import (
    CreateTokenDefinition,
    TransferTokens,
    UnstakeTokens,
    StakeTokens,
    MintTokens,
    BurnTokens,
    ActionType
)
from typing import Union, List
import radixlib as radix

class ActionBuilder():
    """ Used to build a list of Radix actions through a series of simple function calls.

    Some of the actions in the new Gateway API can be rather confusing to create especially ones 
    where there is a series of optional arguments that are either required together or not required
    together. To solve this problem, this action builder class introduces a set of functions which 
    may be used to create the desired actions.

    This class is written with the idea that it should allow for method chaining to take place when
    adding actions. So, you should expect to see most functions return a reference to self in order
    to allow for action additions to be chained.
    """

    def __init__(
        self,
        network: Network
    ) -> None:
        """ Instantiates a new ActionBuilder for the given network.
        
        Args:
            network (Network): The network which the action builder will be used for.
        """

        self.network: Network = network
        self.__actions_list: List[ActionType] = []

    def new_mutable_token(
        self,
        owner_address: str,
        name: str,
        symbol: str,
        description: str,
        icon_url: str,
        url: str,
        granularity: int,
    ) -> 'ActionBuilder':
        """ Creates a new CreateTokenDefinition action which defines a mutable token.

        Args:
            owner_address (str): The address of the owner of the token.
            name (str): The name of the token.
            symbol (str): The symbol of the token. This should be a 3 to 8 long small case symbol 
                for the token.
            description (str): The description of the token.
            icon_url (str): The URL of the token icon.
            url (str): The URL to the token website.
            granularity (int): An integer of the token granularity

        Returns:
            ActionBuilder: A reference to self to allow for method chaining when adding actions.
        """

        # Calculating the RRI of the token based on the information passed to the function
        derived_token_rri: str = radix.derive.token_rri(
            creator_public_key = radix.derive.public_key_from_wallet_address(owner_address),
            token_symbol = symbol,
            network = self.network
        )

        # Creating the action and appending it to the list of actions that have been created so far.
        self.__actions_list.append(
            CreateTokenDefinition(
                name = name,
                symbol = symbol,
                description = description,
                icon_url = icon_url,
                url = url,
                granularity = granularity,
                token_rri = derived_token_rri,
                is_supply_mutable = True,
                owner = owner_address
            )
        )

        return self

    def new_fixed_supply_token(
        self,
        owner_address: str,
        name: str,
        symbol: str,
        description: str,
        icon_url: str,
        url: str,
        granularity: int,
        token_supply: int,
        to_account_address: str
    ) -> 'ActionBuilder':
        """ Creates a new CreateTokenDefinition action which defines a fixed supply token.

        Args:
            owner_address (str): The address of the owner of the token.
            name (str): The name of the token.
            symbol (str): The symbol of the token. This should be a 3 to 8 long small case symbol 
                for the token.
            description (str): The description of the token.
            icon_url (str): The URL of the token icon.
            url (str): The URL to the token website.
            granularity (int): An integer of the token granularity.
            token_supply (int): The amount of supply of the token that we wish to have.
            to_account_address (str): The address that the tokens will be sent to upon their 
                creation.

        Returns:
            ActionBuilder: A reference to self to allow for method chaining when adding actions.
        """

        # Calculating the RRI of the token based on the information passed to the function
        derived_token_rri: str = radix.derive.token_rri(
            creator_public_key = radix.derive.public_key_from_wallet_address(owner_address),
            token_symbol = symbol,
            network = self.network
        )

        # Creating the action and appending it to the list of actions that have been created so far.
        self.__actions_list.append(
            CreateTokenDefinition(
                name = name,
                symbol = symbol,
                description = description,
                icon_url = icon_url,
                url = url,
                granularity = granularity,
                token_rri = derived_token_rri,
                is_supply_mutable = False,
                token_supply = token_supply,
                to_account = to_account_address
            )
        )

        return self

    def unstake_tokens_by_percentage(
        self,
        from_validator_address: str,
        to_account_address: str,
        percentage_amount: Union[int, float],
    ) -> 'ActionBuilder':
        """ Creates a new UnstakeTokens action for a percentage of the tokens to unstake from
        the specified validator.

        Args:
            from_validator_address (str): The validators that tokens will be unstaked from.
            to_account_address (str): The address that the tokens will be sent to once unstaked.
            percentage_amount (Union[int, float]): The percentage amount to unstake from the given
                validator. Keep in mind that this is the percentage amount meaning that it should 
                be a numbet between 0 and 100.

        Returns:
            ActionBuilder: A reference to self to allow for method chaining when adding actions.
        """

        # Creating the action and appending it to the list of actions that have been created so far.
        self.__actions_list.append(
            UnstakeTokens(
                to_account = to_account_address,
                from_validator = from_validator_address,
                unstake_percentage = percentage_amount
            )
        )

        return self

    def unstake_tokens_by_amount(
        self,
        from_validator_address: str,
        to_account_address: str,
        unstake_amount: int,
    ) -> 'ActionBuilder':
        """ Creates a new UnstakeTokens action for a specific amount of the tokens to unstake from
        the specified validator.

        Args:
            from_validator_address (str): The validators that tokens will be unstaked from.
            to_account_address (str): The address that the tokens will be sent to once unstaked.
            unstake_amount (int): The amount of XRD to unstake from the validator. Keep in mind that you 
                must specify this amount in Atto and not in XRD.

        Returns:
            ActionBuilder: A reference to self to allow for method chaining when adding actions.
        """

        # Creating the action and appending it to the list of actions that have been created so far.
        self.__actions_list.append(
            UnstakeTokens(
                to_account = to_account_address,
                from_validator = from_validator_address,
                amount = unstake_amount,
                token_rri = radix.derive.xrd_rri_on_network(self.network)
            )
        )

        return self

    def stake_tokens_by_amount(
        self,
        to_validator_address: str,
        from_account_address: str,
        stake_amount: int,
    ) -> 'ActionBuilder':
        """ Creates a new UnstakeTokens action for a specific amount of the tokens to unstake from
        the specified validator.

        Args:
            to_validator_address (str): The validators that tokens will be unstaked from.
            from_account_address (str): The address that the tokens will be sent to once unstaked.
            stake_amount (int): The amount of XRD to unstake from the validator. Keep in mind that 
                you must specify this amount in Atto and not in XRD.

        Returns:
            ActionBuilder: A reference to self to allow for method chaining when adding actions.
        """

        # Creating the action and appending it to the list of actions that have been created so far.
        self.__actions_list.append(
            StakeTokens(
                from_account = from_account_address,
                to_validator = to_validator_address,
                amount = stake_amount,
                token_rri = radix.derive.xrd_rri_on_network(self.network)
            )
        )

        return self

    def token_transfer(
        self,
        from_account_address: str,
        to_account_address: str,
        token_rri: str,
        transfer_amount: int
    ) -> 'ActionBuilder':
        """ Creates a new TokenTransfer action.

        Args:
            from_account_address (str): The account which will be sending the tokens.
            to_account_address (str): The account which will be getting the tokens.
            token_rri (str): The RRI of the token to send.
            transfer_amount_amount (int): The amount of tokens to send.

        Returns:
            ActionBuilder: A reference to self to allow for method chaining when adding actions.
        """

        # Creating the action and appending it to the list of actions that have been created so far.
        self.__actions_list.append(
            TransferTokens(
                from_account = from_account_address,
                to_account = to_account_address,
                amount = transfer_amount,
                token_rri = token_rri
            )
        )

        return self

    def mint_tokens(
        self,
        to_account_address: str,
        mint_amount: int,
        token_rri: str,
    ) -> 'ActionBuilder':
        """ Creates a new MintTokens action.

        Args:
            to_account_address (str): The account that the tokens will be minted for.
            mint_amount (int, optional): The amount of tokens to mint.
            token_rri (str, optional): The RRI of the token.

        Returns:
            ActionBuilder: A reference to self to allow for method chaining when adding actions.
        """

        # Creating the action and appending it to the list of actions that have been created so far.
        self.__actions_list.append(
            MintTokens(
                to_account = to_account_address,
                amount = mint_amount,
                token_rri = token_rri
            )
        )

        return self

    def burn_tokens(
        self,
        from_account_address: str,
        burn_amount: int,
        token_rri: str,
    ) -> 'ActionBuilder':
        """ Creates a new BurnTokens action.

        Args:
            to_account_address (str): The account that the tokens will be minted for.
            mint_amount (int, optional): The amount of tokens to mint.
            token_rri (str, optional): The RRI of the token.

        Returns:
            ActionBuilder: A reference to self to allow for method chaining when adding actions.
        """

        # Creating the action and appending it to the list of actions that have been created so far.
        self.__actions_list.append(
            BurnTokens(
                from_account = from_account_address,
                amount = burn_amount,
                token_rri = token_rri
            )
        )

        return self

    def to_action_list(self) -> List[ActionType]:
        """ Gets a list of the actions that have been created by the action builder so far """
        return self.__actions_list