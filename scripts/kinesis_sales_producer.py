import datetime
import random
import boto3
import json
import time
import uuid
import pandas as pd

STREAM_NAME = "jl-sales-stream"
REGION = "us-east-1"
CSV_FILE = "stores_sales_forecasting.csv"

kinesis_client = boto3.client("kinesis", region_name=REGION)

REGIONS = ["West", "East", "Central", "South"]

df = pd.read_csv(CSV_FILE)

PRODUCTS = (
    df[["Product ID", "Product Name", "Sales", "Quantity"]]
    .dropna()
    .to_dict(orient="records")
)

print(f"{len(PRODUCTS)} produits chargés depuis le CSV")

def generate_quantity(base_qty):
    if base_qty >= 7:
        return random.randint(3, 6)
    elif base_qty >= 4:
        return random.randint(2, 4)
    else:
        return random.randint(1, 2)

def get_sale_event():
    product = random.choice(PRODUCTS)

    quantity = generate_quantity(product["Quantity"])
    unit_price = product["Sales"] / max(product["Quantity"], 1)

    return {
        "Order_ID": f"ORDER-{uuid.uuid4()}",
        "event_time": (
            datetime.datetime.now()
            - datetime.timedelta(minutes=random.randint(0, 15))
        ).isoformat(timespec="seconds"),
        "Product_ID": product["Product ID"],
        "Product_Name": product["Product Name"],
        "Region": random.choice(REGIONS),
        "Quantity": quantity,
        "Sales": round(unit_price * quantity, 2)
    }

def generate():
    print("Envoi des ventes vers Kinesis...")
    while True:
        data = get_sale_event()
        print("Event:", data)

        kinesis_client.put_record(
            StreamName=STREAM_NAME,
            Data=json.dumps(data),
            PartitionKey=data["Product_ID"]
        )

        time.sleep(random.uniform(2, 5))

if __name__ == "__main__":
    generate()
