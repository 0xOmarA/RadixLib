"""
One of the things which you might find yourself needing to do at some point of time is to create a 
new wallet which has a new random wallet address. The signer class has a functionality which allows
you to create a signer from a random mnemonic phrase to make it easier for you to develop apps which
require you to use random wallet addresses.
"""

import radixlib as radix

def main() -> None:
    # Defining the network that we will be connecting to.
    network: radix.network.Network = radix.network.STOKENET

    # Creating a new signer object using the signer's ability to instnatiate a new signer object by
    # using a random mnemonic phrase. If you run this code multiple times you will see that the code
    # produces different wallet addresses each time it runs.
    signer: radix.Signer = radix.Signer.new_random()
    print('Signer seed:', signer.seed)

    # Create the wallet from the signer object and print the wallet address
    wallet: radix.Wallet = radix.Wallet(
        provider = radix.Provider(network),
        signer = signer
    )
    print("Random wallet address:", wallet.address)

if __name__ == "__main__":
    main()