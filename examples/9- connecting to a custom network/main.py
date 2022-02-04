"""
There are many cases where you might want to connect and quickly test some things on a custom 
network instead of connecting to the mainent or the stokenet. To help you with that, the RadixLib 
python package is fully compatible with custom networks and all that it requires is a definition
for the network and you can get started using that network.
"""

from typing import Dict
import radixlib as radix
import os

def main() -> None:
    # Defining the new custom network that we will be connecting to. 
    network: radix.network.Network = radix.network.Network(
        name = "localnet",
        account_hrp = "ddx",
        resource_hrp_suffix = "_dr",
        validator_hrp = "dv",
        node_hrp = "dn",
        default_gateway_url = "http://192.168.100.92:5308"
    )

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

    # Getting the balances for my wallet on this custom network
    parsed_account_balances: Dict[str, Dict[str, int]] = wallet.get_account_balances()
    print("Parsed account balances:", parsed_account_balances)

if __name__ == "__main__":
    main()