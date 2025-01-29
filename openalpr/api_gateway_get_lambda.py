import json
import boto3
import botocore
from botocore.exceptions import ClientError
import time
from datetime import datetime

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    # body = json.loads(event['body'])
    file_name = event["queryStringParameters"]['filename']
    # body.get('filename')

    try:
        s3.head_object(Bucket='openalpr-image-upload', Key=f'result/{file_name}')
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            return {
                'statusCode': 404,
                'body': json.dumps('The image has not finished processing yet.')
            }
        else:
            # Something else has gone wrong.
            raise
    
    tmp_file_result = '/tmp/result_file.json'
    s3.download_file('openalpr-image-upload', f'result/{file_name}', tmp_file_result)

    with open(tmp_file_result, 'r') as f:
        json_result = json.load(f)

    tmp_file_uuid = '/tmp/uuid_file.json'
    s3.download_file('openalpr-image-upload', f'uuid/{file_name}', tmp_file_uuid)

    with open(tmp_file_uuid, 'r') as f:
        json_uuid = json.load(f)

    images_folder_s3_uri = "s3://openalpr-image-upload/images/"

    epoch_time_ms = json_result["epoch_time"]

    dt_object = datetime.utcfromtimestamp(epoch_time_ms/1000)
    my_datetime = dt_object.strftime('%Y-%m-%d %H:%M:%S')

    # Hardcode the region for now

    returnJson = {
        "uuid": json_uuid["uuid"],
        "link": images_folder_s3_uri + file_name,
        "region": "North America",
        "plate": json_result["results"][0]["plate"],
        "confidence": json_result["results"][0]["confidence"],
        "datetime": my_datetime
    }

    return {
        'statusCode': 200,
        'body': json.dumps(returnJson)
    }
