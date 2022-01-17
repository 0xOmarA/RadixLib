"""
In this example script we will look into how we can use the RadixLib python
package to send tokens to a specific address.

There are two main points which I want you to keep in mind.

* This code will work for sending XRD or other native tokens on Radix. The XRD 
token is built in the exact same way as any other token on the Radix blockchain.
This means that the operation needed to send Radix tokens is the same as the 
operation needed to send other native tokens.

* At the current moment of time, all tokens are made up of 1*10^18 parts. So, 
1 XRD = 1*10^18 atto. This is the same for all tokens on the Radix blockchain 
for the time being
"""

import Radix

def main() -> None:
    # The information of the token that we want to send and the person that we're
    # sending it to.
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
        actions = Radix.Action.new_token_transfer_action(
            from_address = wallet.wallet_address,
            to_address = to_address,
            rri = token_rri,
            amount = amount
        ),
        message = "Here are your tokens, enjoy!",
        encrypt_message = True,
        encrypt_for_address = to_address
    )

    print("Token have been sent and sent to your recipient under transaction:", tx_id)

if __name__ == "__main__":
    main()