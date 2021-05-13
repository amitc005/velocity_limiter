import json

import click

from src.app import FileRepository


@click.command()
@click.argument(
    "input", type=click.File("r"),
)
@click.argument("output", type=click.File("r"))
def cli(*args, **kwargs):
    output_result = FileRepository(kwargs["input"]).add_records()

    print("##########################")
    for output_line in kwargs["output"]:
        formated_out = json.loads(output_line)
        current_output = output_result.pop(0)
        if formated_out == current_output:
            print(f"Correct {formated_out}")
            continue

        print(f"Actual Output f{current_output} --- Expected {formated_out}")
