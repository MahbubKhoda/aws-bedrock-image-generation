# IAM role for Lambda execution
data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "lambda_role" {
  name               = "lambda_execution_role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

# Attach necessary policies to the lambda execution role
resource "aws_iam_role_policy_attachment" "attach_bedrock_lambda" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonBedrockFullAccess"
}
resource "aws_iam_role_policy_attachment" "attach_s3_lambda" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

data "archive_file" "python_lambda_package" {
  type        = "zip"
  source_file = "${path.module}/lambda_function.py"
  output_path = "lambda.zip"
}

resource "aws_lambda_function" "generate_image_lambda" {
  function_name = "generate_image_lambda"
  filename      = "lambda.zip"
  source_code_hash = data.archive_file.python_lambda_package.output_base64sha256
  role          = aws_iam_role.lambda_role.arn
  runtime       = "python3.12"
  handler       = "lambda_function.lambda_handler"
  timeout       = 60
  
  environment {
    variables = {
      BUCKET_NAME = aws_s3_bucket.generatedimage.bucket
    }
  }

  depends_on = [
    aws_iam_role_policy_attachment.attach_bedrock_lambda,
    aws_iam_role_policy_attachment.attach_s3_lambda
  ]
}