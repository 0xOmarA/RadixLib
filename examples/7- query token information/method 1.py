"""
So far in all of the previous examples we have been creating tokens, minting, and burning them. We
have esentially been getting our hands dirty with transactions. Lets now take a step back and go 
back to how to query the blockchain for information. In this module we will look at how we can get 
the information of a token.

This method uses the provider without using a signer as there is no need to create a full wallet 
object to perform this simple query (you can do it from the wallet object, it's just not needed.)
"""

from typing import Dict, Any
import radixlib as radix

def main() -> None:
    # The RRI of the token that we're querying the blockchain for.
    token_rri: str = "fix_tr1qdaj7qea3xz8gup5lgaw8duwwwc3z60w9vrnr7p0xr4q98vkk6"

    # Defining the network that we will be connecting to.
    network: radix.network.Network = radix.network.STOKENET

    # Creating the provider object which is esentially our link or connection to the blockchain
    # via the gateway API.
    provider: radix.Provider = radix.Provider(network)

    # Getting the token information and printing it to the console
    token_info: Dict[str, Any] = provider.get_token_info(token_rri)
    print("Raw token info:", token_info, '\n\n')

    # ###############################################
    # ---------- Optional Response Parsing ----------
    # ###############################################
    # At this point, you have already obtained information about the token and have printed it to 
    # the console. RadixLib offers a parser which helps parse responses from the gateway API into
    # an easy to query format. You can use this parsed format if you prefer or if you prefer using
    # the original format obtained by the API then feel free to do that.
    parsed_token_info: Dict[str, Any] = radix.parsers.DefaultParser.parse(
        data = token_info,
        data_type = 'get_token_info'
    )
    print("Parsed token info:", parsed_token_info)

if __name__ == "__main__":
    main()