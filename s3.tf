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


data "template_file" "env_file_templated" {
  template = file("${path.module}/astro_cakeday/src/.env")
  vars = {
    api_gateway_URL = "${aws_apigatewayv2_api.submit_cake.api_endpoint}/${local.submit_stage_name}/bake"
  }
}

resource "aws_s3_bucket_object" "index_html" {
  bucket  = aws_s3_bucket.site_bucket.id
  key     = "index.html"
  content = file("${path.module}/astro_cakeday/build/index.html")

  content_type = "text/html"
  etag         = md5(file("${path.module}/astro_cakeday/build/index.html"))
}
resource "aws_s3_bucket_object" "env_file" {
  bucket  = aws_s3_bucket.site_bucket.id
  key     = ".env"
  content = data.template_file.env_file_templated.rendered

  content_type = "text"
  etag         = md5(file("${path.module}/astro_cakeday/src/.env"))
}

resource "aws_s3_bucket_object" "manifest_json" {
  bucket  = aws_s3_bucket.site_bucket.id
  key     = "manifest.json"
  content = file("${path.module}/astro_cakeday/build/manifest.json")

  content_type = "application/json"
  etag         = md5(file("${path.module}/astro_cakeday/build/manifest.json"))
}

resource "aws_s3_bucket_object" "asset_manifest_json" {
  bucket  = aws_s3_bucket.site_bucket.id
  key     = "asset-manifest.json"
  content = file("${path.module}/astro_cakeday/build/asset-manifest.json")

  content_type = "application/json"
  etag         = md5(file("${path.module}/astro_cakeday/build/asset-manifest.json"))
}
resource "aws_s3_bucket_object" "static_css" {
  for_each = fileset("${path.module}/astro_cakeday/build/static/css/", "*")

  bucket = aws_s3_bucket.site_bucket.id
  key    = "static/css/${each.value}"
  source = "${path.module}/astro_cakeday/build/static/css/${each.value}"
}

resource "aws_s3_bucket_object" "static_js" {
  for_each = fileset("${path.module}/astro_cakeday/build/static/js/", "*")

  bucket = aws_s3_bucket.site_bucket.id
  key    = "static/js/${each.value}"
  source = "${path.module}/astro_cakeday/build/static/js/${each.value}"
}

resource "aws_s3_bucket_object" "static_media" {
  for_each = fileset("${path.module}/astro_cakeday/build/static/media/", "*")

  bucket = aws_s3_bucket.site_bucket.id
  key    = "static/media/${each.value}"
  source = "${path.module}/astro_cakeday/build/static/media/${each.value}"
}




