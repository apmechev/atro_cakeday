locals {
    prefix = "test-"
    bakery_bucket_name = "${local.prefix}${var.bakery_bucket_prefix}.${var.site_name}"
    frontend_bucket_name = "${local.prefix}${var.site_name}"
    lambda_function_name = "${local.prefix}cakedyas_space_process"
}