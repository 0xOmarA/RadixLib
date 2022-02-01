from radixlib.api_types.identifiers import NetworkIdentifier
from typing import Dict
import unittest

class TestNetworkIdentifier(unittest.TestCase):
    """ Unit tests for the NetworkIdentifier class """

    NetworkIdentifierDict: Dict[str, str] = {
        "network": "mainnet"
    }

    def test_from_dict(self):
        """ Tests the derivation of the mainnet wallet addresses from the public key """

        # The network loaded from the dictionary
        network: NetworkIdentifier = NetworkIdentifier.from_dict(self.NetworkIdentifierDict)

        # Asserting that the NetworkIdentifier object understood the content of the dictionary
        self.assertEqual(network.network, self.NetworkIdentifierDict['network'])

    def test_to_dict(self):
        """ Tests the conversion of the token network to a dictionary """

        # The network loaded from the dictionary
        network: NetworkIdentifier = NetworkIdentifier.from_dict(self.NetworkIdentifierDict)

        self.assertEqual(network.to_dict(), self.NetworkIdentifierDict)