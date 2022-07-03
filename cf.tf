data "aws_cloudfront_origin_request_policy" "corsS3Origin" {
  name = "Managed-CORS-S3Origin"
}
data "aws_cloudfront_cache_policy" "cachingOptimized" {
  name = "Managed-CachingOptimized"
}

resource "aws_cloudfront_distribution" "cakedays_cdn" {
  origin {
    origin_id   = "${local.frontend_bucket_name}-cdn"
    domain_name = "${local.frontend_bucket_name}.s3.amazonaws.com"
  }

  # If using route53 aliases for DNS we need to declare it here too, otherwise we'll get 403s.
  aliases = [local.frontend_bucket_name]

  enabled             = true
  default_root_object = "index.html"

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "${local.frontend_bucket_name}-cdn"
    
    cache_policy_id             = data.aws_cloudfront_cache_policy.cachingOptimized.id
    origin_request_policy_id   = data.aws_cloudfront_origin_request_policy.corsS3Origin.id

    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
    viewer_protocol_policy = "redirect-to-https"

  }

  # The cheapest priceclass
  price_class = "PriceClass_100"

  # This is required to be specified even if it's not used.
  restrictions {
    geo_restriction {
      restriction_type = "none"
      locations        = []
    }
  }

  viewer_certificate {
    acm_certificate_arn = aws_acm_certificate_validation.cakeval.certificate_arn
    ssl_support_method  = "sni-only"
  }
}
