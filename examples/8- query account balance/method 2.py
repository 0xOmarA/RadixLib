"""
This example shows how you can use the wallet object to get the balances for the currently loaded
account in the wallet.
"""

from typing import Dict, Any
import radixlib as radix
import os

def main() -> None:
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

    # Getting the balances information and printing it to the console
    parsed_account_balances: Dict[str, Any] = wallet.get_account_balances()
    print("Parsed token info:", parsed_account_balances)

if __name__ == "__main__":
    main()