from radixlib.api_types import TokenAmount
from typing import Dict, Any
import unittest

class TestTokenAmount(unittest.TestCase):
    """ Unit tests for the TokenAmount class """

    TokenAmountDict: Dict[Any, Any] = {
        "value": "1000000000000000000",
        "token_identifier": {
            "rri": "radogs_rr1q0dlu7y7zh9vxhpu22env640988932a739n6p6haf3msz2y9nl"
        }
    }

    def test_from_dict(self):
        """ Tests the derivation of the mainnet wallet addresses from the public key """

        # The amount loaded from the dictionary
        amount: TokenAmount = TokenAmount.from_dict(self.TokenAmountDict)

        # Asserting that the TokenAmount object understood the content of the dictionary
        self.assertEqual(amount.rri, self.TokenAmountDict['token_identifier']['rri'])
        self.assertEqual(amount.amount, int(self.TokenAmountDict['value']))

    def test_to_dict(self):
        """ Tests the conversion of the token amount to a dictionary """

        # The amount loaded from the dictionary
        amount: TokenAmount = TokenAmount.from_dict(self.TokenAmountDict)

        self.assertEqual(amount.to_dict(), self.TokenAmountDict)