from typing import Type

from .transactions import TransferTransaction, LetterCreditTransaction, InvoiceTransaction, \
    AbstractTransaction


transaction_mapping = {
    'transfer': TransferTransaction,
    'letter_of_credit': LetterCreditTransaction,
    'invoice': InvoiceTransaction
}


def _get_transaction_class(transaction_type: str) -> Type[AbstractTransaction]:
    return transaction_mapping[transaction_type]


class TransactionHandler(object):

    def __init__(self, transaction_type):
        self.transaction_class: AbstractTransaction = _get_transaction_class(transaction_type)()

    def create_transaction(self, transaction_data):
        return self.transaction_class.create_transaction(transaction_data)

    def cancel_transaction(self, transaction_checksum):
        self.transaction_class.cancel_transaction(transaction_checksum)

    def confirm_transaction(self, transaction_checksum):
        self.transaction_class.confirm_transaction(transaction_checksum)
