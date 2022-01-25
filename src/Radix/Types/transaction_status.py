from enum import Enum

class TransactionStatus(Enum):
    PENDING = 'Pending'
    CONFIRMED = 'Confirmed'
    FAILED = 'Failed'
