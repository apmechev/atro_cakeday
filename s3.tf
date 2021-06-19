resource "aws_s3_bucket" "site_bucket" {
  bucket = local.frontend_bucket_name
  acl    = "public-read"

  website {
    index_document = "index.html"
    error_document = "error.html"
  }

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["PUT", "POST"]
    allowed_origins = ["https://${var.site_name}", "http://${var.site_name}"]
    expose_headers  = ["ETag"]
    max_age_seconds = 3000
  }

  tags = {
    Project  = "Cakedays"
    Prefix = local.prefix
  }
}

resource "aws_s3_bucket" "bakery_bucket" {
  bucket = local.bakery_bucket_name
  acl    = "public-read"

  website {
    index_document = "index.html"
    error_document = "error.html"
  }

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["PUT", "POST"]
    allowed_origins = ["https://${var.site_name}", "http://${var.site_name}"]
    expose_headers  = ["ETag"]
    max_age_seconds = 3000
  }

  tags = {
    Project  = "Cakedays"
    Prefix = local.prefix
  }
}