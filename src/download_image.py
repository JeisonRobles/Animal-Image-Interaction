import os
from aws_clients import s3_client, ddb_table

DOWNLOAD_DIR = "downloads"

def download_image(animal: str, uploaded_at: str, image_id: str):
    table = ddb_table()
    s3 = s3_client()

    partition_key = f"ANIMAL#{animal}"
    sort_key = f"IMG#{uploaded_at}#{image_id}"

    response = table.get_item(
        Key={
            "partition_key": partition_key,
            "sort_key": sort_key,
        }
    )

    item = response.get("Item")

    if not item:
        raise Exception("Image not found in DynamoDB.")

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    local_path = os.path.join(DOWNLOAD_DIR, item["filename"])

    s3.download_file(item["s3_bucket"], item["s3_key"], local_path)

    return local_path


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--animal", required=True)
    parser.add_argument("--uploaded_at", required=True)
    parser.add_argument("--image_id", required=True)
    args = parser.parse_args()

    path = download_image(args.animal, args.uploaded_at, args.image_id)
    print("Downloaded to:", path)