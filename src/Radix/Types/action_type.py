from enum import Enum


class ActionType(Enum):
    """ 
    An enum which defines the type of actions 
    
    The full list of ActionTypes can be found at: 
    * https://github.com/radixdlt/radixdlt/tree/develop/radixdlt-java/radixdlt-java/src/main/java/com/radixdlt/client/lib/api/action
    * https://github.com/radixdlt/radixdlt/blob/develop/radixdlt-java/radixdlt-java/src/main/java/com/radixdlt/client/lib/api/ActionType.java
    """
    
    Other = "Other"
    TokenTransfer = "TokenTransfer"
    StakeTokens = "StakeTokens"
    UnstakeTokens = "UnstakeTokens"
    BurnTokens = "BurnTokens"
    MintTokens = "MintTokens"
    RegisterValidator = "RegisterValidator"
    UnregisterValidator = "UnregisterValidator"
    UpdateValidatorMetadata = "UpdateValidatorMetadata"
    UpdateValidatorFee = "UpdateValidatorFee"
    UpdateValidatorOwner = "UpdateValidatorOwner"
    UpdateAllowDelegationFlag = "UpdateAllowDelegationFlag"
    CreateFixedSupplyToken = "CreateFixedSupplyToken"
    CreateMutableSupplyToken = "CreateMutableSupplyToken"

    def __str__(self) -> str:
        """ Converts the enum to a string """
        return self.value