"""
This is a parser module and the whole idea behind it is that it allows the parsing of objects from 
Gateway API from their original format into a format that can be easily queried or used in other
operations.

Additional information about each of the parsing operations is presented in the doc string of each
of the functions in this module
"""

from typing import Dict, Any, Optional, List
import radixlib as radix
import dateparser

def parse_account_balances(dictionary: Dict[Any, Any]) -> Dict[str, Dict[str, int]]:
    """ Parses the account balances obtained from the gateway API into an easy to query dictionary.

    This method is used to parse the response from the `get_account_balances` provider method into 
    a format that is easy to query. This method returns a dictionary mapping a string to dictionary 
    of strings and integers. The format that this function returns is as follows::

        {
            "total_balance": {
                "token_rri": "balance of token"
            },
            "staking_balance": {
                "token_rri": "balance of token"
            },
            "liquid_balance": {
                "token_rri": "balance of token"
            }
        }

    Where the main dictionary has three main keys which describe the balances which are staked, 
    liquid, and the total balances. These three keys map to dictionaries that are identical in their
    format where the keys are the RRI of the token and the value mapped to the key is the balance of 
    this token in the account.

    Args:
        dictionary (dict): A dictionary of the data obtained from the gateway API balances query.

    Returns:
        dict: A dictionary of the balance types mapping the token RRIs to their balance values.

    Example::

        >>> from typing import Dict, Any
        >>> api_response: Dict[Any, Any] = {
                "ledger_state": {
                    "version": 77889156,
                    "timestamp": "2022-02-02T12:07:30.204Z",
                    "epoch": 6979,
                    "round": 4136
                },
                "account_balances": {
                    "staked_and_unstaking_balance": {
                        "value": "0",
                        "token_identifier": {
                            "rri": "xrd_rr1qy5wfsfh"
                        }
                    },
                    "liquid_balances": [
                        {
                            "value": "10000000000000000000000",
                            "token_identifier": {
                                "rri": "foton_rr1qwsqw647kcykj562vzvgekfqthjyt4txmqljqv90mp6s74glca"
                            }
                        },
                        {
                            "value": "3000000000000000000",
                            "token_identifier": {
                                "rri": "natty_rr1qwzuvyajquc7jnudcegkjgsjy0u8qcvmljv5mlyma5vqa7jllg"
                            }
                        }
                    ]
                }
            }
        >>> parse_account_balances(api_response)
        {
            "total_balance": {
                "xrd_rr1qy5wfsfh": 2291600000000000000,
                "thing_rr1qv6vd3nslqnuvgjjryx9np3fle7knszq9varrpdzxypquzcj56": 2000000000000000000,
                "foton_rr1qwsqw647kcykj562vzvgekfqthjyt4txmqljqv90mp6s74glca": 10000000000000000000000,
                "radogs_rr1q0dlu7y7zh9vxhpu22env640988932a739n6p6haf3msz2y9nl": 3000000000000000000,
                "natty_rr1qwzuvyajquc7jnudcegkjgsjy0u8qcvmljv5mlyma5vqa7jllg": 3000000000000000000,
                "gnrd_rr1qv0jw6lf83d5q55plnkfcyj8yr3n2epns0zdveudwzyqtm749w": 1000000000000000000
            },
            "staking_balance": {
                "xrd_rr1qy5wfsfh": 0
            },
            "liquid_balance": {
                "foton_rr1qwsqw647kcykj562vzvgekfqthjyt4txmqljqv90mp6s74glca": 10000000000000000000000,
                "natty_rr1qwzuvyajquc7jnudcegkjgsjy0u8qcvmljv5mlyma5vqa7jllg": 3000000000000000000,
                "radogs_rr1q0dlu7y7zh9vxhpu22env640988932a739n6p6haf3msz2y9nl": 3000000000000000000,
                "xrd_rr1qy5wfsfh": 2291600000000000000,
                "thing_rr1qv6vd3nslqnuvgjjryx9np3fle7knszq9varrpdzxypquzcj56": 2000000000000000000,
                "gnrd_rr1qv0jw6lf83d5q55plnkfcyj8yr3n2epns0zdveudwzyqtm749w": 1000000000000000000
            }
        }
    """

    # Processing the balances into an easy to query dictionary format
    final_balances: Dict[str, Dict[str, int]] = {
        "total_balance": {},
        "staking_balance": {},
        "liquid_balance": {},
    }

    final_balances['staking_balance'][dictionary['account_balances']['staked_and_unstaking_balance']['token_identifier']['rri']] = int(dictionary['account_balances']['staked_and_unstaking_balance']['value'])
    for token_balance in dictionary['account_balances']['liquid_balances']:
        final_balances['liquid_balance'][token_balance['token_identifier']['rri']] = int(token_balance['value'])

    unique_rris: List[str] = list(set(list(final_balances['staking_balance'].keys()) + list(final_balances['liquid_balance'].keys())))
    
    for rri in unique_rris:
        balance1: Optional[int] = final_balances['staking_balance'].get(rri)           
        balance2: Optional[int] = final_balances['liquid_balance'].get(rri)     
        final_balances['total_balance'][rri] = (0 if balance1 is None else balance1) + (0 if balance2 is None else balance2)

    return final_balances

def parse_stake_positions(dictionary: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
    """ Parses the stake positions of obtained from the gateway API into an easy to query format.

    This function parses the stake positions obtained from the gateway API into a format that is 
    both easy to query and easy to understand. This function returns a dictionary where the top 
    level keys are of the `pending_stakes` and the `stakes`. These keys maps to a list of values
    where each item is a dictionary that has the address of the validator, and the amount of tokens 
    staked.

    Therefore, the following is a simplified version of the format that the dictionary will be 
    parsed into::

        {
            "pending_stakes": [
                {
                    "validator_address": "address",
                    "amount": {
                        "xrd_rri": "amount"
                    },
                }
            ],
            "stakes": [
                {
                    "validator_address": "address",
                    "amount": {
                        "xrd_rri": "amount"
                    },
                }
            ]
        }

    Args:
        dictionary (dict): A dictionary of the data obtained from the get stakes API query.

    Returns:
        dict: A dictionary of the parsed data in the format given above.

    Example::

        >>> from typing import Dict, Any
        >>> api_response: Dict[Any, Any] = {
                "ledger_state": {
                    "version": 77930031,
                    "timestamp": "2022-02-02T14:32:17.929Z",
                    "epoch": 6983,
                    "round": 4913
                },
                "pending_stakes": [],
                "stakes": [
                    {
                        "validator_identifier": {
                            "address": "rv1q2yamds428pun7eyu6f9e94esczntwwl4s2m5kf8eq9h5ll3ck9jc0537gm"
                        },
                        "delegated_stake": {
                            "value": "3254365975812708718036002",
                            "token_identifier": {
                                "rri": "xrd_rr1qy5wfsfh"
                            }
                        }
                    },
                    {
                        "validator_identifier": {
                            "address": "rv1qdn4mwharah5c3w5sw4zfyagvkftrj47ruwatjfr6z2r7pmvk5uuu84j45v"
                        },
                        "delegated_stake": {
                            "value": "890993293221117900715400",
                            "token_identifier": {
                                "rri": "xrd_rr1qy5wfsfh"
                            }
                        }
                    },
                    {
                        "validator_identifier": {
                            "address": "rv1qw9xrk6e4sgn4hrzp9e2kerpk3ge7jm693pm889yy9w2fxtscz6vqy46epa"
                        },
                        "delegated_stake": {
                            "value": "274488297838357615196244",
                            "token_identifier": {
                                "rri": "xrd_rr1qy5wfsfh"
                            }
                        }
                    },
                    {
                        "validator_identifier": {
                            "address": "rv1qtnwayrqtr0247f7ehhsq8j7rznqe75d88ggx8mf2p55tzd487thuelzs6w"
                        },
                        "delegated_stake": {
                            "value": "274260594596206472684073",
                            "token_identifier": {
                                "rri": "xrd_rr1qy5wfsfh"
                            }
                        }
                    },
                    {
                        "validator_identifier": {
                            "address": "rv1qgsfrh2wrgr3re9gt7wmsv3kswygacflmvyy26yv8nlwwqkpypy4yvj00p6"
                        },
                        "delegated_stake": {
                            "value": "273217841635944587873183",
                            "token_identifier": {
                                "rri": "xrd_rr1qy5wfsfh"
                            }
                        }
                    },
                    {
                        "validator_identifier": {
                            "address": "rv1qt2mpw9j5av508e2f75q2pxhj04m5waerd5eafgrdvkapaxx3v0wxt36584"
                        },
                        "delegated_stake": {
                            "value": "219699734535122599987906",
                            "token_identifier": {
                                "rri": "xrd_rr1qy5wfsfh"
                            }
                        }
                    },
                    {
                        "validator_identifier": {
                            "address": "rv1q2vwh6sde7mv607fdxa3hyyxty3el7h87057cx3qtsr7eyxs97l6v3m5vh2"
                        },
                        "delegated_stake": {
                            "value": "219538303079085541333240",
                            "token_identifier": {
                                "rri": "xrd_rr1qy5wfsfh"
                            }
                        }
                    }
                ]
            }
        >>> parse_stake_positions(api_response)
        {
            "pending_stakes": [],
            "stakes": [
                {
                    "validator_address": "rv1q2yamds428pun7eyu6f9e94esczntwwl4s2m5kf8eq9h5ll3ck9jc0537gm",
                    "amount": {
                        "xrd_rr1qy5wfsfh": 3254365975812708718036002
                    }
                },
                {
                    "validator_address": "rv1qdn4mwharah5c3w5sw4zfyagvkftrj47ruwatjfr6z2r7pmvk5uuu84j45v",
                    "amount": {
                        "xrd_rr1qy5wfsfh": 890993293221117900715400
                    }
                },
                {
                    "validator_address": "rv1qw9xrk6e4sgn4hrzp9e2kerpk3ge7jm693pm889yy9w2fxtscz6vqy46epa",
                    "amount": {
                        "xrd_rr1qy5wfsfh": 274488297838357615196244
                    }
                },
                {
                    "validator_address": "rv1qtnwayrqtr0247f7ehhsq8j7rznqe75d88ggx8mf2p55tzd487thuelzs6w",
                    "amount": {
                        "xrd_rr1qy5wfsfh": 274260594596206472684073
                    }
                },
                {
                    "validator_address": "rv1qgsfrh2wrgr3re9gt7wmsv3kswygacflmvyy26yv8nlwwqkpypy4yvj00p6",
                    "amount": {
                        "xrd_rr1qy5wfsfh": 273217841635944587873183
                    }
                },
                {
                    "validator_address": "rv1qt2mpw9j5av508e2f75q2pxhj04m5waerd5eafgrdvkapaxx3v0wxt36584",
                    "amount": {
                        "xrd_rr1qy5wfsfh": 219699734535122599987906
                    }
                },
                {
                    "validator_address": "rv1q2vwh6sde7mv607fdxa3hyyxty3el7h87057cx3qtsr7eyxs97l6v3m5vh2",
                    "amount": {
                        "xrd_rr1qy5wfsfh": 219538303079085541333240
                    }
                }
            ]
        }
    """

    return {
        key: list(map(lambda x: dict([
            ('validator_address', x['validator_identifier']['address']),
            ('amount', {
                x['delegated_stake']['token_identifier']['rri']: int(x['delegated_stake']['value'])
            })
        ]), value))
        for key, value 
        in dictionary.items()
        if key in ['pending_stakes', 'stakes']
    }
    
def parse_unstake_positions(dictionary: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
    """ Parses the stake positions of obtained from the gateway API into an easy to query format.

    This function parses the unstake positions obtained from the gateway API into a format that is 
    both easy to query and easy to understand. This function returns a dictionary where the top 
    level keys are of the `pending_unstakes` and the `unstakes`. These keys maps to a list of values
    where each item is a dictionary that has the address of the validator, and the amount of tokens 
    unstaked.

    Therefore, the following is a simplified version of the format that the dictionary will be 
    parsed into::

        {
            "pending_unstakes": [
                {
                    "validator_address": "address",
                    "amount": {
                        "xrd_rri": "amount"
                    },
                    "epochs_until_unlocked": "amount"
                }
            ],
            "unstakes": [
                {
                    "validator_address": "address",
                    "amount": {
                        "xrd_rri": "amount"
                    },
                    "epochs_until_unlocked": "amount"
                }
            ]
        }

    Args:
        dictionary (dict): A dictionary of the data obtained from the get unstakes API query.

    Returns:
        dict: A dictionary of the parsed data in the format given above.
    """

    return {
        key: list(map(lambda x: dict([
            ('validator_address', x['validator_identifier']['address']),
            ('amount', {
                x['delegated_stake']['token_identifier']['rri']: int(x['delegated_stake']['value'])
            }),
            ('epochs_until_unlocked', x['epochs_until_unlocked']),
        ]), value))
        for key, value 
        in dictionary.items()
        if key in ['pending_unstakes', 'unstakes']
    }
    
def parse_account_transactions(dictionary: Dict[str, Any]) -> List[Dict[str, Any]]:
    """ Parses the account transactions obtained from the Gateway API into an easy to query format.

    The main purpose behind this parse function is to parse the transaction information obtained 
    from the gateway API into an easy to query and easy to understand format that is consistent all
    throughout. In the original format, a key value pair is removed if the value is ``null``. But,
    in this format a key value pair would be present even if its value is none.

    The parses parses the transaction dictionary into a list of dictionaries where each dictionary 
    contains information about a transaction. The format that they will be in can be described by 
    the following::

        [
            {
                "hash": "tx_hash",
                "status": "tx_status",
                "confirmed_time": "datetime",
                "actions": [],
                "fee_paid": {
                    "xrd_rri": "amount"
                },
                "transaction_blob": "blob",
                "message_blob": "blob"
            }
        ]

    Args:
        dictionary (dict): A dictionary of the data obtained from the get account transactions API 
            query.

    Returns:
        dict: A dictionary of the parsed data in the format given above.

    Example::

        >>> from typing import Dict, Any
        >>> api_response: Dict[str, Any] = {
            "ledger_state": {
                "version": 52830617,
                "timestamp": "2022-02-03T08:00:38.088Z",
                "epoch": 5217,
                "round": 5786
            },
            "total_count": 61,
            "next_cursor": "eyJ2Ijo1MjQwOTc5Mn0=",
            "transactions": [
                {
                "transaction_status": {
                    "status": "CONFIRMED",
                    "confirmed_time": "2022-02-02T15:30:32.561Z",
                    "ledger_state_version": 52632033
                },
                "transaction_identifier": {
                    "hash": "67d3970dc69096b54f78fef5a47bebfe813c5c68bf47df3bf13adc0cb8c209da"
                },
                "actions": [
                    {
                    "to_account": {
                        "address": "tdx1qspqqecwh3tgsgz92l4d4f0e4egmfe86049dj75pgq347fkkfmg84pgx9um0v"
                    },
                    "amount": {
                        "value": "1",
                        "token_identifier": {
                        "rri": "ttx_tr1qdxxveg4ywhmh6jm2n6n0c4qy9chl6elz6w94praects8wst0j"
                        }
                    },
                    "type": "MintTokens"
                    }
                ],
                "fee_paid": {
                    "value": "62200000000000000",
                    "token_identifier": {
                    "rri": "xrd_tr1qyf0x76s"
                    }
                },
                "metadata": {
                    "hex": "07ba27358d12113705fbd7e40b1c0d0af6d78123f604c3b87fb342735a7f1102dc000000000100210000000000000000000000000000000000000000000000000000dcfa92090780000200450600040200670ebc5688204557eadaa5f9ae51b4e4fa7d4ad97a8140235f26d64ed07a850100000000000000000000000000000000000000000000002f4919aa585b3d00000002005f0600040200670ebc5688204557eadaa5f9ae51b4e4fa7d4ad97a8140235f26d64ed07a85034c66651523afbbea5b54f537e2a021717feb3f169c5a847dce170000000000000000000000000000000000000000000000000000000000000001000b01b90dbb66eaec143ff554ac14ad96e4f56bb7d6f6abc89e6d5009e4698fa14287f57d62f12c0550e243570ec0e56398297d9f64b578c49cad513c5b910f902528"
                }
                },
                {
                "transaction_status": {
                    "status": "CONFIRMED",
                    "confirmed_time": "2022-02-02T15:29:07.203Z",
                    "ledger_state_version": 52631775
                },
                "transaction_identifier": {
                    "hash": "ba27358d12113705fbd7e40b1c0d0af6d78123f604c3b87fb342735a7f1102dc"
                },
                "actions": [
                    {
                    "token_properties": {
                        "name": "ttx",
                        "description": "",
                        "icon_url": "",
                        "url": "",
                        "symbol": "ttx",
                        "is_supply_mutable": True,
                        "granularity": "1",
                        "owner": {
                        "address": "tdx1qspqqecwh3tgsgz92l4d4f0e4egmfe86049dj75pgq347fkkfmg84pgx9um0v"
                        }
                    },
                    "token_supply": {
                        "value": "0",
                        "token_identifier": {
                        "rri": "ttx_tr1qdxxveg4ywhmh6jm2n6n0c4qy9chl6elz6w94praects8wst0j"
                        }
                    },
                    "type": "CreateTokenDefinition"
                    },
                    {
                    "to_account": {
                        "address": "tdx1qspqqecwh3tgsgz92l4d4f0e4egmfe86049dj75pgq347fkkfmg84pgx9um0v"
                    },
                    "amount": {
                        "value": "1",
                        "token_identifier": {
                        "rri": "ttx_tr1qdxxveg4ywhmh6jm2n6n0c4qy9chl6elz6w94praects8wst0j"
                        }
                    },
                    "type": "MintTokens"
                    }
                ],
                "fee_paid": {
                    "value": "100106400000000000000",
                    "token_identifier": {
                    "rri": "xrd_tr1qyf0x76s"
                    }
                },
                "metadata": {
                    "hex": "07af6c771c06119466d7157cb9880d44369999d984a86f8049cc4e033df2110a2800000000010021000000000000000000000000000000000000000000000000056d416069df2a00000200450600040200670ebc5688204557eadaa5f9ae51b4e4fa7d4ad97a8140235f26d64ed07a850100000000000000000000000000000000000000000000002f49f6a4ea64448000000100040274747809003f54347c2a10a8f09efd8398ed4b259909a3f848cc9fa05ca20e225f8bfb1d2d1a00000000034c66651523afbbea5b54f537e2a021717feb3f169c5a847dce170200600400034c66651523afbbea5b54f537e2a021717feb3f169c5a847dce17000000000000000000000000000000000000000000000000000000000000000101010200670ebc5688204557eadaa5f9ae51b4e4fa7d4ad97a8140235f26d64ed07a8502002d0500034c66651523afbbea5b54f537e2a021717feb3f169c5a847dce17000374747800037474780000000000000002005f0600040200670ebc5688204557eadaa5f9ae51b4e4fa7d4ad97a8140235f26d64ed07a85034c66651523afbbea5b54f537e2a021717feb3f169c5a847dce170000000000000000000000000000000000000000000000000000000000000001000b0153abada20de95f18edef283317a490822fff29c056818d0700a1a408123ba26d757299331a1d0abc59402898767db9fae7e014023da94b1defbcab3234e3c29e"
                }
                }
            ]}
        >>> parse_account_transactions(api_response)
        [
            {
                "hash": "67d3970dc69096b54f78fef5a47bebfe813c5c68bf47df3bf13adc0cb8c209da",
                "status": "CONFIRMED",
                "confirmed_time": datetime.datetime(2022, 2, 2, 15, 30, 32, 561000, tzinfo=<StaticTzInfo "Z">),
                "actions": [
                    <radixlib.actions.mint_tokens.MintTokens at 0x107ff3a90>
                ],
                "fee_paid": {
                    "xrd_tr1qyf0x76s": 62200000000000000
                },
                "transaction_blob": "07ba27358d12113705fbd7e40b1c0d0af6d78123f604c3b87fb342735a7f1102dc000000000100210000000000000000000000000000000000000000000000000000dcfa92090780000200450600040200670ebc5688204557eadaa5f9ae51b4e4fa7d4ad97a8140235f26d64ed07a850100000000000000000000000000000000000000000000002f4919aa585b3d00000002005f0600040200670ebc5688204557eadaa5f9ae51b4e4fa7d4ad97a8140235f26d64ed07a85034c66651523afbbea5b54f537e2a021717feb3f169c5a847dce170000000000000000000000000000000000000000000000000000000000000001000b01b90dbb66eaec143ff554ac14ad96e4f56bb7d6f6abc89e6d5009e4698fa14287f57d62f12c0550e243570ec0e56398297d9f64b578c49cad513c5b910f902528",
                "message_blob": None
            },
            {
                "hash": "ba27358d12113705fbd7e40b1c0d0af6d78123f604c3b87fb342735a7f1102dc",
                "status": "CONFIRMED",
                "confirmed_time": datetime.datetime(2022, 2, 2, 15, 29, 7, 203000, tzinfo=<StaticTzInfo "Z">),
                "actions": [
                    <radixlib.actions.create_token_definition.CreateTokenDefinition at 0x106b4e8f0>,
                    <radixlib.actions.mint_tokens.MintTokens at 0x107ff38e0>
                ],
                "fee_paid": {
                    "xrd_tr1qyf0x76s": 100106400000000000000
                },
                "transaction_blob": "07af6c771c06119466d7157cb9880d44369999d984a86f8049cc4e033df2110a2800000000010021000000000000000000000000000000000000000000000000056d416069df2a00000200450600040200670ebc5688204557eadaa5f9ae51b4e4fa7d4ad97a8140235f26d64ed07a850100000000000000000000000000000000000000000000002f49f6a4ea64448000000100040274747809003f54347c2a10a8f09efd8398ed4b259909a3f848cc9fa05ca20e225f8bfb1d2d1a00000000034c66651523afbbea5b54f537e2a021717feb3f169c5a847dce170200600400034c66651523afbbea5b54f537e2a021717feb3f169c5a847dce17000000000000000000000000000000000000000000000000000000000000000101010200670ebc5688204557eadaa5f9ae51b4e4fa7d4ad97a8140235f26d64ed07a8502002d0500034c66651523afbbea5b54f537e2a021717feb3f169c5a847dce17000374747800037474780000000000000002005f0600040200670ebc5688204557eadaa5f9ae51b4e4fa7d4ad97a8140235f26d64ed07a85034c66651523afbbea5b54f537e2a021717feb3f169c5a847dce170000000000000000000000000000000000000000000000000000000000000001000b0153abada20de95f18edef283317a490822fff29c056818d0700a1a408123ba26d757299331a1d0abc59402898767db9fae7e014023da94b1defbcab3234e3c29e",
                "message_blob": None
            },
        ]
    """

    return [
        {
            "hash": tx_info['transaction_identifier']['hash'],
            "status": tx_info['transaction_status']['status'],
            "confirmed_time": dateparser.parse(tx_info['transaction_status']['confirmed_time']),
            "actions": list(map(
                lambda x: getattr(radix.actions, x['type']).from_dict(x), 
                tx_info['actions']
            )),
            "fee_paid": {
                tx_info['fee_paid']['token_identifier']['rri']: int(tx_info['fee_paid']['value'])
            },
            "transaction_blob": tx_info['metadata']['hex'],
            "message_blob": tx_info['metadata'].get('message'),
        }
        for tx_info
        in dictionary['transactions']
    ]

def parse_token_info(dictionary: Dict[str, Any]) -> Dict[str, Any]:
    """ Parses token information into an easy to query format with little repetition.
    
    This function is used to parse the token information obtained from the gateway API into a format
    that is both easy to query. This parser works for all token info endpoints which means that this
    parser may be used for the native token info and also for other tokens. An example of the format
    that this function returns is::

        {
            "rri": "token_rri",
            "total_supply": "amount"
            "total_minted": "amount"
            "total_burned": "amount"
            "name": "token_name"
            "description": "token_description",
            "icon_url": "token_icon_url",
            "url": "token_url",
            "symbol": "token_symbol",
            "is_supply_mutable": "token_is_supply_mutable",
            "granularity": "token_granularity",
        }

    Args:
        dictionary (dict): A dictionary of the data obtained from the get token info query.
    
    Returns:
        dict: A dictionary of the parsed data in the format given above.

    Example::

        >>> from typing import Dict, Any
        >>> api_response: Dict[str, Any] = {
            "ledger_state": {
                "version": 52835220,
                "timestamp": "2022-02-03T08:23:36.863Z",
                "epoch": 5218,
                "round": 476
            },
            "token": {
                "token_identifier": {
                    "rri": "xrd_tr1qyf0x76s"
                },
                "token_supply": {
                    "value": "34117069948058000000000000000",
                    "token_identifier": {
                        "rri": "xrd_tr1qyf0x76s"
                    }
                },
                "info": {
                    "total_minted": {
                        "value": "34117249903139400000000000000",
                        "token_identifier": {
                            "rri": "xrd_tr1qyf0x76s"
                        }
                    },
                    "total_burned": {
                        "value": "179955081400000000000000",
                        "token_identifier": {
                            "rri": "xrd_tr1qyf0x76s"
                        }
                    }
                },
                "token_properties": {
                    "name": "Radix (Stokenet)",
                    "description": "Stokenet-only native tokens, used to pay the Radix Stokenet network's required transaction fees and for other testing.",
                    "icon_url": "https://assets.radixdlt.com/icons/icon-xrd-32x32.png",
                    "url": "https://stokenet-explorer.radixdlt.com/",
                    "symbol": "xrd",
                    "is_supply_mutable": true,
                    "granularity": "1"
                }
            }
        }
        >>> parse_token_info(api_response)
        {
            "rri": "xrd_tr1qyf0x76s",
            "total_supply": 34117069948058000000000000000,
            "total_minted": 34117249903139400000000000000,
            "total_burned": 179955081400000000000000,
            "name": "Radix (Stokenet)",
            "description": "Stokenet-only native tokens, used to pay the Radix Stokenet network's required transaction fees and for other testing.",
            "icon_url": "https://assets.radixdlt.com/icons/icon-xrd-32x32.png",
            "url": "https://stokenet-explorer.radixdlt.com/",
            "symbol": "xrd",
            "is_supply_mutable": true,
            "granularity": 1
        }
    """

    return {
        "rri": dictionary['token']['token_identifier']['rri'],
        "total_supply": int(dictionary['token']['token_supply']['value']),
        "total_minted": int(dictionary['token']['info']['total_minted']['value']),
        "total_burned": int(dictionary['token']['info']['total_burned']['value']),
        "name": dictionary['token']['token_properties']['name'],
        "description": dictionary['token']['token_properties']['description'],
        "icon_url": dictionary['token']['token_properties']['icon_url'],
        "url": dictionary['token']['token_properties']['url'],
        "symbol": dictionary['token']['token_properties']['symbol'],
        "is_supply_mutable": bool(dictionary['token']['token_properties']['is_supply_mutable']),
        "granularity": int(dictionary['token']['token_properties']['granularity']),
    }

def parse_validator_info(dictionary: Dict[str, Any]) -> Dict[str, Any]:
    """ Parses the validator information obtained from the validator info endpoint of the gateway
    API.

    This function parses the validator info into the following format::

        {
            "validator_address": "address",
            "stake": {
                "xrd_rri": "amount"
            },
            "owner_stake": {
                "xrd_rri": "amount"
            },
            "uptime": {
                "epoch_range": {
                    "from": "from_epoch",
                    "to": "to_epoch"
                },
                "uptime_percentage": "uptime_percentage",
                "proposals_missed": "proposals_missed",
                "proposals_completed": "proposals_completed"
            },
            "url": "url",
            "validator_fee_percentage": "validator_fee_percentage",
            "name": "name",
            "registered": "registered",
            "owner_account_address": "owner_account_address",
            "external_stake_accepted": "external_stake_accepted",
        }

    Args:
        dictionary (dict): A dictionary of the data obtained from the get validator info endpoint.
    
    Returns:
        dict: A dictionary of the parsed data in the format given above.

    Example::

        >>> from typing import Dict, Any
        >>> api_response: Dict[str, Any] = {
            "ledger_state": {
                "version": 78231180,
                "timestamp": "2022-02-03T08:40:47.724Z",
                "epoch": 7013,
                "round": 5278
            },
            "validator": {
                "validator_identifier": {
                    "address": "rv1qt36awal5325xja4a8du2repzl5pm8gxus6l8kehq3ng5u36mw7yzzt6msd"
                },
                "stake": {
                    "value": "56863236398215061270779132",
                    "token_identifier": {
                        "rri": "xrd_rr1qy5wfsfh"
                    }
                },
                "info": {
                    "owner_stake": {
                        "value": "1128498487867411109396584",
                        "token_identifier": {
                            "rri": "xrd_rr1qy5wfsfh"
                        }
                    },
                    "uptime": {
                        "epoch_range": {
                            "from": 6513,
                            "to": 7013
                        },
                        "uptime_percentage": 90.42,
                        "proposals_missed": 11138,
                        "proposals_completed": 105128
                    }
                },
                "properties": {
                    "url": "https://viskositystaking.com",
                    "validator_fee_percentage": 1.0,
                    "name": "Viskosity Staking",
                    "registered": true,
                    "owner_account_identifier": {
                        "address": "rdx1qspxucylmhup732069sszrer2j3klah47kq8jsm8pfeh0lsslqqap8swhc2m4"
                    },
                    "external_stake_accepted": true
                }
            }
        }
        >>> parse_validator_info(api_response)
        {
            "validator_address": "rv1qt36awal5325xja4a8du2repzl5pm8gxus6l8kehq3ng5u36mw7yzzt6msd",
            "stake": {
                "xrd_rr1qy5wfsfh": 56863236398215061270779132
            },
            "owner_stake": {
                "xrd_rr1qy5wfsfh": 1128498487867411109396584
            },
            "uptime": {
                "epoch_range": {
                    "from": 6513,
                    "to": 7013
                },
                "uptime_percentage": 90.43,
                "proposals_missed": 11138,
                "proposals_completed": 105197
            },
            "url": "https://viskositystaking.com",
            "validator_fee_percentage": 1.0,
            "name": "Viskosity Staking",
            "registered": true,
            "owner_account_address": "rdx1qspxucylmhup732069sszrer2j3klah47kq8jsm8pfeh0lsslqqap8swhc2m4",
            "external_stake_accepted": true
        }
    """

    return {
        "validator_address": dictionary['validator']['validator_identifier']['address'],
        "stake": {
            dictionary['validator']['stake']['token_identifier']['rri']: int(dictionary['validator']['stake']['value'])
        },
        "owner_stake": {
            dictionary['validator']['info']['owner_stake']['token_identifier']['rri']: int(dictionary['validator']['info']['owner_stake']['value'])
        },
        "uptime": dictionary['validator']['info']['uptime'],
        "url": dictionary['validator']['properties']['url'],
        "validator_fee_percentage": dictionary['validator']['properties']['validator_fee_percentage'],
        "name": dictionary['validator']['properties']['name'],
        "registered": bool(dictionary['validator']['properties']['registered']),
        "owner_account_address": dictionary['validator']['properties']['owner_account_identifier']['address'],
        "external_stake_accepted": dictionary['validator']['properties']['external_stake_accepted'],
    }

def parse_transaction_status(dictionary: Dict[str, Any]) -> Dict[str, Any]:
    """ Parses the account transactions obtained from the Gateway API into an easy to query format.

    The main purpose behind this parse function is to parse the transaction information obtained 
    from the gateway API into an easy to query and easy to understand format that is consistent all
    throughout. In the original format, a key value pair is removed if the value is ``null``. But,
    in this format a key value pair would be present even if its value is none.

    The parses parses the transaction dictionary into a list of dictionaries where each dictionary 
    contains information about a transaction. The format that they will be in can be described by 
    the following::

        {
            "hash": "tx_hash",
            "status": "tx_status",
            "confirmed_time": "datetime",
            "actions": [],
            "fee_paid": {
                "xrd_rri": "amount"
            },
            "transaction_blob": "blob",
            "message_blob": "blob"
        }

    Args:
        dictionary (dict): A dictionary of the data obtained from the get account transactions API 
            query.

    Returns:
        dict: A dictionary of the parsed data in the format given above.

    Example::

        >>> from typing import Dict, Any
        >>> api_response: Dict[str, Any] = {
            "ledger_state": {
                "version": 52830617,
                "timestamp": "2022-02-03T08:00:38.088Z",
                "epoch": 5217,
                "round": 5786
            },
            "transaction": {
                "transaction_status": {
                    "status": "CONFIRMED",
                    "confirmed_time": "2022-02-02T15:30:32.561Z",
                    "ledger_state_version": 52632033
                },
                "transaction_identifier": {
                    "hash": "67d3970dc69096b54f78fef5a47bebfe813c5c68bf47df3bf13adc0cb8c209da"
                },
                "actions": [
                    {
                    "to_account": {
                        "address": "tdx1qspqqecwh3tgsgz92l4d4f0e4egmfe86049dj75pgq347fkkfmg84pgx9um0v"
                    },
                    "amount": {
                        "value": "1",
                        "token_identifier": {
                        "rri": "ttx_tr1qdxxveg4ywhmh6jm2n6n0c4qy9chl6elz6w94praects8wst0j"
                        }
                    },
                    "type": "MintTokens"
                    }
                ],
                "fee_paid": {
                    "value": "62200000000000000",
                    "token_identifier": {
                    "rri": "xrd_tr1qyf0x76s"
                    }
                },
                "metadata": {
                    "hex": "07ba27358d12113705fbd7e40b1c0d0af6d78123f604c3b87fb342735a7f1102dc000000000100210000000000000000000000000000000000000000000000000000dcfa92090780000200450600040200670ebc5688204557eadaa5f9ae51b4e4fa7d4ad97a8140235f26d64ed07a850100000000000000000000000000000000000000000000002f4919aa585b3d00000002005f0600040200670ebc5688204557eadaa5f9ae51b4e4fa7d4ad97a8140235f26d64ed07a85034c66651523afbbea5b54f537e2a021717feb3f169c5a847dce170000000000000000000000000000000000000000000000000000000000000001000b01b90dbb66eaec143ff554ac14ad96e4f56bb7d6f6abc89e6d5009e4698fa14287f57d62f12c0550e243570ec0e56398297d9f64b578c49cad513c5b910f902528"
                }
            }
        >>> parse_transaction_status(api_response)
        {
            "hash": "67d3970dc69096b54f78fef5a47bebfe813c5c68bf47df3bf13adc0cb8c209da",
            "status": "CONFIRMED",
            "confirmed_time": datetime.datetime(2022, 2, 2, 15, 30, 32, 561000, tzinfo=<StaticTzInfo "Z">),
            "actions": [
                <radixlib.actions.mint_tokens.MintTokens at 0x107ff3a90>
            ],
            "fee_paid": {
                "xrd_tr1qyf0x76s": 62200000000000000
            },
            "transaction_blob": "07ba27358d12113705fbd7e40b1c0d0af6d78123f604c3b87fb342735a7f1102dc000000000100210000000000000000000000000000000000000000000000000000dcfa92090780000200450600040200670ebc5688204557eadaa5f9ae51b4e4fa7d4ad97a8140235f26d64ed07a850100000000000000000000000000000000000000000000002f4919aa585b3d00000002005f0600040200670ebc5688204557eadaa5f9ae51b4e4fa7d4ad97a8140235f26d64ed07a85034c66651523afbbea5b54f537e2a021717feb3f169c5a847dce170000000000000000000000000000000000000000000000000000000000000001000b01b90dbb66eaec143ff554ac14ad96e4f56bb7d6f6abc89e6d5009e4698fa14287f57d62f12c0550e243570ec0e56398297d9f64b578c49cad513c5b910f902528",
            "message_blob": None
        }
    """

    return {
        "hash": dictionary['transaction']['transaction_identifier']['hash'],
        "status": dictionary['transaction']['transaction_status']['status'],
        "confirmed_time": dateparser.parse(dictionary['transaction']['transaction_status']['confirmed_time']),
        "actions": list(map(
            lambda x: getattr(radix.actions, x['type']).from_dict(x), 
            dictionary['transaction']['actions']
        )),
        "fee_paid": {
            dictionary['transaction']['fee_paid']['token_identifier']['rri']: int(dictionary['transaction']['fee_paid']['value'])
        },
        "transaction_blob": dictionary['transaction']['metadata']['hex'],
        "message_blob": dictionary['transaction']['metadata'].get('message'),
    }