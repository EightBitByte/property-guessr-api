from src import app

def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': "Hello cruel world!"
    }