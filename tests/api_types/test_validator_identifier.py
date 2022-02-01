from radixlib.api_types.identifiers import ValidatorIdentifier
from typing import Dict
import unittest

class TestValidatorIdentifier(unittest.TestCase):
    """ Unit tests for the ValidatorIdentifier class """

    ValidatorIdentifierDict: Dict[str, str] = {
        "address": "AMadeUpAddress"
    }

    def test_from_dict(self):
        """ Tests the derivation of the mainnet wallet addresses from the public key """

        # The validator loaded from the dictionary
        validator: ValidatorIdentifier = ValidatorIdentifier.from_dict(self.ValidatorIdentifierDict)

        # Asserting that the ValidatorIdentifier object understood the content of the dictionary
        self.assertEqual(validator.address, self.ValidatorIdentifierDict['address'])

    def test_to_dict(self):
        """ Tests the conversion of the token validator to a dictionary """

        # The validator loaded from the dictionary
        validator: ValidatorIdentifier = ValidatorIdentifier.from_dict(self.ValidatorIdentifierDict)

        self.assertEqual(validator.to_dict(), self.ValidatorIdentifierDict)