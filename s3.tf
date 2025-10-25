resource "aws_s3_bucket" "movieposterdesign" {
  bucket_prefix = "movieposterdesign-"
  force_destroy = true
}