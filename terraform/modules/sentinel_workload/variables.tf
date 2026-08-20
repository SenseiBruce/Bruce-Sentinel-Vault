variable "project_name" {
  description = "Name used for labels and resource prefixes."
  type        = string
  default     = "bruce-sentinel-vault"
}

variable "image_name" {
  description = "Container image repository/name to deploy."
  type        = string
  default     = "bruce-sentinel-vault"
}

variable "image_tag" {
  description = "Container image tag."
  type        = string
  default     = "0.1.1"
}

variable "replicas" {
  description = "Desired replica count for the workload."
  type        = number
  default     = 1

  validation {
    condition     = var.replicas >= 1 && var.replicas <= 10
    error_message = "replicas must be between 1 and 10."
  }
}

variable "environment" {
  description = "Deployment environment label (e.g. local, staging, prod)."
  type        = string
  default     = "local"
}

variable "enable_healthcheck" {
  description = "Whether the rendered workload includes a health check."
  type        = bool
  default     = true
}
