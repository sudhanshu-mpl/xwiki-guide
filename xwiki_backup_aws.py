import os
import argparse
import boto3
from botocore.exceptions import NoCredentialsError
import datetime


def upload_to_aws(bucket, local_file, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    print('  Uploading ' + local_file + ' to ' + bucket + '/' + s3_file)
    try:
        s3.upload_file(local_file, bucket, s3_file)
        print('  '+s3_file + ": Upload Successful")
        print('  ---------')
    except NoCredentialsError:
        print("Credentials not available")
        return False


def main(result):
    today = datetime.date.today().strftime('%Y-%m-%d')
    s3_dir = 'xwiki_backup.' + today + '/'
    for source, dirs, files in os.walk(result.local_dir):
        print('Directory: ' + source)
        for filename in files:
            local_file = os.path.join(source, filename)
            relative_path = os.path.relpath(local_file, result.local_dir)
            s3_file = os.path.join(s3_dir, relative_path)
            upload_to_aws(bucket_name, local_file, s3_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='store directory to S3')
    parser.add_argument('-d', '--local_dir',
                        help='provide directory which needs to be stored',
                        required=True)
    args = parser.parse_args()
    main(args)
