import json

import click

from src.parser import FileParser
from src.storage import Storage


@click.command()
@click.argument(
    "input", type=click.File("r"),
)
@click.argument("output", type=click.File("w+"))
def cli(*args, **kwargs):

    db = Storage()
    for transaction in FileParser(kwargs["input"]).parse():
        if not transaction:
            continue

        customer = db.get_customer(transaction.customer_id) or db.add_customer(
            transaction.customer_id
        )

        if customer.is_transaction_processed(transaction.id):
            continue

        res = customer.add_transaction(transaction)
        res = json.dumps(res, separators=(",", ":"))

        print(res)
        kwargs["output"].write(res)
        kwargs["output"].write("\n")
