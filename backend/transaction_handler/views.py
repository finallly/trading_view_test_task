from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated

from .models import Transaction, Account
from .transaction_logic import TransactionHandler


class TransactionCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            request_author = request.user
            account_from = Account.objects.get(
                number=request.data['account_from']
            )
            account_to = Account.objects.get(
                number=request.data['account_to']
            )

            if request.data['type'] == 'invoice':
                if account_to.owner != request_author:
                    raise Exception('you can create invoice transaction only to your account')

                if account_from.owner == request_author:
                    raise Exception('you cannot create invoice transaction from your account')

            elif request_author != account_from.owner:
                raise Exception('this account does not belong to that user')

            request.data['user_from'] = request_author
            transaction_handler = TransactionHandler(
                request.data['type']
            )
            transaction_checksum = transaction_handler.create_transaction(
                request.data
            )

            return JsonResponse(
                data={'checksum': transaction_checksum},
                status=201
            )
        except Exception as exception:
            raise APIException(detail=exception.args[0])


class TransactionCancelView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            transaction_checksum = request.data['checksum']
            transaction = Transaction.objects.get(
                checksum=transaction_checksum
            )
            if transaction.type == 'letter_of_credit':
                if request.user != transaction.account_from.owner:
                    raise Exception('only sender can cancel this transaction')

            elif request.user != transaction.account_to.owner:
                raise Exception('only receiver can cancel this transaction')

            transaction_handler = TransactionHandler(
                transaction.type
            )
            transaction_handler.cancel_transaction(transaction_checksum)

            return JsonResponse(
                data={'checksum': transaction_checksum},
                status=202
            )
        except Exception as exception:
            raise APIException(detail=exception.args[0])


class TransactionConfirmView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            transaction_checksum = request.data['checksum']
            request_author = request.user
            transaction = Transaction.objects.get(
                checksum=transaction_checksum
            )

            if transaction.type == 'invoice':
                if transaction.account_from.owner != request_author:
                    raise Exception('only sender can confirm this transaction')

            if transaction.type == 'letter_of_credit':
                if transaction.account_to.owner != request_author:
                    raise Exception('only receiver can confirm this transaction')

            transaction_handler = TransactionHandler(
                transaction.type
            )
            transaction_handler.confirm_transaction(transaction_checksum)

            return JsonResponse(
                data={'checksum': transaction_checksum},
                status=202
            )
        except Exception as exception:
            raise APIException(detail=exception.args[0])
