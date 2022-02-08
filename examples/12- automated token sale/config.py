import radixlib as radix
import os

# The path of this script
script_path: str = os.path.dirname(os.path.realpath(__file__))

# The path that the data.json file is stored at
data_json_file: str = os.path.join(script_path, 'data.json')
""" The path to the data.json file which is a file used to store the state of the program in terms 
of which transactions has the script handeled so far so that they may be ignored on subsequent runs.

In addition to a list of the payment transactions that have been handeled so far, the data.json file
stores a list of all of the response transactions that this system has sent whether its sending 
tokens back or sending a refund back. This is stored in the ``handeled_transactions_mapping`` key
value pair of the dictionary; where this specific dictionary (refering to 
``handeled_transactions_mapping``) has the following format::

    {
        "tx_hash_of_tx_we_received": "tx_hash_of_tx_we_sent_back"
    }
"""

# The network to use for the automated token sale and a quick variable used to store the RRI of the
# xrd token on the specified network
network: radix.network.Network = radix.network.STOKENET
xrd_rri: str = radix.derive.xrd_rri_on_network(network)

# The mnemonic phrase of the wallet that we will be using to listen for transactions.
mnemonic_phrase: str = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon"

# The information of the token that we will be sending. In this example, we're using bitcoin and its
# information as the imaginary token that we will be sending.
token_name: str = "bitcoin"
token_symbol: str = "btc"
token_description: str = "Bitcoin uses peer-to-peer technology to operate with no central authority or banks."
token_icon_url: str = "https://upload.wikimedia.org/wikipedia/commons/9/9a/BTC_Logo.svg"
token_url: str = "https://bitcoin.org/en/"
token_granularity: int = 1
token_supply: int = 1_000_000_000 * (10**18) # The token supply is 1 billion tokens

# The following is information needed for the sale of the tokens
token_price_in_atto: int = radix.derive.atto_from_xrd(20) # One token costs 20 XRD.