from radixlib.actions import CreateTokenDefinition
from typing import Dict, Any
import unittest

class TestMutableTokenAction(unittest.TestCase):
    """ Unit tests for the CreateTokenDefinition action of mutable tokens """

    ActionDict: Dict[str, Any] = {
        "token_properties": {
            "name": "MutableTest",
            "description": "An amazing new token with great utility!",
            "icon_url": "https://www.google.com/",
            "url": "https://www.google.com/",
            "symbol": "mutable",
            "is_supply_mutable": True,
            "granularity": "1",
            "owner": {
                "address": "tdx1qspqqecwh3tgsgz92l4d4f0e4egmfe86049dj75pgq347fkkfmg84pgx9um0v"
            }
        },
        "token_supply": {
            "value": "0",
            "token_identifier": {
                "rri": "mutable_tr1q06dd0ut3qmyp4pqkvmeu2dvkwg5f7vm8yeslwvpkt9qcl5vqu"
            }
        },
        "type": "CreateTokenDefinition"
    }

    def test_from_dict(self):
        """ Tests the derivation of the mainnet wallet addresses from the public key """

        # The action loaded from the dictionary
        creation: CreateTokenDefinition = CreateTokenDefinition.from_dict(self.ActionDict)

        # Asserting that the CreateTokenDefinition object understood the content of the dictionary
        self.assertEqual(creation.name, self.ActionDict['token_properties']['name'])
        self.assertEqual(creation.description, self.ActionDict['token_properties']['description'])
        self.assertEqual(creation.icon_url, self.ActionDict['token_properties']['icon_url'])
        self.assertEqual(creation.url, self.ActionDict['token_properties']['url'])
        self.assertEqual(creation.symbol, self.ActionDict['token_properties']['symbol'])
        self.assertEqual(creation.is_supply_mutable, self.ActionDict['token_properties']['is_supply_mutable'])
        self.assertEqual(creation.granularity, int(self.ActionDict['token_properties']['granularity']))
        self.assertEqual(creation.owner.address, self.ActionDict['token_properties']['owner']['address'])

        self.assertEqual(creation.token_supply, int(self.ActionDict['token_supply']['value']))
        self.assertEqual(creation.token_rri, self.ActionDict['token_supply']['token_identifier']['rri'])
        self.assertEqual(creation.to_account, None)

    def test_to_dict(self):
        """ Tests the conversion of the token account to a dictionary """

        # The account loaded from the dictionary
        account: CreateTokenDefinition = CreateTokenDefinition.from_dict(self.ActionDict)

        self.assertEqual(account.to_dict(), self.ActionDict)