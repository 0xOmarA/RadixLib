"""
This example examines how tokens can be burned after they've been minted.
"""

import radixlib as radix
import os

def main() -> None:
    # Information on the person who we will be burning the tokens from.
    from_address: str = "tdx1qspqqecwh3tgsgz92l4d4f0e4egmfe86049dj75pgq347fkkfmg84pgx9um0v"
    token_rri: str = "mut_tr1qdal5zydpd947c3rwmk9yquhqyfxepnqu06mu2e0fvsstk7la9"
    burn_amount: int = 1 * (10**18) # This will burn 1 token

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

    # Using the quick transactions capability of the wallet object to create a transaction for the 
    # burning.
    tx_hash: str = wallet.build_sign_and_send_transaction(
        actions = (
            wallet.action_builder
                .burn_tokens(
                    from_account_address = from_address,
                    burn_amount = burn_amount,
                    token_rri = token_rri
                )
        )
    )
    print("Tokens burn under transaction hash:", tx_hash)

if __name__ == "__main__":
    main()