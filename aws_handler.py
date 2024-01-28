from src.app import *

def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': "Hello cruel world!"
    }