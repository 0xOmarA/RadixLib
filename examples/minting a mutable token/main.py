"""
This example script is written to demonstrate how this library can be used
to mint a mutable token. 

This script is written with the assumption that you already have a token which
you have created on Stokenet.
"""

def main() -> None:
    # The information of the token which we have created and wish to mint
    token_rri: str = "example_rri"
    to_address: str = "tdx1qspqqecwh3tgsgz92l4d4f0e4egmfe86049dj75pgq347fkkfmg84pgx9um0v"
    amount: int = 100 * (10 ** 18) # sending 100 of the test tokens

if __name__ == "__main__":
    main()