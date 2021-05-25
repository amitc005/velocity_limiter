from .exceptions import TransactionException


class TransactionHandler:
    def __init__(
        self,
        customer_storage,
        transaction_storage,
        transaction_log,
        customer_aggregated,
    ):
        self._customer_storage = customer_storage
        self._transaction_storage = transaction_storage
        self._transaction_log = transaction_log
        self._aggregated_storage = customer_aggregated

    def perform_transaction(self, customer, transaction):
        try:
            self._transaction_log.add(transaction.transaction_key)
            customer.perform_transaction(transaction, self._aggregated_storage)

            self._transaction_storage.add(transaction)
            self._aggregated_storage.update(customer.customer_id, transaction)

            return {
                "id": transaction.id,
                "customer_id": customer.customer_id,
                "accepted": True,
            }

        except TransactionException:
            return {
                "id": transaction.id,
                "customer_id": customer.customer_id,
                "accepted": False,
            }
