import os
import mimetypes
import uuid
from datetime import datetime, timezone

from aws_clients import s3_client, ddb_table

S3_BUCKET = "animal-images-jeison-2026"

def upload_image(file_path: str, animal: str) -> dict:
    s3 = s3_client()
    table = ddb_table()

    if not os.path.exists(file_path):
        raise FileNotFoundError(file_path)

    image_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    timestamp = now.isoformat().replace("+00:00", "Z")

    filename = os.path.basename(file_path)
    content_type, _ = mimetypes.guess_type(file_path)
    content_type = content_type or "application/octet-stream"

    s3_key = f"animals/{animal}/{date_str}/{image_id}-{filename}"

    # Upload to S3
    s3.upload_file(
        Filename=file_path,
        Bucket=S3_BUCKET,
        Key=s3_key,
        ExtraArgs={"ContentType": content_type},
    )

    # Save metadata to DynamoDB
    item = {
        "partition_key": f"ANIMAL#{animal}",
        "sort_key": f"IMG#{timestamp}#{image_id}",
        "image_id": image_id,
        "animal": animal,
        "s3_bucket": S3_BUCKET,
        "s3_key": s3_key,
        "filename": filename,
        "content_type": content_type,
        "uploaded_at": timestamp,
    }

    table.put_item(Item=item)
    return item


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    parser.add_argument("--animal", required=True)
    args = parser.parse_args()

    result = upload_image(args.file, args.animal)
    print("Uploaded successfully:")
    print(result)