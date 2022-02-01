from radixlib.api_types.identifiers import AccountIdentifier
from typing import Dict
import unittest

class TestAccountIdentifier(unittest.TestCase):
    """ Unit tests for the AccountIdentifier class """

    AccountIdentifierDict: Dict[str, str] = {
        "address": "rdx1qspffuaqpulrtc7ka6zp45kgmwxmujzmrupu8w3rpt384su3ck3svns5enyqq"
    }

    def test_from_dict(self):
        """ Tests the derivation of the mainnet wallet addresses from the public key """

        # The account loaded from the dictionary
        account: AccountIdentifier = AccountIdentifier.from_dict(self.AccountIdentifierDict)

        # Asserting that the AccountIdentifier object understood the content of the dictionary
        self.assertEqual(account.address, self.AccountIdentifierDict['address'])

    def test_to_dict(self):
        """ Tests the conversion of the token account to a dictionary """

        # The account loaded from the dictionary
        account: AccountIdentifier = AccountIdentifier.from_dict(self.AccountIdentifierDict)

        self.assertEqual(account.to_dict(), self.AccountIdentifierDict)