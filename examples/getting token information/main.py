"""
This example demonstrates how we can get the information of a given token from the 
Radix API. 

You can use the Provider class to get the information of the token. However, the recommended
way to do it is through the wallet class and more specifically through the `get_token` 
method.
"""

import Radix
import os

def main() -> None:
    # Information about the token that we want to lookup. All that we need is the RRI
    # for that token and then we can look it up.
    token_rri: str = "hmstr_tr1q0qnazjs66mu4wvekxnj0l8u25ljle8xj0w3uux5f0hq9d59tg"
    network: Radix.Network = Radix.Network.STOKENET

    # Loading up the wallet object and the provider which we will be using the talk to
    # the blockchain. Can you see how I loaded the mnemonic phrase into the signer? 
    # I did it this way because I have the MNEMONIC_PHRASE set as an envirnoment
    # variable. 
    wallet: Radix.Wallet = Radix.Wallet(
        provider = Radix.Provider(network),
        signer = Radix.Signer.from_mnemonic(os.environ['MNEMONIC_PHRASE'])
    )

    # Using the wallet object to get the infomration for the above token. The call to
    # the get_token function will return a `Token` object. An easy way to view the data
    # contained in this object is by converting it to a dictionary and printing it.
    token: Radix.Token = wallet.get_token(token_rri)

    print("Token information:", token.to_dict())

if __name__ == "__main__":
    main()