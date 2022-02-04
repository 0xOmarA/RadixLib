"""
So far in all of the previous examples we have been creating tokens, minting, and burning them. We
have esentially been getting our hands dirty with transactions. Lets now take a step back and go 
back to how to query the blockchain for information. In this module we will look at how we can get 
the information of a token.

This method uses the wallet object to get information about a given token.
"""

from typing import Dict, Any
import radixlib as radix
import os

def main() -> None:
    # The RRI of the token that we're querying the blockchain for.
    token_rri: str = "fix_tr1qdaj7qea3xz8gup5lgaw8duwwwc3z60w9vrnr7p0xr4q98vkk6"

    # Defining the network that we will be connecting to.
    network: radix.network.Network = radix.network.STOKENET

    # Getting the mnemonic phrase for the wallet that we will be connecting to. In this case, my 
    # mnemonic phrase is stored in an envirnoment variable under the name "MNEMONIC_PHRASE". 
    # You might want to do the same or you could also just put your mnemonic phrase as a literal 
    # string. 
    mnemonic_phrase: str = os.environ['MNEMONIC_PHRASE']

    # Creating a new wallet object using the mnemonic phrase above on the network defined.
    wallet: radix.Wallet = radix.Wallet(
        provider = radix.Provider(network),
        signer = radix.Signer.from_mnemonic(mnemonic_phrase)
    )
    print("Wallet address:", wallet.address)
    print("Wallet public key:", wallet.public_key)

    # Getting the token information and printing it to the console
    parsed_token_info: Dict[str, Any] = wallet.get_token_info(token_rri)
    print("Parsed token info:", parsed_token_info)

if __name__ == "__main__":
    main()