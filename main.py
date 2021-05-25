import json
import logging
import sys
import traceback

import click

from src.handlers import TransactionHandler
from src.storage import CustomerAggregatedStorage
from src.storage import CustomerStorage
from src.storage import TransactionLogStorage
from src.storage import TransactionStorage
from src.utils import TransactionFileIterator


logger = logging.getLogger(__name__)
logger.addHandler(logging.FileHandler("error_log.log", mode="w+"))


@click.command()
@click.argument(
    "input", type=click.File("r"),
)
@click.argument("output", type=click.File("w+"))
@click.option("-v", "--verbose", is_flag=True)
def cli(*args, **kwargs):
    main(kwargs["input"], kwargs["output"], kwargs["verbose"])


customer_aggregated = None


def main(input_file, output_file, console_echo=False):
    customer_storage = CustomerStorage()
    transaction_storage = TransactionStorage()
    transaction_log = TransactionLogStorage()
    customer_aggregated = CustomerAggregatedStorage()
    transaction_handler = TransactionHandler(
        customer_storage, transaction_storage, transaction_log, customer_aggregated
    )

    for transaction in TransactionFileIterator(input_file):
        if not transaction:
            continue

        try:
            customer = customer_storage.get(
                transaction.customer_id
            ) or customer_storage.add(transaction.customer_id)

            res = transaction_handler.perform_transaction(customer, transaction)
            formated_res = f'{json.dumps(res, separators=(",", ":"))}\n'
            if console_echo:
                print(formated_res)

            if output_file:
                output_file.write(formated_res)

        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logger.error(
                repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
            )
