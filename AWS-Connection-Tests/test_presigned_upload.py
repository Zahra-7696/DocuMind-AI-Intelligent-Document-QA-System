import boto3

s3 = boto3.client("s3", region_name="us-east-1")

bucket_name = "documind-ai-zahra-pdf-storage"
object_key = "uploads/test.pdf"

url = s3.generate_presigned_url(
    ClientMethod="put_object",
    Params={
        "Bucket": bucket_name,
        "Key": object_key,
        "ContentType": "application/pdf"
    },
    ExpiresIn=300
)

print(url)