"""
One of the best things about radix is that it allows for multi-action transaction. This allows for 
us to build quite powerful transactions that do quite a number of things all at the same time. 
Examples of multi-action transactions include:

#. Sending XRD to 10 people in a transaction.
#. Creating a new mutable supply token and minting it in a single transaction.
#. Sending XRD to somebody and staking some XRD in a single transaction.

So multi-action transactions allow us to do multiple things in a single transaction. This module 
demonstrates how we can build multiaction transactions using the RadixLib python package. 

The example that we will go over is how to send 3 people 10 XRD all in a single transaction. 
"""

import radixlib as radix
import os

def main() -> None:
    # Information about the people who we will be sending the tokens to
    recipient1_address: str = "tdx1qspw6g43xaef9uke65grhn074e00kvp9nr6mdj5gdhksc7r6cen8trch8lr6x"
    recipient2_address: str = "tdx1qsp6t8v6f98rpn0zc4e84f388neca2xdme6rg7vddd9ef4teq444lhgkh4hmu"
    recipient3_address: str = "tdx1qspzutm77jv33jn9v9xsxyelkqw6lyf6ewspkwex6mems4g6m589gxqcnv6g6"
    token_rri: str = radix.constants.XRD_RRI['stokenet']
    transfer_amount: int = radix.derive.atto_from_xrd(10) # 10 XRD for each address

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
    # multi-action token transfer transaction.
    tx_hash: str = wallet.build_sign_and_send_transaction(
        actions = (
            wallet.action_builder
                .token_transfer(
                    from_account_address = wallet.address,
                    to_account_address = recipient1_address,
                    token_rri = token_rri,
                    transfer_amount = transfer_amount
                )
                .token_transfer(
                    from_account_address = wallet.address,
                    to_account_address = recipient2_address,
                    token_rri = token_rri,
                    transfer_amount = transfer_amount
                )
                .token_transfer(
                    from_account_address = wallet.address,
                    to_account_address = recipient3_address,
                    token_rri = token_rri,
                    transfer_amount = transfer_amount
                )
        )
    )
    print("Tokens sent to addresses under transaction hash:", tx_hash)
    # You can view the transaction I obtained from this example by finding it on the explorer at:
    # https://stokenet-explorer.radixdlt.com//#/transactions/91cf51c2e65f08cc643240f4fd4ba8105a9f3026d37dd22826fc4a55e5d03106
    # As you can see, the three addresses that we have put all received their XRD in a single
    # transaction.

if __name__ == "__main__":
    main()