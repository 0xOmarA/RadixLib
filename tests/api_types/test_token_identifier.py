from radixlib.api_types.identifiers import TokenIdentifier
from typing import Dict, Any
import unittest

class TestTokenIdentifier(unittest.TestCase):
    """ Unit tests for the TokenIdentifier class """

    TokenIdentifierDict: Dict[Any, Any] = {
        "rri": "radogs_rr1q0dlu7y7zh9vxhpu22env640988932a739n6p6haf3msz2y9nl"
    }

    def test_from_dict(self):
        """ Tests the derivation of the mainnet wallet addresses from the public key """

        # The amount loaded from the dictionary
        amount: TokenIdentifier = TokenIdentifier.from_dict(self.TokenIdentifierDict)

        # Asserting that the TokenIdentifier object understood the content of the dictionary
        self.assertEqual(amount.rri, self.TokenIdentifierDict['rri'])

    def test_to_dict(self):
        """ Tests the conversion of the token amount to a dictionary """

        # The amount loaded from the dictionary
        amount: TokenIdentifier = TokenIdentifier.from_dict(self.TokenIdentifierDict)

        self.assertEqual(amount.to_dict(), self.TokenIdentifierDict)