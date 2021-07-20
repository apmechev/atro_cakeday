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
    Project = "Cakedays"
    Prefix  = local.prefix
    Branch  = var.branch_name

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
    allowed_methods = ["GET"]
    allowed_origins = ["https://${var.site_name}", "http://${var.site_name}"]
    expose_headers  = ["ETag"]
    max_age_seconds = 3000
  }

  tags = {
    Project = "Cakedays"
    Prefix  = local.prefix
  }
}

resource "aws_s3_bucket_policy" "bakery_bucket_policy" {
  bucket = aws_s3_bucket.bakery_bucket.id

  policy = jsonencode(
    {
      Version = "2012-10-17",
      Statement = [
        {
          Sid       = "PublicReadGetObject",
          Effect    = "Allow",
          Principal = "*",
          Action = [
            "s3:GetObject"
          ],
          Resource = "${aws_s3_bucket.bakery_bucket.arn}/baked/*"
        }
      ]
  })
}

resource "aws_s3_bucket_object" "index_html" {
  bucket = aws_s3_bucket.site_bucket.name
  key    = "index.html"
  source = "astro_cakeday/static/index.html"
  
  etag = filemd5("astro_cakeday/static/index.html")
}