""" 
This script is written to demonstrate how this library can help create a 
new token on the Radix blockchain through the provided methods and functions.
"""

from typing import Dict
import Radix

def main() -> None:
    # The parameters which we would like to use for the token creation
    token_name: str = "TestToken"
    token_symbol: str = "test"
    token_description: str = "A new test token I'm creating on Radix to test how tokens work on Radix"
    token_supply: int = 5000 * (10 ** 18) # 5000 tokens

    # The network parameters as well as the mnemonic phrase to use for the
    # wallet creating the token
    mnemonic_phrase: str = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon"
    network: Radix.Network = Radix.Network.STOKENET

    # Creating a new wallet object with a provider and a signer to use in 
    # this example
    wallet: Radix.Wallet = Radix.Wallet(
        provider =  Radix.Provider(network = network),
        signer = Radix.Signer.from_mnemonic(mnemonic_phrase),
        index = 0,
    )

    # Getting the balance of XRD to ensure that we have enoguh to create
    # a new token on the radix ledger.
    xrd_balance: float = Radix.utils.atto_to_xrd(wallet.get_balance_of_token(Radix.NetworkSpecificConstants.XRD[network]))
    if xrd_balance < 100:
        raise ValueError(f"Radix requires that the creator of a token put forth 100 XRD when creating a new token on the Raidx ledger. However, you only have an XRD balance of {xrd_balance}. Please read the following article for more information on the pricing on Radix: https://learn.radixdlt.com/article/how-do-transaction-fees-work-on-radix-are-they-burned")

    # Perform the transaction through the wallet object and get the transaction
    # id after it is done.
    tx_id: str = wallet.build_sign_and_send_transaction(
        actions = Radix.Action.new_create_fixed_token_action(
            to_address = wallet.wallet_address,
            public_key_of_signer = wallet.public_key,
            symbol = token_symbol,
            name = token_name,
            description = token_description,
            icon_url = "https://qph.fs.quoracdn.net/main-qimg-e5af1b9582725db08148d48bb7c5d3da",
            token_url = "https://www.google.com",
            supply = token_supply
        ),
    )
    print("Token has been created in transaction:", tx_id)
    
    # Calculating the token RRI through the token parameters
    token_rri: str = Radix.utils.calculate_token_rri(
        creator_public_key = wallet.public_key,
        token_symbol = token_symbol,
        network = network
    )
    print(f"Your token has been created and has been given the RRI: {token_rri}")

if __name__ == '__main__':
    main()