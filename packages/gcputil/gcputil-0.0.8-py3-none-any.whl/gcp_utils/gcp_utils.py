"""
@author:        Travis Kirton
@description:   Utility methods to be used for GCP usage.
                Files are input string agnostic with optional params
"""


import logging
from google.cloud import storage


# Implementing Logging to provide more information &
# instantiate client connection to gcp
logging.getLogger().setLevel(logging.INFO)
client = storage.Client()


def upload_to_gcp_storage(bucket, src_filename, dest_filename, ?folder):
    """
    Function to upload file to google cloud storage
    :parameter bucket: name of bucket to upload files to
    :parameter src_filename: name of source filename to upload
    :parameter dest_filename: specify name of file once uploaded
    :parameter ?folder: optional folder path to upload to. (e.g 'folder1/')
    """

    try:
        logging.info('\033[92m Uploading: (%s)\x1B[0m' % filename)
        bucket = client.bucket(bucket)
        blob = bucket.blob(folder + dest_filename)
        blob.upload_from_filename(src_filename)

        logging.info('\033[92m Upload Completed: (%s)\x1B[0m' % filename)
    except Exception as e:
        logging.info(e)


def download_from_gcp_storage(bucket, src_filename, dest_filename, ?folder):
    """
    Function to upload file to google cloud storage
    :parameter bucket: name of bucket to download files from
    :parameter src_filename: name of source filename to download
    :parameter dest_filename: specify name of file once downloaded
    :parameter ?folder: optional folder path to download from. (e.g 'folder1/')
    """

    try:
        logging.info('\033[92m Downloading: (%s)\x1B[0m' % filename)
        bucket = client.bucket(bucket)
        blob = bucket.blob(folder + src_filename)
        blob.download_to_filename(dest_filename)

        logging.info('\033[92m Download Completed: (%s)\x1B[0m' % filename)
    except Exception as e:
        logging.info(e)


def list_gcp_bucket_blobs(bucket, ?prefixStr):
    """
    Function to list bucket from google cloud storage
    :parameter bucket: name of bucket to grab items from
    :return array: returns array of bucket items in blob format
    """
    bucket = client.bucket(bucket)
    blobs = list(bucket.list_blobs(prefix=prefixStr))

    return blobs
