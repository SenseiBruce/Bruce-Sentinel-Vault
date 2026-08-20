variable "project_name" {
  type        = string
  description = "Name used for labels and resource prefixes."
  default     = "bruce-sentinel-vault"
}

variable "image_name" {
  type        = string
  description = "Container image repository/name."
  default     = "bruce-sentinel-vault"
}

variable "image_tag" {
  type        = string
  description = "Container image tag."
  default     = "0.1.4"
}

variable "replicas" {
  type        = number
  description = "Desired replica count."
  default     = 1

  validation {
    condition     = var.replicas >= 1 && var.replicas <= 10
    error_message = "replicas must be between 1 and 10."
  }
}

variable "environment" {
  type        = string
  description = "Deployment environment label."
  default     = "local"
}
