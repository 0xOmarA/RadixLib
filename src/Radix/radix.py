from .provider import Provider
from .signer import Signer

class Radix():
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