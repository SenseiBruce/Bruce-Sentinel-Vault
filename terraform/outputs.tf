output "workload_image" {
  description = "Container image rendered by the sentinel module."
  value       = module.sentinel.image
}

output "workload_manifest" {
  description = "Filesystem path of the generated workload manifest."
  value       = module.sentinel.manifest_path
}

output "workload_labels" {
  description = "Labels applied to the workload."
  value       = module.sentinel.labels
}
