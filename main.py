import json

import click

from src.storage import ApplicationStorage
from src.validators import TransactionInputValidator

storage = ApplicationStorage()


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
            continue
