locals {
  prefix                     = var.branch_name != "master" ? "${replace(lower(var.branch_name), "/\\W|_|\\s/", "-")}-" : "" #https://stackoverflow.com/a/60734389
  prefixed_site_name         = "${local.prefix}${var.site_name}" # has no underscores
  safe_prefixed_site_name    = replace(local.prefixed_site_name, "/\\W|-.|\\s/", "_") # Has no periods or dashes

  bakery_bucket_name         = "${local.prefix}${var.bakery_bucket_prefix}-${var.site_name}"
  frontend_bucket_name       = local.prefixed_site_name
  lambda_function_name       = "${local.prefix}cakedays_space_process"
  api_gateway_name           = "${local.prefixed_site_name}_submit_API"
  lambda_execution_role_name = "${local.prefixed_site_name}_submit_lambda_role"
  api_gateway_stage_name     = "submit_lambda_stage"
}