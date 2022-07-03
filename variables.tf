variable "bakery_bucket_prefix" {
  default = "bakery"
}

variable "site_name" {
  default = "cakedays.space"
}

variable "region" {
  default = "eu-central-1"
}

variable "SECRET_KEY" {

}

variable "branch_name" {
  description = "The name of the branch that's being deployed"
}