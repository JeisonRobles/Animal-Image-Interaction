from aws_clients import s3_client, ddb_table

def delete_image(animal: str, uploaded_at: str, image_id: str):
    table = ddb_table()
    s3 = s3_client()

    partition_key = f"ANIMAL#{animal}"
    sort_key = f"IMG#{uploaded_at}#{image_id}"

    # 1) Read item from DynamoDB to get S3 location
    resp = table.get_item(
        Key={
            "partition_key": partition_key,
            "sort_key": sort_key,
        }
    )
    item = resp.get("Item")
    if not item:
        raise Exception("Item not found in DynamoDB. Nothing to delete.")

    bucket = item["s3_bucket"]
    key = item["s3_key"]

    # 2) Delete from S3
    s3.delete_object(Bucket=bucket, Key=key)

    # 3) Delete from DynamoDB
    table.delete_item(
        Key={
            "partition_key": partition_key,
            "sort_key": sort_key,
        }
    )

    return {"deleted": True, "s3_bucket": bucket, "s3_key": key}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Delete an image from S3 + remove its DynamoDB record.")
    parser.add_argument("--animal", required=True)
    parser.add_argument("--uploaded_at", required=True, help="Exact uploaded_at stored in DynamoDB (e.g. 2026-02-18T20:55:10Z)")
    parser.add_argument("--image_id", required=True)
    args = parser.parse_args()

    result = delete_image(args.animal, args.uploaded_at, args.image_id)
    print("Delete OK:", result)