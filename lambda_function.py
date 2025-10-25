import base64
from datetime import datetime
import json
import os
import uuid
import boto3

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    if 'body' in event:
        # If called via API Gateway, parse the body
        body = json.loads(event['body'])
        prompt = body.get('prompt', '')
    else:
        # Direct invocation
        prompt = event.get('prompt', '')

    if not prompt:
        return {
            'statusCode' : 400,
            'body': json.dumps({'error': 'No prompt provided'})
        }
    else:
        logger.info(f"Generating image for prompt: {prompt}")
        try:
            # Call the Bedrock API to generate the image
            bedrock_client = boto3.client("bedrock-runtime")
            
            # Define model parameters
            model_id = "amazon.titan-image-generator-v1"
            accept = "application/json"
            content_type = "application/json"

            # Create request body
            body = json.dumps({
                "taskType": "TEXT_IMAGE",
                "textToImageParams": {
                    "text": prompt
                },
                "imageGenerationConfig": {
                    "numberOfImages": 1,
                    "height": 1024,
                    "width": 1024,
                    "cfgScale": 8.0,
                    "seed": 0
                }
            })

            # Invoke Bedrock model to generate image
            response = bedrock_client.invoke_model(
                body=body, modelId=model_id, accept=accept, contentType=content_type
            )
            response_body = json.loads(response.get("body").read())

            base64_image = response_body.get("images")[0]
            base64_bytes = base64_image.encode('ascii')
            image_data = base64.b64decode(base64_bytes)
        except Exception as e:
            logger.error(f"Error generating image: {e}")
            return {
                'statusCode' : 500,
                'body': json.dumps({'error': 'Failed to generate image'})
            }
        
        # Store image in S3
        s3_client = boto3.client('s3')
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"generated-images/{timestamp}-{uuid.uuid4()}.png"
        s3_client.put_object(
            Bucket=os.environ['BUCKET_NAME'],
            Key=filename,
            Body=image_data,
            ContentType="image/png"
        )

        # Generate presigned URL
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': os.environ['BUCKET_NAME'], 'Key': filename},
            ExpiresIn=3600
        )
        logger.info(f"Image stored successfully. Access it at: {presigned_url}")

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Image generated and stored successfully',
                'url': presigned_url
            })
        }