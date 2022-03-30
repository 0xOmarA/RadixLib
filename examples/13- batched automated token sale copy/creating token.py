import radixlib as radix
import config # This is the local config file we get the token info from

def main() -> None:
    # Creating the wallet object from the mnemonic and the network specified in the config file
    wallet: radix.Wallet = radix.Wallet(
        provider = radix.Provider(config.network),
        signer = radix.Signer.from_mnemonic(config.mnemonic_phrase)
    )

    # Creating the token and getting the transaction hash for the creation transaction
    tx_hash: str = wallet.build_sign_and_send_transaction(
        actions = (
            wallet.action_builder
                .new_fixed_supply_token(
                    owner_address = wallet.address,
                    name = config.token_name,
                    symbol = config.token_symbol,
                    description = config.token_description,
                    icon_url = config.token_icon_url,
                    url = config.token_url,
                    granularity = 1,
                    token_supply = config.token_supply,
                    to_account_address = wallet.address
                )
        ),
    )
    print(f"Token creation in transaction: {tx_hash}")

if __name__ == "__main__":
    main()