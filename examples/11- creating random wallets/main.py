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

    # Creating a new wallet object using the signer's ability to instnatiate a new signer object by
    # using a random mnemonic phrase. If you run this code multiple times you will see that the code
    # produces different wallet addresses each time it runs.
    wallet: radix.Wallet = radix.Wallet(
        provider = radix.Provider(network),
        signer = radix.Signer.new_random()
    )
    print("Random wallet address:", wallet.address)

if __name__ == "__main__":
    main()