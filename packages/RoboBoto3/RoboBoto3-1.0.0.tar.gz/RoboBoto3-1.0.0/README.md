# RoboBoto3

Utility functions for AWS's Python SDK - `boto3`.

This is meant to be used as an accompaniment to Robot Security Libraries to be integrated into AWS Fargate, step functions, etc

## Install

* `pip install RoboBoto3`

## Keywords
* Currently only S3 push and SSM get has been generated

### Initialize
`Settings  RoboBoto3  <aws-region-name>`


### Write file to S3
`| write file to s3  | tool  | filename  | bucket_name |`

All mandatory params

### Get SSM parameter
`| retrieve_param_from_ssm  | param_name  | decrypt (True/False) | `

default decrypt value is `True`