import json

import click

from src.app import App
from src.utils import FileReader


@click.command()
@click.argument(
    "input", type=click.File("r"),
)
@click.argument("output", type=click.File("w+"))
def cli(*args, **kwargs):
    transactions = FileReader(kwargs["input"]).read()
    app = App()

    for transaction in transactions:
        res = app.add_transaction(transaction)
        res = json.dumps(res)
        kwargs["output"].write(json.dumps(res))
        kwargs["output"].write("\n")
