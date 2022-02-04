"""
This example demonstrates how tokens can be sent from your wallet to another wallet.
"""

import radixlib as radix
import os

def main() -> None:
    # Information about the person who we're sending the tokens to and the amount of tokens we're 
    # sending.
    recipient_address: str = "tdx1qsprkzrtmdhvfjnd9z00xtmmwg9p5wn5yawsuttu7dqqgsx2wfm25eqawk3n0"
    token_rri: str = radix.constants.XRD_RRI['stokenet']
    transfer_amount: int = radix.derive.atto_from_xrd(10) # We will be sending them 10 XRD.
    transaction_message: str = "Here is some XRD for your birthday!"

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
    # token transfer.
    tx_hash: str = wallet.build_sign_and_send_transaction(
        actions = (
            wallet.action_builder
                .token_transfer(
                    from_account_address = wallet.address,
                    to_account_address = recipient_address,
                    token_rri = token_rri,
                    transfer_amount = transfer_amount
                )
        ),
        message_string = transaction_message
    )
    print("Fund transfer done under transaction hash:", tx_hash)

if __name__ == "__main__":
    main()