provider "aws" {
  region                    = "us-east-1"
  profile                   = "default"
  shared_credentials_files  = ["creds/keys"]
  shared_config_files       = ["creds/config"]
}
