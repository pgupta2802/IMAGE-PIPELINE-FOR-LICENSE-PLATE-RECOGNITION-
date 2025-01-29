import json
import boto3
import time
import os
import base64
import uuid

def lambda_handler(event, context):
    print("test 1")
    # # ===========================================================================
    # # CALL INSTANCE OF CONTAINER
    # # ===========================================================================
    client = boto3.client('ecs', region_name='ca-central-1')
    file_name = event['Records'][0]['s3']['object']['key'][7:]

    response = client.run_task(
        cluster='group3-image-processing-cluster',
        taskDefinition='arn:aws:ecs:ca-central-1:941377123257:task-definition/process-image:1',
        launchType='FARGATE',
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': [
                    'subnet-035b2ace188cebaff',
                ],
                'securityGroups': [
                    'sg-0ae29ac73fe58eafc',
                ],
                'assignPublicIp': 'ENABLED'
            }
        },
        count=1,
        overrides={
            'containerOverrides': [
                {
                    "name": "image-processing-pipeline",
                    "cpu": 0,
                    "command": [
                        file_name
                    ],
                    "environment": []
                }
            ]
        }
    )

    print("test 2")

    # # ===========================================================================
    # # WAIT FOR RESPONSE
    # # ===========================================================================
    task_arn = response['tasks'][0]['taskArn']
    
    while True:
        # Check task status
        task_description = client.describe_tasks(
            cluster='group3-image-processing-cluster',
            tasks=[task_arn]
        )
        task_status = task_description['tasks'][0]['lastStatus']
        
        print(f"Task status: {task_status}")
        
        # Break the loop if the task is completed or stopped
        if task_status in ['STOPPED']:
            break
        
        # Wait for a few seconds before polling again
        time.sleep(5)

    # Get exit code or result (if applicable)
    stopped_task = client.describe_tasks(
        cluster='group3-image-processing-cluster',
        tasks=[task_arn]
    )
    
    exit_code = stopped_task['tasks'][0]['containers'][0].get('exitCode', None)
    print(f"Task exit code: {exit_code}")

    print("Response: ")
    print(response)

    return {
        'statusCode': 200,
        'body': json.dumps('Processing complete')
    }
 
