import json

from .models import Customer


class FileRepository:
    def __init__(self, input_file):
        self._loads = self._clean_input_records(input_file)
        self._customer_records = {}

    def _clean_input_records(self, input_file):
        processed_records = {}
        for record in input_file:
            load = json.loads(record)
            processed_records[f"{load['id']}:{load['customer_id']}"] = load

        return list(processed_records.values())

    def add_records(self):
        output = []
        for load_record in self._loads:
            customer = self._customer_records.get(load_record["customer_id"])
            if not customer:
                customer = Customer(load_record["customer_id"])
                self._customer_records[customer.customer_id] = customer

            try:
                customer.add_load(load_record)
                output.append(
                    {
                        "id": load_record["id"],
                        "customer_id": load_record["customer_id"],
                        "accepted": True,
                    }
                )
            except (ValueError, KeyError):
                output.append(
                    {
                        "id": load_record["id"],
                        "customer_id": load_record["customer_id"],
                        "accepted": False,
                    }
                )
        return output
