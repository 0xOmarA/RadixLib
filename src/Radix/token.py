import bech32


class Token():
    """ A class which defines what a token is in radix """

    def __init__(
        self,
        rri: str,
        name: str,
        symbol: str,
        description: str,
        isSupplyMutable: bool,
        icon_url: str,
        token_info_url: str,
        granularity: str,
        current_supply: str,
    ) -> None:
        """
        Instantiates a new token object from the given parameters

        # Arguments

        * `rri: str` - A string of the token's Radix Resource Identifier (RRI).
        * `name: str` - A string of the name of the token.
        * `symbol: str` - A string of of the symbol used for the token.
        * `description: str` - A string of the token description.
        * `isSupplyMutable: bool` - A boolean which defines if this is a fixed or mutable supply token.
        * `icon_url: str` - A string of the url containing the token's icon.
        * `token_info_url: str` - A url of the token's info. This is typically the token's website.
        * `granularity: str` - A string of the token's granularity.
        * `current_supply: str` - A string of the total supply of the token which currently exists.
        """

        self.__rri: str = rri
        self.__name: str = name
        self.__symbol: str = symbol
        self.__description: str = description
        self.__isSupplyMutable: bool = isSupplyMutable
        self.__icon_url: str = icon_url
        self.__token_info_url: str = token_info_url
        self.__granularity: int = int(granularity)
        self.__current_supply: int = int(current_supply)

    def __str__(self) -> str:
        """ Represents this token object as a string """
        return f"<Token name=\"{self.name}\">"

    def __repr__(self) -> str:
        """ A representation of this object """
        return str(self)

    @property
    def rri(self) -> str:
        """ A getter function for the rri of the token. """
        return self.__rri

    @property
    def name(self) -> str:
        """ A getter function for the name of the token. """
        return self.__name

    @property
    def symbol(self) -> str:
        """ A getter function for the symbol of the token. """
        return self.__symbol

    @property
    def description(self) -> str:
        """ A getter function for the description of the token. """
        return self.__description

    @property
    def isSupplyMutable(self) -> bool:
        """ A getter function for the isSupplyMutable of the token. """
        return self.__isSupplyMutable

    @property
    def icon_url(self) -> str:
        """ A getter function for the icon_url of the token. """
        return self.__icon_url

    @property
    def token_info_url(self) -> str:
        """ A getter function for the token_info_url of the token. """
        return self.__token_info_url

    @property
    def granularity(self) -> int:
        """ A getter function for the granularity of the token. """
        return self.__granularity

    @property
    def current_supply(self) -> int:
        """ A getter function for the current_supply of the token. """
        return self.__current_supply

    def to_dict(self) -> dict:
        """ A method that converts this token object to a dictionary """
        
        return {
            "tokenInfoURL": self.token_info_url,
            "symbol": self.symbol,
            "isSupplyMutable": self.isSupplyMutable,
            "granularity": str(self.granularity),
            "name": self.name,
            "rri": self.rri,
            "description": self.description,
            "currentSupply": str(self.currentSupply),
            "iconURL": self.icon_url,
        }