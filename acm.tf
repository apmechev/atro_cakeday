resource "aws_acm_certificate" "cakecert" {
    provider = aws.us-east-1
  domain_name       = local.frontend_bucket_name
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_acm_certificate_validation" "cakeval" {
  provider = aws.us-east-1
  certificate_arn         = aws_acm_certificate.cakecert.arn
  validation_record_fqdns = [for record in aws_route53_record.cert_validation : record.fqdn]
}
