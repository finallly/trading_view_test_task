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
            transaction_author = request.user
            billing_account = Account.objects.get(
                number=request.data['account_from']
            )

            if transaction_author != billing_account.owner:
                raise Exception('this account does not belong to that user')

            request.data['user_from'] = transaction_author
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

            if request.user != transaction.account_to.owner:
                raise Exception('only receiver can cancel this transaction')

            transaction_handler = TransactionHandler(
                transaction.type
            )
            transaction_handler.cancel_transaction(transaction_checksum)

            return JsonResponse(
                data={'checksum': transaction_checksum},
                status=200
            )
        except Exception as exception:
            raise APIException(detail=exception.args[0])


class TransactionConfirmView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            transaction_checksum = request.data['checksum']
            transaction = Transaction.objects.get(
                checksum=transaction_checksum
            )
            transaction_handler = TransactionHandler(
                transaction.type
            )
            transaction_handler.confirm_transaction(transaction_checksum)

            return JsonResponse(
                data={'checksum': transaction_checksum},
                status=200
            )
        except Exception as exception:
            raise APIException(detail=exception.args[0])
