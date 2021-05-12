from .models import Customer


def file_repository(records):
    mapped_data = {}
    output_results = []
    for record in records:
        customer = mapped_data.get(record["customer_id"])
        if not customer:
            customer = Customer(record["customer_id"])
            mapped_data[record["customer_id"]] = customer

        try:
            customer.add_load(record)
            output_results.append(
                {
                    "id": record["id"],
                    "customer_id": record["customer_id"],
                    "accepted": True,
                }
            )
        except ValueError:
            output_results.append(
                {
                    "id": record["id"],
                    "customer_id": record["customer_id"],
                    "accepted": False,
                }
            )

    return output_results
