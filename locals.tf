locals {
  prefix               = var.branch_name != "master" ? "${var.branch_name}-" : ""
  safe_site_name       = replace(var.site_name, ".", "-")
  bakery_bucket_name   = "${local.prefix}${var.bakery_bucket_prefix}-${local.safe_site_name}"
  frontend_bucket_name = "${local.prefix}${local.safe_site_name}"
  lambda_function_name = "${local.prefix}cakedays_space_process"
}