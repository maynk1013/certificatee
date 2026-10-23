terraform {
  required_version = ">= 1.10.0, < 2.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.82"
    }
  }

  # Local validation uses `terraform init -backend=false`.
  # Real state uses the partial config in backend.s3.hcl.example.
  # Do not run `terraform apply` without explicit approval.
  backend "s3" {}
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = local.tags
  }
}
