from radixlib.identifiers import AccountIdentifier, ValidatorIdentifier, TokenIdentifier, NetworkIdentifier
from typing import Dict
import unittest


class TestIdentifiers(unittest.TestCase):
    """ Unit tests for the derive functions """

    def test_account_identifier_to_dict(self):
        """ Tests the conversion of an AccountIdentifier to a dictionary """

        identifier: AccountIdentifier = AccountIdentifier(
            address = "rdx1qspz8wslrhhch7lfw0mukwv386608purn3v4sa62k7wq6m4nv2xejrcmqcvl2"
        )
        expected_dict: Dict[str, str] = {
            "address": "rdx1qspz8wslrhhch7lfw0mukwv386608purn3v4sa62k7wq6m4nv2xejrcmqcvl2"
        }

        self.assertEqual(identifier.to_dict(), expected_dict)
    
    def test_account_identifier_from_dict(self):
        """ Tests the conversion of an AccountIdentifier to a dictionary """

        dictionary: Dict[str, str] = {
            "address": "rdx1qspz8wslrhhch7lfw0mukwv386608purn3v4sa62k7wq6m4nv2xejrcmqcvl2"
        }
        identifier: AccountIdentifier = AccountIdentifier(
            address = "rdx1qspz8wslrhhch7lfw0mukwv386608purn3v4sa62k7wq6m4nv2xejrcmqcvl2"
        )

        self.assertEqual(identifier, AccountIdentifier.from_dict(dictionary))

    def test_network_identifier_to_dict(self):
        """ Tests the conversion of an NetworkIdentifier to a dictionary """

        identifier: NetworkIdentifier = NetworkIdentifier(
            network = "mainnet"
        )
        expected_dict: Dict[str, str] = {
            "network": "mainnet"
        }

        self.assertEqual(identifier.to_dict(), expected_dict)
    
    def test_network_identifier_from_dict(self):
        """ Tests the conversion of an NetworkIdentifier to a dictionary """

        dictionary: Dict[str, str] = {
            "network": "mainnet"
        }
        identifier: NetworkIdentifier = NetworkIdentifier(
            network = "mainnet"
        )

        self.assertEqual(identifier, NetworkIdentifier.from_dict(dictionary))

    def test_token_identifier_to_dict(self):
        """ Tests the conversion of an TokenIdentifier to a dictionary """

        identifier: TokenIdentifier = TokenIdentifier(
            rri = "tdx1qspz8wslrhhch7lfw0mukwv386608purn3v4sa62k7wq6m4nv2xejrc6vd70f"
        )
        expected_dict: Dict[str, str] = {
            "rri": "tdx1qspz8wslrhhch7lfw0mukwv386608purn3v4sa62k7wq6m4nv2xejrc6vd70f"
        }

        self.assertEqual(identifier.to_dict(), expected_dict)
    
    def test_token_identifier_from_dict(self):
        """ Tests the conversion of an TokenIdentifier to a dictionary """

        dictionary: Dict[str, str] = {
            "rri": "tdx1qspz8wslrhhch7lfw0mukwv386608purn3v4sa62k7wq6m4nv2xejrc6vd70f"
        }
        identifier: TokenIdentifier = TokenIdentifier(
            rri = "tdx1qspz8wslrhhch7lfw0mukwv386608purn3v4sa62k7wq6m4nv2xejrc6vd70f"
        )

        self.assertEqual(identifier, TokenIdentifier.from_dict(dictionary))

    def test_validator_identifier_to_dict(self):
        """ Tests the conversion of an ValidatorIdentifier to a dictionary """

        identifier: ValidatorIdentifier = ValidatorIdentifier(
            address = "rv1qtk9m8tew537g7z6mp0nqlms889hdd2xtx75fwwvag067gtwtqkkg7eqgxe"
        )
        expected_dict: Dict[str, str] = {
            "address": "rv1qtk9m8tew537g7z6mp0nqlms889hdd2xtx75fwwvag067gtwtqkkg7eqgxe"
        }

        self.assertEqual(identifier.to_dict(), expected_dict)
    
    def test_validator_identifier_from_dict(self):
        """ Tests the conversion of an ValidatorIdentifier to a dictionary """

        dictionary: Dict[str, str] = {
            "address": "rv1qtk9m8tew537g7z6mp0nqlms889hdd2xtx75fwwvag067gtwtqkkg7eqgxe"
        }
        identifier: ValidatorIdentifier = ValidatorIdentifier(
            address = "rv1qtk9m8tew537g7z6mp0nqlms889hdd2xtx75fwwvag067gtwtqkkg7eqgxe"
        )

        self.assertEqual(identifier, ValidatorIdentifier.from_dict(dictionary))
    