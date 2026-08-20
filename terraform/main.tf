# Root stack: wire the reusable sentinel_workload module for local/dev deploys.

terraform {
  required_version = ">= 1.5.0"

  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.5"
    }
  }
}

module "sentinel" {
  source = "./modules/sentinel_workload"

  project_name       = var.project_name
  image_name         = var.image_name
  image_tag          = var.image_tag
  replicas           = var.replicas
  environment        = var.environment
  enable_healthcheck = true
}

variable "project_name" {
  type    = string
  default = "bruce-sentinel-vault"
}

variable "image_name" {
  type    = string
  default = "bruce-sentinel-vault"
}

variable "image_tag" {
  type    = string
  default = "0.1.1"
}

variable "replicas" {
  type    = number
  default = 1
}

variable "environment" {
  type    = string
  default = "local"
}

output "workload_image" {
  value = module.sentinel.image
}

output "workload_manifest" {
  value = module.sentinel.manifest_path
}
