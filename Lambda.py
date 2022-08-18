"""
serializeImageData

Test event:

{
    "image_data": "",
    "s3_bucket": "sagemaker-us-east-1-942422823978",
    "s3_key": "test/bicycle_s_001789.png"
  }
"""


import json
import boto3
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """A function to serialize target data from S3"""

    # Get the s3 address from the Step Function event input
    key = event['s3_key']
    bucket = event['s3_bucket']

    # Download the data from s3 to /tmp/image.png
    s3.download_file(bucket, key, '/tmp/image.png')

    # We read the data from a file
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read())

    # Pass the data back to the Step Function
    print("Event:", event.keys())
    return {
        'statusCode': 200,
        'body': {
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    }


"""
classificationImageData

Test event:

{
    "statusCode": 200,
    "body": {
      "image_data": "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",
      "s3_bucket": "sagemaker-us-east-1-942422823978",
      "s3_key": "test/bicycle_s_001789.png",
      "inferences": []
    }
  }
"""

import json
import base64
import boto3

# Fill this in with the name of your deployed model
ENDPOINT = 'image-classification-2022-08-17-10-36-02-225'
runtime = boto3.Session().client('sagemaker-runtime')


def lambda_handler(event, context):

    # Decode the image data
    image = base64.b64decode(event['body']['image_data'])

    # Instantiate a Predictor
    response = runtime.invoke_endpoint(EndpointName=ENDPOINT, ContentType = 'image/png', Body = image)

    # Make a prediction:
    predictions = json.loads(response['Body'].read().decode('utf-8'))

    # We return the data back to the Step Function    
    event['body']['inferences'] = predictions
    
    return {
        'statusCode': 200,
        'body': json.dumps(event['body'])
    }

"""
filterInferenceImageData

Test event:

{
    "statusCode": 200,
    "body": {
      "image_data": "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",
      "s3_bucket": "sagemaker-us-east-1-942422823978",
      "s3_key": "test/bicycle_s_001789.png",
      "inferences": []
    }
  }
"""

import json


THRESHOLD = .93


def lambda_handler(event, context):

    # Grab the inferences from the event
    inferences = json.loads(event["body"])['inferences']
    
    # # Check if any values in our inferences are above THRESHOLD
    meets_threshold = any(x >= THRESHOLD for x in inferences)

    # If our threshold is met, pass our data back out of the
    # Step Function, else, end the Step Function with an error
    if meets_threshold:
        pass
    else:
        raise ValueError("THRESHOLD_CONFIDENCE_NOT_MET")

    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }