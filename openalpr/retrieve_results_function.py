import json
import boto3
import time
import os
import mysql.connector
from datetime import datetime
import uuid

def lambda_handler(event, context):
    # ===========================================================================
    # RETRIEVE LATEST JSON RESPONSE FROM RESULT
    # ===========================================================================
    s3 = boto3.client('s3')
    bucket_name = 'openalpr-image-upload'
    folder_name = 'result/'

    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_name)
    objects = response['Contents']
    objects.sort(key=lambda obj: obj['LastModified'], reverse=True)

    latest_file_key = objects[0]['Key']
    tmp_file_name = '/tmp/latest_file.json'

    s3.download_file(bucket_name, latest_file_key, tmp_file_name)
    print(latest_file_key)
    with open(tmp_file_name, 'r') as f:
        json_data = json.load(f)

    # ===========================================================================
    # RETRIEVE CORRESPONDING JSON RESPONSE FROM UUID
    # ===========================================================================
    uuid_folder_s3_uri = "s3://openalpr-image-upload/uuid/"
    uuid_folder_name = 'uuid/'
    uuid_tmp_file_name = '/tmp/uuid_latest_file.json'

    s3.download_file(bucket_name, uuid_folder_name + latest_file_key[7:], uuid_tmp_file_name)
    with open(uuid_tmp_file_name, 'r') as f:
        uuid_json_data = json.load(f)
    
    # ===========================================================================
    # FORMULATE RESPONSE FOR RDS
    # ===========================================================================
    images_folder_s3_uri = "s3://openalpr-image-upload/images/"
    
    # convert to datetime object
    epoch_time_ms = json_data["epoch_time"]

    dt_object = datetime.utcfromtimestamp(epoch_time_ms/1000)
    my_datetime = dt_object.strftime('%Y-%m-%d %H:%M:%S')

    # hardcode the region for now

    returnJson = {
        "link": images_folder_s3_uri + latest_file_key[7:],
        "region": "North America"
        "plate": json_data["results"][0]["plate"],
        "confidence": json_data["results"][0]["confidence"],
        "datetime": my_datetime
    }

    insert_query = """
    INSERT INTO plates (link, region, plate, confidence, datetime)
    VALUES (%s, %s, %s, %s, %s);
    """
    entry_data = (
        returnJson["link"], 
        returnJson["region"], 
        returnJson["plate"], 
        returnJson["confidence"], 
        returnJson["datetime"]
    )
    
    try:
        # connect to DB
        connection = mysql.connector.connect(
            host=os.environ["DB_HOST"],
            database=os.environ["DB_NAME"],
            user=os.environ['DB_USER'],
            password = os.environ['DB_PASSWORD'],
            port=int(os.environ['DB_PORT'])
        )
        cursor = connection.cursor()
        
        # Execute the insert query
        cursor.execute(insert_query, entry_data)
        connection.commit()
        
        return {
            'statusCode': 200,
            'body': json.dumps(entry_data)
        }
    
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"Error: {str(e)}"
        }

    finally:
        # Close connection
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()     
