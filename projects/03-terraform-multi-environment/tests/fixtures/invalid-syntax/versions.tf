terraform {
  required_version = ">= 1.10.0, < 2.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.82"
    }
  }
}

provider "aws" {
  region = "ap-south-1"
}

resource "aws_vpc" "broken" {
  # Intentionally the wrong type so `terraform validate` fails.
  cidr_block = 123
}
