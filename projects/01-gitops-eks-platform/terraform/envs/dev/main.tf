locals {
  tags = {
    Project     = var.project
    Environment = var.environment
    Owner       = var.owner
    ManagedBy   = "terraform"
  }
}

module "vpc" {
  source = "../../modules/vpc"

  name                 = var.cluster_name
  cidr                 = var.vpc_cidr
  azs                  = var.azs
  public_subnet_cidrs  = var.public_subnet_cidrs
  private_subnet_cidrs = var.private_subnet_cidrs
  enable_nat_gateway   = true
  tags                 = local.tags
}

module "iam" {
  source = "../../modules/iam"

  name = var.cluster_name
  tags = local.tags
}

module "eks" {
  source = "../../modules/eks"

  name                   = var.cluster_name
  kubernetes_version     = var.kubernetes_version
  subnet_ids             = module.vpc.private_subnet_ids
  cluster_role_arn       = module.iam.cluster_role_arn
  cluster_role_name      = module.iam.cluster_role_name
  node_role_arn          = module.iam.node_role_arn
  node_role_name         = module.iam.node_role_name
  endpoint_public_access = var.endpoint_public_access
  public_access_cidrs    = var.public_access_cidrs
  tags                   = local.tags
}
