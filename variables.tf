variable "prefix" {
  description = "The prefix used for all resources in this environment"
}

variable "location" {
  description = "The Azure location where all resources in this deployment should be created"
  default = "uksouth"
}

variable "CLIENT_ID" {
  description = "Github Auth Client id"
  sensitive   = true
}

variable "CLIENT_SECRET" {
  description = "Github Auth Client secret"
  sensitive   = true
}
