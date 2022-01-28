import radixlib as radix
import unittest


class TestDerive(unittest.TestCase):
    """ Unit tests for the derive functions """

    def test_mainnet_address_from_public_key(self):
        """ Tests the derivation of the mainnet wallet addresses from the public key """

        # The wallet address we expect to get from the derivation
        expected_wallet_address: str = "rdx1qspz8wslrhhch7lfw0mukwv386608purn3v4sa62k7wq6m4nv2xejrcmqcvl2"
        
        # The public key used for the wallet address derivation
        pub_key: str = "0223ba1f1def8bfbe973f7cb39913eb4f387839c5958774ab79c0d6eb3628d990f"
        derived_wallet_address: str = radix.derive.wallet_address_from_public_key(
            pub_key, 
            radix.network.MAINNET
        )

        self.assertEqual(derived_wallet_address, expected_wallet_address)
    
    def test_stokenet_address_from_public_key(self):
        """ Tests the derivation of the stokenet wallet addresses from the public key """

        # The wallet address we expect to get from the derivation
        expected_wallet_address: str = "tdx1qspz8wslrhhch7lfw0mukwv386608purn3v4sa62k7wq6m4nv2xejrc6vd70f"
        
        # The public key used for the wallet address derivation
        pub_key: str = "0223ba1f1def8bfbe973f7cb39913eb4f387839c5958774ab79c0d6eb3628d990f"
        derived_wallet_address: str = radix.derive.wallet_address_from_public_key(
            pub_key, 
            radix.network.STOKENET
        )

        self.assertEqual(derived_wallet_address, expected_wallet_address)

    def test_public_key_from_wallet_address(self):
        """ Tests the derivation of the public key from a wallet address """

        # The expected public key form the derivation
        expected_pub_key: str = "0223ba1f1def8bfbe973f7cb39913eb4f387839c5958774ab79c0d6eb3628d990f"

        # The wallet addresses which will be used for the derivation of the public key
        mainnet_address: str = "rdx1qspz8wslrhhch7lfw0mukwv386608purn3v4sa62k7wq6m4nv2xejrcmqcvl2"
        stokenet_address: str = "tdx1qspz8wslrhhch7lfw0mukwv386608purn3v4sa62k7wq6m4nv2xejrc6vd70f"

        derived_mainnet_public_key: str = radix.derive.public_key_from_wallet_address(mainnet_address)
        derived_stokenet_public_key: str = radix.derive.public_key_from_wallet_address(stokenet_address)

        self.assertEqual(set([expected_pub_key]), set([derived_mainnet_public_key, derived_stokenet_public_key]))

    def test_stokenet_from_mainnet(self):
        """ Tests the derivation of stokenet wallet addresses from the mainnet addresses """

        # The stokenet and mainnet wallet addresses
        mainnet_address: str = "rdx1qspz8wslrhhch7lfw0mukwv386608purn3v4sa62k7wq6m4nv2xejrcmqcvl2"
        stokenet_address: str = "tdx1qspz8wslrhhch7lfw0mukwv386608purn3v4sa62k7wq6m4nv2xejrc6vd70f"

        # Derive the stokenet address
        derived_stokenet_address: str = radix.derive.wallet_address_on_other_network(
            wallet_address = mainnet_address,
            network = radix.network.STOKENET
        )

        self.assertEqual(derived_stokenet_address, stokenet_address)

    def test_mainnet_from_stokenet(self):
        """ Tests the derivation of mainnet wallet addresses from the stokenet addresses """

        # The stokenet and mainnet wallet addresses
        mainnet_address: str = "rdx1qspz8wslrhhch7lfw0mukwv386608purn3v4sa62k7wq6m4nv2xejrcmqcvl2"
        stokenet_address: str = "tdx1qspz8wslrhhch7lfw0mukwv386608purn3v4sa62k7wq6m4nv2xejrc6vd70f"

        # Derive the mainnet address
        derived_mainnet_address: str = radix.derive.wallet_address_on_other_network(
            wallet_address = stokenet_address,
            network = radix.network.MAINNET
        )

        self.assertEqual(derived_mainnet_address, mainnet_address)

    def test_token_rri_derivation(self):
        """ Tests the derivation of Token RRIs """

        # The parameters of the new token
        creator_public_key: str = "0200670ebc5688204557eadaa5f9ae51b4e4fa7d4ad97a8140235f26d64ed07a85"
        token_symbol: str = "HMSTR"

        # The expected RRI from the derivation
        expected_rri: str = "hmstr_tr1q0qnazjs66mu4wvekxnj0l8u25ljle8xj0w3uux5f0hq9d59tg"

        # The derived RRi
        derived_rri: str = radix.derive.token_rri(
            creator_public_key = creator_public_key,
            token_symbol = token_symbol,
            network = radix.network.STOKENET
        )

        self.assertEqual(derived_rri, expected_rri)