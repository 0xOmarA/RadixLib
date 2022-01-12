from .provider import Provider
from .network import Network
from .signer import Signer
from typing import Dict


class Wallet():
    """ 
    A class which connects a provider with a wallet and allows for transactions to be
    made using this given wallet through the supplied provider.

    This class is written to be a little bit more abstract and higher level as compared
    to the raw API.
    """

    def __init__(
        self,
        provider: Provider,
        signer: Signer,
        index: int = 0
    ) -> None:
        """ 
        Instatiates a new Radix object through the provider and the signer objects passed
        to the object.

        # Arguments

        * `provider: Provider` - A provider object which connects to the Radix blockchain RPC
        API.
        * `signer: Signer` - A signer object which stores the public and private keys for the 
        given radix wallet.
        """

        self.__provider: Provider = provider
        self.__signer: Signer = signer
        self.__index: int = index
    
    @property
    def provider(self) -> Provider:
        """ A getter method for the Raidx provider. """
        return self.__provider

    @property
    def signer(self) -> Signer:
        """ A getter method for the Radix signer """
        return self.__signer

    @property
    def index(self) -> int:
        """ A getter method for the given index """
        return self.__index

    def get_balances(self) -> Dict[str, int]:
        """ 
        This method queries the blockchain for the balances of the tokens that this person
        holds and returns a dictionary mapping of the token RRI and the balance of this token.

        # Returns

        * `Dict[str, int]` - A dictionary mapping which maps the RRI to the balance of the tokens
        """

        # response: dict = self.provider.get_balances(address = self.signer.wallet_address(index = self.index, mainnet=True if self.provider.network is Network.MAINNET else False))
        api_response: dict = self.provider.get_balances(
            address = self.signer.wallet_address(
                index = self.index,
                mainnet = True if self.provider.network is Network.MAINNET else False
            )
        ).json()