
import os
from typing import Dict, Any

import mnemonic
import radixlib
from radixlib.network import *
from radixlib.provider import *


def new_random() -> 'Signer':
        """ Creates a new signer object from a random mnemonic phrase """
        return radixlib.Signer.from_mnemonic(mnemonic.Mnemonic('english').generate(128))

def main() -> None:
   # Getting the mnemonic phrase for the wallet that we will be connecting to. In this case, my 
    # mnemonic phrase is stored in an environment variable under the name "MNEMONIC_PHRASE". 
    # You might want to do the same or you could also just put your mnemonic phrase as a literal 
    # string. 
    mnemonic_phrase: str = os.environ['MNEMONIC_PHRASE']
    if mnemonic_phrase is None:
        print("please set $MNEMONIC_PHRASE environment variable first.") 
    
    network = STOKENET
    signer: radixlib.Signer = radixlib.Signer.from_mnemonic(mnemonic_phrase)
    # wallet: radixlib.Wallet = radixlib.Wallet(Provider(STOKENET), signer, 1)
    print("0:", signer.wallet_address(network, 0))
    print("1:", signer.wallet_address(network, 1))
    print("2:", signer.wallet_address(network, 2))
    print("3:", signer.wallet_address(network, 3))
    print("10000:", signer.wallet_address(network, 10000))

if __name__ == "__main__":
     main()
