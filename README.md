
# AWS Bedrock Image Generation

Generate images using AWS Bedrock Titan model via a serverless Lambda function and API Gateway.

## Features
- Generate high-quality images from text prompts using AWS Bedrock
- Store generated images in Amazon S3
- Simple REST API for integration

## Architecture
This project uses:
- AWS Lambda (Python)
- AWS Bedrock Titan Image Generator
- Amazon S3 (for image storage)
- API Gateway (for REST API)
- Terraform (for infrastructure as code)

## Setup
1. **Clone the repository**
	```bash
	git clone https://github.com/MahbubKhoda/aws-bedrock-image-generation.git
	cd aws-bedrock-image-generation
	```

2. **Configure AWS credentials**
    - Create a folder named creds in the root directory
    - Create two files inside the creds folder - keys and config. Put your aws credentials and configs in the files.
    - keys file structure
    ```
    [default]
    aws_access_key_id = YOUR_ACCESS_KEY
    aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
    ```
    - config file structure
    ```
    [profile default]
    region = us-east-1
    ```
	- Ensure your AWS user has permissions for Lambda, Bedrock, S3, and API Gateway.

3. **Deploy with Terraform**
	```bash
	terraform init
	terraform apply
	```

## Usage
Once deployed, you can generate images by sending a POST request to the API Gateway endpoint:

```bash
curl -X POST <API_URL> \
	  -H "Content-Type: application/json" \
	  -d '{"prompt": "Image of a horse"}'
```

Replace `<API_URL>` with your deployed API Gateway endpoint.

### Example Response
```
{
  "message": "Image generated and stored successfully",
  "url": <presinged url of the generated image>
}
```

## Lambda Function
The Lambda function (`lambda_function.py`) receives a text prompt, calls the Bedrock Titan model to generate an image, decodes the image, and stores it in S3. See code comments for details.

## Files
- `lambda_function.py`: Lambda handler for image generation
- `main.tf`, `lambda.tf`, `s3.tf`, `output.tf`: Terraform configuration files
- `creds/`: AWS credentials/configuration

## License
See `LICENSE` for details.

## Author
Mahbub Khoda
