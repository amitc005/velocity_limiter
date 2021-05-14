import json
import logging
import sys
import traceback

import click

from src.storage import ApplicationStorage
from src.validators import TransactionInputValidator

storage = ApplicationStorage()

logger = logging.getLogger(__name__)
logger.addHandler(logging.FileHandler("error_log.log", mode="w+"))


@click.command()
@click.argument(
    "input", type=click.File("r"),
)
@click.argument("output", type=click.File("w+"))
def cli(*args, **kwargs):
    for data in kwargs["input"]:
        try:
            data = json.loads(data)
            TransactionInputValidator(data).validate()
            res = storage.add_transaction(data)
            res = json.dumps(res, separators=(",", ":"))
            kwargs["output"].write(res)
            kwargs["output"].write("\n")

        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logger.error(
                repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
            )
            continue
