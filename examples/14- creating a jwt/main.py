"""
RadixLib allows for signers to create JWTs which are signed with the signer's private key and can be
validated using the public key of the account. Something like this can be used in a number of ways
such as a simple messaging protocol where the receiver of the message wants to ensure that a certain
Radix address did indeed send the given message. 
"""

from typing import Dict, Any
import radixlib as radix
import os

def main() -> None:
    # Getting the mnemonic phrase for the wallet that we will be connecting to. In this case, my 
    # mnemonic phrase is stored in an environment variable under the name "MNEMONIC_PHRASE". 
    # You might want to do the same or you could also just put your mnemonic phrase as a literal 
    # string. 
    mnemonic_phrase: str = os.environ['MNEMONIC_PHRASE']

    # Creating a new signer from the mnemonic phrase
    signer: radix.Signer = radix.Signer.from_mnemonic(mnemonic_phrase)

    # We can now use the above created signer to create a JSON Web Token with any arbitrary payload
    # that we wish to include in the token. In this case, we include some information on a 
    # hypothetical token sale.
    jwt: str = signer.create_jwt({
        "order": "buy 1 SCORP",
        "before": "1667820406"
    })

    # ----------------------------------------------------------------------------------------------
    # From this point onward we act as the receiver of the message who wishes to read and verify it.
    # ----------------------------------------------------------------------------------------------

    # Getting the JWT payload and printing it
    payload: Dict[Any, Any] = radix.utils.decode_jwt(jwt)
    print("Payload:", payload)

    # Getting the public key included in the payload. By default JWTs created using RadixLib include
    # the public key of the creator in the payload. Therefore, 
    public_key: str = payload['public_key']
    print("Sender's Public Key:", public_key)

    # Verifying that the public key in the payload was indeed the real sender of the message
    is_real_sender: bool = radix.utils.verify_jwt(jwt, public_key)
    print(f"Did {public_key} send the message?", 'Yes.' if is_real_sender else 'No.')

    # Checking if some other public key was the sender of the message
    is_real_sender: bool = radix.utils.verify_jwt(jwt, signer.public_key(1))
    print(f"Did {signer.public_key(1)} send the message?", 'Yes.' if is_real_sender else 'No.')
    
    # Checking if some other public key was the sender of the message
    is_real_sender: bool = radix.utils.verify_jwt(jwt, signer.public_key(2))
    print(f"Did {signer.public_key(2)} send the message?", 'Yes.' if is_real_sender else 'No.')

if __name__ == "__main__":
    main()