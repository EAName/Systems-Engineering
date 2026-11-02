"""Sanity check that the BRFSS index on Amazon Elasticsearch Service is reachable.

Configuration comes from the environment:
    ES_HOST     Elasticsearch domain endpoint, without scheme
                (e.g. search-<domain>-<id>.<region>.es.amazonaws.com). Required.
    AWS_REGION  Region of the domain, used for SigV4 signing. Defaults to us-east-2.
"""
import os
import sys

from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3

host = os.environ.get('ES_HOST')
if not host:
    sys.exit('ES_HOST is not set. Export the Elasticsearch domain endpoint, '
             'e.g. export ES_HOST=search-<domain>-<id>.us-east-2.es.amazonaws.com')
region = os.environ.get('AWS_REGION', 'us-east-2')
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service)

es = Elasticsearch(
    hosts = [{'host': host, 'port': 443}],
    http_auth = awsauth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
)

print(es.count())
