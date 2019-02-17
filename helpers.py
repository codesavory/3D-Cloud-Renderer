import boto3, botocore
from config import S3_KEY, S3_SECRET, S3_BUCKET
from flask import flash, current_app

s3 = boto3.client(
   "s3",
   aws_access_key_id=S3_KEY,
   aws_secret_access_key=S3_SECRET
)


def upload_file_to_s3(file, bucket_name, acl="public-read"):
    try:

        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e

    return "{}{}".format(current_app.config["S3_LOCATION"], file.filename)


def read_models_in_s3():
    return s3.list_objects(Bucket=current_app.config["S3_BUCKET"])['Contents']

def download_model_from_s3(object_name):
    try:
        s3.download_file(current_app.config["S3_BUCKET"], str(object_name),str(object_name))
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise

def upload_image_to_s3(filename):
    s3.upload_file(filename, current_app.config["S3_BUCKET"], filename)