import datetime
import hashlib

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

TRANSACTION_TYPES = (
	('transfer', 'transfer'),
	('letter_of_credit', 'letter_of_credit'),
	('invoice', 'invoice')
)

STATUS_TYPES = (
	('waiting', 'waiting'),
	('done', 'done'),
	('canceled', 'canceled')
)


class Account(models.Model):
	number = models.CharField(
		max_length=67,
		blank=True
	)
	owner = models.ForeignKey(
		User, on_delete=models.CASCADE,
		related_name='account_owner'
	)
	amount = models.DecimalField(
		max_digits=10, decimal_places=2
	)

	class Meta:
		db_table = 'account'

	@classmethod
	def __hash_to_account_number(cls, checksum: str) -> str:
		args = [iter(checksum)] * 16
		return '-'.join(
			[
				''.join(index) for index in zip(*args)
			]
		)

	@classmethod
	def create(cls, **kwargs):
		account = Account(**kwargs)
		account_hash = hashlib.sha256(
			f'{account.owner}{account.id}'.encode('utf-8')
		).hexdigest()
		account.number = cls.__hash_to_account_number(account_hash)
		account.save()

		return account


class Transaction(models.Model):
	type = models.CharField(
		max_length=16,
		choices=TRANSACTION_TYPES,
		default='transfer'
	)
	amount = models.DecimalField(
		max_digits=10, decimal_places=2
	)
	time = models.DateTimeField(
		blank=True
	)
	account_to = models.ForeignKey(
		Account, on_delete=models.PROTECT,
		related_name='transaction_receiver'
	)
	account_from = models.ForeignKey(
		Account, on_delete=models.PROTECT,
		related_name='transaction_author'
	)
	user_from = models.ForeignKey(
		User, on_delete=models.CASCADE
	)
	status = models.CharField(
		max_length=16,
		choices=STATUS_TYPES,
		default='done'
	)
	checksum = models.CharField(
		max_length=64,
		blank=True,
		null=True
	)

	class Meta:
		db_table = 'transaction'

	@classmethod
	def create(cls, **kwargs):
		transaction = Transaction(**kwargs)
		transaction.time = timezone.now()
		transaction_number = hashlib.sha256(
			f'{transaction.id}{transaction.time}{transaction.account_from}{transaction.account_to}'.encode('utf-8')
		).hexdigest()
		transaction.checksum = transaction_number
		transaction.save()

		return transaction
