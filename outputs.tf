output "api_gateway_uri" {
  value = "${aws_apigatewayv2_api.submit_cake.api_endpoint}/${local.submit_stage_name}/bake"
}