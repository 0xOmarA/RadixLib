"""
In this example we demonstrate how you can obtain the balances of a wallet.

This method uses the provider without using a signer as there is no need to create a full wallet 
object to perform this simple query (you can do it from the wallet object, it's just not needed.)
"""

from typing import Optional, List, Dict, Any
import radixlib as radix

def main() -> None:
    # The address of the account that we want to get the transaction history for.
    accound_address: str = "tdx1qspqqecwh3tgsgz92l4d4f0e4egmfe86049dj75pgq347fkkfmg84pgx9um0v"

    # Defining the network that we will be connecting to.
    network: radix.network.Network = radix.network.STOKENET

    # Creating the provider object which is esentially our link or connection to the blockchain
    # via the gateway API.
    provider: radix.Provider = radix.Provider(network)

    # Creating an empty list to store the transactions and beggining to query for the transactions
    transactions_list: List[Dict[str, Any]] = []
    cursor: Optional[str] = None
    while True:
        # Getting the transaction history for the current cursor
        query_response: Dict[str, Any] = provider.get_account_transactions(
            account_address = accound_address,
            cursor = cursor
        )

        # Parsing the query response and then extending the transactions list with the parsed 
        # response.
        parsed_transaction_list: List[Dict[str, Any]] = radix.parsers.DefaultParser.parse(
            data = query_response,
            data_type = "get_account_transactions"
        )
        transactions_list.extend(parsed_transaction_list)

        # Getting the cursor from the query response if it's present. If there is no cursor present
        # then we have reached the end of the transaction history and can safely stop fetching 
        # transactions
        cursor = query_response.get('next_cursor')
        if cursor is None:
            break
        
    # Printing the transactions to the console
    print('Transactions:', transactions_list)

if __name__ == "__main__":
    main()