from robot.api import logger
import boto3
import uuid


class RoboBoto3(object):
    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def __init__(self, region):
        self.region = region

    def write_file_to_s3(self, tool, filename, bucket_name):
        s3 = boto3.client('s3')
        outfile_name = "{}-RESULT-{}.json".format(tool, str(uuid.uuid4()))
        s3.upload_file(filename, bucket_name, outfile_name)
        logger.info("Filename uploaded to S3 is: {}".format(outfile_name))

    def retrieve_param_from_ssm(self, secret, decrypt=True):
        db = boto3.client('ssm', region_name=self.region)
        param = db.get_parameter(Name=secret, WithDecryption=decrypt)['Parameter']['Value']
        return param
