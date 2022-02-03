from radixlib.api_types.identifiers import AccountIdentifier
from radixlib.api_types.token_amount import TokenAmount
from radixlib.serializable import Serializable
from typing import Optional, Dict, Any
import radixlib as radix
import json

class CreateTokenDefinition(Serializable):
    """ Defines a CreateTokenDefinition action  """

    def __init__(
        self,
        name: str,
        symbol: str,
        description: str,
        icon_url: str,
        url: str,
        granularity: int,
        token_rri: str,
        is_supply_mutable: bool,
        owner: Optional[str] = None,
        token_supply: Optional[int] = None,
        to_account: Optional[str] = None,
    ) -> None:
        """ Instantiates a new CreateTokenDefinition action used for the creation of new tokens.

        Args:
            owner (str, optional): An account identifier of the account which will be the owner of 
                the token.
            name (str): The name of the token we're creating
            symbol (str): The symbol which is a 3 to 8 letters symbol for tokens.
            description (str): The description of the token.
            icon_url (str): A string of the URL to the token's image.
            url (str): A string of the URL to the token itself (could be a website with more info 
                on the token, or other related info)
            granularity (str): A string of the token granularity.
            token_rri (str): The Radix Resource Identifier that the token will be created under. 
                Needs to be derived from the public key of the creator of the token and the HRP of 
                the specific network.
            is_supply_mutable (bool): A boolean which defines whether the supply of the token is 
                mutable or not. If true, the token can be minted and burned by the owner of the
                token. If false the token will have a fixed supply. If this argument is false, 
                (fixed supply) then the token_supply and to_account arguments need to be specified.           
            token_supply (int, optional): An optional argument which defaults to None. If the 
                is_supply_mutable is false, then this argument needs to be supplied.
            to_account (str, optional): An optional argument which defaults to None, and defines the
                account to send the fixed supply tokens to.
        
        Raises:
            ValueError: A value error is raised in the following two cases::

                #. When the token supply or the to account are supplied when is_supply_mutable is 
                    True
                #. When the token supply or the to_account are not supplied when the 
                    is_supply_mutable is False
                #. When the symbol given is not all lower case.
                #. When the symbol's length is not between 3 and 8.
        """

        # Checking for incorrect usage of the to_account and token_supply arguments
        if is_supply_mutable and (token_supply is not None or to_account is not None or owner is None):
            raise ValueError(
                "You've specified that the token should be mutable and supplied a value to the " 
                "'token_supply' or the 'to_account' arguments which is an invalid operation. When "
                "creating a mutable token (i.e. is_supply_mutable = True) do not supply anything to "
                "the 'token_supply' and 'to_account' arguments"
            )
        elif not is_supply_mutable and (token_supply is None or to_account is None or owner is not None):
            raise ValueError(
                "You must specify 'token_supply' and the 'to_account' arguments when creating a "
                "fixed supply token and remove the specification for the token owner."
            )

        # Checking if the provided symbol for the token is valid
        if not symbol.islower():
            raise ValueError("Token symbols must be all lower case letters.")
        if not (2 <= len(symbol) <= 8):
            raise ValueError(f"Token symbols must be 2 to 8 characters long.")

        self.owner: Optional[AccountIdentifier] = AccountIdentifier(owner) if owner is not None else None
        self.name: str = name
        self.symbol: str = symbol
        self.description: str = description
        self.icon_url: str = icon_url
        self.url: str = url
        self.granularity: int = granularity
        self.token_rri: str = token_rri
        self.is_supply_mutable: bool = is_supply_mutable
        self.token_supply: int =  token_supply if token_supply is not None else 0  
        self.to_account: Optional[AccountIdentifier] = AccountIdentifier(to_account) if to_account is not None else None

    def to_dict(self) -> Dict[str, Any]:
        """" Converts the object to a dictionary """
        return radix.utils.remove_none_values_recursively(
            radix.utils.convert_to_dict_recursively({ # type: ignore
                "type": "CreateTokenDefinition",
                "to_account": self.to_account,
                "token_supply": TokenAmount(
                    rri = self.token_rri,
                    amount = self.token_supply
                ),
                "token_properties": {
                    "name": self.name,
                    "description": self.description,
                    "icon_url": self.icon_url,
                    "url": self.url,
                    "symbol": self.symbol,
                    "is_supply_mutable": self.is_supply_mutable,
                    "granularity": str(int(self.granularity)),
                    "owner": self.owner
                }            
            })
        )

    def to_json_string(self) -> str:
        """ Converts the object to a JSON string """
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_dict(
        cls, 
        dictionary: Dict[Any, Any]
    ) -> 'CreateTokenDefinition':
        """ Loads a CreateTokenDefinition from a Gateway API response dictionary
        
        Args:
            dictionary (dict): The dictionary to load the object from

        Returns:
            CreateTokenDefinition: A new CreateTokenDefinition initalized from the dictionary
        
        Raises: 
            TypeError: Raised when the type of the action in the dictionary does not match
                the action name of the class
        """

        if dictionary.get('type') != "CreateTokenDefinition":
            raise TypeError(f"Expected a dictionary with a type of CreateTokenDefinition but got: {dictionary.get('type')}")

        return cls(
            owner = None if dictionary['token_properties'].get('owner') is None else dictionary['token_properties']['owner']['address'],
            name = dictionary['token_properties']['name'],
            symbol = dictionary['token_properties']['symbol'],
            description = dictionary['token_properties']['description'],
            icon_url = dictionary['token_properties']['icon_url'],
            url = dictionary['token_properties']['url'],
            granularity = int(dictionary['token_properties']['granularity']),
            token_rri = dictionary['token_supply']['token_identifier']['rri'],
            is_supply_mutable = dictionary['token_properties']['is_supply_mutable'],
            token_supply = None if dictionary['token_properties']['is_supply_mutable'] else int(dictionary['token_supply']['value']),
            to_account = None if dictionary.get('to_account') is None else dictionary['to_account']['address']
        )

    @classmethod
    def from_json_string(
        cls,
        json_string: str
    ) -> 'CreateTokenDefinition':
        """ Loads a CreateTokenDefinition from a Gateway API response JSON string. """
        return cls.from_dict(json.loads(json_string))