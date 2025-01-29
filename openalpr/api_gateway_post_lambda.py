import json
import boto3
import uuid
import base64

def lambda_handler(event, context):
    s3 = boto3.client('s3')

    body = json.loads(event['body'])
    base64_image = body.get('image')
    file_name = body.get('filename')

    ext = body.get('ext')

    image_data = base64.b64decode(base64_image)
    random_uuid = str(uuid.uuid4())

    file_name = f'{random_uuid}.{ext}'

    s3.put_object(Bucket='openalpr-image-upload', Key=f'images/{file_name}', Body=image_data)

    # Poll S3 to confirm the file is uploaded
    def wait_for_s3_upload(bucket_name, file_name):
        while True:
            try:
                s3.head_object(Bucket=bucket_name, Key=file_name)  # Check if the file exists
                print(f"File {file_name} is now available in S3.")
                break
            except s3.exceptions.ClientError as e:
                # If the object is not found, it will raise a 404 error
                if e.response['Error']['Code'] == 'NoSuchKey':
                    print(f"File {file_name} not found in S3. Retrying...")
                else:
                    # If some other error occurs, raise it
                    raise
            time.sleep(1)  # Wait 1 second before checking again

    # Wait for the file to be available in S3
    wait_for_s3_upload('openalpr-image-upload', f'images/{file_name}')

    # set UUID in s3
    json_data = {
        'uuid': random_uuid,
        'link': f's3://openalpr-image-upload/images/{file_name}'
    }
    try:
        s3.put_object(Bucket='openalpr-image-upload', Key=f'uuid/{file_name}', Body=json.dumps(json_data), ContentType='application/json')
        print(f"Successfully uploaded {file_name} UUID mapping to S3")
    except Exception as e:
        print(f"Error uploading file: {e}")


    return {
        'statusCode': 200,
        'body': json.dumps({
            # 'link': f's3://openalpr-image-upload/images/{file_name}',
            # 'uuid': random_uuid, Ended up not needing this
            'filename': file_name
        }),
        'headers': {
            'Content-Type': 'application/json'
        }
    }
