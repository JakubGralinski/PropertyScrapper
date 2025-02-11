import csv
from models.property import Property


def save_properties_to_csv(properties: list, filename: str):
    """
    Saves property data to a CSV file.
    """
    if not properties:
        print("No properties to save.")
        return

    fieldnames = Property.model_fields.keys()

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(properties)
    print(f"Saved {len(properties)} properties to '{filename}'.")