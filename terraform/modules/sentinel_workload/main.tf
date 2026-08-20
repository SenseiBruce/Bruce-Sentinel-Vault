locals {
  full_image = "${var.image_name}:${var.image_tag}"
  labels = {
    app         = var.project_name
    environment = var.environment
    managed_by  = "terraform"
  }
}

# Render a portable workload spec (consumed by docker compose / k8s sync jobs).
# This keeps the module reusable without requiring a live cloud provider in CI.
resource "local_file" "workload_manifest" {
  filename = "${path.module}/generated/workload.json"
  content = jsonencode({
    apiVersion = "sentinel.local/v1"
    kind       = "Workload"
    metadata = {
      name   = var.project_name
      labels = local.labels
    }
    spec = {
      replicas = var.replicas
      image    = local.full_image
      command  = ["python", "health.py"]
      healthcheck = var.enable_healthcheck ? {
        command  = ["python", "health.py"]
        interval = "30s"
        retries  = 3
      } : null
      env_from = [".env"]
    }
  })
}

output "image" {
  description = "Fully qualified image reference."
  value       = local.full_image
}

output "manifest_path" {
  description = "Path to the rendered workload manifest."
  value       = local_file.workload_manifest.filename
}

output "labels" {
  description = "Standard labels applied to the workload."
  value       = local.labels
}
