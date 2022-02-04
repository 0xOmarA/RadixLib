"""
In this example we demonstrate how you can obtain the balances of a wallet.

This method uses the provider without using a signer as there is no need to create a full wallet 
object to perform this simple query (you can do it from the wallet object, it's just not needed.)
"""

from typing import Dict, Any
import radixlib as radix

def main() -> None:
    # The address of the account that we want to get the balances for
    accound_address: str = "tdx1qspqqecwh3tgsgz92l4d4f0e4egmfe86049dj75pgq347fkkfmg84pgx9um0v"

    # Defining the network that we will be connecting to.
    network: radix.network.Network = radix.network.STOKENET

    # Creating the provider object which is esentially our link or connection to the blockchain
    # via the gateway API.
    provider: radix.Provider = radix.Provider(network)

    # Getting the token information and printing it to the console
    account_balances: Dict[str, Any] = provider.get_account_balances(accound_address)
    print("Raw balances info:", account_balances, '\n\n')

    # ###############################################
    # ---------- Optional Response Parsing ----------
    # ###############################################
    # At this point, you have already obtained information about the balances and have printed it to 
    # the console. RadixLib offers a parser which helps parse responses from the gateway API into
    # an easy to query format. You can use this parsed format if you prefer or if you prefer using
    # the original format obtained by the API then feel free to do that.
    parsed_account_balances: Dict[str, Any] = radix.parsers.DefaultParser.parse(
        data = account_balances,
        data_type = 'get_account_balances'
    )
    print("Parsed balances info:", parsed_account_balances)

if __name__ == "__main__":
    main()