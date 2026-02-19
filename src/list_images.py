from aws_clients import ddb_table
from boto3.dynamodb.conditions import Key

def list_images(animal: str, limit: int = 10):
    table = ddb_table()

    response = table.query(
        KeyConditionExpression=Key("partition_key").eq(f"ANIMAL#{animal}"),
        ScanIndexForward=False,
        Limit=limit,
    )

    return response.get("Items", [])


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--animal", required=True)
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    items = list_images(args.animal, args.limit)

    if not items:
        print("No images found.")
    else:
        for i, item in enumerate(items, 1):
            print(f"\n{i})")
            print("  Animal:", item["animal"])
            print("  Image ID:", item["image_id"])
            print("  Uploaded At:", item["uploaded_at"])
            print("  S3 Key:", item["s3_key"])