#***********************************************
# File: aws_graphapi.py
# Purpose: Perform following operation:
#          1. List buckets
#          2. Create bucket
#          3. Delete bucket
#          4. Bucket exists
#          5. List Objects
#          6. Folder exists
#          7. Create Folder
#          8. Delete Folder
#          12. File exists
#************************************************/
from flask import Flask
from graphene import ObjectType, String, Schema
from flask_graphql import GraphQLView
from botocore.exceptions import ClientError
import graphene
import boto3

class BucketMessage(graphene.ObjectType):

    message = graphene.String()


class DeleteBucket(graphene.Mutation):
    """
        GraphiQL Command to to create a new bucket on s3

        {
            deleteBucket(bucketName: "aws-big-data-test")
        }

    """
    class Arguments:
        bucket_name = graphene.String()

    message = graphene.String()

    def mutate(self, info, bucket_name):
        message = ""

        try:
            s3_client = boto3.client('s3')
            s3_client.delete_bucket(Bucket=bucket_name)

            message = 'Bucket {0} deleted successfully.'.format(bucket_name)

        except ClientError as e:
            message = e.response["Error"]["Message"]
        except Exception as e:
            message = str(e)

        return BucketMessage(message)


class CreateBucket(graphene.Mutation):
    """
        GraphiQL Command to to create a new bucket on s3

        {
            createBucket(bucketName: "aws-big-data-test") {
                message
            }
        }

        OR

        {
            createBucket(bucketName: "aws-big-data-test")
        }

        region is optional

        {
            createBucket(bucketName: "aws-big-data-test", region: "us-east-2") {
                message
            }
        }

        OR

        {
            createBucket(bucketName: "aws-big-data-test", region: "us-east-2")
        }

    """
    class Arguments:
        bucket_name = graphene.String()
        region = graphene.String(required=False)

    message = graphene.String()

    def mutate(self, info, bucket_name, region=None):

        if region is None:
            session = boto3.Session(profile_name='default')
            region = session.region_name

        try:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)

            message = 'Created bucket {0} in the S3 region ({1})'.format(bucket_name, region)

        except ClientError as e:
            message = e.response["Error"]["Message"]
        except Exception as e:
            message = str(e)

        return BucketMessage(message)


class DefaultQuery(graphene.ObjectType):
    list_buckets = graphene.List(graphene.String)
    bucket_exists = graphene.String(bucket_name=graphene.String())

    create_bucket = CreateBucket.Field()
    delete_bucket = DeleteBucket.Field()

    list_objects = graphene.List(graphene.String, bucket_name=graphene.String(), object_name=graphene.String())
    folder_exists = graphene.String(bucket_name=graphene.String(), object_name=graphene.String())
    create_folder = graphene.String(bucket_name=graphene.String(),
                                    object_name=graphene.String(),
                                    folder_name=graphene.String())

    delete_folder = graphene.String(bucket_name=graphene.String(), object_name=graphene.String())
    file_exists = graphene.String(bucket_name=graphene.String(),
                                  object_name=graphene.String(),
                                  file_name=graphene.String())


    def resolve_list_buckets(self, info):
        """
            GraphiQL Command to check if a bucket exists or not
            {
              listBuckets
            }
        """

        s3_client = boto3.resource('s3')

        buckets = []

        for bucket in s3_client.buckets.all():
            buckets.append(bucket.name)

        return buckets


    def resolve_bucket_exists(self, info, bucket_name):
        """
            GraphiQL Command to check if a bucket exists or not
            {
              bucketExists(bucketName:"aws-big-data-test")
            }
        """

        try:
            s3_client = boto3.client('s3')
            response = s3_client.head_bucket(Bucket=bucket_name)

            if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
                message = '{0} exists and you have permission to access it.'.format(bucket_name)
            else:
                message = 'Man! Something Else Went Wrong.'

        except ClientError as e:
            message = e.response["Error"]["Message"]
        except Exception as e:
            message = str(e)

        return message


    def resolve_list_objects(self, info, bucket_name, object_name=None):

        """
            GraphiQL Command to to list all the objects in the given bucket_name and object_name
            object_name is optional

            {
                listObjects(bucketName: "aws-big-data-test")
            }

            OR

            {
                listObjects(bucketName: "aws-big-data-test", objectName: "data")
            }
        """

        objects = []
        response = []

        s3 = boto3.client('s3')
        try:
            if object_name is None:
                object_name = ''

            results = s3.list_objects(Bucket=bucket_name, Prefix=object_name)

            try:
                for i in results['Contents']:
                    objects.append(i['Key'])
            except:
                pass

            return objects

        except ClientError as e:
            message = str(e)
            response = [message]

        return response


    def resolve_folder_exists(self, info, bucket_name, object_name):
        """
            GraphiQL Command to check if a folder exists in the bucket or not

            {
                folderExists(bucketName: "aws-big-data-test", objectName: "data")
            }
        """

        message = ""

        objects = []

        s3 = boto3.client('s3')
        try:
            results = s3.list_objects(Bucket=bucket_name, Prefix=object_name)
            try:
                for i in results['Contents']:
                    objects.append(i['Key'])
            except:
                pass

            if objects !=[]:
                message = "objectName '{}' was found in the bucketName '{}'!".format(object_name, bucket_name)

        except ClientError as e:
            message = str(e)

        return message


    def resolve_create_folder(self, info, bucket_name, folder_name, object_name=None):
        """
            GraphiQL Command to create a folder inside a bucket

            {
                createFolder(bucketName: "aws-big-data-test", objectName: "data")
            }

            OR

            {
                createFolder(bucketName: "aws-big-data-test", objectName: "data", folderName: "data2")
            }

        """
        message = ""

        if folder_name is None:
            message = "You must provide the folder_name"
        else:
            objects = []
            s3 = boto3.client('s3')
            orig_object_name = object_name
            try:
                if object_name:
                    object_name = object_name + '/' + folder_name + '/'
                else:
                    object_name = folder_name + '/'

                results = s3.list_objects(Bucket=bucket_name, Prefix=object_name)

                try:
                    for i in results['Contents']:
                        objects.append(i['Key'])
                except:
                    pass

                if objects ==[]:
                    s3.put_object(Bucket=bucket_name, Key=object_name)
                    message = "Folder '{}' was created in the the bucket '{}'".format(folder_name, bucket_name)

                    if object_name:
                        message += " under '{}'".format(orig_object_name)
                else:
                    message = "Failed to create folder '{}' in the the bucket '{}'".format(folder_name, bucket_name)

            except ClientError as e:
                message = e.response["Error"]["Message"]
            except Exception as e:
                message = str(e)

        return message


    def resolve_delete_folder(self, info, bucket_name, object_name):
        """
            GraphiQL Command to create a folder inside a bucket

            {
                deleteFolder(bucketName: "aws-big-data-test", objectName: "data1")
            }
        """

        message = ""

        objects = []
        s3 = boto3.client('s3')
        try:
            if object_name[-1] != '/':
                object_name += '/'

            results = s3.list_objects(Bucket=bucket_name, Prefix=object_name)
            try:
                for i in results['Contents']:
                    objects.append(i['Key'])
            except:
                pass

            if objects !=[]:
                for obj in objects:
                    s3.delete_object(Bucket=bucket_name, Key=obj)

                message = "Given object_name '{}' was deleted from bucket_name '{}'!".format(object_name, bucket_name)
            else:
                message = "Could not delete the object_name from the bucket_name"
        except ClientError as e:
            message = str(e)

        return message


    def resolve_file_exists(self, info, bucket_name, file_name, object_name=None):
        """
            GraphiQL Command to check if a file exists in the bucket or not

            {
                fileExists(bucketName:"aws-big-data-test", fileName: "String")
            }
        """
        '''
        message = None

        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket_name)
        objs = list(bucket.objects.filter(Prefix=file_name))

        if len(objs) > 0 and objs[0].key == file_name:
            message = "Filename '{}' exists in the bucket '{}'!".format(file_name, bucket_name)
        else:
            message = "Filename '{}' doesn't exist in the bucket '{}'!".format(file_name, bucket_name)
        '''

        objects = []


        if file_name is None:
            message = "file name must be provided for search"

        else:
            s3 = boto3.client('s3')
            orig_object_name = object_name
            try:
                # If S3 object_name was not specified, use file_name
                if object_name:
                    object_name += '/' + file_name
                else:
                    object_name = file_name

                results = s3.list_objects(Bucket=bucket_name, Prefix=object_name)

                try:
                    for i in results['Contents']:
                        objects.append(i['Key'])
                except:
                    pass

                if objects !=[]:
                    message = "File '{}' exists under '{}/{}'!".format(file_name, bucket_name, orig_object_name)
                else:
                    message = "File '{}' doesn't exist under '{}/{}'!".format(file_name, bucket_name, orig_object_name)

            except ClientError as e:
                message = str(e)
        return message


schema = graphene.Schema(query=DefaultQuery)


view_func = GraphQLView.as_view("graphql", schema=schema, graphiql=True)


app = Flask(__name__)
app.add_url_rule("/", view_func=view_func)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=True)
