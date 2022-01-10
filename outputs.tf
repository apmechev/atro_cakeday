output "api_gateway_uri" {
  value = "${aws_apigatewayv2_api.submit_cake.api_endpoint}/${local.submit_stage_name}/bake"
}


output "s3_website_url" {
  value = aws_s3_bucket.site_bucket.website_endpoint
}

output "s3_website_bucket" {
  value = aws_s3_bucket.site_bucket.id
}
