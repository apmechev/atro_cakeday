resource "aws_s3_bucket" "site_bucket" {
  bucket = local.frontend_bucket_name
  acl    = "public-read"

  website {
    index_document = "index.html"
    error_document = "error.html"
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
    allowed_origins = ["https://${local.frontend_bucket_name}", "http://${local.frontend_bucket_name}"]
    expose_headers  = ["ETag"]
    max_age_seconds = 3000
  }

  tags = {
    Project = "Cakedays"
    Prefix  = local.prefix
  }

  force_destroy = true
}

######### Policies

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

resource "aws_s3_bucket_policy" "site_bucket_policy" {
  bucket = aws_s3_bucket.site_bucket.id

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
          Resource = "${aws_s3_bucket.site_bucket.arn}/*"
        }
      ]
  })
}

################# S3 Objects

resource "aws_s3_bucket_object" "index_html" {
  bucket = aws_s3_bucket.site_bucket.id
  key    = "index.html"
  source = "astro_cakeday/static/index.html"

  content_type = "text/html"
}

resource "aws_s3_bucket_object" "galaxy_png" {
  bucket = aws_s3_bucket.site_bucket.id
  key    = "galaxy.png"
  source = "astro_cakeday/static/galaxy.png"

  etag = filemd5("astro_cakeday/static/galaxy.png")
}

resource "aws_s3_bucket_object" "cake_cursor_png" {
  bucket = aws_s3_bucket.site_bucket.id
  key    = "cake_cursor.png"
  source = "astro_cakeday/static/cake_cursor.png"

  etag = filemd5("astro_cakeday/static/cake_cursor.png")
}


resource "aws_s3_bucket_object" "birthday_css" {
  bucket = aws_s3_bucket.site_bucket.id
  key    = "styles/birthday.css"
  source = "astro_cakeday/static/styles/birthday.css"

  etag = filemd5("astro_cakeday/static/styles/birthday.css")
}
