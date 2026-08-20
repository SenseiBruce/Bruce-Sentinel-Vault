# Root stack: wire the reusable sentinel_workload module for local/dev deploys.

module "sentinel" {
  source = "./modules/sentinel_workload"

  project_name       = var.project_name
  image_name         = var.image_name
  image_tag          = var.image_tag
  replicas           = var.replicas
  environment        = var.environment
  enable_healthcheck = true
}
