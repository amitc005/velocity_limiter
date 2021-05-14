import json
import logging
import sys
import traceback

import click

from src.storage import ApplicationStorage
from src.storage import CustomerAggregatedStorage
from src.validators import TransactionInputValidator

storage = ApplicationStorage()
aggregated_storage = CustomerAggregatedStorage()

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


def main(input_file, output_file, console_echo=False):
    output_str = ""
    for data in input_file:

        try:
            data = json.loads(data)
            TransactionInputValidator(data).validate()
            customer = storage.get_customer(data["customer_id"])
            if not customer:
                customer = storage.add_customer(data["customer_id"])
            res = storage.add_transaction(data, customer)
            output_str += f'{json.dumps(res, separators=(",", ":"))}\n'

        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logger.error(
                repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
            )
            continue

    if console_echo:
        print(output_str)

    if output_file:
        output_file.write(output_str)
