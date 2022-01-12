"""
This example script is written to demonstrate how this library can be used
to mint a mutable token. 

This script is written with the assumption that you already have a token which
you have created on Stokenet.
"""

import Radix

def main() -> None:
    # The information of the token which we have created and wish to mint
    token_rri: str = "test_tr1qdra2fdxryvre4vpeg8nlxrghc4fz3hpygsaderd67fqythcek"
    to_address: str = "tdx1qspqqecwh3tgsgz92l4d4f0e4egmfe86049dj75pgq347fkkfmg84pgx9um0v"
    amount: int = 100 * (10 ** 18)      # sending 100 of the test tokens

    # The network parameters as well as the mnemonic phrase to use for the
    # wallet creating the token
    mnemonic_phrase: str = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon"
    network: Radix.Network = Radix.Network.STOKENET

    # Creating a new proider and signer to use to talk to the Radix API
    provider: Radix.Provider = Radix.Provider(network = network)
    signer: Radix.Signer = Radix.Signer.from_mnemonic(mnemonic_phrase)
    wallet_address: str = signer.wallet_address(index = 0, mainnet = True if network is Radix.Network.MAINNET else False)

    # Creating the transaction for the minting of the token
    response: dict = provider.build_transaction(
        actions = Radix.Action.new_token_mint_action(
            to_address = to_address,
            amount = amount,
            rri = token_rri
        ),
        fee_payer = wallet_address,
        message = "0000" + "I have entrust you with 100 of my test tokens. Use them wisely...".encode('utf-8').hex()
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

    print(response)
    tx_id: str = response['result']['txID']
    print("Token have been minted and sent to your recipient under transaction:", tx_id)

if __name__ == "__main__":
    main()