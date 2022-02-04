"""
In this example we will take a look at how the RadixLib python package can be used to help you
create mutable tokens quickly.

First of all, let's take a look at some of the borader concepts: to create a mutable token in Radix 
you need to make a transaction with the ``CreateTokenDefinition`` action to define a new token, its
information and details.

You can do all of that using the RadixLib python package. We first begin be creating a new wallet 
by supplying it a provider and a signer. From there we proceed to use the quick transactions feature
of the wallet object to create a new transaction to create this new mutable supply token.
"""

import radixlib as radix
import os

def main() -> None:
    # Information about the token that we're creating
    token_name: str = "Mutable Token"
    token_symbol: str = "mut"
    token_description: str = "Testing the creation of mutable token using the RadixLib python package."
    token_icon_url: str = ""
    token_url: str = ""

    # Defining the network that the token will be created on
    network: radix.network.Network = radix.network.STOKENET

    # Getting the mnemonic phrase for the wallet that we will be connecting to and using to create
    # the token. In this case, my mnemonic phrase is stored in an envirnoment variable under the 
    # name "MNEMONIC_PHRASE". You might want to do the same or you could also just put your mnemonic
    # phrase as a literal string. 
    mnemonic_phrase: str = os.environ['MNEMONIC_PHRASE']

    # Creating a new wallet object using the mnemonic phrase above on the network defined.
    wallet: radix.Wallet = radix.Wallet(
        provider = radix.Provider(network),
        signer = radix.Signer.from_mnemonic(mnemonic_phrase)
    )
    print("Wallet address:", wallet.address)
    print("Wallet public key:", wallet.public_key)

    # Deriving the RRI of the token before we create it.
    token_rri: str = radix.derive.token_rri(wallet.public_key, token_symbol, network)
    print("Creating new token:", token_rri)

    # Using the quick transactions capability of the wallet object to create a transaction for the 
    # new token.
    tx_hash: str = wallet.build_sign_and_send_transaction(
        actions = (
            wallet.action_builder
                .new_mutable_token(
                    owner_address = wallet.address,
                    name = token_name,
                    symbol = token_symbol,
                    description = token_description,
                    icon_url = token_icon_url,
                    url = token_url,
                    granularity = 1 # Only a granularity of 1 is allowed in Radix at the moment.
                )
        )
    )
    print("Token transaction sent under hash:", tx_hash)

if __name__ == "__main__":
    main()