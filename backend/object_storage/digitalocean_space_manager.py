"""
This module provides a class `DigitalOceanSpaceManager`
for managing files in a DigitalOcean Space.

A DigitalOcean Space is an object storage service that provides
scalable and secure storage for documents, images, and data backups.
It's compatible with the S3 API, which allows it to integrate
with existing tools and workflows.
"""
import boto3

from settings import (
    SPACES_ACCESS_KEY,
    SPACES_BUCKET_NAME,
    SPACES_ENDPOINT_URL,
    SPACES_REGION_NAME,
    SPACES_SECRET_ACCESS_KEY,
)


class DigitalOceanSpaceManager:
    def __init__(self):
        session = boto3.session.Session()
        self.client = session.client(
            "s3",
            region_name=SPACES_REGION_NAME,
            endpoint_url=SPACES_ENDPOINT_URL,
            aws_access_key_id=SPACES_ACCESS_KEY,
            aws_secret_access_key=SPACES_SECRET_ACCESS_KEY,
        )
        self.bucket_name = SPACES_BUCKET_NAME

    def upload_file(self, organization_name, file_path, object_name=None):
        """Upload a file to an S3 bucket

        :param organization_name: Name of the organization the file belongs to
        :param file_path: File to upload
        :param object_name: S3 object name. If not specified then file_path is used
        :return: True if file was uploaded, else False
        """

        # If S3 object_name was not specified, use file_path
        if object_name is None:
            object_name = file_path

        # Prepend the organization_name to the object_name
        object_name = f"{organization_name}/{object_name}"

        # Upload the file
        try:
            self.client.upload_file(file_path, self.bucket_name, object_name)
        except Exception as e:
            print(e)
            return False
        return True

    def create_presigned_url(
        self, organization_name, object_name, expiration=900
    ) -> str:
        """Generate a presigned URL to share an S3 object

        :param organization_name: Name of the organization the file belongs to
        :param object_name: name of the object
        :param expiration: Time in seconds for the presigned URL to remain valid
        :return: Presigned URL as string. If error, returns an empty string.
        """

        # Generate a presigned URL for the S3 object
        try:
            response: str = self.client.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": self.bucket_name,
                    "Key": f"{organization_name}/{object_name}",
                },
                ExpiresIn=expiration,
            )
        except Exception as e:
            print(e)
            return ""

        # The response contains the presigned URL
        return response

    def delete_file(self, organization_name, object_name):
        """Delete a file from an S3 bucket

        :param organization_name: Name of the organization the file belongs to
        :param object_name: S3 object name
        :return: True if the referenced object was deleted, otherwise False
        """

        # Prepend the organization_name to the object_name
        object_name = f"{organization_name}/{object_name}"

        # Delete the file
        try:
            self.client.delete_object(Bucket=self.bucket_name, Key=object_name)
        except Exception as e:
            print(e)
            return False
        return True
