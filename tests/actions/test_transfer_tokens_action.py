from radixlib.actions import TransferTokens
from typing import Dict, Any
import unittest

class TestTransferTokensAction(unittest.TestCase):
    """ Unit tests for the TransferTokens action of mutable tokens """

    ActionDict: Dict[str, Any] = {
        "from_account": {
            "address": "tdx1qspqqecwh3tgsgz92l4d4f0e4egmfe86049dj75pgq347fkkfmg84pgx9um0v"
        },
        "to_account": {
            "address": "tdx1qspsl85c9cpgm8t906zewv66quyg6d4gdlru2q9ujgk0u66c8kw2t6caan5qa"
        },
        "amount": {
            "value": "100000000000000000000",
            "token_identifier": {
                "rri": "xrd_tr1qyf0x76s"
            }
        },
        "type": "TransferTokens"
    }

    def test_from_dict(self):
        """ Tests the derivation of the mainnet wallet addresses from the public key """

        # The action loaded from the dictionary
        mint: TransferTokens = TransferTokens.from_dict(self.ActionDict)

        # Asserting that the TransferTokens object understood the content of the dictionary
        self.assertEqual(mint.to_account.address, self.ActionDict['to_account']['address'])
        self.assertEqual(mint.from_account.address, self.ActionDict['from_account']['address'])
        self.assertEqual(mint.amount, int(self.ActionDict['amount']['value']))
        self.assertEqual(mint.token_rri, self.ActionDict['amount']['token_identifier']['rri'])

    def test_to_dict(self):
        """ Tests the conversion of the token account to a dictionary """

        # The account loaded from the dictionary
        account: TransferTokens = TransferTokens.from_dict(self.ActionDict)

        self.assertEqual(account.to_dict(), self.ActionDict)