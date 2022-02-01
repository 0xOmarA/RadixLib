from radixlib.api_types.identifiers import TransactionIdentifier
from typing import Dict
import unittest

class TestTransactionIdentifier(unittest.TestCase):
    """ Unit tests for the TransactionIdentifier class """

    TransactionIdentifierDict: Dict[str, str] = {
        "hash": "b3332fdfc74537d2e56d67635ac14154a21bc14669a7ac33078df0261ff8a061"
    }

    def test_from_dict(self):
        """ Tests the derivation of the mainnet wallet addresses from the public key """

        # The tx_id loaded from the dictionary
        tx_id: TransactionIdentifier = TransactionIdentifier.from_dict(self.TransactionIdentifierDict)

        # Asserting that the TransactionIdentifier object understood the content of the dictionary
        self.assertEqual(tx_id.hash, self.TransactionIdentifierDict['hash'])

    def test_to_dict(self):
        """ Tests the conversion of the token tx_id to a dictionary """

        # The tx_id loaded from the dictionary
        tx_id: TransactionIdentifier = TransactionIdentifier.from_dict(self.TransactionIdentifierDict)

        self.assertEqual(tx_id.to_dict(), self.TransactionIdentifierDict)