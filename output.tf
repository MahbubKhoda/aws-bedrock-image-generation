# terraform output bucket name
output "s3_bucket_name" {
  value = aws_s3_bucket.movieposterdesign.bucket
}