"""
This example script is written to demonstrate how this library can be used
to mint a mutable token. 

This script is written with the assumption that you already have a token which
you have created on Stokenet.
"""

import Radix

def main() -> None:
    # The information of the token which we have created and wish to mint
    token_rri: str = "test_tr1qdra2fdxryvre4vpeg8nlxrghc4fz3hpygsaderd67fqythcek"
    to_address: str = "tdx1qspqqecwh3tgsgz92l4d4f0e4egmfe86049dj75pgq347fkkfmg84pgx9um0v"
    amount: int = 100 * (10 ** 18)      # sending 100 of the test tokens

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

    # Perform the transaction through the wallet object and get the transaction
    # id after it is done.
    tx_id: str = wallet.build_sign_and_send_transaction(
        actions = Radix.Action.new_token_mint_action(
            to_address = to_address,
            amount = amount,
            rri = token_rri
        ),
        message = "Speak to you soon my friend.",
        encrypt_message = True,
        encrypt_for_address = to_address
    )

    print("Token have been minted and sent to your recipient under transaction:", tx_id)

if __name__ == "__main__":
    main()