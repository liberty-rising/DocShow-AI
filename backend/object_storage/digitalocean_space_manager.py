"""
This module provides a class `DigitalOceanSpaceManager`
for managing files in a DigitalOcean Space.

A DigitalOcean Space is an object storage service that provides
scalable and secure storage for documents, images, and data backups.
It's compatible with the S3 API, which allows it to integrate
with existing tools and workflows.
"""
import boto3
import os

from typing import List

from settings import (
    SPACES_ACCESS_KEY,
    SPACES_BUCKET_NAME,
    SPACES_ENDPOINT_URL,
    SPACES_REGION_NAME,
    SPACES_SECRET_ACCESS_KEY,
)


class DigitalOceanSpaceManager:
    def __init__(self, organization_name: str = "", file_paths: List[str] = []):
        session = boto3.session.Session()
        self.client = session.client(
            "s3",
            region_name=SPACES_REGION_NAME,
            endpoint_url=SPACES_ENDPOINT_URL,
            aws_access_key_id=SPACES_ACCESS_KEY,
            aws_secret_access_key=SPACES_SECRET_ACCESS_KEY,
        )
        self.bucket_name = SPACES_BUCKET_NAME

        self.organization_name = organization_name.replace(" ", "_")

        self.file_paths = file_paths
        self.file_names = [os.path.basename(file_path) for file_path in file_paths]
        self.object_names: List[str] = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if self.file_paths:
            self.delete_files()

    def upload_files(self):
        """Upload multiple files to an S3 bucket

        :return: True if files were uploaded, else False
        """
        all_uploaded = True

        # Upload the files
        for file_path, file_name in zip(self.file_paths, self.file_names):
            # Prepend the organization_name to the object_name
            object_name = f"{self.organization_name}/{file_name}"
            try:
                self.client.upload_file(file_path, self.bucket_name, object_name)
                self.object_names.append(object_name)
            except Exception as e:
                print(e)
                all_uploaded = False

        return all_uploaded

    def create_presigned_urls(self, expiration=900) -> List[str]:
        """Generate presigned URLs to share S3 objects

        :param expiration: Time in seconds for the presigned URL to remain valid
        :return: List of presigned URLs as strings. If error, returns an empty string for that URL.
        """
        presigned_urls = []

        # Generate a presigned URL for each S3 object
        for object_name in self.object_names:
            try:
                response: str = self.client.generate_presigned_url(
                    "get_object",
                    Params={
                        "Bucket": self.bucket_name,
                        "Key": object_name,
                    },
                    ExpiresIn=expiration,
                )
                presigned_urls.append(response)
            except Exception as e:
                print(e)
                presigned_urls.append("")

        return presigned_urls

    def delete_files(self):
        """Delete multiple files from an S3 bucket

        :return: True if all files were deleted successfully, else False
        """
        all_deleted = True

        # Delete the files
        for object_name in self.object_names:
            try:
                self.client.delete_object(Bucket=self.bucket_name, Key=object_name)
            except Exception as e:
                print(e)
                all_deleted = False

        return all_deleted
