data "aws_route53_zone" "cakedays_zone" {
  name = "cakedays.space"
}


resource "aws_route53_record" "branch" {
  zone_id = data.aws_route53_zone.cakedays_zone.zone_id
  name    = local.frontend_bucket_name
  type    = "A"
  alias {
      name = aws_s3_bucket.site_bucket.website_domain
      zone_id = aws_s3_bucket.site_bucket.hosted_zone_id
      evaluate_target_health = false
  }

}
