import decimal
from abc import ABC, abstractmethod

from transaction_handler.models import Transaction, Account


class AbstractTransaction(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def create_transaction(self, transaction_data):
        pass

    @abstractmethod
    def confirm_transaction(self, transaction_checksum):
        pass

    @abstractmethod
    def cancel_transaction(self, transaction_checksum):
        pass


class TransferTransaction(AbstractTransaction):

    def confirm_transaction(self, transaction_checksum):
        raise Exception('transaction of type <transfer> cannot be confirmed')

    def cancel_transaction(self, transaction_checksum):
        transaction = Transaction.objects.get(
            checksum=transaction_checksum
        )

        if transaction.status != 'done':
            raise Exception('transaction already canceled')

        account_from = transaction.account_from
        account_to = transaction.account_to
        amount = transaction.amount

        if amount <= account_to.amount:
            account_to.amount -= amount
            account_to.save()

            account_from.amount += amount
            account_from.save()

            transaction.status = 'canceled'
            transaction.save()

            return transaction.checksum
        else:
            raise Exception('not enough money')

    def create_transaction(self, transaction_data):
        account_from = Account.objects.get(
            number=transaction_data['account_from']
        )

        account_to = Account.objects.get(
            number=transaction_data['account_to']
        )

        amount = decimal.Decimal(transaction_data['amount'])

        if amount <= account_from.amount:
            account_to.amount += amount
            account_to.save()

            account_from.amount -= amount
            account_from.save()

            transaction_data['account_from'] = account_from
            transaction_data['account_to'] = account_to
            transaction = Transaction.create(**transaction_data)

            return transaction.checksum
        else:
            raise Exception('not enough money')


class LetterCreditTransaction(AbstractTransaction):

    def cancel_transaction(self, transaction_checksum):
        pass

    def confirm_transaction(self, transaction_checksum):
        pass

    def create_transaction(self, transaction_data):
        pass


class InvoiceTransaction(AbstractTransaction):

    def cancel_transaction(self, transaction_checksum):
        pass

    def confirm_transaction(self, transaction_checksum):
        pass

    def create_transaction(self, transaction_data):
        pass
