"""Upload Client for AWS Event Data to S3."""
# -*- coding: utf-8 -*-
import json
import boto3
import datetime
import lambida.datazone.utils as utils


s3_resource = boto3.resource('s3')


class S3ResourceClient(object):
    """A client to operate on S3 resource actions."""

    def __init__(self, context, config):
        """A handler init."""
        self.function_name = context.function_name
        self.aws_request_id = context.aws_request_id
        self.filename = self.aws_request_id + "_" + \
            utils.get_timestamp() + ".json"
        self.location = "lambda/"
        self.log = config["LOG"]
        self.bucket_name = config["BUCKET"]


    def get_prefix(self, key):
        """Return Prefix."""
        return self.location +  \
            self.function_name  +  \
            "/{}/".format(key) +  \
            utils.get_table_partition_by_day() +  \
            self.filename


    def s3_put_request(self, data, key):
        """Upload Data to S3."""
        s3_object = \
            s3_resource.Object(
                bucket_name=self.bucket_name, 
                key=self.get_prefix(key))
        response = s3_object.put(Body=data)
        self.log.info('S3 Put Requests: {}'.format(s3_object))
        return s3_object, response

