from typing import Optional, Dict, List, Any
import radixlib as radix
import config
import json

def get_all_transactions(
    wallet: radix.Wallet
) -> List[Dict[str, Any]]:
    """ Gets all of the transactions where this wallet was involved. """

    current_cursor: Optional[str] = None
    transactions: List[Dict[str, Any]] = []
    while 1:
        next_cursor, new_transactions = wallet.get_account_transactions(30, current_cursor)
        transactions.extend(new_transactions)

        if next_cursor is not None:
            current_cursor = next_cursor
        else:
            break

    return sorted( # type: ignore
        transactions,
        key = lambda x: x['confirmed_time'],
        reverse = False
    )

def main() -> None:
    # Loading up the data file which contains the state of the program from the last run
    with open(config.data_json_file, 'r') as file:
        data_file_content: Dict[str, Any] = json.load(file)
        handeled_transactions_mapping: Dict[str, str] = data_file_content['handeled_transactions_mapping']

    # Loading up our wallet through the information that we provided in the config file
    wallet: radix.Wallet = radix.Wallet(
        provider = radix.Provider(config.network),
        signer = radix.Signer.from_mnemonic(config.mnemonic_phrase)
    )
    print("Listening on transactions on wallet:", wallet.address)

    # Getting all of the transactions that the wallet address was involved in
    transactions: List[Dict[str, Any]] = get_all_transactions(wallet)
    print(f"Number of transactions on address:", len(transactions))

    # Deriving the token RRI for the token that we will will be selling
    token_rri: str = radix.derive.token_rri(
        creator_public_key = wallet.public_key,
        token_symbol = config.token_symbol.lower(),
        network = config.network
    )
    print("Sale is done on token:", token_rri)

    # Getting our current balance of the token that we are selling
    balance: int = wallet.get_account_balances()['total_balance'].get(token_rri, 0)
    print("Current balance of token is:", balance)

    # Iterating over all of the transaction objects from the oldest to the newest. This way, people
    # who sent their XRD first get their tokens first.
    for tx in transactions[::-1]:

        # Ignore the transaction if we have handeled it already
        if tx['hash'] in handeled_transactions_mapping.keys():
            continue

        # Getting all of the "TransferTokens" actions where tokens where sent from another address
        # to our address.
        actions: List[radix.actions.TransferTokens] = list(filter(
            lambda x: isinstance(x, radix.actions.TransferTokens) and x.from_account.address != wallet.address and x.to_account.address == wallet.address, # type: ignore
            tx['actions']
        ))

        # If there are no actions where we get tokens, then ignore this transaction
        if not actions:
            continue

        # Creating the action builder which will be used by this transaction
        tx_action_builder: radix.ActionBuilder = wallet.action_builder

        # Tallying up the tokens sent and their RRIs into an easy to query dictionary. There are two
        # main reasons as to why we're doing this:
        # 1. Just in case somebody sent XRD as well as other tokens to us in a single transaction, 
        #       we want to refund them the other tokens that they've sent.
        # 2. Just in case somebody is sneaky and knows how radix works and tries to send XRD using
        #       multiple actions just to try to break the system.
        # This tokens tally will be used in a way very very similar to how buckets are used in 
        # scrypto where we take the amount of tokens we need and then return the bucket back with
        # whatever that it has
        tokens_tally: Dict[str, int] = {}
        tokens_tally[token_rri] = 0         # Setting this key as well since we're setting the dict keys
        tokens_tally[config.xrd_rri] = 0    # Setting this key as well since we're setting the dict keys
        for action in actions:
            if action.token_rri not in tokens_tally.keys():
                tokens_tally[action.token_rri] = 0
            tokens_tally[action.token_rri] += action.amount

        # Checking how much is the XRD amount sent enough for and refunding the remaining amount
        requested_amount: int = int(tokens_tally.get(config.xrd_rri, 0) / config.token_price_in_atto) * (10**18)
        amount_to_supply: int = min(balance, requested_amount) # Limit the requested amount by the balance
        tokens_tally[config.xrd_rri] -= int(amount_to_supply * radix.derive.xrd_from_atto(config.token_price_in_atto))
        tokens_tally[token_rri] += amount_to_supply 

        # Reduce the balance by the amount that we took
        balance -= tokens_tally[token_rri]

        # Adding the tokens to the action builder of the transaction. At this stage, we have taken
        # the amount of XRD which is owed to us and we're refunding the remaining xrd (whatever
        # amount that might be).
        for rri, amount in tokens_tally.items():
            if amount == 0:
                continue

            tx_action_builder = tx_action_builder.token_transfer(
                from_account_address = wallet.address,
                to_account_address = actions[0].from_account.address,
                token_rri = rri,
                transfer_amount = amount
            )

        # Check if there are actions or not. If there are no actions, then there is no need to 
        # invoke the code that executes the transaction
        if not tx_action_builder.to_action_list():
            continue

        tx_hash: str = wallet.build_sign_and_send_transaction(
            actions = tx_action_builder,
            message_string = "Here are your tokens good sir!",
            encrypt_for_address = actions[0].from_account.address
        )

        handeled_transactions_mapping[tx['hash']] = tx_hash

        # Saving the state to the data file. We are saving the state with each transaction and not
        # just once at the end. This is done to ensure that even if an exception does happen in the
        # middle of the operation of the code, the transactions which have truly already been 
        # handeled are put into the data file.
        with open(config.data_json_file, 'w') as file:
            data: Dict[str, Any] = {
                "handeled_transactions_mapping": handeled_transactions_mapping
            }
            json.dump(data, file)

if __name__ == "__main__":
    main()