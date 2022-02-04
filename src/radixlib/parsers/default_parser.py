from typing import Callable, Optional, Dict, Any, List
from radixlib.parsers.base_parser import ParserBase
import radixlib as radix
import dateparser

class DefaultParser(ParserBase):
    """ A default parser used to parse the responses of the gateway API into a format that is easy
    to query
    """

    @classmethod
    def parse(
        cls,
        data: Any,
        data_type: str
    ) -> Any:
        """ Routes the parsing of the data to the appropriate parsing function from within the class

        This function acts as a router which tires to find the appropriate parsing function within 
        the class to parse the data. If no parser is implemented for this data type, then the 
        original data is returned without any parsing.

        Args:
            data (Any): Data of any type to pass to the parser function
            data_type (str): Type of the data or the origin of the data

        Returns:
            Any: The parsed data
        """

        # Getting the parsing function for this data type from the attributes of the class
        function_name: str = f'parse_{data_type}'
        parsing_function: Optional[Callable[..., Any]] = getattr(cls, function_name, None)

        # We try calling the parsing function with the data that we have. If the parsing function 
        # works, then we return the parsed data. However, if a TypeError or NotImplementedError is
        # raised, then we return the original data
        try:
            parsed_data: Any = parsing_function(data) # type: ignore
            return parsed_data if parsed_data is not None else data
        except (TypeError, NotImplementedError):
            return data

    @classmethod
    def parse_get_gateway_info(cls, data: Dict[str, Any]) -> Any:
        """ A function used for the parsing of the get_gateway_info API calls. 
        
        This parser function produces output in the following format::

            {
                "network_identifier": {
                    "network": "mainnet"
                },
                "gateway_api": {
                    "version": "1.0.1",
                    "open_api_schema_version": "1.0.3"
                },
                "ledger_state": {
                    "version": 78345123,
                    "timestamp": "2022-02-03T15:24:35.866Z",
                    "epoch": 7024,
                    "round": 8910
                },
                "target_ledger_state": {
                    "version": 78345127
                }
            }

        Args:
            data (dict): A dictionary of the data to parse.

        Returns:
            dict: A dictionary of the parsed data.
        """
        # No parsing is needed in this case, the default format the data is given in is easy to 
        # query.
        raise NotImplementedError("No implementation for the parse_get_gateway_info")
    
    @classmethod
    def parse_derive_account_identifier(cls, data: Dict[str, Dict[str, str]]) -> str:
        """ A function used for the parsing of the derive_account_identifier API calls. 
        
        Args:
            data (dict): A dictionary of the data to parse.

        Returns:
            str: A string of the derived account address.
        """
        return data['account_identifier']['address']
    
    @classmethod
    def parse_get_account_balances(cls, data: Dict[Any, Any]) -> Dict[str, Dict[str, int]]:
        """ A function used for the parsing of the get_account_balances API calls. 
        
        This parser function produces output in the following format::

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

        Args:
            data (dict): A dictionary of the data to parse.

        Returns:
            dict: A dictionary of the parsed data.
        """

        # Processing the balances into an easy to query dictionary format
        final_balances: Dict[str, Dict[str, int]] = {
            "total_balance": {},
            "staking_balance": {},
            "liquid_balance": {},
        }

        final_balances['staking_balance'][data['account_balances']['staked_and_unstaking_balance']['token_identifier']['rri']] = int(data['account_balances']['staked_and_unstaking_balance']['value'])
        for token_balance in data['account_balances']['liquid_balances']:
            final_balances['liquid_balance'][token_balance['token_identifier']['rri']] = int(token_balance['value'])

        unique_rris: List[str] = list(set(list(final_balances['staking_balance'].keys()) + list(final_balances['liquid_balance'].keys())))
        
        for rri in unique_rris:
            balance1: Optional[int] = final_balances['staking_balance'].get(rri)           
            balance2: Optional[int] = final_balances['liquid_balance'].get(rri)     
            final_balances['total_balance'][rri] = (0 if balance1 is None else balance1) + (0 if balance2 is None else balance2)

        return final_balances
    
    @classmethod
    def parse_get_stake_positions(cls, data: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        """ A function used for the parsing of the get_stake_positions API calls. 
        
        This parser function produces output in the following format::

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
            data (dict): A dictionary of the data to parse.

        Returns:
            dict: A dictionary of the parsed data.
        """

        return {
            key: list(map(lambda x: dict([
                ('validator_address', x['validator_identifier']['address']),
                ('amount', {
                    x['delegated_stake']['token_identifier']['rri']: int(x['delegated_stake']['value'])
                })
            ]), value))
            for key, value 
            in data.items()
            if key in ['pending_stakes', 'stakes']
        }
    
    @classmethod
    def parse_get_unstake_positions(cls, data: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        """ A function used for the parsing of the get_unstake_positions API calls. 
        
        This parser function produces output in the following format::

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
            data (dict): A dictionary of the data to parse.

        Returns:
            dict: A dictionary of the parsed data.
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
            in data.items()
            if key in ['pending_unstakes', 'unstakes']
        }
    
    @classmethod
    def parse_get_account_transactions(cls, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """ A function used for the parsing of the get_account_transactions API calls. 
        
        This parser function produces output in the following format::

            [
                {
                    "hash": data['transaction']['transaction_identifier']['hash'],
                    "status": data['transaction']['transaction_status']['status'],
                    "confirmed_time": dateparser.parse(data['transaction']['transaction_status']['confirmed_time']),
                    "actions": list(map(
                        lambda x: getattr(radix.actions, x['type']).from_dict(x), 
                        data['transaction']['actions']
                    )),
                    "fee_paid": {
                        data['transaction']['fee_paid']['token_identifier']['rri']: int(data['transaction']['fee_paid']['value'])
                    },
                    "transaction_blob": data['transaction']['metadata']['hex'],
                    "message_blob": data['transaction']['metadata'].get('message'),
                }
            ]

        Args:
            data (dict): A dictionary of the data to parse.

        Returns:
            dict: A dictionary of the parsed data.
        """

        return list(map(
            lambda x: cls.parse({'transaction': x}, 'transaction_status'),
            data['transactions']
        ))
    
    @classmethod
    def parse_get_native_token_info(cls, data: Any) -> Any:
        """ A function used for the parsing of the get_native_token_info API calls. 
        
        This parser function produces output in the following format::

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
            data (dict): A dictionary of the data to parse.

        Returns:
            dict: A dictionary of the parsed data.
        """

        return cls.parse(data, 'get_token_info')
    
    @classmethod
    def parse_get_token_info(cls, data: Any) -> Any:
        """ A function used for the parsing of the get_token_info API calls. 
        
        This parser function produces output in the following format::

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
            data (dict): A dictionary of the data to parse.

        Returns:
            dict: A dictionary of the parsed data.
        """

        return {
            "rri": data['token']['token_identifier']['rri'],
            "total_supply": int(data['token']['token_supply']['value']),
            "total_minted": int(data['token']['info']['total_minted']['value']),
            "total_burned": int(data['token']['info']['total_burned']['value']),
            "name": data['token']['token_properties']['name'],
            "description": data['token']['token_properties']['description'],
            "icon_url": data['token']['token_properties']['icon_url'],
            "url": data['token']['token_properties']['url'],
            "symbol": data['token']['token_properties']['symbol'],
            "is_supply_mutable": bool(data['token']['token_properties']['is_supply_mutable']),
            "granularity": int(data['token']['token_properties']['granularity']),
        }
    
    @classmethod
    def parse_derive_token_identifier(cls, data: Dict[str, Dict[str, str]]) -> str:
        """ A function used for the parsing of the derive_token_identifier API calls. 
        
        Args:
            data (dict): A dictionary of the data to parse.

        Returns:
            str: A string of the token RRI
        """
        return data['token_identifier']['rri']
    
    @classmethod
    def parse_get_validator(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """ A function used for the parsing of the get_validator API calls. 
        
        This parser function produces output in the following format::

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
            data (dict): A dictionary of the data to parse.

        Returns:
            dict: A dictionary of the parsed data.
        """

        return {
            "validator_address": data['validator']['validator_identifier']['address'],
            "stake": {
                data['validator']['stake']['token_identifier']['rri']: int(data['validator']['stake']['value'])
            },
            "owner_stake": {
                data['validator']['info']['owner_stake']['token_identifier']['rri']: int(data['validator']['info']['owner_stake']['value'])
            },
            "uptime": data['validator']['info']['uptime'],
            "url": data['validator']['properties']['url'],
            "validator_fee_percentage": data['validator']['properties']['validator_fee_percentage'],
            "name": data['validator']['properties']['name'],
            "registered": bool(data['validator']['properties']['registered']),
            "owner_account_address": data['validator']['properties']['owner_account_identifier']['address'],
            "external_stake_accepted": data['validator']['properties']['external_stake_accepted'],
        }
    
    @classmethod
    def parse_get_validator_identifier(cls, data: Dict[str, Dict[str, str]]) -> str:
        """ A function used for the parsing of the get_validator_identifier API calls. 

        Args:
            data (dict): A dictionary of the data to parse.

        Returns:
            str: A string of the validator address
        """

        return data['validator_identifier']['address']
    
    @classmethod
    def parse_get_validators(cls, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """ A function used for the parsing of the get_validators API calls. 
        
        This parser function produces output in the following format::

            [
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
            ]

        Args:
            data (dict): A dictionary of the data to parse.

        Returns:
            dict: A dictionary of the parsed data.
        """

        return list(map(
            lambda x: cls.parse({'validator': x}, 'get_validator'),
            data['validators']
        ))
    
    @classmethod
    def parse_get_transaction_rules(cls, data: Any) -> Any:
        """ A function used for the parsing of the get_transaction_rules API calls. 
        
        This parser function produces output in the following format::

            {

            }

        Args:
            data (dict): A dictionary of the data to parse.

        Returns:
            dict: A dictionary of the parsed data.
        """
    
    @classmethod
    def parse_build_transaction(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """ A function used for the parsing of the build_transaction API calls. 
        
        This parser function produces output in the following format::

            {
                "fee": {
                    "xrd_rri": "amount"
                },
                "unsigned_transaction": "transaction_blob",
                "payload_to_sign": "payload_blob"
            }

        Args:
            data (dict): A dictionary of the data to parse.

        Returns:
            dict: A dictionary of the parsed data.
        """

        return {
            "fee": {
                data['transaction_build']['fee']['token_identifier']['rri']: int(data['transaction_build']['fee']['value'])
            },
            "unsigned_transaction": data['transaction_build']['unsigned_transaction'],
            "payload_to_sign": data['transaction_build']['payload_to_sign'],
        }
    
    @classmethod
    def parse_finalize_transaction(cls, data: Dict[str, Any]) -> Dict[str, str]:
        """ A function used for the parsing of the finalize_transaction API calls. 
        
        This parser function produces output in the following format::

            {
                "signed_transaction": "transaction_blob",
                "transaction_hash": "hash"
            }

        Args:
            data (dict): A dictionary of the data to parse.

        Returns:
            dict: A dictionary of the parsed data.
        """

        return {
            "signed_transaction": data['signed_transaction'],
            "transaction_hash": data['transaction_identifier']['hash']
        }
    
    @classmethod
    def parse_submit_transaction(cls, data: Dict[str, Dict[str, str]]) -> str:
        """ A function used for the parsing of the submit_transaction API calls. 
        
        Args:
            data (dict): A dictionary of the data to parse.

        Returns:
            str: A string of the transaction hash
        """

        return data['transaction_identifier']['hash']
    
    @classmethod
    def parse_transaction_status(cls, data: Any) -> Any:
        """ A function used for the parsing of the transaction_status API calls. 
        
        This parser function produces output in the following format::

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
            data (dict): A dictionary of the data to parse.

        Returns:
            dict: A dictionary of the parsed data.
        """

        return {
            "hash": data['transaction']['transaction_identifier']['hash'],
            "status": data['transaction']['transaction_status']['status'],
            "confirmed_time": dateparser.parse(data['transaction']['transaction_status']['confirmed_time']),
            "actions": list(map(
                lambda x: getattr(radix.actions, x['type']).from_dict(x), 
                data['transaction']['actions']
            )),
            "fee_paid": {
                data['transaction']['fee_paid']['token_identifier']['rri']: int(data['transaction']['fee_paid']['value'])
            },
            "transaction_blob": data['transaction']['metadata']['hex'],
            "message_blob": data['transaction']['metadata'].get('message'),
        }