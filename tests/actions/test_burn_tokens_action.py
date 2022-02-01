from radixlib.actions import BurnTokens
from typing import Dict, Any
import unittest

class TestBurnTokensAction(unittest.TestCase):
    """ Unit tests for the BurnTokens action of mutable tokens """

    ActionDict: Dict[str, Any] = {
        "from_account": {
            "address": "tdx1qspqqecwh3tgsgz92l4d4f0e4egmfe86049dj75pgq347fkkfmg84pgx9um0v"
        },
        "amount": {
            "value": "10000000000000000000",
            "token_identifier": {
                "rri": "mutable_tr1q06dd0ut3qmyp4pqkvmeu2dvkwg5f7vm8yeslwvpkt9qcl5vqu"
            }
        },
        "type": "BurnTokens"
    }

    def test_from_dict(self):
        """ Tests the derivation of the mainnet wallet addresses from the public key """

        # The action loaded from the dictionary
        mint: BurnTokens = BurnTokens.from_dict(self.ActionDict)

        # Asserting that the BurnTokens object understood the content of the dictionary
        self.assertEqual(mint.from_account.address, self.ActionDict['from_account']['address'])
        self.assertEqual(mint.amount, int(self.ActionDict['amount']['value']))
        self.assertEqual(mint.token_rri, self.ActionDict['amount']['token_identifier']['rri'])

    def test_to_dict(self):
        """ Tests the conversion of the token account to a dictionary """

        # The account loaded from the dictionary
        account: BurnTokens = BurnTokens.from_dict(self.ActionDict)

        self.assertEqual(account.to_dict(), self.ActionDict)