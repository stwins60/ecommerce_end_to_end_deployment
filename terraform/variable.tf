variable "namespace" {
  description = "Namespace where the appp will be deployed"
  default     = "dev"
}
variable "image_tag" {
  description = "Image tag for Docker"
  default     = "latest"
}