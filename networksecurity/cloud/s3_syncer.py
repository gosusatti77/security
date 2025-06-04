 
import os

class S3Sync:
    def sync_folder_to_s3(self, folder, aws_bucket_url):
        """
        Syncs a local folder to an S3 bucket.

        :param folder: Local folder path to sync.
        :param aws_bucket_url: S3 bucket URL where the folder will be synced.
        """
        command = f"aws s3 sync {folder} {aws_bucket_url}"

        # Use AWS CLI command to sync the folder to the S3 bucket
        os.system(command)
    
    def sync_folder_from_s3(self, folder,aws_bucket_url ):
        """
        Syncs an S3 bucket to a local folder.

        :param aws_bucket_url: S3 bucket URL to sync from.
        :param folder: Local folder path where the S3 bucket will be synced.
        """
        command = f"aws s3 sync {aws_bucket_url} {folder}"

        # Use AWS CLI command to sync the S3 bucket to the local folder
        os.system(command)