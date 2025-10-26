resource "aws_s3_bucket" "generatedimage" {
  bucket_prefix = "generatedimage-"
  force_destroy = true
}