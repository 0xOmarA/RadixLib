"""
This example is very similar to the first second example where we created a mutable supply token. 
The only difference between creating a fixed supply and mutable supply token is the parameters that
we need to provide and the name of the function to call on the action builder.
"""

import radixlib as radix
import os

def main() -> None:
    # Information about the token that we're creating
    token_name: str = "Fixed Token"
    token_symbol: str = "fix"
    token_description: str = "Testing the creation of fixed supply token using the RadixLib python package."
    token_icon_url: str = ""
    token_url: str = ""
    to_address: str = "tdx1qspqqecwh3tgsgz92l4d4f0e4egmfe86049dj75pgq347fkkfmg84pgx9um0v"
    total_supply: int = 10_000 * (10**18) # The total supply of the token is 10_000

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
                .new_fixed_supply_token(
                    owner_address = wallet.address,
                    name = token_name,
                    symbol = token_symbol,
                    description = token_description,
                    icon_url = token_icon_url,
                    url = token_url,
                    granularity = 1, # Only a granularity of 1 is allowed in Radix at the moment.
                    token_supply = total_supply,
                    to_account_address = to_address
                )
        )
    )
    print("Token transaction sent under hash:", tx_hash)

if __name__ == "__main__":
    main()