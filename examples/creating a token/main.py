""" 
This script is written to demonstrate how this library can help create a 
new token on the Radix blockchain through the provided methods and functions.
"""

from typing import Dict
import Radix

def main() -> None:
    # The parameters which we would like to use for the token creation
    token_name: str = "TestToken"
    token_symbol: str = "test"
    token_description: str = "A new test token I'm creating on Radix to test how tokens work on Radix"
    token_supply: int = 5000 * (10 ** 18) # 5000 tokens

    # The network parameters as well as the mnemonic phrase to use for the
    # wallet creating the token
    mnemonic_phrase: str = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon"
    network: Radix.Network = Radix.Network.STOKENET

    # Creating a new proider and signer to use to talk to the Radix API
    provider: Radix.Provider = Radix.Provider(network = network)
    signer: Radix.Signer = Radix.Signer.from_mnemonic(mnemonic_phrase)
    wallet_address: str = signer.wallet_address( index = 0, mainnet = True if network is Radix.Network.MAINNET else False )

    # Getting the balance of XRD to ensure that we have enoguh to create
    # a new token on the radix ledger.
    balances: dict = provider.get_balances(address = wallet_address).json()['result']

    balances_dict: Dict[str, int] = {
        token_info['rri']: int(token_info['amount'])
        for token_info in balances['tokenBalances']
    }

    atto_balance: int = balances_dict.get(Radix.NetworkSpecificConstants.XRD[network])
    atto_balance: int = 0 if atto_balance is None else atto_balance
    xrd_balance: float = Radix.utils.atto_to_xrd(atto_balance)

    if xrd_balance < 100:
        raise ValueError(f"Radix requires that the creator of a token put forth 100 XRD when creating a new token on the Raidx ledger. However, you only have an XRD balance of {xrd_balance}. Please read the following article for more information on the pricing on Radix: https://learn.radixdlt.com/article/how-do-transaction-fees-work-on-radix-are-they-burned")

    # If the user has enough XRD for the operation of creating a new token then we can
    # continue to the creation of the token.
    response: dict = provider.build_transaction(
        actions = [Radix.Action.new_create_fixed_token_action(
            to_address = wallet_address,
            public_key_of_signer = signer.public_key(),
            symbol = token_symbol,
            name = token_name,
            description = token_description,
            icon_url = "https://qph.fs.quoracdn.net/main-qimg-e5af1b9582725db08148d48bb7c5d3da",
            token_url = "https://www.google.com",
            supply = token_supply
        )],
        fee_payer = wallet_address,
    ).json()

    if 'error' in response.keys():
        raise Exception(f"An error has occured when building the transaction: {response['error']}")

    # Getting the blob which needs to be signed and signing it using the signer object
    blob: str = response['result']['transaction']['blob']
    hash_of_blob_to_sign: str = response['result']['transaction']['hashOfBlobToSign']
    signed_data: str = signer.sign(hash_of_blob_to_sign)

    # Submit the transaction to the blockchain, thus creating the token 
    response: dict = provider.finalize_transaction(
        blob = blob,
        signature_der = signed_data,
        public_key_of_signer = signer.public_key(),
        immediateSubmit = True
    ).json()

    if 'error' in response.keys():
        raise Exception(f"An error has occured when finalizing the transaction: {response['error']}")

    tx_id: str = response['result']['transaction']['txID']
    print("Token has been created in transaction:", tx_id)
    
    # Calculating the token RRI through the token parameters
    token_rri: str = Radix.utils.calculate_token_rri(
        creator_public_key = signer.public_key(),
        token_symbol = token_symbol,
        network = network
    )
    print(f"Your token has been created and has been given the RRI: {token_rri}")

if __name__ == '__main__':
    main()