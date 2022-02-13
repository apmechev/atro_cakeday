data "aws_route53_zone" "cakedays_zone" {
  name = "cakedays.space"
}


resource "aws_route53_record" "branch" {
  zone_id = data.aws_route53_zone.cakedays_zone.zone_id
  name    = local.frontend_bucket_name
  type    = "A"
  alias {
    name                   = aws_cloudfront_distribution.cakedays_cdn.domain_name
    zone_id                = aws_cloudfront_distribution.cakedays_cdn.hosted_zone_id
    evaluate_target_health = false
  }
}

resource "aws_route53_record" "cert_validation" {

 for_each = {
    for dvo in aws_acm_certificate.cakecert.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = data.aws_route53_zone.cakedays_zone.id
}
