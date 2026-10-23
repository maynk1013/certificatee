locals {
  tags = {
    Project     = var.project
    Environment = var.environment
    Owner       = var.owner
    ManagedBy   = "terraform"
  }
}

module "networking" {
  source = "../../modules/networking"

  name                 = "${var.project}-${var.environment}"
  cidr                 = var.vpc_cidr
  azs                  = var.azs
  public_subnet_cidrs  = var.public_subnet_cidrs
  private_subnet_cidrs = var.private_subnet_cidrs
  enable_nat_gateway   = var.enable_nat_gateway
  tags                 = local.tags
}

module "iam" {
  source = "../../modules/iam"

  name   = "${var.project}-${var.environment}"
  create = var.create_compute
  tags   = local.tags
}

module "compute" {
  source = "../../modules/compute"

  name                  = "${var.project}-${var.environment}"
  create                = var.create_compute
  vpc_id                = module.networking.vpc_id
  subnet_ids            = module.networking.private_subnet_ids
  instance_profile_name = module.iam.instance_profile_name
  desired_capacity      = 0
  tags                  = local.tags
}
