import os
import sys
import boto3
from moto import mock_aws
import unittest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import awsapi

class TestAwsApi(unittest.TestCase):

    @mock_aws
    def test_list_buckets_returns_names(self):
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.create_bucket(Bucket='bucket1')
        s3.create_bucket(Bucket='bucket2')

        buckets = awsapi.list_buckets()
        self.assertEqual(set(buckets), {'bucket1', 'bucket2'})

    @mock_aws
    def test_create_bucket_with_region(self):
        region = 'us-west-1'
        bucket = 'mybucket-region'
        result = awsapi.create_bucket(bucket, region=region)
        self.assertTrue(result)

        s3 = boto3.client('s3', region_name=region)
        names = [b['Name'] for b in s3.list_buckets()['Buckets']]
        self.assertIn(bucket, names)
        location = s3.get_bucket_location(Bucket=bucket)['LocationConstraint']
        self.assertEqual(location, region)

    @mock_aws
    def test_create_bucket_in_us_east_1(self):
        # us-east-1 rejects an explicit LocationConstraint
        self.assertTrue(awsapi.create_bucket('mybucket-east1', region='us-east-1'))

    @mock_aws
    def test_file_exists_requires_exact_key(self):
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.create_bucket(Bucket='bucket3')
        s3.put_object(Bucket='bucket3', Key='imdb/title.ratings.tsv.gz', Body=b'x')
        self.assertFalse(awsapi.file_exists('bucket3', 'title.ratings.tsv', 'imdb/'))
        self.assertTrue(awsapi.file_exists('bucket3', 'title.ratings.tsv.gz', 'imdb/'))

if __name__ == '__main__':
    unittest.main()
