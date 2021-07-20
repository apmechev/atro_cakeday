locals {
  prefix               = var.branch_name != "master" ? "${replace(var.branch_name, "/\\W|_|\\s/", "-")}-" : ""  #https://stackoverflow.com/a/60734389
  bakery_bucket_name   = "${local.prefix}${var.bakery_bucket_prefix}-${var.site_name}"
  frontend_bucket_name = "${local.prefix}${var.site_name}"
  lambda_function_name = "${local.prefix}cakedays_space_process"
}