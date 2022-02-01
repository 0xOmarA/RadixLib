import radixlib as radix
import unittest
import os

class TestSigner(unittest.TestCase):
    """ Unit tests for the Signer class """

    # The mnemonic phrase which will be used throughout the signer tests. The mnemonic phrase that 
    # you see here is not of an active wallet or a real wallet. This is the mnemonic phrase a random
    # empty wallet. Do not bother checking what it has or doesn't have.
    MNEMONIC_PHRASE: str = "confirm few beach hamster betray catalog thank wine fish identify brick educate"
    PASSWORD: str = "MySuperStrongPassword"

    def test_public_key(self):
        """ Tests the signer class to ensure that it generates correct public keys. """

        # The public key we're expecting to see derived from the mnemonic phrase
        expected_pub_key: str = "0223ba1f1def8bfbe973f7cb39913eb4f387839c5958774ab79c0d6eb3628d990f"

        signer: radix.Signer = radix.Signer.from_mnemonic(self.MNEMONIC_PHRASE)
        self.assertEqual(signer.public_key(), expected_pub_key)

    def test_private_key(self):
        """ Tests the signer class to ensure that it generates correct private keys. """

        # The private key we're expecting to see derived from the mnemonic phrase
        expected_priv_key: str = "965de1f0fb9fec4cf2f77ae173d92b0034f7ea57682634084b6287e8c2b2db37"

        signer: radix.Signer = radix.Signer.from_mnemonic(self.MNEMONIC_PHRASE)
        self.assertEqual(signer.private_key(), expected_priv_key)

    def test_public_key_acc_index(self):
        """ Test the signer class for the generation of public keys for higher account indexes. """

        # The account index to test for and the expected public key
        account_index: int = 12
        expected_pub_key: str = "02c11234408bc331ec2356f9c14d5381f55e96fdada81dbbf98566a804d5c5ed65"

        signer: radix.Signer = radix.Signer.from_mnemonic(self.MNEMONIC_PHRASE)
        self.assertEqual(signer.public_key(index = account_index), expected_pub_key)

    def test_private_key_acc_index(self):
        """ Test the signer class for the generation of private keys for higher account indexes. """

        # The account index to test for and the expected private key
        account_index: int = 12
        expected_pub_key: str = "35b9c46ea7c944f05d1545503f2ac85fd37961a7e6df64ea1d0c81d93c1939e0"

        signer: radix.Signer = radix.Signer.from_mnemonic(self.MNEMONIC_PHRASE)
        self.assertEqual(signer.private_key(index = account_index), expected_pub_key)

    def test_old_wallet_json_load(self):
        """ Test the loading of the old wallet.json file by the signer class """

        # Loading up the content of the wallet.json file
        script_path: str = os.path.dirname(os.path.realpath(__file__))
        signer: radix.Signer = radix.Signer.from_wallet_json(
            wallet_json_path = os.path.join(script_path, 'old wallet.json'),
            passphrase = self.PASSWORD
        )

        # The private key we're expecting to see derived from the wallet.json file
        expected_priv_key: str = "965de1f0fb9fec4cf2f77ae173d92b0034f7ea57682634084b6287e8c2b2db37"

        self.assertEqual(signer.private_key(), expected_priv_key)

    def test_new_wallet_json_load(self):
        """ Test the loading of the old wallet.json file by the signer class """

        # Loading up the content of the wallet.json file
        script_path: str = os.path.dirname(os.path.realpath(__file__))
        signer: radix.Signer = radix.Signer.from_wallet_json(
            wallet_json_path = os.path.join(script_path, 'new wallet.json'),
            passphrase = self.PASSWORD
        )

        # The private key we're expecting to see derived from the wallet.json file
        expected_priv_key: str = "6b7a90c556a41b37fc7af7dee21fcf39be44a0b201ae6350ea98f7258765109b"

        self.assertEqual(signer.private_key(), expected_priv_key)

    def test_wallet_address_derivation(self):
        """ Tests the ability of the signer to derive the wallet address """

        # Loading up the signer object to use for the operation
        signer: radix.Signer = radix.Signer.from_mnemonic(self.MNEMONIC_PHRASE)

        # The expected resulting address from the operation
        expected_address: str = "rdx1qspz8wslrhhch7lfw0mukwv386608purn3v4sa62k7wq6m4nv2xejrcmqcvl2"

        self.assertEqual(signer.wallet_address(radix.network.MAINNET), expected_address)